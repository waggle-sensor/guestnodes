
# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license
# from http://code.activestate.com/recipes/577911-context-manager-for-a-daemon-pid-file/

# Dual licensed under the MIT and GPL licenses.

import fcntl
import os
import os.path

class PidFile(object):
    """Context manager that locks a pid file.  Implemented as class
    not generator because daemon.py is calling .__exit__() with no parameters
    instead of the None, None, None specified by PEP-343."""
    # pylint: disable=R0903

    def __init__(self, path):
        self.path = path
        self.pidfile = None

    def __enter__(self):
        
        directory = os.path.dirname(self.path)
        
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        self.pidfile = open(self.path, "a+")
        try:
            fcntl.flock(self.pidfile.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError:
            raise AlreadyRunning("Already running according to " + self.path)
        self.pidfile.seek(0)
        self.pidfile.truncate()
        self.pidfile.write(str(os.getpid()))
        self.pidfile.flush()
        self.pidfile.seek(0)
        return self.pidfile

    def __exit__(self, exc_type=None, exc_value=None, exc_tb=None):
        try:
            self.pidfile.close()
        except IOError as err:
            # ok if file was just closed elsewhere
            if err.errno != 9:
                raise
        os.remove(self.path)


class AlreadyRunning(Exception):
    pass

# example usage
#import daemon
#context = daemon.DaemonContext()
#context.pidfile = PidFile("/var/run/mydaemon"
