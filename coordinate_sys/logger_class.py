import logging

logger = logging.getLogger('log')
logger.setLevel(level=logging.DEBUG)
handle = logging.FileHandler('logger.log')
handle.setLevel(level=logging.DEBUG)
# %(levelno)s：打印日志级别的数值
# %(levelname)s：打印日志级别的名称
# %(pathname)s：打印当前执行程序的路径，其实就是sys.argv[0]
# %(filename)s：打印当前执行程序名
# %(funcName)s：打印日志的当前函数
# %(lineno)d：打印日志的当前行号
# %(asctime)s：打印日志的时间
# %(thread)d：打印线程ID
# %(threadName)s：打印线程名称
# %(process)d：打印进程ID
# %(message)s：打印日志信息
formatter = logging.Formatter('%(levelname)s--%(asctime)s--%(filename)s--【func】%(funcName)s--【line】%(lineno)d--【msg】%(message)s')
handle.setFormatter(formatter)
logger.addHandler(handle)

