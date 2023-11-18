# this file contains some placeholders
# that are changed in a local copy if a release is made

import setuptools

README = 'README.md'  # the path to your readme file
README_MIME = 'text/markdown'  # it's mime type

with open(README, "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="topenai",  # placeholder (name of repo)
    version="1",  # placeholder (tag of release)
    author="vladzima",  # placeholder (owner of repo)
    description="",  # placeholder (description of repo)
    url="https://github.com/vladzima/topenai",  # placeholder (url of repo)
    long_description=long_description,
    long_description_content_type=README_MIME,
    packages=setuptools.find_packages(),
    author_email="",  # the email of the repo owner
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: OS Independent"
    ],
    install_requires=[  # add required pypi packages here
    ]
)
