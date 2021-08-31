import os
import sys
sys.dont_write_bytecode = True

author = 'Maoqiang Jing <jingmq@ihep.ac.cn>'
date = '16:48 30-August-2021'
copyright = 'Copyright (c) 2021-2023 Maoqiang Jing'

os.system('mkdir -p rootfiles')
cur_dir = os.path.abspath(os.path.dirname('__file__'))
steering_file = cur_dir + '/src/tau2Kpi0_sel.py'
release = 'light-2106-rhea'
files_perjob = '2'
campaign = 'MC14ri_a'
mc_samples = {
    'taupair': ['taupair'],
    'uubar': ['uubar-1', 'uubar-2', 'uubar-3', 'uubar-4'],
    'ddbar': ['ddbar'],
    'ssbar': ['ssbar'],
    'ccbar': ['ccbar-1', 'ccbar-2', 'ccbar-3', 'ccbar-4'],
    'charged': ['charged-1', 'charged-2'],
    'mixed': ['mixed-1', 'mixed-2']
}
mc_projects = []
for _, v in mc_samples.items():
    for p in v:
        mc_projects.append(p)
mc_source_roots = []
for mc_sample in mc_samples.keys():
    mc_source_roots.append(cur_dir + '/rootfiles/' + mc_sample + '/' + mc_sample + '_source.root')
