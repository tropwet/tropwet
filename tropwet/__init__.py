import sys
from distutils.version import LooseVersion

TROPWET_VERSION_MAJOR = 0
TROPWET_VERSION_MINOR = 0
TROPWET_VERSION_PATCH = 1

TROPWET_VERSION = "{}.{}.{}".format(
    TROPWET_VERSION_MAJOR,
    TROPWET_VERSION_MINOR,
    TROPWET_VERSION_PATCH,
)
TROPWET_VERSION_OBJ = LooseVersion(TROPWET_VERSION)
__version__ = TROPWET_VERSION

py_sys_version = sys.version_info
py_sys_version_str = "{}.{}".format(py_sys_version.major, py_sys_version.minor)
py_sys_version_flt = float(py_sys_version_str)

TROPWET_COPYRIGHT_YEAR = "2024"
TROPWET_COPYRIGHT_NAMES = "Andy Hardy, Greg Oakes and Pete Bunting"
