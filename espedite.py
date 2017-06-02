#!/usr/bin/env python

import os
import subprocess
import time

import util.opt_parser as parser
from util.toolkit import log, check_executable_exists, check_file_exists, properties, \
    get_modified_files, execute_shell_command, execute_shell_command_get_output, read_file_to_list, check_folder_exists, remove_files_by_ext_recursively,timestamp_to_human_readable

timestamp = 0
timestamp_file = parser.options.path + properties.osDirSeparator + properties.timeStampFilename
skip_files = []

# Remove any compiled files
remove_files_by_ext_recursively(parser.options.path, properties.binaryCodeExtension)

# Read timestamp
if check_file_exists(timestamp_file):
    with open(timestamp_file, 'r') as f:
        timestamp = f.readline().strip()

log.info("Running script in path '{}'". format(parser.options.path))

check_executable_exists("ampy", True)
if parser.options.connect:
    check_executable_exists("picocom", True)

log.debug("Last execution was on {} (UNIX Timestamp: {}) ".format(timestamp_to_human_readable(timestamp), str(timestamp)))

modified_relative_files = get_modified_files(parser.options.path, timestamp, True)

if parser.options.skip:
    # READ SKIPFILE
    log.info("Reading skip file '{}' ....".format(parser.options.skip))
    skip_files = read_file_to_list(parser.options.path + properties.osDirSeparator + parser.options.skip)

if parser.options.uninstall:
    # UNINSTALL
    log.info("Uninstalling ....")

    installed_files = execute_shell_command_get_output("sudo ampy --port /dev/ttyUSB0 ls /").split("\n")

    for f in installed_files:
        # ampy returns an empty string at the end so skip that
        if f == "":
            continue
        log.info("Removing file or folder '{}' ....".format(f))
        execute_shell_command("sudo ampy --port /dev/ttyUSB0 rmdir {}".format(f), stderr=subprocess.PIPE)
        execute_shell_command("sudo ampy --port /dev/ttyUSB0 rm {}".format(f), stderr=subprocess.PIPE)

    # Remove timestamp file
    try:
        os.remove(timestamp_file)
        log.info("Removing timestamp file '{}' ....".format(timestamp_file))
    except OSError:
        pass

    log.info("Uninstallation complete ....")

if modified_relative_files and parser.options.install:

    if parser.options.compile:
        # COMPILE
        log.info("Compiling ....")

        if not check_folder_exists(os.getcwd() + properties.osDirSeparator + "micropython"):
            log.debug("Compiling the compiler ...")
            pushd = os.getcwd()
            execute_shell_command("git clone https://github.com/micropython/micropython")
            os.chdir(os.getcwd() + "/micropython/mpy-cross")
            execute_shell_command("make")
            os.chdir(pushd)

        for f in modified_relative_files:
            extension = os.path.splitext(f)[1]
            if extension == properties.sourceCodeExtension:
                log.info("Compiling file {}".format(f))
                execute_shell_command("{}/micropython/mpy-cross/mpy-cross {}".format(os.getcwd(), parser.options.path + properties.osDirSeparator + f))


    if parser.options.install:
        log.info("Installation ....")
        for f in modified_relative_files:
            if f in skip_files:
                log.debug("Skipping '{}' although it was modified".format(f))
                continue
            log.debug("Installing file '{}'".format(f))

            execute_shell_command("sudo ampy --port /dev/ttyUSB0 rm {}".format(f), stderr=subprocess.PIPE)
            if os.path.splitext(f)[1] == properties.sourceCodeExtension: execute_shell_command("sudo ampy --port /dev/ttyUSB0 rm {}{}".format(os.path.splitext(f)[0], properties.binaryCodeExtension), stderr=subprocess.PIPE)
            if parser.options.compile:
                execute_shell_command("sudo ampy --port /dev/ttyUSB0 put {} {}".format(parser.options.path + properties.osDirSeparator +
                                                                                       os.path.splitext(f)[0] + properties.binaryCodeExtension,
                                                                                       os.path.splitext(f)[0] + properties.binaryCodeExtension))
            else:

                execute_shell_command("sudo ampy --port /dev/ttyUSB0 put {} {}".format(parser.options.path + properties.osDirSeparator + f, f))


        # Write installation timestamp
        with open(timestamp_file, "w") as text_file:
            text_file.write("{}\n".format(time.time()))

elif parser.options.install and not modified_relative_files:
    log.warn("No modified files detected since last execution on {}. Installation skipped.".format(timestamp_to_human_readable(timestamp)))



if parser.options.connect:
    # CONNECT
    log.info("Connecting to '{}' ....".format(parser.options.device))
    execute_shell_command("sudo picocom --baud 115200 /dev/ttyUSB0")



# Salute!
log.info("Bye bye! :-)")
