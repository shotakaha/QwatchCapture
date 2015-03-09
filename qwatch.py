# coding: utf-8

import ConfigParser
import os
import sys
from time import localtime, strftime
import argparse

##################################################
class Config:
    config = ConfigParser.RawConfigParser()

    if os.path.exists('default.cfg'):
        config.read('default.cfg')
    else:
        config.read('example.cfg')

    uri = config.get('Capture', 'uri')
    user = config.get('Capture', 'user')
    passwd = config.get('Capture', 'pass')

##################################################
class QwatchCapture(object):
    def __init__(self, user, passwd, uri):
        '''
        Set parameters.
        '''
        self.user = user
        self.passwd = passwd
        self.uri = uri

    def set_tries(self, tries):
        self.tries = tries

    def set_timeout(self, timeout):
        self.timeout = timeout

    def set_logfile(self, logfile):
        self.logfile = logfile

    def run(self):
        '''
        $ wget --http-user=USER --http-password=PASS URI
        $ mv snapshot.jpg YYYY-MM-DD-hh-mm-ss.jpg
        '''

        param = {'user' : self.user,
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
        os.system(wget.format(**param))
        if os.path.exists('snapshot.jpg'):
            os.system(mv.format(**param))

    def loop(self):
        pass

##################################################
if __name__ == '__main__':

    usage = 'usage: %s [-tT]' % sys.argv[0]

    desc = 'プログラムの簡単な説明'
    epi = 'ヘルプの最後に付ける説明'

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
