# coding: utf-8

import ConfigParser
import os
import sys
from time import localtime, strftime
import argparse

##################################################
class Config(object):
    config = ConfigParser.RawConfigParser()

    if not os.path.exists('default.cfg'):
        sys.stderr.write('ERROR: no config file.\n')
        sys.stderr.write('ERROR: create new config using example.cfg.\n')
        sys.stderr.write('ERROR: (>w<)\n')
        sys.exit()
    else:
        sys.stderr.write('Reading default.cfg.\n')
        config.read('default.cfg')

    uri = config.get('Capture', 'uri')
    user = config.get('Capture', 'user')
    passwd = config.get('Capture', 'pass')

##################################################
class QwatchCapture(object):
    ##############################
    def __init__(self, user, passwd, uri):
        '''
        Set parameters.
        '''
        self.user = user
        self.passwd = passwd
        self.uri = uri

    ##############################
    def set_tries(self, tries):
        self.tries = tries

    ##############################
    def set_timeout(self, timeout):
        self.timeout = timeout

    ##############################
    def set_logfile(self, logfile):
        self.logfile = logfile

    ##############################
    def run(self):
        '''
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

    usage = 'usage: %s [-tT]' % sys.argv[0]

    desc = 'Image capture for Qwatch webcamera.'
    epi = 'What you have to prepare:\n'
    epi += '  1) Prepare default.cfg based on example.cfg.\n'
    epi += '  2) Prepare snapshots/ directory manually.\n'
    epi += 'For periodic capture:\n'
    epi += '  3) Add to cron.\n'

    parser = argparse.ArgumentParser(description=desc,
                                     epilog=epi,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

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

    ## オプションのデフォルトを一括設定する
    parser.set_defaults(number=1,
                        seconds=10,
                        logfile='qwatch.log')

    ## オプション、引数を引き出す
    args = parser.parse_args()

    qw = QwatchCapture(user=Config.user,
                       passwd=Config.passwd,
                       uri=Config.uri)

    qw.set_tries(args.number)
    qw.set_timeout(args.seconds)
    qw.set_logfile(args.logfile)

    qw.run()
