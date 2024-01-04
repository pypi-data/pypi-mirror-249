import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="readretro",
    version="1.0.0",
    author="Taein Kim",
    author_email="tedori725@kaist.ac.kr",
    description="READRetro lib test",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SeulLee05/READRetro",
    project_urls={
        "Bug Tracker": "https://github.com/SeulLee05/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)