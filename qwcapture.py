#! /usr/bin/env python
# coding: utf-8

import os
import argparse
import ConfigParser
import qwatch

##################################################
if __name__ == '__main__':

    desc = 'Image capture for Qwatch webcamera.'
    epi = 'What you have to prepare:\n'
    epi += '  1) Prepare default.cfg based on example.cfg.\n'
    epi += '  2) Prepare snapshots/ directory manually.\n'
    epi += 'For periodic capture:\n'
    epi += '  3) Add to cron.\n'

    parser = argparse.ArgumentParser(description=desc,
                                     epilog=epi,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(dest='conffile',
                        nargs='+',
                        help='specify CONFIGFILE')
    parser.add_argument('-t', '--tries',
                        dest='number',
                        type=int,
                        help='set number of retries to NUMBER (0 unlimits)')
    parser.add_argument('-T', '--timeout',
                        dest='seconds',
                        type=int,
                        help='set all timeout values to SECONDS')
    parser.add_argument('-a', '--append-log',
                        dest='logfile',
                        help='append messages to LOGFILE')
    ## Set option defaults
    parser.set_defaults(conffile='conf.example',
                        number=1,
                        seconds=10,
                        logfile='qw-wget.log')
    ## Get args and options
    args = parser.parse_args()

    ## Print config files
    for f in args.conffile:
        print f, os.path.exists(f)

    ## Read config files
    config = ConfigParser.SafeConfigParser()
    config.read(args.conffile)

    ## Set QwatchCaptures
    sections = config.sections()
    for section in sections:
        name = section
        uri = config.get(section, 'uri')
        user = config.get(section, 'user')
        passwd = config.get(section, 'pass')
        base = config.get(section, 'base')
        log = config.get(section, 'log')

        ## Init Qwatch
        qw = qwatch.QwatchCapture(name=name,
                                  user=user,
                                  passwd=passwd,
                                  uri=uri,
                                  base=base,
                                  log=log)

        ## Set Options
        qw.set_tries(args.number)
        qw.set_timeout(args.seconds)
        qw.set_logfile(args.logfile)

        ## Run
        print(qw)
        qw.run()
