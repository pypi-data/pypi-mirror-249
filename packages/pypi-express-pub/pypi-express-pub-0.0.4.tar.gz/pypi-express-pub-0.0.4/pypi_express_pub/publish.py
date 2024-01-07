import os
import subprocess
import sys
import traceback

import pkg_resources


def run_command(command):
    """
    The function `run_command` executes a shell command and handles any exceptions that may occur.

    :param command: The `command` parameter is a string that represents the command you want to run in
    the shell. It can be any valid shell command, such as `ls`, `pwd`, or `git clone <repository_url>`
    """
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Exception: {e}")
        print(traceback.format_exc())
        sys.exit(1)


def install_dependencies():
    """
    The function checks if the required dependencies (wheel, twine, setuptools) are installed and if
    not, it attempts to install them.
    """
    dependencies = ["setuptools", "wheel", "twine"]
    to_install = []

    for dep in dependencies:
        try:
            pkg_resources.get_distribution(dep)
        except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
            to_install.append(dep)

    if to_install:
        run_command([sys.executable, "-m", "pip", "install", "--upgrade"] + to_install)


def deploy_package():
    """
    The function `deploy_package` installs dependencies, builds a wheel, and uploads it to PyPI.
    """
    install_dependencies()

    print("Building wheel...")
    run_command([sys.executable, "setup.py", "sdist", "bdist_wheel"])

    print("Uploading to PyPI...")
    run_command(
        [
            sys.executable,
            "-m",
            "twine",
            "upload",
            "--repository-url",
            "https://upload.pypi.org/legacy/",
            "dist/*",
            "--username",
            "__token__",
            "--password",
            "$PYPI_TOKEN",
        ]
    )
