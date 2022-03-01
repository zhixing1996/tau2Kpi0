import sys
sys.dont_write_bytecode = False

samples_text = {
    'uubar' : ['u#bar{u}', 3, 3001],
    'ddbar' : ['d#bar{d}', 4, 3001],
    'ssbar' : ['s#bar{s}', 5, 3001],
    'ccbar' : ['c#bar{c}', 6, 3001],
    'charged' : ['B^{+}B^{-}', 7, 3001],
    'mixed' : ['B^{0}#bar{B^{0}}', 8, 3001],
    'taupair' : ['#tau^{+}#tau^{-}', 2, 3001],
    'eeee' : ['e^{+}e^{-}e^{+}e^{-}', 9, 3001],
    'eemumu' : ['e^{+}e^{-}#mu^{+}#mu^{-}', 10, 3001],
    'eeKK' : ['e^{+}e^{-}K^{+}K^{-}', 11, 3001],
    'eepp' : ['e^{+}e^{-}p#bar{p}', 12, 3001],
    'ee' : ['e^{+}e^{-}', 13, 3001],
    'mumu' : ['#mu^{+}#mu^{-}', 14, 3001],
    'Kpi0' : ['K^{+}#pi^{0}', 1, 3001]
}
