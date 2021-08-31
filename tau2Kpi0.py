#!/usr/bin/env python

"""
Main script for 

                 l+ nu nu
                 |
       e+ e- -> tau+ tau-
                      |
                      K- pi0 nu

"""
import os
import sys
import optparse
import attr

def print_sep(marker = '-', width = 55):
    sys.stdout.write(marker * width + '\n')

def main():
    print_sep()
    sys.stdout.write('      Author: %s    \n' % attr.author)
    sys.stdout.write('        Date: %s    \n' % attr.date)
    sys.stdout.write('   Copyright: %s    \n' % attr.copyright)
    print_sep()

    parser = optparse.OptionParser()
    parser.add_option('-d', dest = 'debug', default = False, action = 'store', help = 'debug mode')
    parser.add_option('-v', dest = 'verbose', default = False, action = 'store', help = 'verbose level')
    parser.add_option('--type', dest = 'run_type', default = 'mc', action = 'store', help = 'run mc or data sample? [mc]/[data]')
    parser.add_option('--gb2', dest = 'gb2', default = False, action = 'store_true', help = 'gbasf2 job and project relative command collections')
    parser.add_option('--sub', dest = 'sub', default = '--dryrun', action = 'store', help = 'really submit or not? [--dryrun]/[--force]')
    parser.add_option('--root', dest = 'root', default = False, action = 'store_true', help = 'execute root files or macros \
                                                                                              [merge (sample)]/[make_one (sample)]')

    opts, args = parser.parse_args()

    attr.debug = opts.debug
    attr.run_type = opts.run_type
    if opts.gb2:
        coll = args[0]
        run_type = opts.sub
        if run_type != '--dryrun' and run_type != '--force':
            print('run type should be --dryrun or --force, now is {}!'.format(run_type))
            sys.exit()
        from tools.CmdColls import CmdColls
        print_sep('/')
        print('executing command collections: ' + coll)
        CC = CmdColls(coll, run_type)
        CC.process()
        print_sep('/')
    elif opts.root:
        from tools.ROOTFiles import ROOTFiles
        if len(args) == 1: RF = ROOTFiles()
        elif len(args) == 2:
            if 'root' in args[1]: RF = ROOTFiles([args[1]])
            else: RF = ROOTFiles(args[1])
        else:
            print('class ROOTFiles initialization error, please check your input args!')
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
        print('Please use -h for help.')

if __name__ == '__main__':
    main()
