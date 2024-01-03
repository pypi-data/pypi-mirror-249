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
import os
import sys

from qiskit_ibm_runtime import QiskitRuntimeService

from qiskit_ibm_runtime.accounts.exceptions import AccountNotFoundError
from qiskit_ibm_runtime.accounts.exceptions import AccountAlreadyExistsError
from qiskit import QiskitError

def get_parser(channel_required=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--account-name',
                        help='account name',
                        default=None)
    parser.add_argument('--channel',
                        help='IBM Quantum System channel',
                        choices=['ibm_quantum', 'ibm_cloud'],
                        default=None,
                        required=channel_required)
    return parser

def get_service(args):
    service = QiskitRuntimeService(name=args.account_name,
                                   channel=args.channel)

    account = service.active_account()

    print('%s @ %s' % (account['instance'],
                       account['channel']))

    return service

def saved_accounts(args):
    accounts = QiskitRuntimeService.saved_accounts()
    name_maxlen = max([len(x) for x in accounts.keys()])
    name_format = '%%-%ds' % name_maxlen
    channel_maxlen = max([len(x['channel']) for x in accounts.values()])
    channel_format = '%%-%ds' % channel_maxlen
    for (k, v) in accounts.items():
        print(name_format % k, end='')
        print(' @ ', end='')
        print(channel_format % v['channel'], end='')
        print(' = %s' % v['instance'])

def delete_account(argv):
    parser = get_parser()
    args = parser.parse_args(args=argv)
    QiskitRuntimeService.delete_account(channel=args.channel,
                                        name=args.account_name)

def save_account(argv):
    parser = get_parser(channel_required=True)

    parser.add_argument('--token',
                        help='IBM Cloud API key',
                        required=True)

    parser.add_argument('--instance',
                        help='hub/group/project or CRN',
                        required=True)

    parser.add_argument('--set-as-default',
                        help='set the account as default',
                        action='store_true',
                        default=False)

    parser.add_argument('--overwrite',
                        help='update the saved credentials',
                        action='store_true',
                        default=False)

    parser.add_argument('--channel-strategy',
                        help='set the error mitigation strategy',
                        default=None)

    args = parser.parse_args(args=argv)

    QiskitRuntimeService.save_account(channel=args.channel,
                                      token=args.token,
                                      instance=args.instance,
                                      name=args.account_name,
                                      set_as_default=args.set_as_default,
                                      channel_strategy=args.channel_strategy,
                                      overwrite=args.overwrite)

def backends(argv):
    parser = get_parser()

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

    service = get_service(args)

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
    parser = get_parser()

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

    service = get_service(args)

    jobs = service.jobs(limit=args.limit,
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
        try:
            if cmd == 'backends':
                backends(argv)
            elif cmd == 'delete-account':
                delete_account(argv)
            elif cmd == 'jobs':
                jobs(argv)
            elif cmd == 'save-account':
                save_account(argv)
            elif cmd == 'saved-accounts':
                saved_accounts(argv)
            else:
                print('unknown command')
                main_help()
        except AccountNotFoundError:
            print('ERROR: unable to find an account, use save-account command first and then use --account-name with commands if the acount is not set as default')
        except AccountAlreadyExistsError:
            print('ERROR: credentials already exists, use --overwrite to update the file')
        except QiskitError as e:
            print('ERROR: QiskitError: %s' % type(e).__name__)
            print('set iqscli_debug=1 environment variable for stack trace')
            if os.environ.get('iqscli_debug', False):
                raise
        except Exception as e:
            print('ERROR: Error: %s' % type(e).__name__)
            print('set iqscli_debug=1 environment variable for stack trace')
            if os.environ.get('iqscli_debug', False):
                raise
    else:
        main_help()

if __name__ == '__main__':
    main()
