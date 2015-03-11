#! /usr/bin/env python
# coding: utf-8

import os
import sys
import time
import argparse
import ConfigParser

##################################################
class QwatchCapture(object):
    '''
    Image capture for Qwatch webcamera.
    '''
    ##############################
    def __init__(self, name, user, passwd, uri, savedir):
        '''
        Set Qwatch parameters.
        '''
        self.name = name
        self.user = user
        self.passwd = passwd
        self.uri = uri
        self.savedir = savedir
        datedir = time.strftime('%Y/%m/%d/', time.localtime())
        jpg = time.strftime('%Y-%m%d-%H%M-%S.jpg', time.localtime())
        self.jpgfile = os.path.join(self.savedir, datedir, jpg)

        sys.stdout.write(20 * '-' + '\n')
        sys.stdout.write('name : {0}\n'.format(self.name))
        sys.stdout.write('uri  : {0}\n'.format(self.uri))
        sys.stdout.write('save : {0}\n'.format(self.savedir))
        sys.stdout.write('jpg  : {0}\n'.format(self.jpgfile))

    ##############################
    def set_tries(self, tries):
        '''
        Set number of times to retry.
        '''
        self.tries = tries

    ##############################
    def set_timeout(self, timeout):
        '''
        Set timeout duration in SECONDS.
        '''
        self.timeout = timeout

    ##############################
    def set_logfile(self, logfile):
        '''
        Set log output file for wget.
        '''
        self.logfile = logfile

    ##############################
    def run(self):
        '''
        Original shell command is:
        $ wget --http-user=USER --http-password=PASS URI
        $ mv snapshot.jpg snapshots/YYYY-MMDD-hhmm-ss.jpg
        '''

        # sd = os.path.dirname(self.jpgfile)
        # if not os.path.isdir(sd):
        #     sys.stderr.write('WARNING : No "{0}" directory.\n'.format(sd))
        #     sys.stderr.write('WARNING : Create the directory automatically.\n')
        #     os.makedirs(sd)
        #     if not os.path.isdir(sd):
        #         sys.stderr.write('ERROR : No "{0}" directory.\n'.format(sd))
        #         sys.stderr.write('ERROR : Could not create the directory automatically.\n')
        #         sys.exit()

        conf = {'user':self.user,
                'passwd':self.passwd,
                'uri':self.uri,
                'tries':self.tries,
                'timeout':self.timeout,
                'logfile':self.logfile,
                'jpgfile': self.jpgfile}

        ## wget-ing
        wget = 'wget --http-user={user} --http-password={passwd} -T {timeout} -t {tries} -a {logfile} {uri}'
        message = 'Executing wget ... See {logfile} for detail.\n'.format(**conf)
        sys.stderr.write(message)
        os.system(wget.format(**conf))

        ## rename-ing
        ss = 'snapshot.jpg'
        # if not os.path.exists(ss):
        #     sys.stderr.write('Error : No {0} found.\n'.format(ss))
        #     sys.stderr.write('Error : Could not rename the file.\n')
        #     sys.stderr.write('Error : (>W<)\n')
        #     sys.exit()
        os.renames(ss, '{jpgfile}'.format(**conf))

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
                        nargs=1,
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
    parser.set_defaults(conffile='example.cfg',
                        number=1,
                        seconds=10,
                        logfile='qwatch.log')
    ## Get args and options
    args = parser.parse_args()

    ## Read config
    config = ConfigParser.SafeConfigParser()

    if not os.path.exists(args.conffile[0]):
        sys.stderr.write('ERROR: no config file.\n')
        sys.stderr.write('ERROR: create new config using example.cfg.\n')
        sys.stderr.write('ERROR: (>w<)\n')
        sys.exit()
    else:
        sys.stderr.write('Reading {0}.\n'.format(args.conffile[0]))
        config.read(args.conffile[0])

    ## Set QwatchCaptures
    qws = []
    sections = config.sections()
    for section in sections:
        name = config.get(section, 'name')
        uri = config.get(section, 'uri')
        user = config.get(section, 'user')
        passwd = config.get(section, 'pass')
        savedir = config.get(section, 'savedir')
        ## Init Qwatch
        qw = QwatchCapture(name=name,
                           user=user,
                           passwd=passwd,
                           uri=uri,
                           savedir=savedir
        )
        qw.set_tries(args.number)
        qw.set_timeout(args.seconds)
        qw.set_logfile(args.logfile)
        ## Add to list
        qws.append(qw)

    for qw in qws:
        print qw.name
        qw.run()
