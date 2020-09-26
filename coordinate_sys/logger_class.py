from datetime import datetime
class Logger():
    '''
    记录运行日志
    '''

    class __SingletonLogger():
        def __init__(self, file_name):
            self.val = None
            self.file_name = file_name

        def __str__(self):
            return f'logger[{self.file_name}] -- var[{self.val}]'

        def _write_log(self, level, msg):
            with open(self.file_name, 'a') as log_file:
                log_file.write(f'\n【{level}】:{datetime.now().isoformat(timespec="seconds")}>>>>{msg}')

        def critical(self, msg):
            self._write_log('CRITICAL', msg)

        def error(self, msg):
            self._write_log('ERROR',msg)

        def warning(self, msg):
            self._write_log('WARNING', msg)

        def info(self, msg):
            self._write_log('INFO', msg)

        def debug(self, msg):
            self._write_log('DEBUG', msg)

    instance = None

    def __new__(cls, file_name, **kwargs):
        if not Logger.instance:
            Logger.instance = Logger.__SingletonLogger(file_name)
        return Logger.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, key, value):
        return setattr(self.instance, key, value)


logger = Logger('logger.log')