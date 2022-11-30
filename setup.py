import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_requires = ["numpy>=1.19.5"]

dev_specific_install_requires = [
    "pre-commit==2.12.1",
    "pandas>=1.1.5",
    "scipy>=1.5.4",
]

dev_install_requires = dev_specific_install_requires + install_requires

setuptools.setup(
    name="utils",
    version="0.0.2",
    author="Fan Grayson",
    author_email="fangrayson@hotmail.com",
    description=("Random utils functions"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    # download_url="https://github.com/fangrayson/utils/archive/refs/tags/v0.0.1.tar.gz",
    url="https://github.com/fangrayson/utils/",
    #project_urls={
    #    "Bug Tracker": "https://github.com/fangrayson/utils/issues",
    #},
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6.8",
    install_requires=install_requires,
    extras_require={"dev": dev_install_requires, "ci": dev_install_requires},
)