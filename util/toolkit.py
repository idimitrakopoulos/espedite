import getpass
import logging.config
import os
import platform
import random
import signal
import socket
import subprocess
import sys
import time
from ConfigParser import RawConfigParser

from util.color_formatter import ColorFormatter
from util.fun_stuff import SpinCursor


def die(msg="Error"):
    log.fatal(msg)
    sys.exit()


def raise_NotImplementedException():
    raise NotImplementedError, "Oops! This part of the functionality has not been implemented ... Bye bye!"


def kill_process(pid):
    log.warn("kill -9 " + pid)
    os.kill(int(pid), signal.SIGKILL)


def terminate_process(pid):
    log.warn("kill " + pid)
    os.kill(int(pid), signal.SIGTERM)

def execute_shell_command(command, shell=False, stderr=None):
    log.debug("Executing command '{}'".format(command))
    return subprocess.call(command.split(), shell=shell, stderr=stderr)

def execute_shell_command_get_output(command, shell=False, stderr=None):
    log.debug("Executing command '{}'".format(command))
    return subprocess.check_output(command.split(), shell=shell, stderr=stderr)

def print_os_information():
    log.info("Script running on '" + " ".join(platform.uname()) + "' from within '" + os.getcwd() +"' by user '" + getpass.getuser() + "'" )


def print_script_information():
    log.info(
        "Script version  '" + properties.version + "  r" + properties.revision + "' built on '" + properties.build_date + "'")

def read_file_to_list(filename):
    with open(filename) as f:
        list = f.read().splitlines()
    return list

def read_property_from_file(propertyName, propertiesSectionName, propertiesFilename, warnIfEmpty=True):
    result = ""
    if os.path.isfile(propertiesFilename):
        try:
            cfg = RawConfigParser()
            cfg.read(propertiesFilename)
            result = cfg.get(propertiesSectionName, propertyName)
            if (globals().has_key('log')):
                log.debug(
                    "Value of '" + propertyName + "' from '[" + propertiesSectionName + "]' in '" + propertiesFilename + "' = '" + result + "'")
                if result == "" and warnIfEmpty:
                    log.warn("No value exists for '" + propertyName + "' on section '[" + propertiesSectionName + "]' inside file '" + propertiesFilename + "'")
                elif result == "" and not warnIfEmpty:
                    log.info("No value exists for '" + propertyName + "' on section '[" + propertiesSectionName + "]' inside file '" + propertiesFilename + "' however empty values for this property are expected and some times intentional.")
        except:
            raise
    else:
        if globals().has_key('log'):
            log.warn("Properties file '" + propertiesFilename + "' does not exist.")
        result = None

    return result


def get_current_hostname():
    result = ""
    try:
        result = socket.gethostbyname(socket.gethostname())
    except Exception:
        result = socket.gethostname()

    return result


def generate_guid(*args):
    """
    Generates a universally unique ID.
    Any arguments only create more randomness.
    """
    t = long( time.time() * 1000 )
    r = long( random.random()*100000000000000000L )
    try:
        a = get_current_hostname()
    except:
        # if we can't get a network address, just imagine one
        a = random.random()*100000000000000000L

    data = str(t)+' '+str(r)+' '+str(a)+' '+str(args)
    import hashlib
    data = hashlib.md5(data).hexdigest()
    return data


def check_filepath_exists(filename, separator):
    if os.path.isfile(sys.path[0] + separator + filename):
        return True
    else:
        return False


def check_file_exists(filename):
    if os.path.isfile(filename):
        return True
    else:
        return False

def check_folder_exists(path):
    if os.path.isdir(path):
        return True
    else:
        return False

def check_executable_exists(executable, mandatory=False):
    from distutils.spawn import find_executable
    if not find_executable(executable):
        if mandatory:
            die("Mandatory executable '{}' wasn't found in your system. Exiting...".format(executable))
    else:
        log.info("Executable '{}' was found in your system.".format(executable))
        return True


def get_class(fully_qualified_path, module_name, class_name, *instantiation):
    """
    Returns an instantiated class for the given string descriptors
    :param fully_qualified_path: The path to the module eg("Utilities.Printer")
    :param module_name: The module name eg("Printer")
    :param class_name: The class name eg("ScreenPrinter")
    :param instantiation: Any fields required to instantiate the class
    :return: An instance of the class
    """
    p = __import__(fully_qualified_path)
    m = getattr(p, module_name)
    c = getattr(m, class_name)
    instance = c(*instantiation)
    return instance

def get_modified_files(path, reference_timestamp, relative_paths=True):
    modified_files = []
    for root, dirs, files in os.walk(path):
        for basename in files:
            if not basename == properties.timeStampFilename:
                filename = os.path.join(root, basename)
                status = os.stat(filename)

                if float(status.st_mtime) > float(reference_timestamp):
                    if relative_paths:
                        modified_files.append(os.path.relpath(filename, path))
                    else:
                        modified_files.append(filename)

    return modified_files

def ab_path_to_class(path, p):
    # pkg.module.ClassName
    _p_name = path.split(".")[0] + "." + path.split(".")[1]  # pkg.module
    _m_name = path.split(".")[1]  # module
    _c_name = path.split(".")[2]  # ClassName

    # Instantiate class
    c = get_class(_p_name, _m_name, _c_name, p)
    return c



def get_string_from_list(lst, n, s):
    r = False
    for i in lst:
        # log.debug("Comparing '", str(i[n]), "' with '", s, "'")
        if i[n] == s:
            r = True
            break
    return r


def start_busy_indicator(msg):
    spin = SpinCursor(msg)
    spin.start()
    return spin


def stop_busy_indicator(busyIndicator):
    busyIndicator.stop()


class PropertyReader(object):
    '''
    classdocs
    '''

    property_file = "conf/global.properties"

    def __init__(self):
        '''
        Constructor
        '''

        # Get properties from global.properties
        # [propertyFiles]
        self.log_properties = read_property_from_file("logProperties", "propertyFiles", self.property_file)

        # [variousProperties]
        self.default_logger = read_property_from_file("defaultLogger", "variousProperties", self.property_file)
        self.manifest_file = read_property_from_file("manifestFile", "variousProperties", self.property_file)
        self.manifest_template_file = read_property_from_file("manifestTemplateFile", "variousProperties",
                                                              self.property_file)
        self.script_name = read_property_from_file("scriptName", "variousProperties", self.property_file)
        self.osDirSeparator = read_property_from_file("osDirSeparator", "variousProperties", self.property_file)
        self.timeStampFilename = read_property_from_file("tsFilename", "variousProperties", self.property_file)

        # [loggingProperties]
        self.custom_logging_format = read_property_from_file("customLoggingFormat", "loggingProperties",
                                                             self.property_file)


        # MANIFEST.MF
        if not check_file_exists(self.manifest_file):
            print "File '" + self.manifest_file + "' does not exist. Sorry, you cannot work with an unreleased version of this script. If you must work with it please execute 'cp " + self.manifest_template_file + " " + self.manifest_file + "' and retry running the script."
            sys.exit()
        self.version = read_property_from_file("version", self.script_name, self.manifest_file)
        self.revision = read_property_from_file("revision", self.script_name, self.manifest_file)
        self.build_date = read_property_from_file("buildDate", self.script_name, self.manifest_file)



# Change working directory in case someone executed the script outside the script's directory
os.chdir(sys.path[0])

# Initialize script global properties
properties = PropertyReader()

# Initialize loggers
logging.ColorFormatter = ColorFormatter
logging.config.fileConfig(properties.log_properties)
log = logging.getLogger(properties.default_logger)
