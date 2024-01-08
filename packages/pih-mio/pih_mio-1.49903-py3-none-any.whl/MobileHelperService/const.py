import importlib.util
import sys
from enum import Enum, auto

pih_is_exists = importlib.util.find_spec("pih") is not None
if not pih_is_exists:
    sys.path.append("//pih/facade")
from pih import A
from pih.tools import j, js, b
from pih.collection import IntStorageVariableHolder
from pih.rpc_collection import ServiceDescription
from shared.host_collection import HOSTS
from pih.console_api import SPLITTER

NAME: str = "MobileHelper"

DEFAULT_COUNT: int = 100
ADMIN_ALIAS: str = "admin"
COUNT_ALIAS: str = "count"

HOST = HOSTS.WS255

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Mobile helper service",
    host=HOST.NAME,
    commands=["send_mobile_helper_message"],
)

MOBILE_HELPER_USER_SETTINGS_NAME: str = "mobile_helper_user_settings"


class USER_SETTINGS_FLAGS:
    JOKELESS: int = 1
    TIME_TRACKINGLESS: int = 2
    VISITLESS: int = 4


POLIBASE_PERSON_PIN: str = "polibase_person_pin"
POLIBASE_PERSON_CARD_REGISTRY_FOLDER: str = "polibase_person_card_registry_folder"

USER_DATA_INPUT_TIMEOUT: int = 180

MOBILE_HELPER_USER_DATA_INPUT_TIMEOUT: IntStorageVariableHolder = (
    IntStorageVariableHolder(
        "MOBILE_HELPER_USER_DATA_INPUT_TIMEOUT",
        USER_DATA_INPUT_TIMEOUT,
    )
)


class InteraptionTypes:
    NEW_COMMAND: int = 1
    TIMEOUT: int = 2
    EXIT: int = 3
    BACK: int = 4


FROM_FILE_REDIRECT_SYMBOL: str = "<"
FILE_PATTERN_LIST: tuple[str] = (
    j(("file", SPLITTER)),
    FROM_FILE_REDIRECT_SYMBOL,
    "file=",
)
PARAMETER_PATTERN: str = r"\B(\$[\w+а-яА-Я]+)(:[\w \(\)\.\,а-яА-Я]+)?"

Groups = A.CT_AD.Groups

MAX_MESSAGE_LINE_LENGTH: int = 12


class MessageType(Enum):
    SEPARATE_ONCE: int = auto()
    SEPARATED: int = auto()


class COMMAND_KEYWORDS:
    PIH: tuple[str] = (A.root.NAME, A.root.NAME_ALT)
    EXIT: list[str] = ["exit", "выход"]
    BACK: list[str] = ["back", "назад"]
    FIND: list[str] = ["find", "поиск", "search", "найти"]
    CREATE: list[str] = ["create", "создать", "+"]
    CHECK: list[str] = ["check", "проверить"]
    ADD: list[str] = ["add", "добавить", "+"]
    PASSWORD: list[str] = ["password", "пароль"]
    USER: list[str] = ["user^s", "пользовател^ь"]
    POLIBASE: list[str] = ["polibase", "полибейс"]
    NOTES: list[str] = ["note^s", "заметк^и"]
    JOURNALS: list[str] = ["journal^s", "журнал^ы"]
    RUN: list[str] = ["run", "заметк^и"]
    PATIENT: list[str] = ["patient", "пациент"]
    DOCTOR: list[str] = ["doc^tor", "доктор", "врач"]
    JOKE: list[str] = ["joke", "шутка", "анекдот"]


YES_VARIANTS: str = ["1", "yes", "ok", "да"]
YES_LABEL: str = js(("", A.CT.VISUAL.BULLET, b("Да"), "- отправьте", A.O.get_number(1)))
NO_LABEL: str = js(("", A.CT.VISUAL.BULLET, b("Нет"), "- отправьте", A.O.get_number(0)))


class Flags(Enum):
    CYCLIC: int = 1
    ADDRESS: int = 2
    ALL: int = 4
    ADDRESS_AS_LINK: int = 8
    FORCED: int = 16
    SILENCE: int = 32
    HELP: int = 64
    SILENCE_NO: int = 128
    SILENCE_YES: int = 256
    CLI: int = 512
    ONLY_RESULT: int = 1024
    TEST: int = 2048


class FLAG_KEYWORDS:
    ALL_SYMBOL: str = "*"
    ADDRESS_SYMBOL: str = ">"
    LINK_SYMBOL: str = ADDRESS_SYMBOL * 2
    SILENCE: str = "_"
    ONLY_RESULT: str = SILENCE * 2


COMMAND_LINK_SYMBOL: str = "@"

FLAG_MAP: dict[str, Flags] = {
    "-0": Flags.CYCLIC,
    "-t": Flags.TEST,
    "to": Flags.ADDRESS,
    FLAG_KEYWORDS.ADDRESS_SYMBOL: Flags.ADDRESS,
    "!": Flags.FORCED,
    FLAG_KEYWORDS.SILENCE: Flags.SILENCE,
    "_0": Flags.SILENCE_NO,
    "_1": Flags.SILENCE_YES,
    FLAG_KEYWORDS.ALL_SYMBOL: Flags.ALL,
    FLAG_KEYWORDS.ONLY_RESULT: Flags.ONLY_RESULT,
    "all": Flags.ALL,
    "все": Flags.ALL,
    "всё": Flags.ALL,
    "link": Flags.ADDRESS_AS_LINK,
    FLAG_KEYWORDS.LINK_SYMBOL: Flags.ADDRESS_AS_LINK,
    "?": Flags.HELP,
}

ADMIN_GROUP: list[Groups] = [Groups.Admin]

COMMAND_NAME_BASE_DELEMITER: str = "^"

WORKSTATION_CHECK_WORD: str = "Workstation"

VERSION: str = "1.49903"
VERSION_STRING: str = js((VERSION, "👨‍💻"))
MODULE_NAME: str = j((A.root.NAME, "mio"), "-")
