import sys
sys.dont_write_bytecode = False

def print_sep(marker = '-', width = 55):
    sys.stdout.write(marker * width + '\n')

def main(opts, args):
    if opts.gb2:
        coll = args[0]
        run_type = opts.sub
        if run_type != '--dryrun' and run_type != '--force':
            print('run type should be --dryrun or --force, now is {}!'.format(run_type))
            sys.exit()
        from tools.CmdColls import CmdColls
        print_sep('/')
        print('executing command collections: ' + coll)
        if len(args) == 1: CC = CmdColls(coll, projects = None, run_type = run_type)
        elif len(args) == 2:
            project = args[1]
            CC = CmdColls(coll, projects = project, run_type = run_type)
        else:
            print('args for gb2 should be no larger than 2!')
            sys.exit()
        CC.process()
        print_sep('/')
    elif opts.root:
        from tools.ROOTFiles import ROOTFiles
        if len(args) == 1: RF = ROOTFiles()
        elif len(args) == 2:
            if 'root' in args[1]: RF = ROOTFiles([args[1]])
            else: RF = ROOTFiles(args[1])
        else:
            print('maximum one arg is acceptable (class ROOTFiles initialization error), please check your input args!')
            sys.exit()
        if args[0] == 'merge':
            print_sep('/')
            print('merging files...')
            RF.merge()
            print_sep('/')
        elif args[0] == 'make_one':
            print_sep('/')
            print('making one files...')
            if len(args) == 1: RF.make_one()
            elif len(args) == 2: RF.make_one(args[1])
            print_sep('/')
    else:
        print('opts must be gb2 or merge, please check your input!')
