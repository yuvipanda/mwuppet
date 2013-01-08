from setuptools import setup
setup(
        name="python-mwuppet",
        version="0.0.3",
        author="Yuvi Panda",
        author_email="yuvipanda@gmail.com",
        url="https://github.com/yuvipanda/mwuppet",
        packages=['mwuppet',],
        license="MIT License",
        description = " Mediawiki UserScript Deploy Script",
        long_description = open("README").read(),
        install_requires = ["python-mwapi"],
)
