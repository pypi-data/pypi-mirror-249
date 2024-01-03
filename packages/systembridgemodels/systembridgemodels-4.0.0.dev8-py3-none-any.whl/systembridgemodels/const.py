"""Model constants."""
# Model
from .keyboard_key import KeyboardKey
from .keyboard_text import KeyboardText
from .media_directories import MediaDirectories
from .media_files import MediaFile, MediaFiles
from .modules import ModulesData
from .modules.battery import Battery
from .modules.cpu import CPU
from .modules.disks import Disks
from .modules.displays import Displays
from .modules.gpus import GPU
from .modules.media import Media
from .modules.memory import Memory
from .modules.networks import Networks
from .modules.processes import Processes
from .modules.sensors import Sensors
from .modules.system import System
from .notification import Notification
from .open_path import OpenPath
from .open_url import OpenUrl
from .response import Response

MODEL_BATTERY = "battery"
MODEL_CPU = "cpu"
MODEL_DATA = "data"
MODEL_DISKS = "disks"
MODEL_DISPLAYS = "displays"
MODEL_GENERIC = "generic"
MODEL_GPU = "gpu"
MODEL_KEYBOARD_KEY = "keyboard_key"
MODEL_KEYBOARD_TEXT = "keyboard_text"
MODEL_MEDIA = "media"
MODEL_MEDIA_DIRECTORIES = "media_directories"
MODEL_MEDIA_FILE = "media_file"
MODEL_MEDIA_FILES = "media_files"
MODEL_MEMORY = "memory"
MODEL_NETWORKS = "networks"
MODEL_NOTIFICATION = "notification"
MODEL_OPEN_PATH = "open_path"
MODEL_OPEN_URL = "open_url"
MODEL_PROCESSES = "processes"
MODEL_RESPONSE = "response"
MODEL_SECRETS = "secrets"
MODEL_SENSORS = "sensors"
MODEL_SETTINGS = "settings"
MODEL_SYSTEM = "system"

MODEL_MAP = {
    MODEL_BATTERY: Battery,
    MODEL_CPU: CPU,
    MODEL_DATA: ModulesData,
    MODEL_DISKS: Disks,
    MODEL_DISPLAYS: Displays,
    MODEL_GPU: GPU,
    MODEL_KEYBOARD_KEY: KeyboardKey,
    MODEL_KEYBOARD_TEXT: KeyboardText,
    MODEL_MEDIA_DIRECTORIES: MediaDirectories,
    MODEL_MEDIA_FILE: MediaFile,
    MODEL_MEDIA_FILES: MediaFiles,
    MODEL_MEDIA: Media,
    MODEL_MEMORY: Memory,
    MODEL_NETWORKS: Networks,
    MODEL_NOTIFICATION: Notification,
    MODEL_OPEN_PATH: OpenPath,
    MODEL_OPEN_URL: OpenUrl,
    MODEL_PROCESSES: Processes,
    MODEL_RESPONSE: Response,
    MODEL_SENSORS: Sensors,
    MODEL_SYSTEM: System,
}
