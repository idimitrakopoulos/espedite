#!/usr/bin/env python

import os
import subprocess
import time

import util.opt_parser as parser
from util.toolkit import log, check_executable_exists, check_file_exists, properties, \
    get_modified_files, execute_shell_command, execute_shell_command_get_output, read_file_to_list, \
    check_folder_exists, remove_files_by_ext_recursively,timestamp_to_human_readable, \
    get_subdirectory_structure_by_filelist, die

timestamp = 0
timestamp_file = parser.options.path + properties.osDirSeparator + properties.timeStampFilename
skip_files = []
start_time = time.time()

# Remove any compiled files
remove_files_by_ext_recursively(parser.options.path, properties.binaryCodeExtension)

# Read timestamp
if check_file_exists(timestamp_file):
    with open(timestamp_file, 'r') as f:
       timestamp = f.readline().strip()
       log.debug("Last execution was on {} (UNIX Timestamp: {}) ".format(timestamp_to_human_readable(timestamp), str(timestamp)))

log.info("Running script in path '{}'". format(parser.options.path))

check_executable_exists("ampy", True)
if parser.options.connect:
    check_executable_exists("picocom", True)

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
    # print(get_subdirectory_structure(parser.options.path))

    if parser.options.compile:
        # COMPILE
        log.info("Compiling ....")

        if not check_folder_exists(os.getcwd() + properties.osDirSeparator + "micropython"):
            log.debug("Compiling the compiler ..."),
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


    if parser.options.install or parser.options.profile:
        log.info("Installing ....")

        # Create folder structure for modified files
        dir_structure = get_subdirectory_structure_by_filelist(modified_relative_files)
        log.info("Creating folder structure (if required)")
        for d in dir_structure:
            execute_shell_command("sudo ampy --port /dev/ttyUSB0 mkdir {}".format(d), stderr=subprocess.PIPE)

        # Do this for all files modified or new
        for f in modified_relative_files:
            # Skip if it's included in the skip file
            if f in skip_files:
                log.debug("Skipping '{}' although it was modified".format(f))
                continue
            log.info("Installing file '{}'".format(f))

            # Remove file to be uploaded
            execute_shell_command("sudo ampy --port /dev/ttyUSB0 rm {}".format(f), stderr=subprocess.PIPE)

            # Remove compiled file if exist
            if os.path.splitext(f)[1] == properties.sourceCodeExtension:
                execute_shell_command("sudo ampy --port /dev/ttyUSB0 rm {}{}".format(os.path.splitext(f)[0],
                                                                                     properties.binaryCodeExtension), stderr=subprocess.PIPE)

            # Prefer to install compiled file rather than source
            if parser.options.compile and os.path.splitext(f)[1] == properties.sourceCodeExtension:
                execute_shell_command("sudo ampy --port /dev/ttyUSB0 put {} {}".format(parser.options.path + properties.osDirSeparator +
                                                                                       os.path.splitext(f)[0] + properties.binaryCodeExtension,
                                                                                       os.path.splitext(f)[0] + properties.binaryCodeExtension))
            # Otherwise upload original file
            else:
                execute_shell_command("sudo ampy --port /dev/ttyUSB0 put {} {}".format(parser.options.path + properties.osDirSeparator + f, f))

        # Apply selected profile
        if parser.options.profile and check_folder_exists("{}/profile/{}".format(parser.options.path, parser.options.profile)):
            log.info("Applying profile '{}'".format(parser.options.profile))
            execute_shell_command("sudo ampy --port /dev/ttyUSB0 rm main.py", stderr=subprocess.PIPE)
            execute_shell_command("sudo ampy --port /dev/ttyUSB0 rm main.mpy", stderr=subprocess.PIPE)
            execute_shell_command("sudo ampy --port /dev/ttyUSB0 rm conf/profile.properties", stderr=subprocess.PIPE)
            execute_shell_command("sudo ampy --port /dev/ttyUSB0 put {} {}".format("{}/profile/{}/{}".format(parser.options.path, parser.options.profile, "main.mpy"), "main.mpy"))
            execute_shell_command("sudo ampy --port /dev/ttyUSB0 put {} {}".format("{}/profile/{}/{}".format(parser.options.path, parser.options.profile, "main.py"), "main.py"))
            execute_shell_command("sudo ampy --port /dev/ttyUSB0 put {} {}".format("{}/profile/{}/conf/{}".format(parser.options.path, parser.options.profile, "profile.properties"), "conf/profile.properties"))

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
log.info("Execution time '{} sec'".format(time.time() - start_time))
log.info("Bye bye! :-)")
