#!/usr/bin/env python

import time
from subprocess import call
import util.opt_parser as parser
from util.toolkit import log, check_executable_exists, check_file_exists, properties, get_modified_files

timestamp = 0
timestamp_file = parser.options.path + properties.osDirSeparator + properties.timeStampFilename

# Read timestamp
if check_file_exists(timestamp_file):
    with open(timestamp_file, 'r') as f:
        timestamp = f.readline().strip()

log.info("Running script in path '{}'". format(parser.options.path))

check_executable_exists("ampy", True)

log.info("TIMESTAMP = " + str(timestamp))

mf = get_modified_files(parser.options.path, timestamp)

log.fatal(mf)

# call(["sudo ampy --port " + parser.options.device])

# Write timestamp
with open(timestamp_file, "w") as text_file:
    text_file.write("{}\n".format(time.time()))

# Salute!
log.info("Bye bye! :-)")
