#!/user/bin/python3
# +++++++++++++++++++++++++++++++++++++++++++++++++++
# @File Name: args.py
# @Author: Qing-Yuan Jiang
# @Mail: qyjiang24 AT gmail.com
# +++++++++++++++++++++++++++++++++++++++++++++++++++
import argparse
import os

from datetime import datetime

parser = argparse.ArgumentParser()
'''basic setting'''
parser.add_argument('--bit', '-B', type=int, default=16, help='binary code length (default: 12 bits)')
parser.add_argument('--seed', '-S', type=int, default=1, help='random seed (default: 0)')
parser.add_argument('--output-path', type=str, default='log', help='output path (default: ./log)')

'''dataset setting'''
parser.add_argument('--dataname', type=str, default='flickr25k', help='data name (default: flickr25k)')
parser.add_argument('--no-deep-feature', action='store_true', default=True, help='utilizing deep feature or not')

'''logger setting'''
parser.add_argument('--en-local-log', action='store_true', default=False,
                    help='enable save log to local file (default: True)')

'''approach param'''
parser.add_argument('--approach', default='dlfh', type=str)
parser.add_argument('--max-iter', default=50, type=float)
parser.add_argument('--lamda', default=8, type=float)
parser.add_argument('--gamma', default=1e-6, type=float)

args = parser.parse_args()
args.timestamp = datetime.now().strftime('%y-%m-%d-%H-%M-%S')
parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

logdir = os.path.join(parentddir, args.output_path, '-'.join(['log', args.approach, args.timestamp]))
args.logdir = logdir

if args.en_local_log:
    os.mkdir(logdir)

import platform
if 'linux' in platform.platform().lower():
    args.datapath = '/home/jiangqy/DLFH-TIP2019/data'

if 'darwin' in platform.platform().lower():
    args.datapath = '/Users/jiangqy/DLFH-TIP2019/data'

