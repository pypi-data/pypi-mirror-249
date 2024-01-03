from setuptools import setup, find_packages


DESCRIPTION = 'Clash of Clans API wrapper'
LONG_DESCRIPTION = 'Clash of Clans API wrapper'

# Setting up
setup(
    name="cocapiwrapper",
    version='0.0.6',
    author="PyGIne (Ronan.T)",
    author_email="<ronan.tremoureux@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests','python-dotenv'],
    keywords=['clashofclans', 'api', 'wrapper'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)