# coding: utf-8

import os
import sys
from time import localtime, strftime
import argparse
import ConfigParser

##################################################
class QwatchCapture(object):
    '''
    Image capture for Qwatch webcamera.
    '''
    ##############################
    def __init__(self, user, passwd, uri):
        '''
        Set Qwatch parameters.
        '''
        self.user = user
        self.passwd = passwd
        self.uri = uri

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

        if not os.path.isdir('snapshots'):
            sys.stderr.write('ERROR: no snapshots/ directory.\n')
            sys.stderr.write('ERROR: create or make symlink for snapshots/ directory manually.\n')
            sys.stderr.write('ERROR: (>w<)\n')
            sys.stderr.write('HINT1: type "mkdir snapshots"\n')
            sys.stderr.write('HINT2: type "ln -s PATH_TO_ANOTHER_SNAPSHOTS snapshots"\n')
            sys.exit()

        param = {'user':self.user,
                 'passwd':self.passwd,
                 'uri':self.uri,
                 'tries':self.tries,
                 'timeout':self.timeout,
                 'logfile':self.logfile,
                 'snapfile':'snapshot.jpg',
                 'ofn': strftime("snapshots/%Y-%m%d-%H%M-%S.jpg", localtime())
             }

        wget = 'wget --http-user={user} --http-password={passwd} -T {timeout} -t {tries} -a {logfile} {uri}'
        mv = 'mv {snapfile} {ofn}'

        message = 'Executing wget ... See {logfile} for detail.\n'.format(**param)
        sys.stderr.write(message)
        os.system(wget.format(**param))

        if os.path.exists('snapshot.jpg'):
            os.system(mv.format(**param))


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
    config = ConfigParser.RawConfigParser()
    if not os.path.exists(args.conffile[0]):
        sys.stderr.write('ERROR: no config file.\n')
        sys.stderr.write('ERROR: create new config using example.cfg.\n')
        sys.stderr.write('ERROR: (>w<)\n')
        sys.exit()
    else:
        sys.stderr.write('Reading {0}.\n'.format(args.conffile[0]))
        config.read(args.conffile[0])


    uri = config.get('Capture', 'uri')
    user = config.get('Capture', 'user')
    passwd = config.get('Capture', 'pass')
    sys.stderr.write('Destination {0}.\n'.format(uri))

    ## Set QwatchCapture
    qw = QwatchCapture(user=user,
                       passwd=passwd,
                       uri=uri)

    qw.set_tries(args.number)
    qw.set_timeout(args.seconds)
    qw.set_logfile(args.logfile)

    ## Run QwatchCapture
    qw.run()
