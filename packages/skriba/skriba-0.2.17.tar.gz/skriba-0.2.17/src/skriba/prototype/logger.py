import os
import logging
from datetime import datetime

from rich.logging import RichHandler

import inspect

PREVIOUS_FUNCTION = 1
PENULTIMATE_FUNCTION = 2


def _add_verbose_info(message: str, color: str = "blue") -> str:
    function_name = inspect.stack()[PENULTIMATE_FUNCTION].function
    return (
        "[ [{color}]{function_name}[/] ]: {message}".format(
            function_name=function_name,
            message=message,
            color=color
        ))


def info(message, markup=False, verbose=False):
    logger_name = os.getenv("SKRIBA_LOGGER_NAME")

    if verbose:
        message = _add_verbose_info(message=message, color="blue")

    logger = get_logger(logger_name=logger_name)
    logging.getLogger('numba').setLevel(logging.INFO)
    logger.info(message, extra={"markup": markup})


def debug(message, markup=False, verbose=False):
    logger_name = os.getenv("SKRIBA_LOGGER_NAME")

    if verbose:
        message = _add_verbose_info(message=message, color="green")

    logger = get_logger(logger_name=logger_name)
    logging.getLogger('numba').setLevel(logging.INFO)
    logger.debug(message, extra={"markup": markup})


def warning(message, markup=False, verbose=False):
    logger_name = os.getenv("SKRIBA_LOGGER_NAME")

    if verbose:
        message = _add_verbose_info(message=message, color="yellow")

    logger = get_logger(logger_name=logger_name)
    logging.getLogger('numba').setLevel(logging.INFO)
    logger.warning(message, extra={"markup": markup})


def critical(message, markup=False, verbose=False):
    logger_name = os.getenv("SKRIBA_LOGGER_NAME")

    if verbose:
        message = _add_verbose_info(message=message, color="bold red blink")

    logger = get_logger(logger_name=logger_name)
    logging.getLogger('numba').setLevel(logging.INFO)
    logger.critical(message, extra={"markup": markup})


def error(message, markup=True, verbose=False):
    logger_name = os.getenv("SKRIBA_LOGGER_NAME")

    if verbose:
        message = _add_verbose_info(message=message, color="blink red")

    logger = get_logger(logger_name=logger_name)
    logging.getLogger('numba').setLevel(logging.INFO)
    logger.error(message, extra={"markup": markup})


class LoggingFormatter(logging.Formatter):
    function = " [ {function} ] ".format(function="%(funcName)s")
    verbose = " [ {exechain} ] ".format(
        exechain="%(filename)s:%(lineno)s : %(module)s.%(funcName)s")

    start_msg = "[ {time} ] ".format(time="%(asctime)s")
    middle_msg = "{level}".format(level="%(levelname)8s")
    execution_msg = " {name} [ {filename} ]: {exec_info}: ".format(
        name="%(name)10s",
        filename="%(filename)-20s",
        exec_info="%(callchain)-45s")

    FORMATS = {
        logging.DEBUG: start_msg + middle_msg + "  %(name)10s: " + verbose + " %(message)s",
        logging.INFO: start_msg + middle_msg + "  %(name)10s: " + function + " %(message)s",
        logging.INFO: start_msg + middle_msg + "  %(name)10s: " + function + " %(message)s",
        logging.ERROR: start_msg + middle_msg + "  %(name)10s: " + function + " %(message)s",
        logging.CRITICAL: start_msg + middle_msg + "  %(name)10s: " + function + " %(message)s",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(logger_name=None):
    from dask.distributed import get_worker

    if logger_name is None:
        logger_name = "SKRIBA-LOGGER"

    try:
        worker = get_worker()

    except ValueError:
        # Scheduler processes
        logger_dict = logging.Logger.manager.loggerDict
        if logger_name in logger_dict:
            logger = logging.getLogger(logger_name)
        else:
            # If main logger is not started using client function it defaults to printing to term.
            logging.basicConfig(
                level="INFO",
                format="%(message)s",
                datefmt="[%Y-%m-%d,%H:%M:%S]",
                handlers=[RichHandler(rich_tracebacks=True)]
            )

            logger = logging.getLogger(logger_name)

        return logger

    try:
        logger = worker.plugins['worker_logger'].logger

        return logger

    except Exception as error:
        print("Could not load worker logger: {}".format(error))
        print(worker.plugins.keys())

        return logging.getLogger()


def setup_logger(
        logger_name=None,
        log_to_term=False,
        log_to_file=True,
        log_file='LOGGER',
        log_level='INFO',
):
    """To set up as many loggers as you want"""
    if logger_name is None:
        logger_name = "SKRIBA-LOGGER"

    os.environ["SKRIBA_LOGGER_NAME"] = logger_name

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.getLevelName(log_level))
    logging.getLogger('numba').setLevel(logging.INFO)

    logger.handlers.clear()

    if log_to_term:
        logging.basicConfig(
            level=log_level,
            format="%(message)s ",
            datefmt="[%Y-%m-%d,%H:%M:%S]",
            handlers=[RichHandler(rich_tracebacks=True)]
        )
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.getLevelName(log_level))
        logging.getLogger('numba').setLevel(logging.INFO)

    if log_to_file:
        logger = logging.getLogger(logger_name)

        log_file = log_file + datetime.today().strftime('%Y%m%d_%H%M%S') + '.log'
        handler = logging.FileHandler(log_file)
        handler.setFormatter(LoggingFormatter())
        logging.getLogger('numba').setLevel(logging.INFO)
        logger.addHandler(handler)

    return logger


def get_worker_logger_name(logger_name=None):
    from dask.distributed import get_worker
    if logger_name is None:
        logger_name = "SKRIBA-LOGGER"

    return logger_name + '_' + str(get_worker().id)


def setup_worker_logger(
        logger_name,
        log_to_term,
        log_to_file,
        log_file,
        log_level,
        worker_id
):
    parallel_logger_name = logger_name + '_' + str(worker_id)

    if log_to_term:
        logging.basicConfig(
            level=log_level,
            format="%(message)s",
            datefmt="[%Y-%m-%d,%H:%M:%S]",
            handlers=[RichHandler(rich_tracebacks=True)]
        )
        logging.getLogger('numba').setLevel(logging.INFO)

    if log_to_file:
        log_file = log_file + '_' + str(worker_id) + '_' + datetime.today().strftime('%Y%m%d_%H%M%S') + '.log'
        handler = logging.FileHandler(log_file)
        handler.setFormatter(LoggingFormatter())

    logger = logging.getLogger(parallel_logger_name)

    logger.setLevel(logging.getLevelName(log_level))
    logging.getLogger('numba').setLevel(logging.INFO)

    return logger
