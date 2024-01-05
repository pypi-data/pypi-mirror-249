from setuptools import find_packages, setup

PACKAGE_NAME = "kenakamu_pf_hello_world"

setup(
    name=PACKAGE_NAME,
    version="0.0.1",
    description="This is my tools package",
    packages=find_packages(),
    entry_points={
        "package_tools": ["hello_world_tool = hello_world.utils:list_package_tools"],
    },
    install_requires=[
        "promptflow",
        "promptflow-tools"
    ]
)