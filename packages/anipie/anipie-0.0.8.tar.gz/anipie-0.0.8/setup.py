from setuptools import setup, find_packages

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setup(
    name="anipie", 
    version='0.0.8',
    author="Aritsu",
    author_email="lynniswaifu@gmail.com",
    description="a simple python wrapper for the Anilist API",
    # long_description=long_description,
    long_description="find out on github",
    long_description_content_type="text/markdown",
    url="https://github.com/aritsulynn/anipie",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires= ['requests'],
    python_requires='>=3.6',
)