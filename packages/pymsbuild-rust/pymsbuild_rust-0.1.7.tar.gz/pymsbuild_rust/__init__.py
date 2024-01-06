from .pymsbuild import Cargo, RustPydFile

__version__ = "%VERSION%"
try:
    NEXT_INCOMPATIBLE_VERSION = "{}.0".format(int(__version__.partition(".")[0]) + 1)
    PYMSBUILD_REQUIRES_SPEC = f"pymsbuild_rust>={__version__},<{NEXT_INCOMPATIBLE_VERSION}"
except ValueError:
    PYMSBUILD_REQUIRES_SPEC = "pymsbuild_rust"

__all__ = ["Cargo", "RustPydFile"]
