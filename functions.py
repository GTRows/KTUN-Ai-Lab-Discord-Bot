import datetime
import logging
import os
import sys


def restart_client():
    os.execv(sys.executable, ['python'] + sys.argv)


async def is_it_me(ctx):
    result = True
    if not (ctx.author.id == 317674611628179456 or ctx.author.id == 336601194451435522):
        # await ctx.send("Bu işlem için yetkiniz yetmiyor")
        result = False
    return result


def get_channel_by_id(client, channel):
    if channel[0] == '<' and channel[-1] == '>':
        channel = channel[2:-1]
    try:
        channel = int(channel)
    except ValueError:
        print("ValueError <@317674611628179456>")
    return client.get_channel(channel)


def log_start():
    global logger
    path = os.getcwd()
    path = os.path.abspath(os.path.join(path, os.pardir)) + "/"
    file_name = path + "log_main/" + "test_" + datetime.now().strftime("log-%m-%d-%H.%M.%S") + ".log"
    logging.basicConfig(filename=file_name,
                        format='%(asctime)s %(processName)s %(process)d %(funcName)s %(name)s - %(levelname)s - %('
                               'message)s',
                        filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


def log_set(level=1, message="Null"):
    global logger
    if level == 0:
        logger.debug(message)
    elif level == 1:
        logger.info(message)
    elif level == 2:
        logger.warning(message)
    elif level == 3:
        logger.error(message)
    elif level == 4:
        logger.critical(message)
    elif level == 5:
        logger.exception(message)
