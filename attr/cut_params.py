import sys
sys.dont_write_bytecode = False

cut_vars = {
    'dr': {
        'var': {
            'dr_K': 'dr_K',
            'dr_l': 'dr_l',
        },
        'xtitle': {
            'dr_K': 'dr_{K} (cm)',
            'dr_l': 'dr_{e/#mu} (cm)',
        },
        'ytitle': 'Events',
        'xrange': [-5., 5., 100],
        'widget': ['legend'],
        'legend': [0.25, 0.35, 0.45, 0.85],
        'cut': ''
    },
    'dz': {
        'var': {
            'dz_K': 'dz_K',
            'dz_l': 'dz_l',
        },
        'xtitle': {
            'dz_K': 'dz_{K} (cm)',
            'dz_l': 'dz_{e/#mu} (cm)',
        },
        'ytitle': 'Events',
        'xrange': [-1., 1., 100],
        'widget': ['legend'],
        'legend': [0.25, 0.35, 0.45, 0.85],
        'cut': '(abs(dr_K) < 0.5 && abs(dr_l) < 0.5)'
    },
    'pid': {
        'var': {
            'K': 'pid_K_K',
            'e': 'pid_l_e',
            'mu': 'pid_l_mu'
        },
        'xtitle': {
            'K': 'PID_{K}',
            'e': 'PID_{e}',
            'mu': 'PID_{mu}'
        },
        'ytitle': 'Events',
        'xrange': [0., 1., 50],
        'widget': ['arrow', 'legend'],
        'pos': {
            'K': 0.9,
            'e': 0.9,
            'mu': 0.9
        },
        'legend': [0.25, 0.35, 0.45, 0.85],
        'arrow': [0.03, '<-|', 2],
        'cut': '(abs(dr_K) < 0.5 && abs(dr_l) < 0.5) && (abs(dz_K) < 2.5 && abs(dz_l) < 2.5)'
    },
    'thrust': {
        'var': {
            'all': 'thrust',
        },
        'xtitle': {
            'all': 'Thrust',
        },
        'ytitle': 'Events',
        'xrange': [0.6, 1., 100],
        'widget': ['arrow', 'legend'],
        'pos': {
            'all': 0.9,
        },
        'legend': [0.2, 0.35, 0.45, 0.85],
        'arrow': [0.03, '<-|', 2],
        'cut': '(abs(dr_K) < 0.5 && abs(dr_l) < 0.5) && (abs(dz_K) < 2.5 && abs(dz_l) < 2.5) && pid_K_K > 0.9 && (pid_l_e > 0.9 || pid_l_mu > 0.9)'
    },
    'foxWolframR2': {
        'var': {
            'all': 'foxWolframR2',
        },
        'xtitle': {
            'all': 'P^{2rnd}_{Fox-Wolfram}/P^{0th}_{Fox-Wolfram}',
        },
        'ytitle': 'Events',
        'xrange': [0., 1., 100],
        'widget': ['arrow', 'legend'],
        'pos': {
            'all': 0.62,
        },
        'legend': [0.2, 0.35, 0.45, 0.85],
        'arrow': [0.03, '<-|', 2],
        'cut': '(abs(dr_K) < 0.5 && abs(dr_l) < 0.5) && (abs(dz_K) < 2.5 && abs(dz_l) < 2.5) && pid_K_K > 0.9 && (pid_l_e > 0.9 || pid_l_mu > 0.9) && thrust > 0.9'
    },
    'pt_K_cms': {
        'var': {
            'all': 'pt_K_cms',
        },
        'xtitle': {
            'all': 'p^{K}_{T, cms} (GeV)',
        },
        'ytitle': 'Events',
        'xrange': [0., 6., 100],
        'widget': ['arrow', 'legend'],
        'pos': {
            'all': 0.5,
        },
        'legend': [0.7, 0.35, 0.9, 0.85],
        'arrow': [0.03, '<-|', 2],
        'cut': '(abs(dr_K) < 0.5 && abs(dr_l) < 0.5) && (abs(dz_K) < 2.5 && abs(dz_l) < 2.5) && pid_K_K > 0.9 && (pid_l_e > 0.9 || pid_l_mu > 0.9) && thrust > 0.9 && foxWolframR2 > 0.62'
    },
    'mm_miss': {
        'var': {
            'all': 'mm_miss',
        },
        'xtitle': {
            'all': 'M^{2}_{miss} (GeV^{2})',
        },
        'ytitle': 'Events',
        'xrange': [-20., 60., 500],
        'widget': ['arrow', 'legend'],
        'pos': {
            'all': 1.,
        },
        'legend': [0.7, 0.35, 0.9, 0.85],
        'arrow': [0.03, '<-|', 2],
        'cut': '(abs(dr_K) < 0.5 && abs(dr_l) < 0.5) && (abs(dz_K) < 2.5 && abs(dz_l) < 2.5) && pid_K_K > 0.9 && (pid_l_e > 0.9 || pid_l_mu > 0.9) && thrust > 0.9 && foxWolframR2 > 0.62 && pt_K_cms > 0.5'
    },
    'p_miss_theta_cms': {
        'var': {
            'all': 'p_miss_theta_cms',
        },
        'xtitle': {
            'all': '#theta^{P}_{miss, cms}',
        },
        'ytitle': 'Events',
        'xrange': [0., 3.45, 100],
        'widget': ['arrow', 'legend'],
        'pos': {
            'all': 0.5,
        },
        'legend': [0.7, 0.35, 0.9, 0.85],
        'arrow': [0.03, '<-|', 2],
        'cut': '(abs(dr_K) < 0.5 && abs(dr_l) < 0.5) && (abs(dz_K) < 2.5 && abs(dz_l) < 2.5) && pid_K_K > 0.9 && (pid_l_e > 0.9 || pid_l_mu > 0.9) && thrust > 0.9 && foxWolframR2 > 0.62 && pt_K_cms > 0.5 && mm_miss > 1.'
    },
    'm_Kpi0': {
        'var': {
            'all': 'm_Kpi0',
        },
        'xtitle': {
            'all': 'M(K^{-}#pi^{0}) (GeV)',
        },
        'ytitle': 'Events',
        'xrange': [0.6, 1.7, 100],
        'widget': ['legend'],
        'pos': {
            'all': 0.5,
        },
        'legend': [0.7, 0.35, 0.9, 0.85],
        'arrow': [0.03, '<-|', 2],
        'cut': '(abs(dr_K) < 0.5 && abs(dr_l) < 0.5) && (abs(dz_K) < 2.5 && abs(dz_l) < 2.5) && pid_K_K > 0.9 && (pid_l_e > 0.9 || pid_l_mu > 0.9) && thrust > 0.9 && foxWolframR2 > 0.62 && pt_K_cms > 0.5 && mm_miss > 1.'
    },



















    'm_pi0': {
        'var': {
            'all': 'm_pi0',
        },
        'xtitle': {
            'all': 'M(#pi^{0}) (GeV)',
        },
        'ytitle': 'Events',
        'xrange': [0.134, 0.147, 100],
        'widget': ['legend'],
        'pos': {
            'all': 0.5,
        },
        'legend': [0.7, 0.35, 0.9, 0.85],
        'arrow': [0.03, '<-|', 2],
        'cut': '(abs(dr_K) < 0.5 && abs(dr_l) < 0.5) && (abs(dz_K) < 2.5 && abs(dz_l) < 2.5) && pid_K_K > 0.9 && (pid_l_e > 0.9 || pid_l_mu > 0.9) && thrust > 0.9 && foxWolframR2 > 0.62 && pt_K_cms > 0.5 && mm_miss > 1. && p_miss_theta_cms > 0.5'
    },

    'p_miss_lab': {
        'var': {
            'all': 'p_miss_lab',
        },
        'xtitle': {
            'all': 'P^{lab}_{miss} (GeV)',
        },
        'ytitle': 'Events',
        'xrange': [0., 6., 100],
        'widget': ['legend'],
        'pos': {
            'all': 0.5,
        },
        'legend': [0.7, 0.35, 0.9, 0.85],
        'arrow': [0.03, '<-|', 2],
        'cut': '(abs(dr_K) < 0.5 && abs(dr_l) < 0.5) && (abs(dz_K) < 2.5 && abs(dz_l) < 2.5) && pid_K_K > 0.9 && (pid_l_e > 0.9 || pid_l_mu > 0.9) && thrust > 0.9 && foxWolframR2 > 0.62 && pt_K_cms > 0.5'
    },
    'p_miss_cms': {
        'var': {
            'all': 'p_miss_cms',
        },
        'xtitle': {
            'all': 'P^{cms}_{miss} (GeV)',
        },
        'ytitle': 'Events',
        'xrange': [0., 6., 100],
        'widget': ['legend'],
        'pos': {
            'all': 0.5,
        },
        'legend': [0.7, 0.35, 0.9, 0.85],
        'arrow': [0.03, '<-|', 2],
        'cut': '(abs(dr_K) < 0.5 && abs(dr_l) < 0.5) && (abs(dz_K) < 2.5 && abs(dz_l) < 2.5) && pid_K_K > 0.9 && (pid_l_e > 0.9 || pid_l_mu > 0.9) && thrust > 0.9 && foxWolframR2 > 0.62 && pt_K_cms > 0.5'
    },
}
