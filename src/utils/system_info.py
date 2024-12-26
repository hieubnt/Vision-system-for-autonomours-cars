# Contain system information and constants

from pathlib import Path

PROJECT_ABS_ROOT = Path(__file__).parent.parent.parent.resolve()

LOGS_PATH = PROJECT_ABS_ROOT.joinpath('logs')

STORAGE_PATH = PROJECT_ABS_ROOT.joinpath('storage')

SUPPORTED_TOPICS = {""}

SUPPORTED_CONNECTORS = {""}

