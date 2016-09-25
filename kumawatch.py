# coding: utf-8

import os
import sys
import time
import datetime
import argparse
import configparser
import logging

##################################################
class KumaWatch(object):
    '''
    Image capture for webcamera.
    '''
    ##############################
    def __init__(self, name, user, passwd, uri, base, log):
        '''
        Configure KumaWatch.
        '''
        self.name = name
        self.user = user
        self.passwd = passwd
        self.uri = uri
        self.base = base
        self.log = log

        jpgfmt = 'snapshots/%Y/%m/%d/%Y-%m%d-%H%M-%S.jpg'
        mp4fmt = 'timelapse/%Y-%m-%d.mp4'
        self.jpgfile = os.path.join(self.base, jpgfmt)
        self.mp4file = os.path.join(self.base, mp4fmt)
        self.set_logger()

    ##############################
    def __str__(self):
        '''
        Print initial configurations.
        '''
        self.logger.info(20 * '-')
        self.logger.info('name : {0}'.format(self.name))
        self.logger.info('uri  : {0}'.format(self.uri))
        self.logger.info('base : {0}'.format(self.base))
        self.logger.info('log  : {0}'.format(self.log))
        return ''

    ##############################
    def set_logger(self):
        self.logger = logging.getLogger('KumaWatch')
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(name)-12s %(module)s.%(funcName)-20s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=self.log,
                            filemode='w')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(levelname)-8s %(name)-12s %(module)s.%(funcName)-20s %(message)s')
        console.setFormatter(formatter)
        self.logger.addHandler(console)

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

    ##################################################
    def set_ffmpeg(self, ifr, ofr, vcodec, pixfmt, ofn):
        '''
        Set option for ffmpeg
        '''
        self.ifr = ifr
        self.ofr = ofr
        self.vcodec = vcodec
        self.pixfmt = pixfmt
        self.ofn = ofn

    ##################################################
    def set_date(self, date):
        '''
        Read date and return directory
        '''
        dt = date
        if date == 'today':
            dt = datetime.date.today()
        elif date == 'yesterday':
            dt = datetime.date.today() - datetime.timedelta(1)
        else:
            dt = datetime.datetime.strptime(date, '%Y/%m/%d')

        self.logger.debug(self.jpgfile)
        self.logger.debug(os.path.dirname(self.jpgfile))
        d = time.strftime(os.path.dirname(self.jpgfile), dt.timetuple())
        self.logger.debug(d)

        if not os.path.exists(d):
            self.logger.error('No such directory : "{0}".'.format(d))
            self.logger.error('(>W<)')
            sys.exit()
        else:
            self.date = dt
            self.pattern = os.path.join(d, '*.jpg')

    ##############################
    def capture(self):
        '''
        To capture:
        $ wget --http-user=USER --http-password=PASS URI
        $ mv snapshot.jpg $BASE/YYYY/mm/dd/YYYY-mmdd-HHMM-SS.jpg

        '''
        ## config for wget
        conf = {'user':self.user,
                'passwd':self.passwd,
                'uri':self.uri,
                'tries':self.tries,
                'timeout':self.timeout,
                'logfile':self.logfile,
                'jpgfile': time.strftime(self.jpgfile)}

        self.logger.debug('uri     : {uri}'.format(**conf))
        self.logger.debug('retries : {tries}'.format(**conf))
        self.logger.debug('timeout : {timeout}'.format(**conf))
        self.logger.debug('logfile : {logfile}'.format(**conf))

        ## wget-ing
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
        except OSError(errno, strerror):
            message = 'OSError({0}): {1}'.format(errno, strerror)
            self.logger.error(message)
        else:
            self.logger.info('Finished CAPTURE')

    ##############################
    def timelapse(self):
        '''
        To ffmpeg:
        $ ffmpeg -y -f image2 -r 15 -pattern_type glob -i '$BASE/YYYY/mm/dd/*.jpg' -r 15 -an -vcodec libx264 -pix_fmt yuv420p video.mp4
        $ mv video.mp4 $BASE/YYYY-mm-dd.mp4
        '''
        ## config for ffmpeg
        conf = {'ifr':self.ifr,
                'pattern':self.pattern,
                'ofr':self.ofr,
                'vcodec':self.vcodec,
                'pixfmt':self.pixfmt,
                'ofn':self.ofn,
                'date':self.date}

        self.logger.debug('input frame rate  : {ifr}'.format(**conf))
        self.logger.debug('output frame rate : {ofr}'.format(**conf))
        self.logger.debug('vcodec            : {vcodec}'.format(**conf))
        self.logger.debug('pixel format      : {pixfmt}'.format(**conf))
        self.logger.debug('output filename   : {ofn}'.format(**conf))

        ## ffmpeg-ing
        ffmpeg = "ffmpeg -y -f image2 -r {ifr} -pattern_type glob -i '{pattern}' -r {ofr} -an -vcodec {vcodec} -pix_fmt {pixfmt} {ofn}"
        message = 'Execute ffmpeg ... {pattern}'.format(**conf)
        self.logger.info(message)
        os.system(ffmpeg.format(**conf))

        # self.logger.info(ffmpeg)
        mp4file = time.strftime(self.mp4file, self.date.timetuple())
        try:
            message = 'Rename ... {ofn} -> {0}'.format(mp4file, **conf)
            self.logger.info(message)
            os.renames('{ofn}'.format(**conf), mp4file)
        except OSError(errno, strerror):
            message = 'OSError({0}): {1}'.format(errno, strerror)
            self.logger.error(message)
        else:
            self.logger.info('Finished FFMPEG')

##################################################
if __name__ == '__main__':

    desc = 'Image capture for webcamera.'
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
                        logfile='qwwget.log')
    ## Get args and options
    args = parser.parse_args()

    ## Print config files
    for f in args.conffile:
        print(f, os.path.exists(f))

    ## Read config files
    config = configparser.SafeConfigParser()
    config.read(args.conffile)

    ## Set KumaWatch
    sections = config.sections()
    for section in sections:
        name = section
        uri = config.get(section, 'uri')
        user = config.get(section, 'user')
        passwd = config.get(section, 'pass')
        base = config.get(section, 'base')
        log = config.get(section, 'log')

        ## Init KumaWatch
        kw = KumaWatch(name=name,
                           user=user,
                           passwd=passwd,
                           uri=uri,
                           base=base,
                           log=log)

        ## Set Options
        kw.set_tries(args.number)
        kw.set_timeout(args.seconds)
        kw.set_logfile(args.logfile)

        ## Run
        print(kw)
        kw.capture()
