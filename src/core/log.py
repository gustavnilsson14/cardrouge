class Log:

    ERROR = 'ERROR'
    DEBUG = 'DEBUG'
    INFO = 'INFO'

    LEVEL = 3
    LEVELS = [
        [],
        [ERROR],
        [ERROR,DEBUG],
        [ERROR,DEBUG,INFO],
    ]

    @classmethod
    def log(cls,message,logtype = 'ERROR'):
        if logtype in Log.LEVELS[Log.LEVEL]:
            print('%s - %s: %s'%(cls.__name__,logtype,message,))
