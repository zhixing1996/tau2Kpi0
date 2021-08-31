#!/usr/bin/env python

"""
Main script for 

                 l nu nu
                 |
       e+ e- -> tau+ tau-
                      |
                      K pi0 nu

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
    parser.add_option('-d', dest = 'debug', default = False, action = 'store_true', help = 'debug mode')
    parser.add_option('-v', dest = 'verbose', default = False, action = 'store_true', help = 'verbose level')
    parser.add_option('--gb2', dest = 'gb2', default = False, action = 'store_true', help = 'gbasf2 job and project relative command collections')
    parser.add_option('--sub', dest = 'sub', default = '--dryrun', action = 'store', help = 'really submit or not? [--dryrun]/[--force]')

    opts, args = parser.parse_args()

    if opts.gb2:
        coll = args[0]
        run_type = opts.sub
        if run_type != '--dryrun' and run_type != '--force':
            print('run type should be --dryrun or --force, now is {}!'.format(run_type))
            sys.exit()
        from tools.Cmd_Colls import Cmd_Colls
        print_sep('/')
        print('executing command collections: ' + coll)
        CC = Cmd_Colls(coll, run_type)
        CC.process()
        print_sep('/')
    else:
        import ROOT

if __name__ == '__main__':
    main()
