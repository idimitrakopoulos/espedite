#!/usr/bin/env python

import time

import util.opt_parser as parser
from util.toolkit import log, check_executable_exists, check_file_exists, properties, \
    get_modified_files, execute_shell_command, read_file_to_list, die

timestamp = 0
timestamp_file = parser.options.path + properties.osDirSeparator + properties.timeStampFilename

# Read timestamp
if check_file_exists(timestamp_file):
    with open(timestamp_file, 'r') as f:
        timestamp = f.readline().strip()

log.info("Running script in path '{}'". format(parser.options.path))

check_executable_exists("ampy", True)
if parser.options.connect:
    check_executable_exists("picocom", True)

log.info("TIMESTAMP = " + str(timestamp))

modified_relative_files = get_modified_files(parser.options.path, timestamp, True)

if parser.options.skip:
    # READ SKIPFILE
    log.info("Reading skip file '{}' ....".format(parser.options.skip))
    skip_files = read_file_to_list(parser.options.path + properties.osDirSeparator + parser.options.skip)

if parser.options.format == 1:
    # UNINSTALL
    log.info("Uninstalling ....")

if modified_relative_files and parser.options.installmode > 0:

    if parser.options.installmode == 2:
        # COMPILE / INSTALL
        log.info("Compiling ....")
        log.info("Installing ....")

    if parser.options.installmode == 3:
        # UPDATE
        log.info("Updating ....")
        for f in modified_relative_files:
            if f in skip_files:
                log.debug("Skipping '{}' although it was modified".format(f))
                continue
            log.debug("Updating file '{}'".format(f))
            execute_shell_command("sudo ampy --port /dev/ttyUSB0 rm {}".format(f))
            execute_shell_command("sudo ampy --port /dev/ttyUSB0 put {}".format(f))
elif parser.options.installmode > 0:
    die("No modified files detected. Installation cannot be completed.")



if parser.options.connect:
    # CONNECT
    log.info("Connecting to '{}' ....".format(parser.options.device))
    execute_shell_command("sudo picocom --baud 115200 /dev/ttyUSB0")

# Write timestamp
with open(timestamp_file, "w") as text_file:
    text_file.write("{}\n".format(time.time()))

# Salute!
log.info("Bye bye! :-)")
