#!/usr/bin/env python

from os import path

import context
from helpers import utils
from helpers.subprocess_wrappers import check_call


def get_sample_config(config_name):
    if config_name == 'vivace-cubic-fillp':
        config = ('test-name: test-bbr \n'
                  'runtime: 60 \n'
                  'interval: 1 \n'
                  'random_order: true \n'
                  'extra_mm_link_args: --uplink-queue=droptail '
                  '--uplink-queue-args=packets=512 \n'
                  'prepend_mm_cmds: mm-delay 10 \n'
                  'flows: \n'
                  '  - scheme: vivace \n'
                  '  - scheme: cubic \n'
                  '  - scheme: fillp')

    elif config_name == 'fillp-cubic':
        config = ('test-name: test-bbr \n'
                  'runtime: 30 \n'
                  'interval: 1 \n'
                  'random_order: true \n'
                  'extra_mm_link_args: --uplink-queue=droptail '
                  '--uplink-queue-args=packets=512 \n'
                  'prepend_mm_cmds: mm-delay 30 \n'
                  'flows: \n'
                  '  - scheme: fillp \n'
                  '  - scheme: cubic')
    elif config_name == 'vivace':
        config = ('test-name: test-bbr \n'
                  'runtime: 30 \n'
                  'interval: 1 \n'
                  'random_order: true \n'
                  'extra_mm_link_args: --uplink-queue=droptail '
                  '--uplink-queue-args=packets=512 \n'
                  'prepend_mm_cmds: mm-delay 30 \n'
                  'flows: \n'
                  '  - scheme: vivace')
    elif config_name == 'cubic':
        config = ('test-name: test-bbr \n'
                  'runtime: 30 \n'
                  'interval: 1 \n'
                  'random_order: true \n'
                  'extra_mm_link_args: --uplink-queue=droptail '
                  '--uplink-queue-args=packets=512 \n'
                  'prepend_mm_cmds: mm-delay 30 \n'
                  'flows: \n'
                  '  - scheme: cubic')
    elif config_name == 'fillp':
        config = ('test-name: test-bbr \n'
                  'runtime: 30 \n'
                  'interval: 1 \n'
                  'random_order: true \n'
                  'extra_mm_link_args: --uplink-queue=droptail '
                  '--uplink-queue-args=packets=512 \n'
                  'prepend_mm_cmds: mm-delay 30 \n'
                  'flows: \n'
                  '  - scheme: fillp')
        

    config_path = path.join(utils.tmp_dir, '%s.yml' % config_name)
    with open(config_path, 'w') as f:
        f.write(config)

    return config_path


def main():
    data_trace = path.join(context.src_dir, 'experiments', '50mbps.trace')
    ack_trace = path.join(context.src_dir, 'experiments', '50mbps.trace')

    test_py = path.join(context.src_dir, 'experiments', 'test.py')
    config_name = 'vivace-cubic-fillp'
    data_dir = path.join(context.src_dir, 'experiments', 'data', config_name)
    # test running with a config file -- one receiver first, one sender first scheme
    config = get_sample_config(config_name)
    cmd = ['python', test_py, '-c', config, 'local',
           '--uplink-trace', data_trace, '--downlink-trace', ack_trace,
           '--pkill-cleanup', '--data-dir', data_dir]
    check_call(cmd)
    analyze_path = path.join(context.src_dir, 'analysis', 'analyze.py')
    analyze_cmd = ['python', analyze_path, '--data-dir', data_dir]
    check_call(analyze_cmd)

if __name__ == '__main__':
    main()
