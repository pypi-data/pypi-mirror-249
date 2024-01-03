# iqscli

iqscli is an unofficial CLI for IBM Quantum Systems.

*This project has NO connection with IBM. It is my personal project. As of 2024-01-03, I am not employed by IBM and I have no connection with IBM other than having an IBM Quantum and IBM Cloud user account. All information in this repository is acquired from the public documents for example from docs.quantum.ibm.com and cloud.ibm.com/docs.*

## IBM Quantum Systems

### Channels and Plans

There are two channels and four plans (two on each channel) to use IBM Quantum Systems. 

The channels are:

- [IBM Quantum](https://quantum.ibm.com) (`ibm_quantum` in qiskit)
- [IBM Cloud](https://cloud.ibm.com) (`ibm_cloud` in qiskit)

The credentials (API tokens) on these systems are not the same. Tokens are created separately. 

IBM Quantum has:

- Open Plan: provides a 10 minute monthly access to 127-qubit systems and unlimited access to Simulators. This plan is free.

- Premium Plan: provides access to both 127-qubit and 27-qubit systems as well as exploratory systems and Simulators and support. This is a paid plan and the price varies.

IBM Cloud has:

- Lite Plan: provides unlimited access to Simulators only. This plan is free.

- Standard Plan: provides Pay-As-You-Go access to 127-qubit and 27-qubit systems and unlimited access to Simulators. This is a paid plan and the price at the moment (2024-01-03) is 1.60 USD/second.

At the moment (2024-01-03), the best (free) way to access the simulators is IBM Quantum Open plan or IBM Cloud Lite plan. The best (free) way to access the real IBM Quantum Systems is IBM Quantum Open plan. Thus, IBM Quantum Open plan seems to be the best starting point.

### Instances

The services both on IBM Quantum and IBM Cloud are controlled by instances. An instance is identified by:

- hub/group/project in IBM Quantum
- CRN in IBM Cloud

When a user is signed up on IBM Quantum, it is assigned to the Open plan, and the Open plan's instance, which is `ibm-q/open/main` (i.e. hub is IBM Quantum called ibm, group is open, project is main). When a user is assigned to a premium plan, a particular hub/group/project is given.

When a Qiskit Runtime instance is created on IBM Cloud, the plan, lite or standard, has to be chosen. When a Qiskit Runtime instance is created, its CRN is displayed on the instance details.

### Quantum Systems

At the moment, I see the following Eagle based 127-qubit systems in both of my IBM Quantum and IBM Cloud accounts: `ibm_brisbane`, `ibm_kyoto` and `ibm_osaka`. IBM Cloud account also shows a Falcon based 27-qubit system called `ibm_algiers`. 

These are not all the systems. A comprehensive listing can be found in [Compute resources @ IBM Cloud](https://cloud.ibm.com/quantum/resources/systems) and [Compute resources @ IBM Quantum Platform](https://quantum.ibm.com/services/resources?tab=systems).

## Installation

```
pip install iqscli
```

## Usage

*The account information and the credentials including the token is saved to an open file, it is not encrypted. Thus, it is readable by anyone. On Linux, the credentials file is $HOME/.qiskit/qiskit-ibm.json.*

### save-account, saved-accounts, delete-account

Before using any other command, `save-account` command should be run to save the credentials (API token) for later use. One account can be marked as default with `--set-as-default` and it is used when no `--account-name` or `--channel` is provided with the commands.

With `save-account`, if no `--account-name` is provided, account is saved with a default name, `default-ibm-quantum` or `default-ibm-cloud` depending on the channel. Thus, each channel can have one default account. This account is selected if `--channel` is provided. Thus, all commands (except `saved-accounts`) have `--channel` and `--account-name` options. The account selection is (as described in Qiskit Runtime IBM Client):

- when `--account-name` is given, corresponding account is used
- when `--account-name` is not given but `--channel` is given, the default account for the channel is used (default-ibm-quantum or default-ibm-cloud)
- when neither `--account-name` nor `--channel` is given, the default account is used

After the credentials are saved once, the subsequent runs to `save-account` works successfully only with `--overwrite`, since the credentials file should be overwritten.

For example, save a default IBM Quantum Open instance account:

```
$ iqscli save-account --channel ibm_quantum --instance ibm-q/open/main --token <token>
```

List saved accounts:

```
$ iqscli saved-accounts
default-ibm-quantum @ ibm_quantum = ibm-q/open/main
```

### backends

List all backends:

```
$ iqscli backends
ibm-q/open/main @ ibm_quantum
ibm_brisbane                      ONLINE (13 jobs)
ibm_kyoto                         ONLINE (13 jobs)
ibm_osaka                         ONLINE (0 jobs)
ibmq_qasm_simulator               ONLINE (0 jobs)
simulator_mps                     ONLINE (0 jobs)
simulator_statevector             ONLINE (0 jobs)
```

Show details of a particular backend:

```
$ iqscli backends --show-details --name ibm_brisbane
ibm-q/open/main @ ibm_quantum
ibm_brisbane ONLINE (13 jobs)
     processor: Eagle r3
    num_qubits: 127
     max_shots: 100000
   basis_gates: ecr, id, rz, sx, x
  instructions: ecr, id, delay, measure, reset, rz, sx, x, if_else, for_loop, switch_case
  meas_kernels: hw_qmfk
```

### jobs

Show jobs:

```
$ iqscli jobs
ibm-q/open/main @ ibm_quantum
cma3f8oiidfp3m905ft0 ibmq_qasm_simulator sampler DONE 20240102171947812375
cma3688iidfp3m904dq0 ibmq_qasm_simulator sampler DONE 20240102170033755981
cma32c6879ps6bbv1mb0 ibmq_qasm_simulator sampler DONE 20240102165216597386
```

## Changes

0.4:
- improvements to existing commands

0.3:
- jobs command added

0.2:
- first pypi release
