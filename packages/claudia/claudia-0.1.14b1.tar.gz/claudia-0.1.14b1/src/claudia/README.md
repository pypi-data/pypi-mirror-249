# Claudia

Claudia is a tool which helps make a few XRPL specific tasks look very easy. Tasks like running a local instance of
rippled, managing a local network, managing a sidechain network, running tests and even learning a few neat tricks with
XRPL in a quick fashion can be done effortlessly with this tool.

Claudia was developed by the XRPL Automation Team as an internal tool to help with XRPL local development, debugging and
testing. As the tool matured, the team quickly realized its potential and decided to expose it outside of Ripple, so
that everyone can benefit from its capabilities.

Following are some of the important tasks that can be performed using Claudia:

- Build rippled from local code.
- Install rippled from pre-built binaries released by Ripple.
- Manage a local-mainnet network using local rippled instance.
- Locally build a local witness server to start a sidechain network.
- Manage a local-sidechain network.
- Run unit tests on the built/installed rippled instance.
- Run system tests on local-mainnet, local-sidechain, devnet and testnet networks.
- Manage rippled features on the local-mainnet and local-sidechain networks.
- Learn more about XRPL capabilities and perform real-time learning activities on local-mainnet, local-sidechain, devnet
  and testnet networks.

---

## General Prerequisites

Claudia can be installed on both macOS and Ubuntu. Currently, there is no support for Windows. Following prerequisites
must be installed before installing Claudia:

- [Python3](https://www.python.org/)
    - Run ```python3 --version``` to check if Python3 is already installed.
    - If Python3 is not installed, please install it using the
      official [Python installer](https://www.python.org/downloads/).
    - Verify installation by running: ```python3 --version```
- [pip3](https://pip.pypa.io/en/stable/)
    - Run ```pip3 --version``` to check if Python3 is already installed.
    - If pip3 is not installed, follow the next steps:
        - macOS:
            - ```python3 -m ensurepip --upgrade```
        - Linux:
            - ```sudo apt update```
            - ```sudo apt install python3-pip```
        - Verify installation by running: ```pip3 --version```
- [docker](https://www.docker.com/)
    - Run ```docker --version``` to check if docker is already installed.
    - If docker is not installed, follow the next steps:
        - macOS:
            - Download and then run
              the [Docker Desktop installer for macOS](https://docs.docker.com/desktop/install/mac-install/).
        - Linux:
            - Download and then run
              the [Docker Desktop installer for Linux](https://docs.docker.com/desktop/install/linux-install/).
- Claudia allows its users to run System tests using Javascript client library. The following is **ONLY** required if you
  intend to run the Javascript system tests:
    - [node](https://nodejs.org/en/download)
        - Run ```node --version``` to check if node is already installed.
        - If node is not installed, follow the next steps:
            - macOS:
                - ```brew install node```
            - Linux:
                - ```curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt-get install -y nodejs```
    - [npm](https://www.npmjs.com/package/download)
        - Run ```npm -v``` to check if npm ia already installed.
        - If npm in not installed, follow the next steps:
            - macOS:
                - ```brew install npm```
            - Linux:
                - ```sudo apt install npm```

---

## Installation

Once the general prerequisites have been installed, Claudia can be installed
from [PyPi](https://pypi.org/project/claudia/). From your terminal please run:

    pip3 install claudia

### If you want to build Claudia from the local code, you can run:

      rm -fr build/ dist/ claudia.egg-info
      pip uninstall -y claudia
      python3 setup.py sdist bdist_wheel
      pip install dist/*.tar.gz
      rm -fr build/ dist/ claudia.egg-info

---

## Usage

Claudia has a bunch of self-explanatory features which are offered via a seamless UI and CLI experience. Please note that
XRPL Learning Center is only available with Claudia UI.

Claudia CLI offers two modes:

1. Demo mode. This is an interactive mode that can help reduce typing efforts significantly. You would mostly navigate a
   pre-built menu using ↑ ↓ and ↵ keys. Minimal typing will be required.
2. (Standard) CLI mode.

### How to run Claudia CLI commands?

After installing claudia, go to your terminal and run claudia. Each command supports --help flag that displays the usage
and arguments. e.g. claudia --help, claudia run --help

### How to run Claudia in demo mode?

From your terminal and run claudia demo

### How to start Claudia UI?

From your terminal, run claudia ui. Alternatively, you can launch the UI via the Claudia demo mode by selecting Launch
Claudia UI

---

## Features

Claudia offers a bunch of features which allows you to manage local rippled instance, manage networks, run tests and
even learn a few XRPL tricks. This section walks you through some major features.

### How to build rippled?

Claudia offers a way to build rippled from local code. You will need to
clone [rippled](https://github.com/XRPLF/rippled) repository first before starting with this step. If you intend to use
sidechain functionality, please use [this](https://github.com/seelabs/rippled/tree/xbridge) rippled fork instead.

Once the repository has been cloned, you can build rippled as follows. Each option would require you to provide the ***
absolute path*** to the cloned repository.

- UI
    - Navigate to `Custom XRPL Networks` and select `Build rippled`
- CLI Mode
    - Run `claudia rippled build --repo <repo_path>`
- Demo Mode
    - Select `Custom XRPL Networks` -> `Build rippled from local code`

### How to install rippled?
Claudia offers a way to install rippled using the pre-built binaries distributed by Ripple.
By default, Claudia will choose binaries generated from the master branch.
You also have an option to specify different branches.
Possible options are: master, develop and release (case-sensitive).
You can install rippled as follows:
- UI
    - Navigate to `Custom XRPL Networks` and select `Install rippled`
- CLI Mode
  - Run `claudia rippled install` to install rippled binaries built from master branch.
  - Run `claudia rippled install --rippled_branch <branch_name>` and choose the rippled branch.
- Demo Mode
    - Select `Custom XRPL Networks` -> `Install rippled`

### How to switch between build and install rippled modes?

Once you build or install rippled, Claudia will remember that context forever. If you have already built and installed
rippled in both modes, and would like to switch between the two modes, run the following:

- UI
    - Navigate to `Settings` and select `Set Install Mode`
- CLI Mode
    - Run `claudia set-install-mode build` to set build mode.
    - Run `claudia set-install-mode install` to set install mode.
- Demo Mode
    - Select `Settings` -> `Set install mode as build` to set build mode.
    - Select `Settings` -> `Set install mode as install` to set install mode.

*Please note that all previously running networks will have to be stopped and started again after switching rippled
modes.*

### How to enable a feature in rippled?

Please note that there is no validation for feature name. Please make sure the feature name is correct (case-sensitive).
You can follow these instructions to enable a rippled feature:

- UI
    - Navigate to `Settings` and select `Enable a rippled feature`
- CLI Mode
    - Run `claudia enable-feature --feature <feature_name>`
- Demo Mode
    - Select `Settings` -> `Enable a rippled feature`

### How to disable a feature in rippled?

Please note that there is no validation for feature name. Please make sure the feature name is correct (case-sensitive).
You can follow these instructions to disable a rippled feature:

- UI
    - Navigate to `Settings` and select `Disable a rippled feature`
- CLI Mode
    - Run `claudia disable-feature --feature <feature_name>`
- Demo Mode
    - Select `Settings` -> `Disable a rippled feature`

### How to build witness server?

Before you can start a sidechain network, you will need to build a witness server locally. You will need to
clone [XBridge Witness](https://github.com/seelabs/xbridge_witness) repository first before starting on this step. Once
the repository has been cloned, you can build the witness server as follows. Each option would require you to provide
the absolute path to the cloned repository.

- UI
    - Navigate to `Custom XRPL Networks` and select `Build Witness Server`
- CLI Mode
    - Run `claudia witness build --repo <repo_path>`
- Demo Mode
    - Select `Custom XRPL Networks` -> `Build witness server`

### How to deploy custom network to AWS?

You can use Claudia to spin up a custom network on your AWS cloud infrastructure. This option is only supported via UI. 

Navigate to `Custom XRPL Networks` and select `Deploy Network to Cloud`. You will be asked to provide the following information: 
* AWS IAM user access key
* AWS IAM user secret access key
* Region

Claudia runs each a validator node on a separate EC2 instance. At least two validator nodes are required to spin up a network.
You can choose to run up to 10 validator nodes running the rippled variant built using the latest master branch code. 
Similarly, you can choose to run up to 10 validator nodes running the rippled variant built using the latest release and
develop branches code each. This way you can run up to 30 validator nodes running three different rippled variants.

The deployment process takes a while. Once finished, the details will be provided along with the connection URLs.

### How to start a local-mainnet network?

Before you can start a local mainnet network, rippled has to be built or installed locally. Afterwards, you can follow
these instructions to start a local mainnet network:

- UI
    - Navigate to `Custom XRPL Networks` and select `Start Network`
- CLI Mode
    - Run `claudia local-mainnet start`
- Demo Mode
    - Select `Custom XRPL Networks` -> `Start local-mainnet`

### How to stop a local-mainnet network?

You can follow these instructions to stop a local mainnet network:

- UI
    - Navigate to `Custom XRPL Networks` and select `Stop Network`
- CLI Mode
    - Run `claudia local-mainnet stop`
- Demo Mode
    - Select `Custom XRPL Networks` -> `Stop local-mainnet`

### How to start a local-sidechain network?

Before you can start a local sidechain network:

1. rippled has to be built/installed locally.
2. Witness server has to be built locally.
3. `XChainBridge` rippled feature has to be enabled.
4. The local-mainnet network has to be running.

Once all the requirements have been met, you can start the local sidechain network as follows:

- UI
    - Navigate to `Custom XRPL Networks` and select `Start Sidechain Network`
- CLI Mode
    - Run `claudia local-sidechain start`
- Demo Mode
    - Select `Custom XRPL Networks` -> `Start local-sidechain`

### How to stop a local-sidechain network?

You can follow these instructions to stop a local sidechain network:

- UI
    - Navigate to `Custom XRPL Networks` and select `Stop Sidechain Network`
- CLI Mode
    - Run `claudia local-sidechain stop`
- Demo Mode
    - Select `Custom XRPL Networks` -> `Stop local-sidechain`

Please note that once the sidechain has been stopped, local-mainnet has to be restarted before attempting to start the
local-sidechain again.

### How to run unit tests?

Before you can run unit tests, rippled has to be built or installed locally. Afterwards, you can run the unit tests as
follows:

- UI
    - Navigate to `XRPL tests` and select `Run Unit Tests`
- CLI Mode
    - Run `claudia run unittests`. Run `claudia run unittests --help` to see options.
- Demo Mode
    - Select `XRPL Tests` -> `Run unit tests`

By default, all tests will run. Optionally, you can also set a filter to run a selected few tests in each mode.

### How to run system tests?

Claudia offers a way to run system tests on different networks. If you wish to run tests on locally running mainnet or
sidechain networks, the networks should be running first. Alternatively, you can run the tests on devnet and testnet as
well.

The system tests can run using either JavaScript or Python client libraries. For Python client, both `JSON-RPC`
and `WebSocket` connections are supported. JavaScript client only supports `WebSocket` connection.

These tests are broken down into different features and are tagged as well. You can choose to run a few or all tests.
Please note that if you chose regression tag, all test in the chosen feature will be executed.

The system tests can be configured to be run in any way you need them to. By default, the following configuration is
selected:

- **Client Library:** `Python`
- **Connection:** `JSON-RPC`
- **Network:** `local-mainnet`
- **Test Tag:** `smoke`
- **Feature:** `payments`

The system test run can be started as follows:

- UI
    - Navigate to `XRPL tests` and select `Run System Tests`. Choose your options and start the run.
- CLI Mode
    - Run `claudia run systemtests`. Run `claudia run systemtests --help` to see options.
- Demo Mode
    - Select `XRPL Tests` -> `Run system tests`

### How to cleanup your computer and free resources after running Claudia?

While using claudia, there are a few files created permanently. Also, there are a few system resources which are
reserved for future use. Running this command will delete these files and free up resources. As a result, any progress
made by using Claudia will be lost. This action cannot be undone. Resources can be freed and your machine can be freed
as follows:

- UI
    - Navigate to `Settings` and select `Cleanup`
- CLI Mode
    - Run `claudia clean`
- Demo Mode
    - Select `Settings` -> `Clean up the host and free resources`

### How to run XRPL Learning Center?

Claudia offers a neat interactive learning environment in which you can learn a few things about XRPL. These learning
activities can be performed on local-mainnet, local-sidechain, devnet and testnet networks. You can launch the XRPL
Learning Center only via UI.

Navigate to `XRPL Learning Center`, select a learning activity and follow the instructions.

### How to uninstall Claudia?

*We recommend that you cleanup your machine before uninstalling Claudia.* Afterwards, please run:

    pip3 uninstall claudia

## Contributions

Claudia is developed by Ripple Automation Team. The following people contributed to this release:

- Manoj Doshi <mdoshi@ripple.com>
- Ramkumar SG <rsg@ripple.com>
- Kaustubh Saxena <ksaxena@ripple.com>
- Michael Legleux <mlegleux@ripple.com>
- Anagha Agashe <aagashe@ripple.com>
- Mani Mounika Kunasani <mkunasani@ripple.com>
