import os
import sys
from optparse import OptionParser, OptionGroup, SUPPRESS_HELP

from util.toolkit import properties, log, logging

mandatory_options = ['path', 'device']

# Init Optparser
parser = OptionParser(
    version="%prog \n\n version: '" + properties.version + "'\n revision: '" + properties.revision + "'\n build date: '" + properties.build_date + "'")

# Main options
mainOptionsGroup = OptionGroup(parser, "Main Options", "(Main script options)")
mainOptionsGroup.add_option("-i", "--install", action="store_true", dest="install", default=False, help="Deploy code")
mainOptionsGroup.add_option("-C", "--compile",  action="store_true", dest="compile", default=False, help="Crosscompile when deploying code")
mainOptionsGroup.add_option("-u", "--uninstall", action="store_true", dest="uninstall", default=False, help="Uninstall code")
mainOptionsGroup.add_option("-c", "--connect", action="store_true", dest="connect", default=False, help="Connect to your board after the operation")

mainOptionsGroup.add_option("-P", "--path", dest="path", help=SUPPRESS_HELP, metavar="<path>", default=os.environ["PWD"])
mainOptionsGroup.add_option("-p", "--profile", dest="profile", help="Pre-existing profile", metavar="<profile>")
mainOptionsGroup.add_option("-s", "--skip", dest="skip", help="Specify a file that contains files and folders that should be skipped", metavar="<skip>")
mainOptionsGroup.add_option("-d", "--device", dest="device", help="Device path of your board", metavar="<device>", default="/dev/ttyUSB0")
mainOptionsGroup.add_option("-b", "--baud", dest="baud", help="Baud speed for connecting to your board", metavar="<baud>", default="115200")

parser.add_option_group(mainOptionsGroup)

# # Common Options
# commonOptionsGroup = OptionGroup(parser, "Common Options", "(Common throughout all actions supported by the script)")
# parser.add_option_group(commonOptionsGroup)

# Logging Options
loggingOptionsGroup = OptionGroup(parser, "Logging Options", "(Regulate the logging of the script. Default loglevel: INFO)")
loggingOptionsGroup.add_option("-v", "--verbose",        action="store_const",       const=1, dest="verbose",        help="Verbose mode (loglevel: DEBUG)")
parser.add_option_group(loggingOptionsGroup)


# Parse arguments
(options, args) = parser.parse_args()

# Make sure all mandatory options are provided
for m in mandatory_options:
    if not options.__dict__[m]:
        log.critical("Mandatory option '" + m + "' is missing\n")
        parser.print_help()
        sys.exit()

# Make path absolute in case it was given as . or ../ etc
# options.path = os.path.abspath(options.path)

# Set logging level
if options.verbose == 1:
    log.root.handlers[0].setLevel(logging.DEBUG)
    logging.getLogger(properties.default_logger).handlers[0].setLevel(logging.DEBUG)
