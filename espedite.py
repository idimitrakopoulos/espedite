#!/usr/bin/env python

import sys
import time
from distutils.spawn import find_executable

import util.opt_parser as parser
from util.toolkit import log

log.info("Running script in path '{}'". format(parser.options.path))

if not find_executable("ampy"):
    log.critical("Required ampy executable wasn't found in your system. To install it please go to https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy")
    sys.exit()


with open("lastrun.ts", "w") as text_file:
    text_file.write("{}\n".format(time.time()))

# Salute!
log.info("Bye bye! :-)")
