import setuptools

README = 'README.md'
README_MIME = 'text/markdown'

with open(README, "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="topenai",
    version="0.0.1",
    author="vladzima",
    description="",
    url="https://github.com/vladzima/topenai",
    long_description=long_description,
    long_description_content_type=README_MIME,
    packages=setuptools.find_packages(),
    author_email="v.o.arbatov@gmail.com",
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: OS Independent"
    ],
    install_requires=[  
    ]
)
