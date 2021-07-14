import logging
import ctypes

# output "logging" messages to DbgView via OutputDebugString (Windows only!)

class DbgViewHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        self.OutputDebugString = ctypes.windll.kernel32.OutputDebugStringW

    def emit(self, record):
        self.OutputDebugString(self.format(record))

class Logger():
    def __init__(self):
        self.log = logging.getLogger("output.debug.string.example")
        self.config_logging()

    def config_logging(self):
        # format
        fmt = logging.Formatter(fmt='%(asctime)s.%(msecs)03d [%(thread)5s] %(levelname)-8s %(funcName)-20s %(lineno)d %(message)s', datefmt='%Y:%m:%d %H:%M:%S')
        
        self.log.setLevel(logging.DEBUG)

        # "OutputDebugString\DebugView"
        ods = DbgViewHandler()
        ods.setLevel(logging.DEBUG)
        ods.setFormatter(fmt)
        self.log.addHandler(ods)
        
        # "Console"
        con = logging.StreamHandler()
        con.setLevel(logging.DEBUG)
        con.setFormatter(fmt)
        self.log.addHandler(con)

    def print(self, msg):
        self.log.debug(str(msg))

    def test(self):
        self.log.debug("debug message")
        self.log.info("info message")
        self.log.warning("warn message")
        self.log.error("error message")
        self.log.critical("critical message")