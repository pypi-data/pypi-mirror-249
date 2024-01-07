import os

import setuptools

lib_folder = os.path.dirname(os.path.realpath(__file__))
requirements = os.path.join(lib_folder, "requirements.txt")

package_dependency_list = []
if os.path.isfile(requirements):
    with open(requirements) as f:
        package_dependency_list = f.read().splitlines()

setuptools.setup(
    name="flask-chest",
    version="0.0.4",
    author="Peter Bryant",
    author_email="peter.bryant@gatech.edu",
    description="A Python package for Flask applications, providing a decorator to track and record global context variables (g.variables) for each request.",
    packages=setuptools.find_packages(),
    install_requires=package_dependency_list,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
