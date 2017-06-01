#!/usr/bin/env python

import time, os, subprocess

import util.opt_parser as parser
from util.toolkit import log, check_executable_exists, check_file_exists, properties, \
    get_modified_files, execute_shell_command, read_file_to_list, die

timestamp = 0
timestamp_file = parser.options.path + properties.osDirSeparator + properties.timeStampFilename
skip_files = []

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

if parser.options.uninstall:
    # UNINSTALL
    log.info("Uninstalling ....")

    installed_files = execute_shell_command("sudo ampy --port /dev/ttyUSB0 ls /")

    for f in installed_files:
        log.info("Removing file or folder '{}' ....".format(f))
        execute_shell_command("sudo ampy --port /dev/ttyUSB0 rmdir {}".format(f), stderr=subprocess.PIPE)
        execute_shell_command("sudo ampy --port /dev/ttyUSB0 rm {}".format(f), stderr=subprocess.PIPE)

    # Remove timestamp file
    try:
        os.remove(timestamp_file)
        log.info("Removing timestamp file '{}' ....".format(timestamp_file))
    except OSError:
        pass

if modified_relative_files and parser.options.install:

    if parser.options.compile:
        # COMPILE
        log.info("Compiling ....")

    if parser.options.install:
        log.info("Installing ....")
        for f in modified_relative_files:
            if f in skip_files:
                log.debug("Skipping '{}' although it was modified".format(f))
                continue
            log.debug("Updating file '{}'".format(f))

            execute_shell_command("sudo ampy --port /dev/ttyUSB0 rm {}".format(f), stderr=subprocess.PIPE)
            execute_shell_command("sudo ampy --port /dev/ttyUSB0 put {} {}".format(parser.options.path + properties.osDirSeparator + f, f))


        # Write installation timestamp
        with open(timestamp_file, "w") as text_file:
            text_file.write("{}\n".format(time.time()))

elif parser.options.install and not modified_relative_files:
    die("No modified files detected. Installation cannot be completed.")



if parser.options.connect:
    # CONNECT
    log.info("Connecting to '{}' ....".format(parser.options.device))
    execute_shell_command("sudo picocom --baud 115200 /dev/ttyUSB0")



# Salute!
log.info("Bye bye! :-)")
