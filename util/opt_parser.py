import sys
from optparse import OptionParser, OptionGroup

from util.toolkit import properties, log, logging

mandatory_options = []

# Init Optparser
parser = OptionParser(
    version="%prog \n\n version: '" + properties.version + "'\n revision: '" + properties.revision + "'\n build date: '" + properties.build_date + "'")

# Main options
mainOptionsGroup = OptionGroup(parser, "Main Options", "(Main script options)")
mainOptionsGroup.add_option("-i", "--install", action="store_const", const=1, dest="installmode", default=0, help="Deploy code")
mainOptionsGroup.add_option("-I", "--installc", action="store_const", const=2, dest="installmode", default=0, help="Crosscompile and deploy code")

mainOptionsGroup.add_option("-p", "--profile", dest="profile", help="Pre-existing profile", metavar="<profile>")
mainOptionsGroup.add_option("-d", "--device", dest="device", help="Device path of your board", metavar="<device>", default="/dev/ttyUSB0")

parser.add_option_group(mainOptionsGroup)

# Common Options
commonOptionsGroup = OptionGroup(parser, "Common Options", "(Common throughout all actions supported by the script)")


parser.add_option_group(commonOptionsGroup)

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


# Set logging level
if options.verbose == 1:
    log.root.handlers[0].setLevel(logging.DEBUG)
    logging.getLogger(properties.default_logger).handlers[0].setLevel(logging.DEBUG)
