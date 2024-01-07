import setuptools

with open("README.md", "r", encoding="utf-8") as info:
    long_description = info.read()

setuptools.setup(
    name="pip-nftables",
    version="1.0.9.post1",
    author="Felipe Quecole",
    author_email="felipequecole@gmail.com",
    description="Copy of the python3-nftables module used to interact with libnftables",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/felipequecole/python3-nftables",
    project_urls={
        "Repository": "https://github.com/felipequecole/python3-nftables",
        "Bug Tracker": "https://github.com/felipequecole/python3-nftables/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3",
)
