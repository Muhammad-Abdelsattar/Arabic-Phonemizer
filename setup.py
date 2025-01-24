# from setuptools import setup

# setup()
# import os
# import shutil
# import platform
# from setuptools import setup
# from setuptools.dist import Distribution

# # Determine the current platform and architecture
# current_platform = platform.system().lower()
# current_arch = platform.machine().lower()

# # Map platforms and architectures to their respective library directories
# PLATFORM_LIB_DIRS = {
#     "windows": {
#         "amd64": os.path.join("win", "amd64"),  # Windows x86_64
#         "arm64": os.path.join("win", "arm64"),  # Windows ARM64
#     },
#     "linux": {
#         "x86_64": os.path.join("linux", "x86_64"),  # Linux x86_64
#         "aarch64": os.path.join("linux", "arm64"),  # Linux ARM64
#     },
#     "darwin": {
#         "x86_64": os.path.join("macos", "x86_64"),  # macOS x86_64
#         "arm64": os.path.join("macos", "arm64"),    # macOS ARM64
#     },
# }

# lib_dir = PLATFORM_LIB_DIRS.get(current_platform, {}).get(current_arch)
# if not lib_dir:
#     raise RuntimeError(f"Unsupported platform/architecture: {current_platform}/{current_arch}")


# package_data = {
#     "arabic_phonemizer": [os.path.join("espeak","libs", lib_dir, "*")]
# }



# setup(
#     # package_data=package_data,
#     # include_package_data=True,
#     distclass=BinaryDistribution,
# )
# setup(
#     package_data={'my_package': lib_files},
#     # Include the platform name in the wheel metadata
#     options={'bdist_wheel': {'plat_name': plat_name}},
#     # ... other metadata ...
# )


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

print(os.listdir())
platform_dir = get_platform_dir()
lib_files = [str(Path('arabic_phonemizer')/'shared_libs' / platform_dir / filename)
             for filename in os.listdir(str(Path('arabic_phonemizer')/'shared_libs' / platform_dir))]

lib_files.append(str(Path('arabic_phonemizer')/'shared_libs' / 'espeak-ng-data'))

print(os.listdir())

# Include the platform-specific libraries as package data
package_data = {package_name: lib_files}

class BinaryDistribution(Distribution):
    def is_pure(self):
        return False  
    
    def has_ext_modules(self):
        return True

# Set up the package
setup(
    package_dir={'arabic_phonemizer': 'arabic_phonemizer'},
    # package=find_packages(),
    packages=["arabic_phonemizer"],
    package_data=package_data,
    include_package_data=True,
    distclass=BinaryDistribution,
)