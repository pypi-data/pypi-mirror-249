"""
IMcore

Python Version Required: 3.7+
Dependencies: numpy, opencv-python>=4.5.5.64, Pillow>=9.0.1, PySide6>=6.4.2, PyYAML>=6.0, captcha>=0.4
"""
import sys
import warnings

import pkg_resources

# Check Python version
if not sys.version_info >= (3, 7):
    warnings.warn("Python 3.7 or above is recommended.")

# Check other dependencies
required_packages = {
    "numpy": "",  # Dependency on the numpy library
    "Pillow": "9.0.1",  # Dependency on the Pillow library with a minimum version of 9.0.1
    "PySide6": "6.4.2",  # Dependency on the PySide6 library with a minimum version of 6.4.2
    "captcha": "0.4"  # Dependency on the captcha library with a minimum version of 0.4
}

for package, required_version in required_packages.items():
    try:
        pkg_resources.get_distribution(package)
        if required_version:
            actual_version = pkg_resources.get_distribution(package).version
            if pkg_resources.parse_version(actual_version) < pkg_resources.parse_version(required_version):
                warnings.warn(
                    f"{package} {required_version} or above is recommended, but {actual_version} is installed.")
    except pkg_resources.DistributionNotFound:
        warnings.warn(f"{package} is recommended but is not installed.")

__package_name__ = 'IMcore'
__version__ = '0.2.6'
__author__ = 'Seasal Wesley'
__email__ = 'seasalwesley@gmail.com'

