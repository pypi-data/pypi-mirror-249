from loguru import logger

class Bruce_loguru():
    def document(self):
        """
        官方文档
        """
        url="https://loguru.readthedocs.io/en/stable/index.html"
        return url

    def print_debug(self,data:str):
        logger.debug(data)

    def save_log(self,log_name:str,rotation,compression):
        logger.add("file_1.log", rotation="500 MB")  # Automatically rotate too big file
        logger.add("file_2.log", rotation="12:00")  # New file is created each day at noon
        logger.add("file_3.log", rotation="1 week")  # Once the file is too old, it's rotated
        logger.add("file_X.log", retention="10 days")  # Cleanup after some time
        logger.add("file_Y.log", compression="zip")  # Save some loved space



# cc=Bruce_loguru()
# cc.print_debug("123")

# import logging
#
# # 创建一个logger对象
# logger = logging.getLogger('my_logger')
# logger.setLevel(logging.DEBUG)
#
# # 创建一个handler对象，用于将日志消息发送到控制台
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)
#
# # 创建一个formatter对象，用于设置日志消息的格式
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#
# # 将formatter对象添加到handler对象中
# console_handler.setFormatter(formatter)
#
# # 将handler对象添加到logger对象中
# logger.addHandler(console_handler)
#
# # 记录日志消息
# logger.debug('This is a debug message')
# logger.info('This is an info message')
# logger.warning('This is a warning message')
# logger.error('This is an error message')
# logger.critical('This is a critical message')