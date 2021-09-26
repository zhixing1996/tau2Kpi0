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
from tools import print_sep

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
    parser.add_option('--type', dest = 'sample_type', default = 'mc', action = 'store', help = 'run mc or data sample? [mc]/[data]')
    parser.add_option('--gb2', dest = 'gb2', default = False, action = 'store_true', help = 'gbasf2 job and project relative command collections')
    parser.add_option('--sub', dest = 'sub', default = '--dryrun', action = 'store', help = 'really submit or not? [--dryrun]/[--force]')
    parser.add_option('--root', dest = 'root', default = False, action = 'store_true', help = 'preprocess of root files \
                                                                                               [merge (sample)]/[make_one (sample)]')

    opts, args = parser.parse_args()

    attr.debug = opts.debug
    attr.sample_type = opts.sample_type
    if opts.gb2 or opts.root:
        import tools
        tools.main(opts, args)
    else:
        module_name = args[0]
        module = __import__(module_name)
        module.main(args[1:])

if __name__ == '__main__':
    main()
