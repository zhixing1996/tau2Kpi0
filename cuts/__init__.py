import sys
sys.dont_write_bytecode = False

def main(args):
    from cuts.EventSelect import EventSelect
    if args[0] == 'extract':
        if len(args) == 1: samples = 'all'
        elif len(args) == 2: samples = args[1]
        else:
            print('extract args should not be larger than 2: all or one, please check!')
            sys.exit()
        ES = EventSelect(args[0], samples)
        ES.extract()

    if not args[0] == 'extract':
        if len(args) == 1: var = 'all'
        elif len(args) == 2: var = args[1]
        else:
            print('pid args should not be larger than 2 ([var] [samples]): all or one, please check!')
            sys.exit()
        ES = EventSelect('cut', vars = args[0])
        ES.cuts()
