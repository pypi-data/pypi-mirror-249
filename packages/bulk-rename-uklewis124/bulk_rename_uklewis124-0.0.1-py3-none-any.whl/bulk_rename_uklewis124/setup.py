from setuptools import setup, find_packages

setup(
    name='bulk_rename',
    version='0.0.1',
    author='Lewis Davies',
    author_email='lewisastondavies1@gmail.com',
    description='A package to rename multiple files and folders',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows"
    ],
    python_requires='>=3.6',
    install_requires=['os', 'sys']
)