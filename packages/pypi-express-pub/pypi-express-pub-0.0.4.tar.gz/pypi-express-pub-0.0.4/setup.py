import os

import setuptools

lib_folder = os.path.dirname(os.path.realpath(__file__))
requirements = os.path.join(lib_folder, "requirements.txt")

package_dependency_list = []
if os.path.isfile(requirements):
    with open(requirements) as f:
        package_dependency_list = f.read().splitlines()

setuptools.setup(
    name="pypi-express-pub",
    version="0.0.4",
    author="Peter Bryant",
    author_email="peter.bryant@gatech.edu",
    description="A Python package for publishing packages to PyPI.",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "pypi-express-pub = pypi_express_pub.publish:deploy_package",
        ],
    },
    install_requires=package_dependency_list,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
