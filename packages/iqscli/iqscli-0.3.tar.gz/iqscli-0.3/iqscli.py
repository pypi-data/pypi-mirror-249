#!/usr/bin/env python3

#
# SPDX-FileCopyrightText: 2024 Mete Balci
#
# SPDX-License-Identifier: Apache-2.0
#
# Copyright (c) 2024 Mete Balci
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import argparse
import sys

from qiskit_ibm_runtime.accounts.exceptions import AccountNotFoundError

parser = argparse.ArgumentParser()

def save_account(argv):
    from qiskit_ibm_runtime import QiskitRuntimeService

    parser.add_argument('--channel',
                        help='IBM Quantum System channel',
                        choices=['ibm_quantum', 'ibm_cloud'],
                        required=True)

    parser.add_argument('--token',
                        help='IBM Cloud API key',
                        required=True,
                        default=False)

    parser.add_argument('--instance',
                        help='hub/group/project or CRN',
                        default=None)

    parser.add_argument('--set-as-default',
                        help='set the account as default',
                        action='store_true',
                        default=False)

    args = parser.parse_args(args=argv)

    QiskitRuntimeService.save_account(channel=args.channel,
                                      token=args.token,
                                      instance=args.instance,
                                      name=args.account_name,
                                      set_as_default=args.set_as_default)

def saved_accounts(args):
    from qiskit_ibm_runtime import QiskitRuntimeService

    for (k, v) in QiskitRuntimeService.saved_accounts().items():
        print('%s -> %s' % (k, v['channel']))

def backends(argv):
    from qiskit_ibm_runtime import QiskitRuntimeService

    parser.add_argument('--sim',
                        help='only show simulators',
                        action='store_true',
                        default=False)

    parser.add_argument('--real',
                        help='only show real computers',
                        action='store_true',
                        default=False)

    parser.add_argument('--name',
                        help='only show this backend')

    parser.add_argument('--show-details',
                        help='show details of each backend',
                        action='store_true',
                        default=False)

    args = parser.parse_args(args=argv)

    filterfn = lambda x:True

    if args.name:
        filterfn = lambda x:x.name == args.name
    elif args.sim:
        filterfn = lambda x:x.simulator
    elif args.real:
        filterfn = lambda x:not x.simulator

    service = QiskitRuntimeService(name=args.account_name)
    backends = sorted(service.backends(filters=filterfn),
                      key=lambda x:x.name)

    max_len_name = max([len(x.name) for x in backends])
    name_format = '%%-%ds' % (max_len_name + 4)

    for b in backends:

        # there is an error in the API with stabilizers at the moment
        if b.name == 'simulator_stabilizer':
            continue
        if b.name == 'simulator_extended_stabilizer':
            continue

        status = b.status()
        operational = 'ONLINE' if status.operational else 'OFFLINE'

        if args.show_details:
            print('%s' % b.name, end='')
        else:
            print(name_format % b.name, end='')

        print(' %s (%d jobs)' % (operational,
                                 status.pending_jobs))

        if args.show_details:

            if hasattr(b, 'processor_type'):
                pt = b.processor_type
                print('     processor: %s r%s' % (pt['family'],
                                                  pt['revision']))

            print('    num_qubits: %d' % b.num_qubits)
            print('     max_shots: %d' % b.max_shots)
            print('   basis_gates: %s' % ', '.join(b.basis_gates))

            if hasattr(b, 'supported_instructions'):
                print('  instructions: %s' % ', '.join(b.supported_instructions))

            if hasattr(b, 'meas_kernels'):
                print('  meas_kernels: %s' % ', '.join(b.meas_kernels))

            print()

def jobs(argv):
    from qiskit_ibm_runtime import QiskitRuntimeService

    parser.add_argument('--limit',
                        help='number of jobs in a page',
                        type=int,
                        default=10)

    parser.add_argument('--page',
                        help='page number',
                        type=int,
                        default=0)

    parser.add_argument('--backend-name',
                        help='backend name',
                        default=None)

    parser.add_argument('--show-not-pending',
                        help='show not queued or running but done, cancelled and error',
                        action='store_true',
                        default=True)

    parser.add_argument('--program-id',
                        help='filter by program id',
                        default=None)

    parser.add_argument('--instance',
                        help='filter by instance (hub/group/project)',
                        default=None)

    args = parser.parse_args(args=argv)

    jobs = QiskitRuntimeService().jobs(limit=args.limit,
                                       skip=args.limit * args.page,
                                       backend_name=args.backend_name,
                                       pending=not args.show_not_pending,
                                       program_id=args.program_id,
                                       instance=args.instance,
                                       descending=True)

    for j in jobs:
        print('%s %s %s %s %s' % (j.job_id(),
                                  j.backend().name,
                                  j.program_id,
                                  j.status().name,
                                  j.creation_date.strftime('%Y%m%d%H%M%S%f')))

def main_help():
    print()
    print('Usage: iqscli <command>')
    print()
    print('  <command> can be:')
    print()
    print('  - backends:       show backends')
    print('  - jobs:           show jobs')
    print('  - save_account:   save account')
    print('  - saved_accounts: list saved accounts')
    print()

def main():
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        argv = sys.argv[2:]
        parser.add_argument('--account-name',
                            help='account name',
                            default=None)
        try:
            if cmd == 'backends':
                backends(argv)
            elif cmd == 'jobs':
                jobs(argv)
            elif cmd == 'save_account':
                save_account(argv)
            elif cmd == 'saved_accounts':
                saved_accounts(argv)
            else:
                print('unknown command')
                main_help()
        except AccountNotFoundError:
            print('unable to find account, use save_account command first and use --account-name if not default')
    else:
        main_help()

if __name__ == '__main__':
    main()
