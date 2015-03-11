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
    def __init__(self, name, user, passwd, uri, base):
        '''
        Configure Qwatch.
        '''
        self.name = name
        self.user = user
        self.passwd = passwd
        self.uri = uri
        self.base = base
        datedir = time.strftime('%Y/%m/%d/', time.localtime())
        jpg = time.strftime('%Y-%m%d-%H%M-%S.jpg', time.localtime())
        self.jpgfile = os.path.join(self.base, datedir, jpg)

    ##############################
    def __str__(self):
        '''
        Print initial configurations.
        '''
        sys.stdout.write(20 * '-' + '\n')
        sys.stdout.write('name : {0}\n'.format(self.name))
        sys.stdout.write('uri  : {0}\n'.format(self.uri))
        sys.stdout.write('base : {0}\n'.format(self.base))
        sys.stdout.write('jpg  : {0}\n'.format(self.jpgfile))
        return '\n'

    ##############################
    def set_tries(self, tries):
        '''
        Set option : number of times to retry.
        '''
        self.tries = tries

    ##############################
    def set_timeout(self, timeout):
        '''
        Set option : timeout duration in SECONDS.
        '''
        self.timeout = timeout

    ##############################
    def set_logfile(self, logfile):
        '''
        Set option : output logfile for wget.
        '''
        self.logfile = logfile

    ##############################
    def run(self):
        '''
        Original shell command is:
        $ wget --http-user=USER --http-password=PASS URI
        $ mv snapshot.jpg snapshots/YYYY-MMDD-hhmm-ss.jpg
        '''
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
        try:
            os.renames(ss, '{jpgfile}'.format(**conf))
        except OSError as (errno, strerror):
            print 'OS error({0}): {1}'.format(errno, strerror)


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
    parser.set_defaults(conffile='conf.example',
                        number=1,
                        seconds=10,
                        logfile='qw-wget.log')
    ## Get args and options
    args = parser.parse_args()

    ## Read config
    config = ConfigParser.SafeConfigParser()

    conffile = args.conffile[0]
    if not os.path.exists(conffile):
        sys.stderr.write('ERROR: No "{0}" found.\n'.format(conffile))
        sys.stderr.write('ERROR: Create new conf file using qwconf.example.\n')
        sys.stderr.write('ERROR: (>w<)\n')
        sys.exit()

    sys.stderr.write('Reading {0}.\n'.format(conffile))
    config.read(conffile)

    ## Set QwatchCaptures
    qws = []
    sections = config.sections()
    for section in sections:
        name = config.get(section, 'name')
        uri = config.get(section, 'uri')
        user = config.get(section, 'user')
        passwd = config.get(section, 'pass')
        base = config.get(section, 'base')
        ## Init Qwatch
        qw = QwatchCapture(name=name,
                           user=user,
                           passwd=passwd,
                           uri=uri,
                           base=base)
        ## Set Options
        qw.set_tries(args.number)
        qw.set_timeout(args.seconds)
        qw.set_logfile(args.logfile)
        ## Add to list
        qws.append(qw)

    for qw in qws:
        print qw
        qw.run()
