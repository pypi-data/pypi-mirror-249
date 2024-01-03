from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='google_nest_client',
    version='1.1.0',
    description='Google Nest API Client',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='',
    author='Jimming Cheng',
    author_email='jimming@gmail.com',
    packages=['google_nest_client'],
    install_requires=[
        'opencv-python',
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
