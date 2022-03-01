import sys
sys.dont_write_bytecode = False

def main(args):
    from cuts.EventSelect import EventSelect
    if args[0] == 'extract' or args[0] == 'apply':
        if len(args) == 1: samples = 'all'
        elif len(args) == 2: samples = args[1]
        else:
            print('extract args should not be larger than 2: all or one, please check!')
            sys.exit()
        ES = EventSelect(args[0], samples)
        if args[0] == 'extract': ES.extract()
        if args[0] == 'apply': ES.apply()

    if args[0] == 'study' or args[0] == 'show':
        if len(args[1:]) == 1: var = args[1]
        else:
            print('args should be 2 (study [var])!')
            sys.exit()
        ES = EventSelect(args[0], vars = var)
        ES.plot()
