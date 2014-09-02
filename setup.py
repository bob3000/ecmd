from setuptools import setup

setup(
    name="ecmd",
    version="0.0.0",
    license="GNU GPL v3",
    packages=[
        "ecmd",
    ],
    test_suite="ecmd",
    install_requires={
    },
    entry_points={
        "console_scripts": [
            "ecmd = ecmd.__main__:main",
        ],
    },
    data_files=[
        ('/usr/share/man/man1', ['man/ecmd.1.gz']),
        ('/usr/share/bash-completion/completions', ['completion/ecmd']),
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: BSD :: FreeBSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Topic :: System :: Archiving :: Packaging",
        "Intended Audience :: End Users/Desktop",
    ],
)
