#!/usr/bin/env python

from os import path
import argparse
import context
from helpers import utils
from helpers.subprocess_wrappers import check_call

VALID_LIST = ["vegas-bbr-cubic",
            "vegas-cubic-bbr",
            "bbr-vegas-cubic",
            "bbr-cubic-vegas",
            "cubic-vegas-bbr",
            "cubic-bbr-vegas"]

def get_args():
    parser = argparse.ArgumentParser(description = "Processing the test live generation")
    parser.add_argument("--config-name", help="Enter config-names, supoorted options are cubic, bbr, vegas, cubic-vegas, ...")
    parser.add_argument("--trace-file-path", help="enter path of trace file")
    parser.add_argument("--data-dir-path", help="enter the path to save the trace experiments")
    parser.add_argument("--delay", help="enter delay in seconds")
    args = parser.parse_args()
    return args


def get_sample_config(config_name, delay):
    if config_name in VALID_LIST:
        config = ('test-name: test-vegas-bbr-cubic \n'
                  'runtime: 60 \n'
                  'random_order: true \n'
                  f'prepend_mm_cmds: mm-delay {delay} \n'
                  'flows: \n'
                  '  - scheme: vegas \n'
                  '  - scheme: cubic \n'
                  '  - scheme: bbr')
    elif config_name == 'vegas-bbr' or config_name == 'cubic-bbr':
        config = ('test-name: test-vegas-bbr \n'
                  'runtime: 60 \n'
                  'random_order: true \n'
                  f'prepend_mm_cmds: mm-delay {delay} \n'
                  'flows: \n'
                  '  - scheme: vegas \n'
                  '  - scheme: bbr')
    elif config_name == 'vegas-cubic' or config_name == 'cubic-vegas':
        config = ('test-name: test-vegas-cubic \n'
                  'runtime: 60 \n'
                  'random_order: true \n'
                  f'prepend_mm_cmds: mm-delay {delay} \n'
                  'flows: \n'
                  '  - scheme: vegas \n'
                  '  - scheme: cubic')
    elif config_name == 'bbr-cubic' or config_name == 'cubic-bbr':
        config = ('test-name: test-bbr-cubic \n'
                  'runtime: 60 \n'
                  'random_order: true \n'
                  f'prepend_mm_cmds: mm-delay {delay} \n'
                  'flows: \n'
                  '  - scheme: bbr \n'
                  '  - scheme: cubic')
    elif config_name == 'cubic':
        config = ('test-name: test-cubic \n'
                  'runtime: 60 \n'
                  'random_order: true \n'
                  f'prepend_mm_cmds: mm-delay {delay} \n'
                  'flows: \n'
                  '  - scheme: cubic')
    elif config_name == 'bbr':
        config = ('test-name: test-bbr \n'
                  'runtime: 60 \n'
                  'interval: 1 \n'
                  'random_order: true \n'
                  f'prepend_mm_cmds: mm-delay {delay} \n'
                  'flows: \n'
                  '  - scheme: bbr')
    elif config_name == 'vegas':
        config = ('test-name: test-vegas \n'
                  'runtime: 60 \n'
                  'random_order: true \n'
                  f'prepend_mm_cmds: mm-delay {delay} \n'
                  'flows: \n'
                  '  - scheme: vegas')
        

    config_path = path.join(utils.tmp_dir, '%s.yml' % config_name)
    with open(config_path, 'w') as f:
        f.write(config)

    return config_path


def main():
    args = get_args()
    data_trace = path.abspath(args.trace_file_path)
    ack_trace = path.abspath(args.trace_file_path)
    test_py = path.join(context.src_dir, 'experiments', 'test.py')
    config_name = args.config_name
    data_dir = path.abspath(args.data_dir_path)
    delay = int(args.delay)
    # test running with a config file -- one receiver first, one sender first scheme
    config = get_sample_config(config_name, delay)
    cmd = [test_py, '-c', config, 'local',
           '--uplink-trace', data_trace, '--downlink-trace', ack_trace,
           '--pkill-cleanup', '--data-dir', data_dir]
    check_call(cmd)
    analyze_path = path.join(context.src_dir, 'analysis', 'analyze.py')
    analyze_cmd = [analyze_path, '--data-dir', data_dir]
    check_call(analyze_cmd)

if __name__ == '__main__':
    main()
