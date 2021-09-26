import sys
sys.dont_write_bytecode = False

campaign = {
    'mc': 'MC14ri_a',
    'data': 'test_data'
}

samples = {
    'mc': {
        'Kpi0': ['Kpi0'],
        'taupair': ['taupair'],
        'uubar': ['uubar-1', 'uubar-2', 'uubar-3', 'uubar-4'],
        'ddbar': ['ddbar'],
        'ssbar': ['ssbar'],
        'ccbar': ['ccbar-1', 'ccbar-2', 'ccbar-3', 'ccbar-4'],
        'charged': ['charged-1', 'charged-2'],
        'mixed': ['mixed-1', 'mixed-2']
    },
    'data': {
        'taupair': ['taupair']
    }
}

projects = {}
for k, v in samples.items():
    l = []
    for _, vv in v.items():
        for p in vv: l.append(p)
    projects[k] = l
