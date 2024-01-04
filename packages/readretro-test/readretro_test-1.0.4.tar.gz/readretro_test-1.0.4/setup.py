from setuptools import setup, find_packages
# import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="readretro_test",
    version="1.0.4",
    author="Taein Kim",
    author_email="tedori725@kaist.ac.kr",
    description="READRetro lib test",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package=find_packages(),
    install_requires=[
        'h5py',
        'typing-extensions',
        'wheel',
        'easydict',
        'pandas',
        'tqdm',
        'numpy==1.22',
        'OpenNMT-py==2.3.0',
        'networkx==2.5'
    ],
    extras_require={
        'torch_cuda': ['torch==1.12.0', 'cudatoolkit==11.3'],
    },
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
    # packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)