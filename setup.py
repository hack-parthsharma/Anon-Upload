import setuptools
from anonupload.main import __version__

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setuptools.setup(
    name="anonupload",
    version=__version__,
    author="Jak Bin",
    author_email="jakbin4747@gmail.com",
    description="upload and download to anonfiles server",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/redevil1/anonfiles",
    install_requires=["tqdm","requests","requests-toolbelt"],
    python_requires=">=3",
    project_urls={
        "Bug Tracker": "https://github.com/redevil1/anonfiles/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
    ],
    keywords='anonfile,anonfile-api,anonfile-cli,anonymous,upload',
    packages=["anonupload"],
    entry_points={
        "console_scripts":[
            "anon = anonupload.main:main"
        ]
    }
)
