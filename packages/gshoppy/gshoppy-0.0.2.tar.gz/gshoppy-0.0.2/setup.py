from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'A package to facilitate the use of Google Shopping API'

setup(
    name="gshoppy",
    version=VERSION,
    author="Jake Williamson",
    author_email="<brianjw88@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests', 'pandas', 'google-api-python-client', 'google-auth-httplib2', 'google-auth-oauthlib'],
    keywords=['python', 'google', 'shopping', 'api', 'google shopping api'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3"
    ]
)
