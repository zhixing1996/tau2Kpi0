import os
import sys
from attr.run_params import campaign, samples, projects
from attr.cut_params import cut_vars
from attr.text_params import samples_text
sys.dont_write_bytecode = False

author = 'Maoqiang Jing <jingmq@ihep.ac.cn>'
date = '16:48 30-August-2021'
copyright = 'Copyright (c) 2021-2023 Maoqiang Jing'

os.system('mkdir -p ./rootfiles/')
debug = False
cur_dir = os.path.abspath(os.path.dirname('__file__'))
steering_file = cur_dir + '/src/tau2Kpi0_sel.py'
release = 'light-2106-rhea'
files_perjob = '2'
sample_type = 'mc'

tree_name = 'tau2Kpi0'
