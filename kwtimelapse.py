#! /usr/bin/env python3
# coding: utf-8

import os
import argparse
import configparser
import kumawatch as kwatch

##################################################
if __name__ == '__main__':

    desc = 'Concat Images to make TimeLapse movie.'
    epi = 'What you have to prepare:\n'
    epi += '  1) Prepare myconf.conf based on qwconf.example.\n'
    epi += 'For periodic capture:\n'
    epi += '  2) Add to cron.\n'

    parser = argparse.ArgumentParser(description=desc,
                                     epilog=epi,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(dest='date',
                        nargs=1,
                        help='specify DATE in YYYY/mm/dd format')
    parser.add_argument(dest='conffile',
                        nargs='+',
                        help='specify CONFIGFILE')
    parser.add_argument('-ifr', '--input-frame-rate',
                        dest='ifr',
                        type=int,
                        help='set number of frames in input files')
    parser.add_argument('-ofr', '--output-frame-rate',
                        dest='ofr',
                        type=int,
                        help='set number of frames in output file')
    parser.add_argument('-vc', '--vcodec',
                        dest='vcodec',
                        help='set vcodec of output file')
    parser.add_argument('-pf', '--pix-fmt',
                        dest='pixfmt',
                        help='set pixel format of output file')
    parser.add_argument('-ofn', '--output-filename',
                        dest='ofn',
                        help='set output filename')

    ## Set option defaults
    parser.set_defaults(ifr=15,
                        ofr=15,
                        vcodec='libx264',
                        pixfmt='yuv420p',
                        ofn='video.mp4')
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
        kw = kwatch.KumaWatch(name=name,
                                  user=user,
                                  passwd=passwd,
                                  uri=uri,
                                  base=base,
                                  log=log)

        ## Set Options
        kw.set_ffmpeg(ifr=args.ifr,
                      ofr=args.ofr,
                      vcodec=args.vcodec,
                      pixfmt=args.pixfmt,
                      ofn=args.ofn)
        kw.set_date(date=args.date[0])

        ## Run
        print(kw)
        kw.timelapse()
