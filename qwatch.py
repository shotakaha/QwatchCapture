#! /usr/bin/env python
# coding: utf-8

import os
import sys
import time
import argparse
import ConfigParser

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(name)-12s %(module)s.%(funcName)-20s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='example.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)-8s %(name)-12s %(module)s.%(funcName)-20s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

##################################################
class QwatchCapture(object):
    '''
    Image capture for Qwatch webcamera.
    '''
    ##############################
    def __init__(self, name, user, passwd, uri, base, log):
        '''
        Configure Qwatch.
        '''
        self.name = name
        self.user = user
        self.passwd = passwd
        self.uri = uri
        self.base = base
        self.log = log
        datedir = time.strftime('%Y/%m/%d/', time.localtime())
        jpg = time.strftime('%Y-%m%d-%H%M-%S.jpg', time.localtime())
        self.jpgfile = os.path.join(self.base, datedir, jpg)
        self.logger = logging.getLogger('QwatchCapture')

    ##############################
    def __str__(self):
        '''
        Print initial configurations.
        '''
        self.logger.info(20 * '-')
        self.logger.info('name : {0}'.format(self.name))
        self.logger.info('uri  : {0}'.format(self.uri))
        self.logger.info('base : {0}'.format(self.base))
        self.logger.info('jpg  : {0}'.format(self.jpgfile))
        return ''

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
    def capture(self):
        '''
        To capture:
        $ wget --http-user=USER --http-password=PASS URI
        $ mv snapshot.jpg $BASE/YYYY/mm/dd/YYYY-mmdd-HHMM-SS.jpg

        '''
        conf = {'user':self.user,
                'passwd':self.passwd,
                'uri':self.uri,
                'tries':self.tries,
                'timeout':self.timeout,
                'logfile':self.logfile,
                'jpgfile': self.jpgfile}

        wget = 'wget --http-user={user} --http-password={passwd} -T {timeout} -t {tries} -a {logfile} {uri}'
        message = 'Execute wget ... See {logfile} for detail.'.format(**conf)
        self.logger.info(message)
        os.system(wget.format(**conf))

        ## rename-ing
        ss = 'snapshot.jpg'
        try:
            message = 'Rename ... {0} -> {jpgfile}'.format(ss, **conf)
            self.logger.info(message)
            os.renames(ss, '{jpgfile}'.format(**conf))
        except OSError as (errno, strerror):
            message = 'OSError({0}): {1}'.format(errno, strerror)
            self.logger.error(message)
        else:
            self.logger.info('Finished')
            os.renames('example.log', self.log)

    ##############################
    def timelapse(self):
        '''
        To ffmpeg:
        $ ffmpeg -y -f image2 -r 15 -pattern_type glob -i '$BASE/YYYY/mm/dd/*.jpg' -r 15 -an -vcodec libx264 -pix_fmt yuv420p video.mp4
        $ mv video.mp4 $BASE/YYYY-mm-dd.mp4
        '''
        pass

        # ## ffmpeg-ing
        # ## pbweb
        # datedir = time.strftime('%Y/%m/%d/', time.localtime())
        # pattern = os.path.join(self.base, datedir, '*.jpg')
        # video = 'video.mp4'

        # ffmpeg_in = "-y -f image2 -r 15 -pattern_type glob -i '{0}'".format(pattern)
        # ffmpeg_out = "-r 15 -an -vcodec libx264 -pix_fmt yuv420p {0}".format(video)
        # ffmpeg = 'ffmpeg {0} {1}'.format(ffmpeg_in, ffmpeg_out)
        # self.logger.info(ffmpeg)
        # os.system(ffmpeg)
        # mp4file = os.path.join(self.base, '{0}.mp4'.format(time.strftime('%Y-%m-%d')))
        # os.rename(video, mp4file)

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
        qw = QwatchCapture(name=name,
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
        qw.capture()
