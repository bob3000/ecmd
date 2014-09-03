# ecmd - elastichosts Command Line Client

This an unofficial command line client for the
[elastichosts](http://www.elastichosts.com) API. At the moment this
program is only a **technical demonstration**.

## Table of contents

- [Features](#features)
- [Getting started](#getting-started)
    - [Setup](#setup)
- [Usage example](#usage-example)
    - [Obtaining General Information](#obtaining-general-information)
- [Documentation](#documentation)
    - [Command line help](#command-line-help)
    - [Manpage](#manpage)
    - [Doctest](#doctest)
- [Hacking](#hacking)
    - [Requirements](#requirements)
    - [Bootstrap](#bootstrap)
    - [Makefile](#makefile)
    - [Running the tests](#running-the-tests)
    - [Cleaning up](#cleaning-up)
- [Bugs](#bugs)

## Features

- Obtain information about drives and by which servers they are used

## Getting started

To try the program you could simply run it form inside the sandbox like it's
described in the [hacking section](#hacking)

**or**

you can simply use this alias

    alias ecmd='PYTHONPATH=/<path>/<to>/ecmd/ python3 -m ecmd'

to run the program directly on your computer.

### Setup

Provide user credentials and API Base URL via environment variables.

    export EHUUD=<your uudi>
    export EHSECRET=<your secret>
    export EHBASEURL=<API base url>

**EHUUD** and **EHSECRET** can be found in your elastichosts profile in the
Authentication tab.
**EHBASEURL** corresponds to the hostname in the url shown in the browser
while logged into the management console (e.g. https://lon-b.elastichosts.com)
prefixed by `api-` (e.g. https://api-lon-b.elastichosts.com)

## Usage Example

Print out information about servers and belonging drives.

    ecmd drives

## Documentation

### Command line help

Inside the vagrant box type `ecmd --help` to get an overview of the command
line interface.

### Manpage

Inside the vagrant box type `man ecmd` to open the manpage. At the moment the
manpage is still work in progress.

### Doctest

The projects integration test is supposed to serve a documentation purpose as
well as blackbox testing. The file can be found here:
[integration\_test.md](ecmd/tests/integration_test.md)

## Hacking

### Requirements

- [VirtualBox](https://www.virtualbox.org)
- [Vagrant](http://www.vagrantup.com/)

### Bootstrap

After cloning the project enter the project directory and type `vagrant up`.
Wait until everything is setup and enter the sandbox with `vagrant ssh`.

### Makefile

There is a Makefile inside the project root directory which server as a central
entry point for developing tasks like running tests or package building. All
tasks described inside the Makefile are **supposed to be run from inside the
sandbox** in order to to run properly and to keep your host system clean.

### Running the tests

The following command will run the unittests as well as the integration test.

    make test

Code coverage can be figured out with

    make coverage

This will create a `htmlcov` directory in the project root. Open the
`index.html` inside this folder to see the coverage report.

### Cleaning up

Run the following command to safely delete all temporary files which are
are created while running test and building packages.

    make clean

## Bugs

I encourage you to report bugs in github issues.
