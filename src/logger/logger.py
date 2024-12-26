from utils.singleton import SingletonMeta
from typing import Literal
from utils.system_info import PROJECT_ABS_ROOT
from pathlib import Path
from pydantic import validate_call
import datetime

class Logger(metaclass=SingletonMeta):
    @validate_call
    def __init__(self,
                 *,
                 init_message: str = None,
                 level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = 'INFO',
                 save_path: Path = PROJECT_ABS_ROOT.joinpath('logs'),
                 file_name: str = 'system_log.txt',
                 is_saved: bool = True,
                 is_print: bool = True,
                 message_format="[{}] - [{}]:\n{}",
                 mess_sep = f"{"="*10}[END]{"="*10}\n"
                 ):
        self._saved_path = save_path
        self._level = level
        self._file_name = file_name
        self._is_saved = is_saved
        self._is_print = is_print
        self._init_message = init_message
        self._message_format = message_format
        self._mess_sep = mess_sep

        if self._level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            raise ValueError(
                f'Invalid log level: {self._level}, supported levels are [DEBUG, INFO, WARNING, ERROR, CRITICAL].')

        if init_message:
            self.log(init_message)
        else:
            self.log("Logger is initialized.")

    def log(self,
            message: str,
            *,
            log_name: str = None,
            level: str = None,
            save_path: Path =None,
            file_name: str = None,
            is_saved: bool = None,
            is_print: bool = None,
            message_format: str = None,
            new_file: bool = False,

    ):
        level, save_path, file_name, is_saved, is_print, message_format=\
            self._load_default(level, save_path, file_name, is_saved, is_print, message_format)

        log_message = self._compose_log(message, log_name, level, message_format)

        if is_print:
            self._print_log(log_message)

        if is_saved:
            self._save_log(log_message, save_path, file_name, new_file)


    def _load_default(self, level, save_path, file_name, is_saved, is_print, message_format):
        if level is None:
            level = self._level
        if save_path is None:
            save_path = self._saved_path
        if file_name is None:
            file_name = self._file_name
        if is_saved is None:
            is_saved = self._is_saved
        if is_print is None:
            is_print = self._is_print
        if message_format is None:
            message_format = self._message_format
        return level, save_path, file_name, is_saved, is_print, message_format


    def _compose_log(self, message, log_name, level, message_format):

        date_time = datetime.datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
        if log_name :
            message = f"[{log_name}]: " + message
        log_message = message_format.format(level, date_time, message) + f"\n{self._mess_sep}"

        return log_message


    def _save_log(self, message: str,
                  save_path:Path,
                  file_name: str,
                  new_file:bool): # TODO
        pass


    def _print_log(self, message):
        print(message)

