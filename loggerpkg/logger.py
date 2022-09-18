import logging
import datetime
import os

#def make_logger(name=None, consoleLevel, fileLevel)

def make_logger(name=None, consoleLevel=logging.DEBUG, fileLevel=logging.INFO):
    if name == None :
        name = datetime.datetime.today().strftime('%Y%m%d')
    
    # 1 logger instance를 만든다.
    logger = logging.getLogger(name)

    # 2 logger의 level을 가장 낮은 수준인 DEBUG로 설정해둔다.
    logger.setLevel(logging.DEBUG)

    # 3 formatter 지정
    formatter = logging.Formatter(fmt="%(levelname)s:%(lineno)d:%(asctime)s - %(message)s", datefmt='%m-%d %H:%M:%S')
    # formatter = logging.Formatter(fmt="%(funcName)s, %(lineno)d, %(asctime)s - %(message)s", datefmt='%m-%d %H:%M:%S')

    try :
        os.remove('.\\' + name + '.log')
    except Exception as e:
        pass
    # 4 handler instance 생성
    console = logging.StreamHandler()
    file_handler = logging.FileHandler(filename='.\\' + name + '.log')

    # 5 handler 별로 다른 level 설정
    console.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.INFO)

    # 6 handler 출력 format 지정
    console.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # 7 logger에 handler 추가
    logger.addHandler(console)
    logger.addHandler(file_handler)

    return logger