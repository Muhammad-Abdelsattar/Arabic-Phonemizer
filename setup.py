from setuptools import setup, find_packages
import sys
import os
from pathlib import Path
import platform
from setuptools.dist import Distribution

# Define the package name
package_name = 'arabic_phonemizer'

# Determine the current platform and architecture
def get_platform_dir():
    # cibw_arch = os.environ.get('CIBW_ARCHS')
    # cibw_platform = os.environ.get('CIBW_PLATFORM')

    # # For the current build
    # target_arch = os.environ.get('CIBW_ARCHS_{}'.format(cibw_platform.upper()))
    # if target_arch:
    #     target_arch = target_arch.strip()
    # else:
    #     target_arch = platform.machine()

    target_arch = platform.machine()

    system = platform.system()
    PLATFORM_LIB_DIRS = {
        "windows": {
            "amd64": os.path.join("win", "amd64"),  # Windows x86_64
            "arm64": os.path.join("win", "arm64"),  # Windows ARM64
        },
        "linux": {
            "x86_64": os.path.join("linux", "x86_64"),  # Linux x86_64
            "aarch64": os.path.join("linux", "arm64"),  # Linux ARM64
        },
        "darwin": {
            "x86_64": os.path.join("macosx", "x86_64"),  # macOS x86_64
            "arm64": os.path.join("macosx", "arm64"),    # macOS ARM64
        },
    }
    return PLATFORM_LIB_DIRS.get(system.lower(), {}).get(target_arch.lower())

parent = Path(__file__).parent / "arabic_phonemizer"
# parent = Path(".")

platform_dir = get_platform_dir()
lib_files = []
lib_files.extend([str(p) for p in (parent / 'espeak' / 'shared_libs' / platform_dir).rglob("*")])
shared = [str(p) for p in (parent / 'espeak' / 'shared_libs' / platform_dir).rglob("*")]

lib_files.extend([str(p) for p in (parent / 'espeak' / 'espeak-ng-data' ).rglob("*")])

# Include the platform-specific libraries as package data
package_data = {package_name+".espeak": lib_files}

class BinaryDistribution(Distribution):
    def is_pure(self):
        return False  
    
    def has_ext_modules(self):
        return True

# Set up the package
setup(
    package_dir={'arabic_phonemizer': 'arabic_phonemizer'},
    # package=find_packages(),
    # packages=["arabic_phonemizer"],
    package_data=package_data,
    # include_package_data=True,
    distclass=BinaryDistribution,
)