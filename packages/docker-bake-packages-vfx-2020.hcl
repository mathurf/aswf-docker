group "default" {
	targets = [
		# "package-alembic",
		"package-blosc",
		# "package-ocio",
		# "package-oiio",
		"package-openexr",
		# "package-opensubdiv",
		# "package-openvdb",
		# "package-ptex",
		# "package-usd",
	]
}

target "settings" {
	dockerfile = "packages/Dockerfile"
}

target "package-alembic" {
	target = "ci-vfx-alembic-package"
	inherits = ["settings", "settings-2020"]
	tags = ["docker.io/aswftesting/ci-package-alembic:2020"]
}

target "package-blosc" {
	target = "ci-vfx-blosc-package"
	inherits = ["settings", "settings-2020"]
	tags = ["docker.io/aswftesting/ci-package-blosc:2020"]
}

target "package-ocio" {
	target = "ci-vfx-ocio-package"
	inherits = ["settings", "settings-2020"]
	tags = ["docker.io/aswftesting/ci-package-ocio:2020"]
}

target "package-oiio" {
	target = "ci-vfx-oiio-package"
	inherits = ["settings", "settings-2020"]
	tags = ["docker.io/aswftesting/ci-package-oiio:2020"]
}

target "package-openexr" {
	target = "ci-vfx-openexr-package"
	inherits = ["settings", "settings-2020"]
	tags = ["docker.io/aswftesting/ci-package-openexr:2020"]
}

target "package-opensubdiv" {
	target = "ci-vfx-opensubdiv-package"
	inherits = ["settings", "settings-2020"]
	tags = ["docker.io/aswftesting/ci-package-opensubdiv:2020"]
}

target "package-openvdb" {
	target = "ci-vfx-openvdb-package"
	inherits = ["settings", "settings-2020"]
	tags = ["docker.io/aswftesting/ci-package-openvdb:2020"]
}

target "package-ptex" {
	target = "ci-vfx-ptex-package"
	inherits = ["settings", "settings-2020"]
	tags = ["docker.io/aswftesting/ci-package-ptex:2020"]
}

target "package-usd" {
	target = "ci-base-usd-package"
	inherits = ["settings", "settings-2020"]
	tags = ["docker.io/aswftesting/ci-package-usd:2020"]
}
