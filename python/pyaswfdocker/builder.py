import logging
import subprocess
import json
import os

from . import constants, buildinfo

logger = logging.getLogger("build-packages")


class Builder:
    def __init__(
        self,
        buildInfo: buildinfo.BuildInfo,
        dryRun: bool = False,
        groupName: str = "",
        groupVersion: str = "",
        push: bool = False,
        imageType: str = "",
    ):
        self.dryRun = dryRun
        self.groupName = groupName
        self.groupVersion = groupVersion
        self.push = push
        self.buildInfo = buildInfo
        self.imageType = imageType

    def make_bake_dict(self) -> dict:
        targets = {}
        for img in constants.GROUPS[self.imageType][self.groupName]:
            if self.imageType == "packages":
                dockerFile = "packages/Dockerfile"
                target = f"ci-{img}-package"
            else:
                dockerFile = f"{img}/Dockerfile"
                target = f"ci-{img}"

            if self.groupVersion in constants.VERSIONS[self.imageType][img]:
                versionInfo = constants.VERSION_INFO[self.groupVersion]
                tags = [
                    versionInfo.version,
                    versionInfo.aswfVersion,
                ]
                if versionInfo.label:
                    tags.append(versionInfo.label)
                tags = list(
                    map(
                        lambda tag: f"docker.io/{self.buildInfo.dockerOrg}/ci-package-{img}:{tag}",
                        tags,
                    )
                )

                targetDict = {
                    "context": ".",
                    "dockerfile": dockerFile,
                    "args": {
                        "ASWF_ORG": self.buildInfo.dockerOrg,
                        "ASWF_PKG_ORG": self.buildInfo.pkgOrg,
                        "ASWF_VERSION": versionInfo.aswfVersion,
                        "CI_COMMON_VERSION": versionInfo.ciCommonVersion,
                        "PYTHON_VERSION": versionInfo.pythonVersion,
                        "BUILD_DATE": "dev",
                        "VCS_REF": "dev",
                        "VFXPLATFORM_VERSION": self.groupVersion,
                    },
                    "tags": tags,
                    "target": target,
                    "output": [
                        "type=registry,push=true" if self.push else "type=docker"
                    ],
                }
                targets[f"package-{img}"] = targetDict
        root = {}
        root["target"] = targets
        root["group"] = {"default": {"targets": list(targets.keys())}}
        return root

    def make_bake_jsonfile(self) -> str:
        d = self.make_bake_dict()
        path = os.path.join(
            "packages", f"docker-bake-{self.groupName}-{self.groupVersion}.json"
        )
        with open(path, "w") as f:
            json.dump(d, f, indent=4, sort_keys=True)
        return path

    def build(self) -> None:
        path = self.make_bake_jsonfile()
        cmd = f"docker buildx bake -f {path}"
        logger.info("Building %r", cmd)
        subprocess.run(
            cmd, shell=True, check=True,
        )
