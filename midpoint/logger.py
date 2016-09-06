import sys

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Logger:
        INFO = Colors.OKBLUE + "INFO: "
        SUCCESS = Colors.OKBLUE + "SUCCESS: "
        FAIL = Colors.FAIL + "FAIL: "

        def __init__(self,backupLog=None):
		if backupLog is not None:
			self.log = open(backupLog, 'a')
			self.write_method = 'write_log'
		else:
			self.write_method = 'write_nolog'

	def write(self,msg_type, msg):
		getattr(self, self.write_method)(msg_type,msg)

        def write_nolog(self,msg_type, msg):
                output = msg_type + msg + Colors.ENDC 
		print output
		if msg_type == self.FAIL:
			sys.exit()

        def write_log(self,msg_type, msg):
                output = msg_type + msg + Colors.ENDC
		print output
                self.log.write(output+'\n')
		if msg_type == self.FAIL:
			sys.exit()
