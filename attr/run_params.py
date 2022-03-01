import sys
sys.dont_write_bytecode = False

campaign = {
    'mc': 'MC13a',
    'data': 'Proc11'
}

samples = {
    'mc': {
        'uubar': ['uubar-1', 'uubar-2'],
        'ddbar': ['ddbar'],
        'ssbar': ['ssbar'],
        'ccbar': ['ccbar-1', 'ccbar-2'],
        'charged': ['charged'],
        'mixed': ['mixed'],
        'taupair': ['taupair'],
        'eeee': ['eeee'],
        'eemumu': ['eemumu'],
        'eeKK': ['eeKK'],
        'eepp': ['eepp'],
        'ee': ['ee'],
        'mumu': ['mumu'],
        'Kpi0': ['taupair']
    },
    'data': {
        'proc11': ['exp7']
    }
}

projects = {}
for k, v in samples.items():
    l = []
    for _, vv in v.items():
        for p in vv: l.append(p)
    projects[k] = l
