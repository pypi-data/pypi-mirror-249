"""Setup."""
import json
import os
from shutil import copytree

from setuptools import find_packages, setup

# Get setup packages from requirements.txt
with open("requirements_setup.txt", encoding="utf-8") as f:
    requirements_setup = f.read().splitlines()

# Get packages from requirements.txt
with open("requirements.txt", encoding="utf-8") as f:
    requirements = f.read().splitlines()

copytree(
    "WindowsSensors/bin/net8.0-windows8.0",
    "systembridgewindowssensors/bin",
    dirs_exist_ok=True,
)

package_data = []

for file in os.listdir("systembridgewindowssensors/bin"):
    if os.path.isfile(os.path.join("systembridgewindowssensors/bin", file)):
        package_data.append(os.path.join("bin", file).replace("\\", "/", -1))

for root, directories, files in os.walk("systembridgewindowssensors/bin"):
    for file in files:
        package_data.append(
            os.path.join(root, "/".join(directories), file)
            .replace("systembridgewindowssensors/", "")
            .replace("\\", "/", -1)
        )

print(json.dumps(package_data))  # noqa: T201

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="systembridgewindowssensors",
    author="Aidan Timson (Timmo)",
    author_email="aidan@timmo.dev",
    description="System Bridge Windows Sensors",
    keywords="system-bridge windows",
    license="Apache-2.0",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/timmo001/system-bridge-windows-sensors",
    install_requires=requirements,
    packages=find_packages(exclude=["tests", "generator"]),
    package_data={"": package_data},
    python_requires=">=3.11",
    setup_requires=requirements_setup,
    use_incremental=True,
)
