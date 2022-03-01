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
        'logy': False,
        'cut': '(((n_l_pos != 0 && n_gam_pos == 0) || (n_l_neg != 0 && n_gam_neg == 0)))'
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
        'logy': False,
        'cut': '(((n_l_pos != 0 && n_gam_pos == 0) || (n_l_neg != 0 && n_gam_neg == 0)) && (abs(dr_K) < 0.5 && abs(dr_l) < 0.5))'
    },
    'K_pid': {
        'var': {
            'K': 'pid_K_K',
        },
        'xtitle': {
            'K': 'PID_{K#rightarrowK}',
        },
        'ytitle': 'Events',
        'xrange': [0.5, 1., 100],
        'widget': ['arrow', 'legend'],
        'pos': {
            'K': [0.9],
        },
        'legend': [0.25, 0.45, 0.45, 0.85],
        'arrow': [[0.03, '<-|', 2]],
        'logy': True,
        'cut': '(((n_l_pos != 0 && n_gam_pos == 0) || (n_l_neg != 0 && n_gam_neg == 0)) && (abs(dr_K) < 0.5 && abs(dr_l) < 0.5) && (abs(dz_K) < 2.5 && abs(dz_l) < 2.5))'
    },
    'e_pid': {
        'var': {
            'e': 'pid_l_e',
        },
        'xtitle': {
            'e': 'PID_{l#rightarrowe}',
        },
        'ytitle': 'Events',
        'xrange': [0.5, 1., 100],
        'widget': ['arrow', 'legend'],
        'pos': {
            'e': [0.9],
        },
        'legend': [0.25, 0.45, 0.45, 0.85],
        'arrow': [[0.03, '<-|', 2]],
        'logy': True,
        'cut': '(((n_l_pos != 0 && n_gam_pos == 0) || (n_l_neg != 0 && n_gam_neg == 0)) && (abs(dr_K) < 0.5 && abs(dr_l) < 0.5) && (abs(dz_K) < 2.5 && abs(dz_l) < 2.5) && (dmID_1prong1 == 11 && pid_K_K > 0.9))'
    },
    'mu_pid': {
        'var': {
            'mu': 'pid_l_mu',
        },
        'xtitle': {
            'mu': 'PID_{l#rightarrow#mu}',
        },
        'ytitle': 'Events',
        'xrange': [0.5, 1., 50],
        'widget': ['arrow', 'legend'],
        'pos': {
            'mu': [0.9],
        },
        'legend': [0.25, 0.45, 0.45, 0.94],
        'arrow': [[0.03, '<-|', 2]],
        'logy': True,
        'cut': '(((n_l_pos != 0 && n_gam_pos == 0) || (n_l_neg != 0 && n_gam_neg == 0)) && (abs(dr_K) < 0.5 && abs(dr_l) < 0.5) && (abs(dz_K) < 2.5 && abs(dz_l) < 2.5) && (dmID_1prong1 == 13 && pid_K_K > 0.9))'
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
            'all': [0.94],
        },
        'legend': [0.2, 0.35, 0.45, 0.85],
        'arrow': [[0.03, '<-|', 2]],
        'logy': False,
        'cut': '(((n_l_pos != 0 && n_gam_pos == 0) || (n_l_neg != 0 && n_gam_neg == 0)) && (abs(dr_K) < 0.5 && abs(dr_l) < 0.5) && (abs(dz_K) < 2.5 && abs(dz_l) < 2.5) && (((dmID_1prong1 == 11 && pid_l_e > 0.9) || (dmID_1prong1 == 13 && pid_l_mu > 0.9)) && pid_K_K > 0.9))'
    },
    'mm_miss': {
        'var': {
            'all': 'mm_miss',
        },
        'xtitle': {
            'all': 'M^{2}_{miss} (GeV^{2})',
        },
        'ytitle': 'Events',
        'xrange': [-10., 100., 100],
        'widget': ['arrow', 'legend'],
        'pos': {
            'all': [1., 55.],
        },
        'legend': [0.7, 0.35, 0.9, 0.85],
        'arrow': [[0.03, '<-|', 2], [0.03, '<-|', 2]],
        'logy': False,
        'cut': '(((n_l_pos != 0 && n_gam_pos == 0) || (n_l_neg != 0 && n_gam_neg == 0)) && (abs(dr_K) < 0.5 && abs(dr_l) < 0.5) && (abs(dz_K) < 2.5 && abs(dz_l) < 2.5) && (((dmID_1prong1 == 11 && pid_l_e > 0.9) || (dmID_1prong1 == 13 && pid_l_mu > 0.9)) && pid_K_K > 0.9) && thrust > 0.94)'
    },
    'n_gam_pos': {
        'var': {
            'all': 'n_gam_pos',
        },
        'xtitle': {
            'all': 'N_{#gamma}^{extra} In Positive Thrust',
        },
        'ytitle': 'Events',
        'xrange': [0., 5., 5],
        'widget': ['arrow', 'legend'],
        'pos': {
            'all': [1.],
        },
        'legend': [0.7, 0.35, 0.9, 0.85],
        'arrow': [[0.03, '<-|', 2]],
        'logy': False,
        'cut': '(((n_l_pos != 0 && n_gam_pos == 0) || (n_l_neg != 0 && n_gam_neg == 0)) && (abs(dr_K) < 0.5 && abs(dr_l) < 0.5) && (abs(dz_K) < 2.5 && abs(dz_l) < 2.5) && (((dmID_1prong1 == 11 && pid_l_e > 0.9) || (dmID_1prong1 == 13 && pid_l_mu > 0.9)) && pid_K_K > 0.9) && thrust > 0.94 && n_l_pos == 0)'
    },
    'n_gam_neg': {
        'var': {
            'all': 'n_gam_neg',
        },
        'xtitle': {
            'all': 'N_{#gamma}^{extra} In Negtive Thrust',
        },
        'ytitle': 'Events',
        'xrange': [0., 5., 5],
        'widget': ['arrow', 'legend'],
        'pos': {
            'all': [1.],
        },
        'legend': [0.7, 0.35, 0.9, 0.85],
        'arrow': [[0.03, '<-|', 2]],
        'logy': False,
        'cut': '(((n_l_pos != 0 && n_gam_pos == 0) || (n_l_neg != 0 && n_gam_neg == 0)) && (abs(dr_K) < 0.5 && abs(dr_l) < 0.5) && (abs(dz_K) < 2.5 && abs(dz_l) < 2.5) && (((dmID_1prong1 == 11 && pid_l_e > 0.9) || (dmID_1prong1 == 13 && pid_l_mu > 0.9)) && pid_K_K > 0.9) && thrust > 0.94 && n_l_neg == 0)'
    },
    'n_gam_other': {
        'var': {
            'all': 'n_gam_other',
        },
        'xtitle': {
            'all': 'N_{#gamma}^{other}',
        },
        'ytitle': 'Events',
        'xrange': [0, 5, 5],
        'widget': ['arrow', 'legend'],
        'pos': {
            'all': [2],
        },
        'legend': [0.7, 0.35, 0.9, 0.85],
        'arrow': [[0.03, '<-|', 2]],
        'logy': False,
        'cut': '(((n_l_pos != 0 && n_gam_pos == 0) || (n_l_neg != 0 && n_gam_neg == 0)) && (abs(dr_K) < 0.5 && abs(dr_l) < 0.5) && (abs(dz_K) < 2.5 && abs(dz_l) < 2.5) && (((dmID_1prong1 == 11 && pid_l_e > 0.9) || (dmID_1prong1 == 13 && pid_l_mu > 0.9)) && pid_K_K > 0.9) && thrust > 0.94 && ((n_l_pos == 0 && n_gam_pos < 1) || (n_l_neg == 0 && n_gam_neg < 1)))'
    },
    'n_pi0': {
        'var': {
            'all': 'n_pi0',
        },
        'xtitle': {
            'all': 'N_{#pi^{0}}',
        },
        'ytitle': 'Events',
        'xrange': [1., 12., 11],
        'widget': ['arrow', 'legend'],
        'pos': {
            'all': [2.],
        },
        'legend': [0.7, 0.35, 0.9, 0.85],
        'arrow': [[0.03, '<-|', 2]],
        'logy': False,
        'cut': '(((n_l_pos != 0 && n_gam_pos == 0) || (n_l_neg != 0 && n_gam_neg == 0)) && (abs(dr_K) < 0.5 && abs(dr_l) < 0.5) && (abs(dz_K) < 2.5 && abs(dz_l) < 2.5) && (((dmID_1prong1 == 11 && pid_l_e > 0.9) || (dmID_1prong1 == 13 && pid_l_mu > 0.9)) && pid_K_K > 0.99) && thrust > 0.94 && ((n_l_pos == 0 && n_gam_pos < 1) || (n_l_neg == 0 && n_gam_neg < 1)) && n_gam_other < 2)'
    },
    'm_Kpi0': {
        'var': {
            'all': 'm_Kpi0',
        },
        'xtitle': {
            'all': 'M(K^{-}#pi^{0}) (GeV)',
        },
        'ytitle': 'Events',
        'xrange': [0.6, 1.8, 600],
        'widget': ['legend'],
        'pos': {
            'all': [0.5],
        },
        'legend': [0.7, 0.35, 0.9, 0.85],
        'arrow': [[0.03, '<-|', 2]],
        'logy': False,
        'cut': '(((n_l_pos != 0 && n_gam_pos == 0) || (n_l_neg != 0 && n_gam_neg == 0)) && (abs(dr_K) < 0.5 && abs(dr_l) < 0.5) && (abs(dz_K) < 2.5 && abs(dz_l) < 2.5) && (((dmID_1prong1 == 11 && pid_l_e > 0.9) || (dmID_1prong1 == 13 && pid_l_mu > 0.9)) && pid_K_K > 0.9) && thrust > 0.94 && ((n_l_pos == 0 && n_gam_pos < 1) || (n_l_neg == 0 && n_gam_neg < 1)) && n_gam_other < 2 && n_pi0 < 2)'
    },

    # 'K_pi_pid': {
    #     'var': {
    #         'K': 'pid_K_pi',
    #     },
    #     'xtitle': {
    #         'K': 'PID_{K#rightarrowK}',
    #     },
    #     'ytitle': 'Events',
    #     'xrange': [0., 1., 100],
    #     'widget': ['legend'],
    #     'pos': {
    #         'K': [0.9],
    #     },
    #     'legend': [0.25, 0.45, 0.45, 0.85],
    #     'arrow': [[0.03, '<-|', 2]],
    #     'logy': True,
    #     'cut': '(((n_l_pos != 0 && n_gam_pos == 0) || (n_l_neg != 0 && n_gam_neg == 0)) && (abs(dr_K) < 0.5 && abs(dr_l) < 0.5) && (abs(dz_K) < 2.5 && abs(dz_l) < 2.5) && (((dmID_1prong1 == 11 && pid_l_e > 0.9) || (dmID_1prong1 == 13 && pid_l_mu > 0.9)) && pid_K_K > 0.99) && thrust > 0.94 && ((n_l_pos == 0 && n_gam_pos < 1) || (n_l_neg == 0 && n_gam_neg < 1)) && n_gam_other < 2 && n_pi0 < 2)'
    # },









    ########################################################################################################################################
    #
    #   TBD CUTS
    #
    ########################################################################################################################################
    'angle_Kpi0': {
        'var': {
            'all': 'angle_Kpi0',
        },
        'xtitle': {
            'all': '#theta^{K, #pi^{0}}_{cms}',
        },
        'ytitle': 'Events',
        'xrange': [0., 1.1, 100],
        'widget': ['arrow', 'legend'],
        'pos': {
            'all': [0.7],
        },
        'legend': [0.7, 0.35, 0.9, 0.85],
        'arrow': [[0.03, '<-|', 2]],
        'logy': False,
        'cut': '(((n_l_pos != 0 && n_gam_pos == 0) || (n_l_neg != 0 && n_gam_neg == 0)) && (abs(dr_K) < 0.5 && abs(dr_l) < 0.5) && (abs(dz_K) < 2.5 && abs(dz_l) < 2.5) && (((dmID_1prong1 == 11 && pid_l_e > 0.9) || (dmID_1prong1 == 13 && pid_l_mu > 0.9)) && pid_K_K > 0.9) && thrust > 0.94 && ((n_l_pos == 0 && n_gam_pos < 1) || (n_l_neg == 0 && n_gam_neg < 1)) && n_pi0 < 4)'
    },
    'pt_K_cms': {
        'var': {
            'all': 'pt_K_cms',
        },
        'xtitle': {
            'all': 'p^{K}_{T, cms} (GeV)',
        },
        'ytitle': 'Events',
        'xrange': [0., 4.5, 100],
        'widget': ['legend'],
        'pos': {
            'all': [0.5],
        },
        'legend': [0.7, 0.35, 0.9, 0.85],
        'arrow': [[0.03, '<-|', 2]],
        'logy': False,
        'cut': ''
    },
    'pt_l_cms': {
        'var': {
            'all': 'pt_l_cms',
        },
        'xtitle': {
            'all': 'p^{e/#mu}_{T, cms} (GeV)',
        },
        'ytitle': 'Events',
        'xrange': [0., 4.5, 100],
        'widget': ['legend'],
        'pos': {
            'all': [0.4],
        },
        'legend': [0.7, 0.35, 0.9, 0.85],
        'arrow': [[0.03, '<-|', 2]],
        'logy': False,
        'cut': ''
    },
    'p_miss_theta_cms': {
        'var': {
            'all': 'p_miss_theta_cms',
        },
        'xtitle': {
            'all': '#theta^{P_{miss}}_{cms}',
        },
        'ytitle': 'Events',
        'xrange': [0., 3.5, 100],
        'widget': ['legend'],
        'pos': {
            'all': [0.7, 2.5],
        },
        'legend': [0.7, 0.35, 0.9, 0.85],
        'arrow': [[0.03, '<-|', 2], [0.03, '<-|', 2]],
        'logy': False,
        'cut': ''
    },
    'angle_Kl': {
        'var': {
            'all': 'angle_Kl',
        },
        'xtitle': {
            'all': '#theta^{e/#mu, K}_{lab}',
        },
        'ytitle': 'Events',
        'xrange': [1.4, 3.5, 100],
        'widget': ['legend'],
        'pos': {
            'all': [2.1],
        },
        'legend': [0.7, 0.35, 0.9, 0.85],
        'arrow': [[0.03, '<-|', 2]],
        'logy': False,
        'cut': ''
    },
    'p_miss_cms': {
        'var': {
            'all': 'p_miss_cms',
        },
        'xtitle': {
            'all': 'P^{cms}_{miss} (GeV)',
        },
        'ytitle': 'Events',
        'xrange': [0., 7., 100],
        'widget': ['legend'],
        'pos': {
            'all': [0.5],
        },
        'legend': [0.7, 0.35, 0.9, 0.85],
        'arrow': [[0.03, '<-|', 2]],
        'logy': False,
        'cut': ''
    },

    'foxWolframR2': {
        'var': {
            'all': 'foxWolframR2',
        },
        'xtitle': {
            'all': 'P^{2rnd}_{Fox-Wolfram}/P^{0th}_{Fox-Wolfram}',
        },
        'ytitle': 'Events',
        'xrange': [0.6, 1.01, 100],
        'widget': ['legend'],
        'pos': {
            'all': [0.62],
        },
        'legend': [0.2, 0.35, 0.45, 0.85],
        'arrow': [[0.03, '<-|', 2]],
        'logy': False,
        'cut': ''
    },
    'p_cms': {
        'var': {
            'all': 'p_cms',
        },
        'xtitle': {
            'all': 'p^{e, #mu, K}_{cms} (GeV)',
        },
        'ytitle': 'Events',
        'xrange': [0., 5.5, 100],
        'widget': ['legend'],
        'pos': {
            'all': [0.4],
        },
        'legend': [0.7, 0.35, 0.9, 0.85],
        'arrow': [[0.03, '<-|', 2]],
        'logy': False,
        'cut': ''
    },
    'Ep_K': {
        'var': {
            'all': 'Ep_K',
        },
        'xtitle': {
            'all': 'E/p_{K}',
        },
        'ytitle': 'Events',
        'xrange': [-4., 2., 100],
        'widget': ['legend'],
        'pos': {
            'all': [0.4],
        },
        'legend': [0.7, 0.35, 0.9, 0.85],
        'arrow': [[0.03, '<-|', 2]],
        'logy': False,
        'cut': ''
    },
    'Ep_l': {
        'var': {
            'all': 'Ep_l',
        },
        'xtitle': {
            'all': 'E/p_{e/#mu}',
        },
        'ytitle': 'Events',
        'xrange': [0., 1.1, 100],
        'widget': ['legend'],
        'pos': {
            'all': [0.4],
        },
        'legend': [0.55, 0.35, 0.76, 0.85],
        'arrow': [[0.03, '<-|', 2]],
        'logy': False,
        'cut': ''
    },
}

cuts_apply = '(((n_l_pos != 0 && n_gam_pos == 0) || (n_l_neg != 0 && n_gam_neg == 0)) && (abs(dr_K) < 0.5 && abs(dr_l) < 0.5) && (abs(dz_K) < 2.5 && abs(dz_l) < 2.5) && (((dmID_1prong1 == 11 && pid_l_e > 0.9) || (dmID_1prong1 == 13 && pid_l_mu > 0.9)) && pid_K_K > 0.9) && thrust > 0.94 && ((n_l_pos == 0 && n_gam_pos < 2) || (n_l_neg == 0 && n_gam_neg < 2)) && n_pi0 < 4 && angle_Kpi0 < 0.7)'
