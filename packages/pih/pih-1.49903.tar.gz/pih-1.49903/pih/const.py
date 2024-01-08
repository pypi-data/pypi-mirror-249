﻿from enum import Enum, auto
import os

from pih.collection import (
    FieldItem,
    FieldItemList,
    EventDescription,
    ParamItem,
    PasswordSettings,
    StorageVariableHolder,
    ResourceDescription,
    SiteResourceDescription,
    PolibaseDocumentDescription,
    MedicalDirectionDescription,
    ActionDescription,
    IntStorageVariableHolder,
    BoolStorageVariableHolder,
    TimeStorageVariableHolder,
    DateListStorageVariableHolder,
    FloatStorageVariableHolder,
    MinIntStorageVariableHolder,
    IntListStorageVariableHolder,
    OrderedNameCaptionDescription,
    IconedOrderedNameCaptionDescription,
    StringListStorageVariableHolder,
)
from pih.rpc_collection import ServiceDescription, ServiceInformationBase
from pih.rpc_const import ServiceCommands


class DATA:
    # deprecated
    class EXTRACTOR:
        USER_NAME_FULL: str = "user_name_full"
        USER_NAME: str = "user_name"
        AS_IS: str = "as_is"

    class FORMATTER(Enum):
        MY_DATETIME: str = "my_datetime"
        MY_DATE: str = "my_date"
        CHILLER_INDICATIONS_VALUE_INDICATORS: str = (
            "chiller_indications_value_indicators"
        )
        CHILLER_FILTER_COUNT: str = "chiller_filter_count"


class INDICATIONS:
    class CHILLER:
        ACTUAL_VALUES_TIME_DELTA_IN_MINUTES: int = 5

        INDICATOR_NAME: list[str] = [
            "Активный сигнал тревоги",
            "Работает нагреватель",
            "Замораживание включено",
            "Работает вентилятор конденсатора",
            "Работает насос/вытяжной вентилятор",
            "Работает компрессор",
        ]

        INDICATOR_EMPTY_DISPLAY: int = -1

    class MRI:
        # hours
        PERIOD: int = 2


class USER_PROPERTIES:
    TELEPHONE_NUMBER: str = "telephoneNumber"
    EMAIL: str = "mail"
    DN: str = "distinguishedName"
    USER_ACCOUNT_CONTROL: str = "userAccountControl"
    LOGIN: str = "samAccountName"
    DESCRIPTION: str = "description"
    PASSWORD: str = "password"
    USER_STATUS: str = "userStatus"
    NAME: str = "name"

ARGUMENT_PREFIX: str = "--"
ISOLATED_ARG_NAME: str = "isolated"

class BARCODE:
    CODE128: str = "code128"
    I25: str = "i25"


class AD:
    SPLITTER: str = "."
    SEARCH_ATTRIBUTES: list[str] = [USER_PROPERTIES.LOGIN, USER_PROPERTIES.NAME]
    SEARCH_ATTRIBUTE_DEFAULT: str = SEARCH_ATTRIBUTES[0]
    DOMAIN_NAME: str = "fmv"
    DOMAIN_ALIAS: str = "pih"
    DOMAIN_SUFFIX: str = "lan"
    DOMAIN_DNS: str = SPLITTER.join([DOMAIN_NAME, DOMAIN_SUFFIX])
    DOMAIN_MAIN: str = DOMAIN_DNS
    USER_HOME_FOLDER_DISK: str = "U:"
    OU: str = "OU="
    ROOT_CONTAINER_DN: str = f"{OU}Unit,DC={DOMAIN_NAME},DC={DOMAIN_SUFFIX}"
    WORKSTATIONS_CONTAINER_DN: str = f"{OU}Workstations,{ROOT_CONTAINER_DN}"
    SERVERS_CONTAINER_DN: str = f"{OU}Servers,{ROOT_CONTAINER_DN}"
    USERS_CONTAINER_DN_SUFFIX: str = f"Users,{ROOT_CONTAINER_DN}"
    ACTIVE_USERS_CONTAINER_DN: str = f"{OU}{USERS_CONTAINER_DN_SUFFIX}"
    INACTIVE_USERS_CONTAINER_DN: str = f"{OU}dead{USERS_CONTAINER_DN_SUFFIX}"
    PATH_ROOT: str = f"//{DOMAIN_MAIN}"
    SEARCH_ALL_PATTERN: str = "*"
    GROUP_CONTAINER_DN: str = f"{OU}Groups,{ROOT_CONTAINER_DN}"
    JOB_POSITION_CONTAINER_DN: str = f"{OU}Job positions,{GROUP_CONTAINER_DN}"
    LOCATION_JOINER: str = ":"
    TEMPLATED_USER_SERACH_TEMPLATE: str = "_*_"
    PROPERTY_ROOT_DN: str = f"{OU}Property,{GROUP_CONTAINER_DN}"
    PROPERTY_WS_DN: str = f"{OU}WS,{PROPERTY_ROOT_DN}"

    USER_ACCOUNT_CONTROL: list[str] = [
        "SCRIPT",
        "ACCOUNTDISABLE",
        "RESERVED",
        "HOMEDIR_REQUIRED",
        "LOCKOUT",
        "PASSWD_NOTREQD",
        "PASSWD_CANT_CHANGE",
        "ENCRYPTED_TEXT_PWD_ALLOWED",
        "TEMP_DUPLICATE_ACCOUNT",
        "NORMAL_ACCOUNT",
        "RESERVED",
        "INTERDOMAIN_TRUST_ACCOUNT",
        "WORKSTATION_TRUST_ACCOUNT",
        "SERVER_TRUST_ACCOUNT",
        "RESERVED",
        "RESERVED",
        "DONT_EXPIRE_PASSWORD",
        "MNS_LOGON_ACCOUNT",
        "SMARTCARD_REQUIRED",
        "TRUSTED_FOR_DELEGATION",
        "NOT_DELEGATED",
        "USE_DES_KEY_ONLY",
        "DONT_REQ_PREAUTH",
        "PASSWORD_EXPIRED",
        "TRUSTED_TO_AUTH_FOR_DELEGATION",
        "RESERVED",
        "PARTIAL_SECRETS_ACCOUNT",
    ]

    WORKSTATION_PREFIX_LIST: list[str] = ["ws-", "nb-", "fmvulianna"]

    class USER:
        MARKETER_ADMINISTRATOR: str = "marketer_admin"
        CALL_CENTRE_ADMINISTRATOR: str = "callCentreAdmin"
        REGISTRATION_AND_CALL: str = "reg_and_call"
        CONTROL_SERVICE: str = "cctv"
        INDICATIONS_ALL: str = "indications_all"
        ADMINISTRATOR: str = "Administrator"

    class JobPositions(Enum):
        HR: int = auto()
        IT: int = auto()
        CALL_CENTRE: int = auto()
        REGISTRATOR: int = auto()
        RD: int = auto()
        MARKETER: int = auto()

    class Groups(Enum):
        TimeTrackingReport: int = auto()
        Inventory: int = auto()
        Polibase: int = auto()
        Admin: int = auto()
        ServiceAdmin: int = auto()
        CardRegistry: int = auto()
        PolibaseUsers: int = auto()
        RD: int = auto()
        IndicationWatcher: int = auto()
        FunctionalDiagnostics: int = auto()

    class WSProperies(Enum):
        Watchable: int = 1
        Shutdownable: int = 2
        Rebootable: int = 4
        DiskReportable: int = 8


class FONT:
    FOR_PDF: str = "DejaVuSerif"


class FILE:
    class EXTENSION:
        EXCEL_OLD: str = "xls"
        EXCEL_NEW: str = "xlsx"
        JPEG: str = "jpeg"
        JPG: str = "jpg"
        PNG: str = "png"
        PDF: str = "pdf"
        TXT: str = "txt"
        PYTHON: str = "py"
        BASE64: str = "base64"
        EXE: str = "exe"
        ARCHIVE: str = "zip"
        TRUE_TYPE_FONT: str = "ttf"


class HOSTS:
    class SERVICE_CONTROL_WORKSTATION:
        NAME: str = "ws-207"
        IP: str = "192.168.254.51"

    class ORION:
        NAME: str = "orion"
        IP: str = "192.168.100.90"

    class SERVICES:
        NAME: str = "svshost"
        ALIAS: str = "zabbix"
        IP: str = "192.168.100.95"

        LOGIN_ALIAS: str = "SERVICES_LOGIN"
        PASSWORD_ALIAS: str = "SERVICES_PASSWORD"

    class BACKUP_WORKER:
        NAME: str = "backup_worker"
        ALIAS: str = NAME
        IP: str = "192.168.100.11"

    class WS255:
        NAME: str = "ws-255"
        IP: str = "192.168.100.138"

    class WS816:
        NAME: str = "ws-816"
        IP: str = "192.168.254.81"

    class WS735:
        NAME: str = "ws-735"
        ALIAS: str = "shared_disk_owner"
        IP: str = "192.168.254.102"

    class DEVELOPER(WS735):
        pass

    class DC1:
        NAME: str = "fmvdc1"
        ALIAS: str = "dc1"
        IP: str = "192.168.100.4"

    class DC2:
        NAME: str = "fmvdc2"
        ALIAS: str = "dc2"
        IP: str = "192.168.100.23"

    class PRINTER_SERVER:
        NAME: str = "fmvdc1"

    class POLIBASE1:
        # shit - cause polibase is not accessable
        NAME: str = "polibase1.fmv.lan"
        ALIAS: str = "polibase1"
        IP: str = "192.168.100.3"

    class POLIBASE2:
        NAME: str = "polibase2.fmv.lan"
        ALIAS: str = "polibase2"
        IP: str = "192.168.110.3"

    class POLIBASE(POLIBASE1):
        ALIAS: str = "polibase"

    class POLIBASE_TEST(POLIBASE2):
        ALIAS: str = "polibase_test"

    class _1C:
        NAME: str = "1c"
        ALIAS: str = "1c"
        IP: str = "192.168.100.22"

    class NAS:
        NAME: str = "nas"
        ALIAS: str = "nas"
        IP: str = "192.168.100.200"

    class PACS_ARCHVE:
        NAME: str = "pacs_archive"
        ALIAS: str = "ea_archive"
        IP: str = "192.168.110.108"


class URLS:
    PYPI: str = "https://pypi.python.org/pypi/pih/json"


class EmailVerificationMethods(Enum):
    NORMAL: int = auto()
    ABSTRACT_API: int = auto()
    DEFAULT: int = NORMAL


class ROBOCOPY:
    ERROR_CODE_START: int = 8

    STATUS_CODE: dict[int, str] = {
        0: "No errors occurred, and no copying was done. The source and destination directory trees are completely synchronized.",
        1: "One or more files were copied successfully (that is, new files have arrived).",
        2: "Some Extra files or directories were detected. No files were copied Examine the output log for details.",
        4: "Some Mismatched files or directories were detected. Examine the output log. Housekeeping might be required.",
        8: "Some files or directories could not be copied (copy errors occurred and the retry limit was exceeded). Check these errors further.",
        16: "Serious error. Robocopy did not copy any files. Either a usage error or an error due to insufficient access privileges on the source or destination directories.",
        3: "Some files were copied. Additional files were present. No failure was encountered.",
        5: "Some files were copied. Some files were mismatched. No failure was encountered.",
        6: "Additional files and mismatched files exist. No files were copied and no failures were encountered. This means that the files already exist in the destination directory",
        7: "Files were copied, a file mismatch was present, and additional files were present.",
    }


class WINDOWS:
    class ENVIROMENT_VARIABLES:
        PATH: str = "PATH"

    ENVIROMENT_COMMAND: str = "$Env"

    class CHARSETS:
        ALTERNATIVE: str = "CP866"

    class SERVICES:
        WIA: str = "stisvc"  # Обеспечивает службы получения изображений со сканеров и цифровых камер
        TASK_SCHEDULER: str = "schtasks"

    class PROCESSES:
        POWER_SHELL_REMOTE_SESSION: str = "wsmprovhost.exe"

    class PORTS:
        SMB: int = 445


class LINK:
    ADMINISTRATOR_PASSWORD: str = "ADMINISTRATOR_PASSWORD"
    ADMINISTRATOR_LOGIN: str = "ADMINISTRATOR_LOGIN"

    DEVELOPER_LOGIN: str = "DEVELOPER_LOGIN"
    DEVELOPER_PASSWORD: str = "DEVELOPER_PASSWORD"

    USER_LOGIN: str = "USER_LOGIN"
    USER_PASSWORD: str = "USER_PASSWORD"

    SERVICES_USER_LOGIN: str = "SERVICES_LOGIN"
    SERVICES_USER_PASSWORD: str = "SERVICES_PASSWORD"

    DATABASE_ADMINISTRATOR_LOGIN: str = "DATABASE_ADMINISTRATOR_LOGIN"
    DATABASE_ADMINISTRATOR_PASSWORD: str = "DATABASE_ADMINISTRATOR_PASSWORD"


class CONST:
    class NOTES:
        FILE_SECTION: str = "Мобильные файлы"
        JOURNAL_SECTION: str = "Журналы"

    # in seconds
    HEART_BEAT_PERIOD: int = 60

    NEW_LINE: str = "\n"

    class TEST:
        WORKSTATION_MAME: str = HOSTS.DEVELOPER.NAME
        USER: str | None = "nak"
        EMAIL_ADDRESS: str | None = "nak@pacifichosp.com"
        PIN: int = 100310
        NAME: str = "test"

    GROUP_PREFIX: str = "group:"

    SITE_PROTOCOL: str = "https://"
    UNTRUST_SITE_PROTOCOL: str = "http://"

    SITE_NAME: str = "pacifichosp"
    SITE_ADDRESS: str = f"{SITE_NAME}.com"
    EMAIL_SERVER_ADDRESS: str = f"mail.{SITE_ADDRESS}"
    OUTGOING_EMAIL_SERVER_PORT: int = 587
    INCOMING_EMAIL_SERVER_PORT: int = 993
    RECEPTION_EMAIL_LOGIN: str = f"reception.{SITE_NAME}"

    WIKI_SITE_NAME: str = f"wiki"
    WIKI_SITE_ADDRESS: str = WIKI_SITE_NAME
    OMS_SITE_NAME: str = "oms"
    OMS_SITE_ADDRESS: str = OMS_SITE_NAME
    API_SITE_ADDRESS: str = f"api.{SITE_ADDRESS}"
    BITRIX_SITE_URL: str = "bitrix.cmrt.ru"

    INTERNATIONAL_TELEPHONE_NUMBER_PREFIX: str = "7"
    TELEPHONE_NUMBER_PREFIX: str = f"+{INTERNATIONAL_TELEPHONE_NUMBER_PREFIX}"
    INTERNAL_TELEPHONE_NUMBER_PREFIX: str = "тел."

    DATETIME_SPLITTER: str = "T"
    HOUR_TIME_FORMAT: str = "%H"
    SECONDLESS_TIME_FORMAT: str = f"{HOUR_TIME_FORMAT}:%M"
    SECOND_ZEROS_TIME_FORMAT: str = f"{SECONDLESS_TIME_FORMAT}:00"
    TIME_FORMAT: str = f"{SECONDLESS_TIME_FORMAT}:%S"
    DAY_FORMAT: str = "%d"

    ISO_DATE_FORMAT: str = f"%Y-%m-{DAY_FORMAT}"
    ISO_DATETIME_FORMAT: str = (
        f"{ISO_DATE_FORMAT}{DATETIME_SPLITTER}{SECOND_ZEROS_TIME_FORMAT}"
    )

    DATE_PART_DELIMITER: str = "."
    YEARLESS_DATE_FORMAT: str = f"{DAY_FORMAT}{DATE_PART_DELIMITER}%m"
    DATE_FORMAT: str = f"{YEARLESS_DATE_FORMAT}{DATE_PART_DELIMITER}%Y"
    DAYLESS_DATE_FORMAT: str = f"%m{DATE_PART_DELIMITER}%Y"

    DATETIME_ONLY_HOUR_FORMAT: str = f"{DATE_FORMAT} {HOUR_TIME_FORMAT}"
    DATETIME_SECOND_ZEROS_FORMAT: str = f"{DATE_FORMAT} {SECOND_ZEROS_TIME_FORMAT}"
    DATETIME_FORMAT: str = f"{DATE_FORMAT} {TIME_FORMAT}"

    class CACHE:
        class TTL:
            # in seconds
            WORKSTATIONS: int = 60
            USERS: int = 300

    class ERROR:
        class WAPPI:
            PROFILE_NOT_PAID: int = 402

    class TIME_TRACKING:
        REPORT_DAY_PERIOD_DEFAULT: int = 15

    class MESSAGE:
        class WHATSAPP:
            SITE_NAME: str = "https://wa.me/"
            SEND_MESSAGE_TO_TEMPLATE: str = SITE_NAME + "{}?text={}"
            GROUP_SUFFIX: str = "@g.us"

            class GROUP(Enum):
                PIH_CLI: str = "120363163438805316@g.us"
                REGISTRATOR_CLI: str = "120363212130686795@g.us"
                RD: str = "79146947050-1595848245@g.us"
                MAIN: str = "79644300470-1447044803@g.us"
                EMAIL_CONTROL: str = "120363159605715569@g.us"
                CT_INDICATIONS: str = "120363084280723039@g.us"
                DOCUMENTS_WORK_STACK: str = "120363115241877592@g.us"
                REGISTRATION_AND_CALL: str = "79242332784-1447983812@g.us"
                DOCUMENTS_WORK_STACK_TEST: str = "120363128816931482@g.us"
                CONTROL_SERVICE_INDICATIONS: str = "120363159210756301@g.us"

            class WAPPI:
                PROFILE_SUFFIX: str = "profile_id="
                URL_API: str = "https://wappi.pro/api"
                URL_API_SYNC: str = f"{URL_API}/sync"
                URL_MESSAGE: str = f"{URL_API_SYNC}/message"
                URL_SEND_MESSAGE: str = f"{URL_MESSAGE}/send?{PROFILE_SUFFIX}"
                URL_SEND_VIDEO: str = f"{URL_MESSAGE}/video/send?{PROFILE_SUFFIX}"
                URL_SEND_IMAGE: str = f"{URL_MESSAGE}/img/send?{PROFILE_SUFFIX}"
                URL_SEND_DOCUMENT: str = f"{URL_MESSAGE}/document/send?{PROFILE_SUFFIX}"
                URL_SEND_LIST_MESSAGE: str = f"{URL_MESSAGE}/list/send?{PROFILE_SUFFIX}"
                URL_SEND_BUTTONS_MESSAGE: str = (
                    f"{URL_MESSAGE}/buttons/send?{PROFILE_SUFFIX}"
                )
                URL_GET_MESSAGES: str = f"{URL_MESSAGE}s/get?{PROFILE_SUFFIX}"
                URL_GET_STATUS: str = f"{URL_API_SYNC}/get/status?{PROFILE_SUFFIX}"
                CONTACT_SUFFIX: str = "@c.us"

                class Profiles(Enum):
                    IT: str = "e6706eaf-ae17"
                    CALL_CENTRE: str = "285c71a4-05f7"
                    MARKETER: str = "c31db01c-b6d6"
                    DEFAULT: str = CALL_CENTRE

                AUTHORIZATION: str = "6b356d3f53124af3078707163fdaebca3580dc38"

    class PYTHON:
        EXECUTOR_ALIAS: str = "py"
        EXECUTOR: str = "python"
        EXECUTOR3: str = "python3"
        PYPI: str = "pip"
        SEARCH_PATTERN: str = "\\Python\\Python"

        class COMMAND:
            VERSION: str = "--version"
            INSTALL: str = "install"
            SHOW: str = "show"

    class SERVICE:
        NAME: str = "service"

    class FACADE:
        NAME: str = "facade"
        SERVICE_FOLDER_SUFFIX: str = "Service"

    class VALENTA:
        PROCESS_NAME: str = "Vlwin"

    class POWERSHELL:
        NAME: str = "powershell"

    class PSTOOLS:
        NAME: str = "pstools"
        PS_EXECUTOR: str = "psexec"
        PS_KILL_EXECUTOR: str = "pskill"
        PS_PING: str = "psping"

        COMMAND_LIST: list[str] = [
            PS_KILL_EXECUTOR,
            "psfile",
            "psgetsid",
            "psinfo",
            "pslist",
            "psloggedon",
            "psloglist",
            "pspasswd",
            PS_PING,
            "psservice",
            "psshutdown",
            "pssuspend",
        ]

        NO_BANNER: str = "-nobanner"
        ACCEPTEULA: str = "-accepteula"

    class MSG:
        NAME: str = "msg"
        EXECUTOR: str = NAME

    class BARCODE_READER:
        PREFIX: str = "("
        SUFFIX: str = ")"

    class NAME_POLICY:
        PARTS_LIST_MIN_LENGTH: int = 3
        PART_ITEM_MIN_LENGTH: int = 3

    class RPC:
        PING_COMMAND: str = "__ping__"
        EVENT_COMMAND: str = "__event__"
        SUBSCRIBE_COMMAND: str = "__subscribe__"

        @staticmethod
        def PORT(add: int = 0) -> int:
            return 50051 + add

        TIMEOUT: int | None = None
        TIMEOUT_FOR_PING: int = 20
        LONG_OPERATION_DURATION: int | None = None

    HOST = HOSTS()

    class CARD_REGISTRY:
        PLACE_NAME: dict[str, str] = {"Т": "Приёмное отделение", "П": "Поликлиника"}
        PLACE_CARD_HOLDER_MAPPER: dict[str, str] = {"Т": "М-Я", "П": "А-Л"}
        MAX_CARD_PER_FOLDER: int = 60
        SUITABLE_FOLDER_NAME_SYMBOL: tuple[str] = ("!", " ")

    class POLIBASE:
        NAME: str = "Polibase"
        SERVICE_NAME: str = "OracleServiceORCL"
        PROCESS_NAME: str = "Polibase ODAC"

        DBMS_OUTPUT: str = "dbms_output"

        DOCTEMPLETS_LAST_OPERATED_ID: str = "doctemplete_last_operated_id"

        PRERECORDING_PIN: int = 10
        PERSON_MINIMAL_PIN: int = 100
        RESERVED_TIME_A_PIN: int = 5
        RESERVED_TIME_B_PIN: int = 6
        RESERVED_TIME_C_PIN: int = 7
        EMPTY_VALUE: str = "xxxxx"
        EMPTY_EMAIL_VARIANTS: list[str] = ["нет", "-", "no"]
        TELEPHONE_NUMBER_COUNT: int = 4

        CARD_REGISTRY_FOLDER_QR_CODE_COUNT: int = 2

        CARD_REGISTRY_FOLDER_NAME_CHECK_PATTERN: list[str] = ["п", "т"]

        # 145 - Средний Медицинский Персонал
        # 300 - Реанимация
        # 361 - Операционная блок
        # 421 - СМП
        # 221 -
        # 229 -
        CABINET_NUMBER_EXCLUDED_FROM_VISIT_RESULT: list[int] = [
            145,
            221,
            229,
            300,
            361,
            421,
        ]

        # 147 - УЗИ
        # 201 - ЭНДОСКОПИЯ
        # 202 - МРТ
        # 203 - КТ

        class AppointmentServiceGroupId(Enum):
            ULTRASOUND: int = 147
            ENDOSCOPY: int = 201
            MRI: int = 202
            CT: int = 203

        APPOINTMENT_SERVICE_GROUP_NAME: dict[Enum, str] = {
            AppointmentServiceGroupId.ULTRASOUND: "ультразвуковое исследование",
            AppointmentServiceGroupId.ENDOSCOPY: "эндоспопичекое исследование",
            AppointmentServiceGroupId.MRI: "МРТ исследование",
            AppointmentServiceGroupId.CT: "рентген исследование",
        }

        STATUS_EXCLUDE_FROM_VISIT_RESULT: list[int] = [63]

        ###

        TELEGRAM_BOT_URL: str = "https://t.me/pacifichospital_bot"

        REVIEW_ACTION_URL: str = "https://forms.gle/qriwujnAknYXga4eA"
        REVIEW_ACTION_URL_FOR_INPATIENT: str = "https://forms.gle/ULRFv4aujQQsrvFG7"

        PERSON_VISIT_NOTIFICATION_TEXT_CANCEL_OR_REPLACE_RECEPTION: str = "\nВ случае отмены или переноса записи обязательно свяжитесь с нами по номеру +7(423)2790790.\n С уважением, больница Пасифик Интернешнл Хоспитал."

        PERSON_VISIT_NOTIFICATION_HEADER: str = "_Здравствуйте, это *автоматическая* рассылка от Пасифик Интернешнл Хоспитал (Falck)._\n\n"

        SEND_TELEGRAM_BOT_TEXT: str = (
            "\n\nОтправляем ссылку на наш telegram-бот с *важной информацией* (подготовка к исследованиям, врачи, услуги, схема проезда и др.):\n"
            + TELEGRAM_BOT_URL
        )

        ASK_TO_SEND_TELEGRAM_BOT_URL_TEXT: str = "\n\nОтправьте в ответ любое сообщение и мы пришлём Вам ссылку на наш telegram-бот с *важной информацией* (подготовка к исследованиям, врачи, услуги, схема проезда и др.)"

        PERSON_VISIT_NOTIFICATION_APPOINTMENT_INFORMATION: str = "*{name}*, Вы записаны в Пасифик Интернешнл Хоспитал на {appointment_information}."

        HAVE_A_GOOD_DAY: str = "\n\nХорошего дня!"

        PERSON_VISIT_GREETING_NOTIFICATION_TEXT_BASE: str = (
            PERSON_VISIT_NOTIFICATION_HEADER
            + PERSON_VISIT_NOTIFICATION_APPOINTMENT_INFORMATION
        )

        PERSON_VISIT_GREETING_NOTIFICATION_TEXT_WITHOUT_TEXT: str = (
            PERSON_VISIT_GREETING_NOTIFICATION_TEXT_BASE
            + ASK_TO_SEND_TELEGRAM_BOT_URL_TEXT
        )

        PERSON_VISIT_GREETING_NOTIFICATION_TEXT_FOR_CONFIRMED_NOTIFICATION: str = (
            PERSON_VISIT_GREETING_NOTIFICATION_TEXT_BASE
        )

        PERSON_VISIT_NOTIFICATION_WITH_TIME_TEXT: str = (
            "\n\nВаш приём запланирован на {day_string} {month_string} в {hour_string}{minute_string}."
            + PERSON_VISIT_NOTIFICATION_TEXT_CANCEL_OR_REPLACE_RECEPTION
        )

        ###

        PERSON_REVIEW_NOTIFICATION_TEXT_BASE: str = "Добрый день, *{name}*!\n\nМеня зовут Анна, я директор отдела качества *Pacific International Hospital* (ранее Falck).\n\nВы недавно обращались в нашу больницу. Будем очень признательны, если в целях улучшения качества обслуживания вы ответите на несколько вопросов"

        SEND_REVIEW_ACTION_URL_TEXT: str = (
            ", перейдя по ссылке ниже:\n" + REVIEW_ACTION_URL
        )

        PERSON_REVIEW_NOTIFICATION_TEXT_FOR_CONFIRMED_NOTIFICATION: str = (
            PERSON_REVIEW_NOTIFICATION_TEXT_BASE + SEND_REVIEW_ACTION_URL_TEXT
        )

        ASK_TO_SEND_REVIEW_ACTION_TEXT: str = ". Согласны ли Вы пройти опрос?"

        PERSON_REVIEW_NOTIFICATION_TEXT: str = (
            PERSON_REVIEW_NOTIFICATION_TEXT_BASE + ASK_TO_SEND_REVIEW_ACTION_TEXT
        )

        YES_ANSWER: list[str] = [
            "да",
            "согласен",
            "согласна",
            "ok",
            "ок",
            "yes",
            "хорошо",
            "ага",
        ]

        NO_ANSWER: list[str] = ["нет", "не согласен", "не согласна", "no", "занят"]

        TAKE_TELEGRAM_BOT_URL_TEXT: str = "*{name}*, отправляем Вам ссылку:\n"

        PERSONLESS_TAKE_TELEGRAM_BOT_URL_TEXT: str = "Отправляем Вам ссылку:\n"

        TAKE_REVIEW_ACTION_URL_TEXT: str = (
            "*{name}*, отправляем Вам ссылку для прохождения опроса:"
        )

        DATE_FORMAT: str = "%d.%m.%Y"
        DATE_IS_NOT_SET_YEAR: int = 1899
        DATETIME_FORMAT: str = "dd.mm.yyyy hh24:mi:ss"

        INSTANCE: str = "orcl.fmv.lan"
        USER: str = "POLIBASE"
        PASSWORD: str = "POLIBASE"

        DB_DATETIME_FORMAT: str = "%d-%m-%Y-%H-%M-00"

        class BARCODE:
            NOT_FOUND: str = "_@barcode_not_found@_"

            class PERSON:
                IMAGE_FORMAT: str = FILE.EXTENSION.JPEG

            class PERSON_CARD_REGISTRY_FOLDER:
                IMAGE_FORMAT: str = FILE.EXTENSION.PNG

            ACTUAL_FORMAT: str = BARCODE.CODE128
            OLD_FORMAT: str = BARCODE.I25

            SUPPORT_FORMATS: list[str] = [ACTUAL_FORMAT, OLD_FORMAT]

            NEW_PREFIX: str = "new_"

            @staticmethod
            def get_file_name(pin: int, with_extension: bool = False) -> str:
                extension: str = (
                    f".{CONST.POLIBASE.BARCODE.PERSON.IMAGE_FORMAT}"
                    if with_extension
                    else ""
                )
                return "".join((CONST.POLIBASE.BARCODE.NEW_PREFIX, str(pin), extension))

        class DocumentDescriptions(Enum):
            ABPM_JOURNAL: PolibaseDocumentDescription = PolibaseDocumentDescription(
                "Дневник суточного мониторинга АД", 70, 70, 80
            )
            HOLTER_JOURNAL: PolibaseDocumentDescription = PolibaseDocumentDescription(
                "Дневник суточного мониторинга ЭКГ", 70, 70, 80
            )
            PATIENT_CARD_AMBULATORY: PolibaseDocumentDescription = PolibaseDocumentDescription(
                "Медицинская карта\nпациента, получившего медицинскую помощь\nв амбулаторных условиях",
                70,
                120,
                120,
            )
            PROCESSING_PRESONAL_DATA_CONSENT: PolibaseDocumentDescription = (
                PolibaseDocumentDescription(
                    "согласие\nпациента на обработку персональных данных",
                    70,
                    70,
                    120,
                    1,
                )
            )
            INFORMED_VOLUNTARY_MEDICAL_INVENTION_CONSENT: PolibaseDocumentDescription = PolibaseDocumentDescription(
                "информированное добровольное согласие\nна медицинское вмешательство",
                70,
                70,
                120,
                1,
            )
            INFORMED_VOLUNTARY_MEDICAL_INVENTION_CONSENT_SPECIFIC: PolibaseDocumentDescription = PolibaseDocumentDescription(
                "информированное добровольное согласие на виды медицинских\nвмешательств, включенные в перечень определенных видов\nмедицинских вмешательств, на которые граждане дают\nинформированное добровольное согласие при выборе врача и\nмедицинской организации для получения первичной медико-\nсанитарной помощи",
                70,
                70,
                280,
                2,
            )

            @staticmethod
            def sorted() -> list:
                return sorted(
                    CONST.POLIBASE.DocumentDescriptions,
                    key=lambda item: item.value.title_height,
                    reverse=True,
                )

    class VISUAL:
        YES: str = "✅"
        NO: str = "❌"
        WARNING: str = "⚠️"
        WAIT: str = "⏳"
        NOTIFICATION: str = "🔔"
        ROBOT: str = "🤖"
        GOOD: str = YES
        ERROR: str = NO
        ORANGE_ROMB: str = "🔸"
        TASK: str = "✳️"
        EYE: str = "👁️"
        HAND_INDICATE: str = "👉"
        INFORMATION: str = "ℹ️"

        NUMBER_SYMBOLS: list[str] = [
            "0️⃣",
            "1️⃣",
            "2️⃣",
            "3️⃣",
            "4️⃣",
            "5️⃣",
            "6️⃣",
            "7️⃣",
            "8️⃣",
            "9️⃣",
            "🔟",
        ]

        TEMPERATURE_SYMBOL: str = "°C"

        ARROW: str = "➜"

        BULLET: str = "•"


class MATERIALIZED_RESOURCES:
    NAME: str = "MATERIALIZED_RESOURCES"
    ALIAS: str = "MR"

    class TYPES(Enum):
        CHILLER_FILTER: MinIntStorageVariableHolder = MinIntStorageVariableHolder(
            "CHF", description="Фильтры для чиллера", min_value=2
        )

        OPTICAL_DISK_IN_STOCK: MinIntStorageVariableHolder = (
            MinIntStorageVariableHolder(
                "ODS",
                description="Оптические диски для записи исследований на складе",
                min_value=50,
            )
        )

        OPTICAL_DISK_IN_USE: MinIntStorageVariableHolder = MinIntStorageVariableHolder(
            "ODU",
            description="Оптические диски для записи исследований в пользовании",
            min_value=10,
        )


class RESOURCES:
    class DESCRIPTIONS:
        INTERNET: ResourceDescription = ResourceDescription(
            "77.88.55.242", "Интернет соединение"
        )

        VPN_PACS_SPB: ResourceDescription = ResourceDescription(
            "192.168.5.3", "VPN соединение для PACS SPB", (2, 100, 5)
        )

        PACS_SPB: ResourceDescription = ResourceDescription(
            "10.76.12.124:4242", "Соединение PACS SPB", (2, 100, 5)
        )

        POLIBASE: ResourceDescription = ResourceDescription(
            "polibase", "Polibase", inaccessibility_check_values=(2, 10000, 15)
        )

        SITE_LIST: list[SiteResourceDescription] = [
            SiteResourceDescription(
                CONST.SITE_ADDRESS,
                f"Сайт компании: {CONST.SITE_ADDRESS}",
                check_certificate_status=True,
                check_free_space_status=False,
            ),
            SiteResourceDescription(
                CONST.EMAIL_SERVER_ADDRESS,
                f"Сайт корпоративной почты: {CONST.EMAIL_SERVER_ADDRESS}",
                check_certificate_status=True,
                check_free_space_status=True,
                driver_name="/dev/mapper/centos_tenant26--02-var",
            ),
            SiteResourceDescription(
                CONST.API_SITE_ADDRESS,
                f"Api сайта {CONST.SITE_ADDRESS}: {CONST.API_SITE_ADDRESS}",
                check_certificate_status=True,
                check_free_space_status=False,
            ),
            SiteResourceDescription(
                CONST.BITRIX_SITE_URL, f"Сайт ЦМРТ24: {CONST.BITRIX_SITE_URL}"
            ),
            SiteResourceDescription(
                CONST.OMS_SITE_ADDRESS,
                f"Внутренний сайт омс: {CONST.OMS_SITE_ADDRESS}",
                internal=True,
            ),
            SiteResourceDescription(
                CONST.WIKI_SITE_ADDRESS,
                f"Внутренний сайт Вики: {CONST.WIKI_SITE_ADDRESS}",
                internal=True,
            ),
        ]

    class InaccessableReasons(Enum):
        CERTIFICATE_ERROR: str = "Ошибка проверки сертификата"
        SERVICE_UNAVAILABLE: str = "Ошибка 503: Сервис недоступен"


class MEDICAL_DOCUMENT:
    class DirectionTypes(Enum):
        MRI: MedicalDirectionDescription = MedicalDirectionDescription(
            ("Магнитно-резонансная томография",), "МРТ"
        )
        CT: MedicalDirectionDescription = MedicalDirectionDescription(
            ("Компьютерная томография",), "КТ"
        )
        ULTRASOUND: MedicalDirectionDescription = MedicalDirectionDescription(
            ("ультразвуковая допплерография",), "УЗИ"
        )


class CheckableSections(Enum):
    RESOURCES: int = auto()
    WS: int = auto()
    PRINTERS: int = auto()
    INDICATIONS: int = auto()
    BACKUPS: int = auto()
    VALENTA: int = auto()
    SERVERS: int = auto()
    MATERIALIZED_RESOURCES: int = auto()
    TIMESTAMPS: int = auto()
    DISKS: int = auto()
    POLIBASE: int = auto()

    @staticmethod
    def all():
        return [item for item in CheckableSections]


class DocumentTypes(Enum):
    POLIBASE: int = auto()
    MEDICAL_DIRECTION: int = auto()
    PERSONAL: int = auto()


class PATH_SHARE:
    NAME: str = "shares"
    PATH: str = os.path.join(AD.PATH_ROOT, NAME)


class PATH_FACADE:
    SHARED_POINT_PATH: str = os.path.join("S$", CONST.FACADE.NAME)
    LINUX_MOUNT_POINT_PATH: str = f"/mnt/{CONST.FACADE.NAME}/"

    VALUE: str = f"//{AD.DOMAIN_MAIN}/{CONST.FACADE.NAME}/"

    @staticmethod
    def STORAGE_PATH() -> str:
        return os.path.join(HOSTS.DC1.NAME, PATH_FACADE.SHARED_POINT_PATH)


class PATH_DATA_STORAGE:
    NAME: str = "data"
    DATA_FOLDER: str = os.path.join(PATH_FACADE.VALUE, NAME)


class PATH_SCAN:
    NAME: str = "scan"
    VALUE: str = os.path.join(AD.PATH_ROOT, NAME)


class PATH_SCAN_TEST:
    NAME: str = "test"
    VALUE: str = os.path.join(PATH_SCAN.VALUE, NAME)


class PATH_SCAN_SOURCE:
    NAME: str = "Исходники"
    VALUE: str = os.path.join(PATH_SCAN.VALUE, NAME)


class PATH_SCAN_RESULT:
    NAME: str = "Результат"
    VALUE: str = os.path.join(PATH_SCAN.VALUE, NAME)

    @staticmethod
    def get_path(type: DocumentTypes) -> str:
        if type == DocumentTypes.MEDICAL_DIRECTION:
            return os.path.join(PATH_SCAN_RESULT.VALUE, "Направления")


class PATH_WS_816_SCAN:
    NAME: str = r"C$/Users/Nurse/Documents/Scanned Documents"
    VALUE: str = os.path.join(r"//", HOSTS.WS816.NAME, NAME)


class PATH_OMS:
    NAME: str = "oms"
    VALUE: str = os.path.join(AD.PATH_ROOT, NAME)


class PATH_MARKS:
    NAME: str = "MarkServise"
    VALUE: str = os.path.join(AD.PATH_ROOT, NAME)


class PATH_IT:
    NAME: str = "5. IT"
    NEW_EMPLOYEES_NAME: str = "New employees"
    ROOT: str = os.path.join(PATH_SHARE.PATH, NAME)

    @staticmethod
    def get_new_employee_path(name: str) -> str:
        return os.path.join(
            os.path.join(PATH_IT.ROOT, PATH_IT.NEW_EMPLOYEES_NAME), name
        )


class PATH_APP:
    NAME: str = "apps"
    FOLDER: str = os.path.join(PATH_FACADE.VALUE, NAME)


class PATH_DOCS:
    NAME: str = f"Docs{CONST.FACADE.SERVICE_FOLDER_SUFFIX}"
    FOLDER: str = os.path.join(PATH_FACADE.VALUE, NAME)


class PATH_FONTS:
    NAME: str = "fonts"
    FOLDER: str = os.path.join(PATH_DOCS.FOLDER, NAME)

    @staticmethod
    def get(name: str) -> str:
        from pih.tools import PathTool

        return os.path.join(
            PATH_FONTS.FOLDER,
            PathTool.add_extension(name, FILE.EXTENSION.TRUE_TYPE_FONT),
        )


class PATH_APP_DATA:
    NAME: str = "data"
    FOLDER: str = os.path.join(PATH_APP.FOLDER, NAME)

    OCR_RESULT_NAME: str = "ocr result"
    OCR_RESULT_FOLDER: str = os.path.join(FOLDER, OCR_RESULT_NAME)


class PATH_STATISTICS:
    NAME: str = "statistics"
    CHART_FILE_NAME_PREFIX: str = "chart_"
    FOLDER: str = os.path.join(PATH_APP_DATA.FOLDER, NAME)

    @staticmethod
    def get_file_path(name: str | Enum) -> str:
        from pih.tools import PathTool, EnumTool

        name = EnumTool.get(name)
        return PathTool.path(
            os.path.join(PATH_STATISTICS.FOLDER, f"{name}.{FILE.EXTENSION.PNG}")
        )


class PATH_INDICATIONS:
    NAME: str = "indications"
    FOLDER: str = os.path.join(PATH_APP_DATA.FOLDER, NAME)

    CHILLER_DATA_NAME: str = "chiller"
    CHILLER_DATA_FOLDER: str = os.path.join(FOLDER, CHILLER_DATA_NAME)

    CHILLER_DATA_IMAGE_LAST: str = os.path.join(
        CHILLER_DATA_FOLDER, f"last.{FILE.EXTENSION.JPG}"
    )
    CHILLER_DATA_IMAGE_LAST_RESULT: str = os.path.join(
        CHILLER_DATA_FOLDER, f"last_result.{FILE.EXTENSION.JPG}"
    )

    @staticmethod
    def CHILLER_DATA_IMAGE_RESULT(
        datetime_string: str, temperature: float | None, indications: int
    ) -> str:
        name_list: list[str] = [str(indications)]
        if temperature is not None:
            name_list += [str(temperature)]
        name_list += [datetime_string]
        return os.path.join(
            PATH_INDICATIONS.CHILLER_DATA_FOLDER,
            f"{'_'.join(name_list)}.{FILE.EXTENSION.JPG}",
        )


class PATH_MOBILE_HELPER:
    NAME: str = "mobile helper"
    FOLDER: str = os.path.join(PATH_APP_DATA.FOLDER, NAME)

    QR_CODE_NAME: str = "qr code"
    QR_CODE_FOLDER: str = os.path.join(FOLDER, QR_CODE_NAME)

    INCOME_IMAGES_NAME: str = "income images"
    INCOME_IMAGES_FOLDER: str = os.path.join(FOLDER, INCOME_IMAGES_NAME)

    FILES_NAME: str = "files"
    FILES_FOLDER: str = os.path.join(FOLDER, FILES_NAME)

    TIME_TRACKING_REPORT: str = "time tracking report"
    TIME_TRACKING_REPORT_FOLDER: str = os.path.join(FOLDER, TIME_TRACKING_REPORT)


class PATH_POLIBASE_APP_DATA:
    NAME: str = "polibase"
    FOLDER: str = os.path.join(PATH_APP_DATA.FOLDER, NAME)
    PERSON_CARD_REGISTRY_FOLDER: str = os.path.join(FOLDER, "person card folder")

    SERVICE_FOLDER_PATH: str = os.path.join(
        PATH_FACADE.VALUE, f"{NAME}{CONST.FACADE.SERVICE_FOLDER_SUFFIX}"
    )

    class SETTINGS:
        MAIN: str = "polibase_main_settings.vbs"
        TEST: str = "polibase_test_settings.vbs"


class PATH_USER:
    NAME: str = "homes"
    HOME_FOLDER: str = os.path.join(AD.PATH_ROOT, NAME)
    HOME_FOLDER_FULL: str = os.path.join(AD.PATH_ROOT, NAME)

    @staticmethod
    def private_folder(login: str) -> str:
        return os.path.join(PATH_USER.HOME_FOLDER, login)

    @staticmethod
    def get_document_name(user_name: str, login: str | None = None) -> str:
        return (
            PATH_IT.get_new_employee_path(user_name)
            + (f" ({login})" if login else "")
            + ".docx"
        )


class PATH_POLIBASE:
    NAME: str = CONST.HOST.POLIBASE.NAME
    TEST_SUFFIX: str = "_test"
    PERSON_CARD_REGISTRY_FOLDER: str = (
        PATH_POLIBASE_APP_DATA.PERSON_CARD_REGISTRY_FOLDER
    )

    @staticmethod
    def get_person_folder(pin: int, test: bool = False) -> str:
        root: str = PATH_POLIBASE.NAME
        if test:
            if root.find(".") != -1:
                root_parts: list[str] = root.split(".")
                root_parts[0] += PATH_POLIBASE.TEST_SUFFIX
                root = ".".join(root_parts)
            else:
                root += PATH_POLIBASE.TEST_SUFFIX
        return os.path.join(
            f"\\\\{root}", "Data", "PERSONS", str(pin)
        )


class PATH_WS:
    NAME: str = f"WS{CONST.FACADE.SERVICE_FOLDER_SUFFIX}"
    PATH: str = os.path.join(PATH_FACADE.VALUE, NAME)


class PATHS:
    SHARE: PATH_SHARE = PATH_SHARE()
    SCAN: PATH_SCAN = PATH_SCAN()
    SCAN_TEST = PATH_SCAN_TEST()
    SCAN_SOURCE = PATH_SCAN_SOURCE()
    SCAN_RESULT = PATH_SCAN_RESULT()
    WS_816_SCAN: PATH_WS_816_SCAN = PATH_WS_816_SCAN()
    OMS: PATH_OMS = PATH_OMS()
    IT: PATH_IT = PATH_IT()
    USER: PATH_USER = PATH_USER()
    POLIBASE: PATH_POLIBASE = PATH_POLIBASE()
    POLIBASE_APP_DATA: PATH_POLIBASE_APP_DATA = PATH_POLIBASE_APP_DATA()
    WS: PATH_WS = PATH_WS()
    DOCS: PATH_DOCS = PATH_DOCS()
    FONTS: PATH_FONTS = PATH_FONTS()
    MOBILE_HELPER: PATH_MOBILE_HELPER = PATH_MOBILE_HELPER()
    APP_DATA: PATH_APP_DATA = PATH_APP_DATA()
    INDICATIONS: PATH_INDICATIONS = PATH_INDICATIONS()
    STATISTICS: PATH_STATISTICS = PATH_STATISTICS()
    FACADE: PATH_FACADE = PATH_FACADE()
    DATA_STORAGE: PATH_DATA_STORAGE = PATH_DATA_STORAGE()


class MarkType(Enum):
    NORMAL: int = auto()
    FREE: int = auto()
    GUEST: int = auto()
    TEMPORARY: int = auto()


class FIELD_NAME_COLLECTION:
    ACTION_NAME: str = "action_name"
    ACTION_DESCRIPTION: str = "action_description"
    FULL_NAME: str = "FullName"
    IP_ADDRESS: str = "ip_address"
    TYPE: str = "type"
    GROUP_NAME: str = "GroupName"
    GROUP_ID: str = "GroupID"
    COMMENT: str = "Comment"
    CARD_REGISTRY_FOLDER: str = "ChartFolder"
    DESTINATION: str = "destination"
    BIRTH: str = "Birth"
    TAB_NUMBER: str = "TabNumber"
    OWNER_TAB_NUMBER: str = "OwnerTabNumber"
    NAME: str = USER_PROPERTIES.NAME
    TITLE: str = "title"
    MIDNAME: str = "MidName"
    PERSON_ID: str = "pID"
    MARK_ID: str = "mID"
    ID: str = "id"
    PIN: str = "pin"
    PID: str = "pid"
    VISIT_ID: str = "visitID"
    MESSAGE_ID: str = "messageID"
    VALUE: str = "value"
    FILE: str = "file"
    DIVISION_NAME: str = "DivisionName"
    DIVISION_ID: str = "DivisionID"
    BARCODE: str = "barcode"
    EMAILED: str = "emailed"
    PROPERTIES: str = "properties"
    PARAMETERS: str = "parameters"
    MESSAGE: str = "message"
    STATUS: str = "status"
    FEEDBACK_CALL_STATUS: str = "feedbackCallStatus"
    REGISTRATION_DATE: str = "registrationDate"
    CABINET_ID: str = "cabinetID"
    DOCTOR_ID: str = "doctorID"
    DOCTOR_FULL_NAME: str = "doctorFullName"
    SERVICE_GROUP_ID: str = "serviceGroupID"
    PORT_NAME: str = "portName"
    TEMPERATURE: str = "temperature"
    HUMIDITY: str = "humidity"
    INDICATORS: str = "indicators"
    DATA: str = "data"
    COUNT: str = "count"
    FORCED: str = "forced"

    SEARCH_ATTRIBUTE_LOGIN: str = USER_PROPERTIES.LOGIN
    SEARCH_ATTRIBUTE_NAME: str = USER_PROPERTIES.NAME

    TELEPHONE_NUMBER: str = USER_PROPERTIES.TELEPHONE_NUMBER
    EMAIL: str = f"e{USER_PROPERTIES.EMAIL}"
    DN: str = USER_PROPERTIES.DN
    LOGIN: str = USER_PROPERTIES.LOGIN
    ACTIVE_USERS_LOGIN: str = "active_" + USER_PROPERTIES.LOGIN
    DESCRIPTION: str = USER_PROPERTIES.DESCRIPTION
    PASSWORD: str = USER_PROPERTIES.PASSWORD
    ACCESSABLE: str = "accessable"
    STEP: str = "step"
    STEP_CONFIRMED: str = "stepConfirmed"
    GRADE: str = "grade"
    INFORMATION_WAY: str = "informationWay"
    TIME: str = "time"

    TIMESTAMP: str = "timestamp"
    DATE: str = "date"
    BEGIN_DATE: str = "beginDate"
    COMPLETE_DATE: str = "completeDate"
    RECIPIENT: str = "recipient"
    SENDER: str = "sender"
    ANSWER: str = "answer"
    STATE: str = "state"

    INVENTORY_NUMBER: str = "inventory_number"
    QUANTITY: str = "quantity"
    ROW: str = "row"
    NAME_COLUMN: str = "name_column"
    INVENTORY_NUMBER_COLUMN: str = "inventory_number_column"
    QUANTITY_COLUMN: str = "quantity_column"

    TEMPLATE_USER_CONTAINER: str = "templated_user"
    CONTAINER: str = "container"

    REMOVE: str = "remove"
    AS_FREE: str = "as_free"
    CANCEL: str = "cancel"

    WORKSTATION_NAME: str = "workstation_name"
    WORKSTATION_DESCRIPTION: str = "workstation_description"
    PERSON_NAME: str = "person_name"
    PERSON_PIN: str = "person_pin"
    REGISTRATOR_PERSON_NAME: str = "registrator_person_name"
    REGISTRATOR_PERSON_PIN: str = "registrator_person_pin"


class FIELD_ITEM_COLLECTION:
    TAB_NUMBER: FieldItem = FieldItem(
        FIELD_NAME_COLLECTION.TAB_NUMBER, "Табельный номер"
    )
    OWNER_TAB_NUMBER: FieldItem = FieldItem(
        FIELD_NAME_COLLECTION.OWNER_TAB_NUMBER, "Табельный номер владельца"
    )
    FULL_NAME: FieldItem = FieldItem(FIELD_NAME_COLLECTION.FULL_NAME, "Полное имя")
    TEMPERATURE: FieldItem = FieldItem(
        FIELD_NAME_COLLECTION.TEMPERATURE, "Температура", data_formatter="{data}°C"
    )
    INDICATORS: FieldItem = FieldItem(
        FIELD_NAME_COLLECTION.INDICATORS,
        "Индикаторы",
        data_formatter=DATA.FORMATTER.CHILLER_INDICATIONS_VALUE_INDICATORS.value,
    )
    INDICATION_TIMESTAMP: FieldItem = FieldItem(
        FIELD_NAME_COLLECTION.TIMESTAMP,
        "Время снятия показаний",
        data_formatter=DATA.FORMATTER.MY_DATETIME.value,
    )


class FIELD_COLLECTION:
    INDEX: FieldItem = FieldItem("__Index__", "Индекс", True)
    POSITION: FieldItem = FieldItem(
        "position", "Расположение", True, default_value="Нет в реестре карт"
    )

    VALUE: FieldItem = FieldItem("", "Значение", True)
    VALUE_LIST: FieldItem = FieldItem("", "Список значений", True)

    class ORION:
        MARK_ACTION: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.REMOVE, "Удалить"),
            FieldItem(FIELD_NAME_COLLECTION.AS_FREE, "Сделать свободной"),
            FieldItem(FIELD_NAME_COLLECTION.CANCEL, "Оставить"),
        )

        GROUP_BASE: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.GROUP_NAME, "Группа доступа"),
            FieldItem(FIELD_NAME_COLLECTION.COMMENT, "Описание", False),
        )

        TAB_NUMBER_BASE: FieldItemList = FieldItemList(FIELD_ITEM_COLLECTION.TAB_NUMBER)

        FREE_MARK: FieldItemList = FieldItemList(TAB_NUMBER_BASE, GROUP_BASE)

        TAB_NUMBER: FieldItemList = FieldItemList(
            TAB_NUMBER_BASE,
            FieldItem(
                FIELD_NAME_COLLECTION.DIVISION_NAME,
                "Подразделение",
                default_value="Без подразделения",
            ),
            GROUP_BASE,
        ).position(FIELD_NAME_COLLECTION.DIVISION_NAME, 2)

        TEMPORARY_MARK: FieldItemList = FieldItemList(
            FIELD_ITEM_COLLECTION.TAB_NUMBER,
            FIELD_ITEM_COLLECTION.OWNER_TAB_NUMBER,
            FIELD_ITEM_COLLECTION.FULL_NAME,
            FieldItem(FIELD_NAME_COLLECTION.PERSON_ID, "Person ID", False),
            FieldItem(FIELD_NAME_COLLECTION.MARK_ID, "Mark ID", False),
        )

        PERSON: FieldItemList = (
            FieldItemList(
                TAB_NUMBER,
                FieldItem(FIELD_NAME_COLLECTION.TELEPHONE_NUMBER, "Телефон", True),
                FIELD_ITEM_COLLECTION.FULL_NAME,
            )
            .position(FIELD_NAME_COLLECTION.FULL_NAME, 1)
            .position(FIELD_NAME_COLLECTION.TELEPHONE_NUMBER, 2)
        )

        PERSON_DIVISION: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.ID, "ID", False),
            FieldItem(FIELD_NAME_COLLECTION.NAME, "Название подразделения"),
        )

        PERSON_EXTENDED: FieldItemList = FieldItemList(
            PERSON,
            FieldItem(FIELD_NAME_COLLECTION.PERSON_ID, "Person ID", False),
            FieldItem(FIELD_NAME_COLLECTION.MARK_ID, "Mark ID", False),
        )

        GROUP: FieldItemList = FieldItemList(
            GROUP_BASE, FieldItem(FIELD_NAME_COLLECTION.GROUP_ID, "Group id", False)
        ).visible(FIELD_NAME_COLLECTION.COMMENT, True)

        GROUP_STATISTICS: FieldItemList = FieldItemList(
            GROUP,
            FieldItem("Count", "Количество"),
        ).visible(FIELD_NAME_COLLECTION.COMMENT, False)

        TIME_TRACKING: FieldItemList = FieldItemList(
            FIELD_ITEM_COLLECTION.FULL_NAME,
            FIELD_ITEM_COLLECTION.TAB_NUMBER,
            FieldItem("TimeVal", "Время"),
            FieldItem("Remark", "Remark"),
            FieldItem("Mode", "Mode"),
        )

        TIME_TRACKING_RESULT: FieldItemList = FieldItemList(
            FIELD_ITEM_COLLECTION.FULL_NAME,
            FIELD_ITEM_COLLECTION.TAB_NUMBER,
            FieldItem("Date", "Дата"),
            FieldItem("EnterTime", "Время прихода"),
            FieldItem("ExitTime", "Время ухода"),
            FieldItem("Duration", "Продолжительность"),
        )

    class INRENTORY:
        ITEM: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.NAME, "Название инвентарного объекта"),
            FieldItem(FIELD_NAME_COLLECTION.INVENTORY_NUMBER, "Инвентарный номер"),
            FieldItem(FIELD_NAME_COLLECTION.QUANTITY, "Количество"),
            FieldItem(FIELD_NAME_COLLECTION.NAME_COLUMN, None, False),
            FieldItem(FIELD_NAME_COLLECTION.INVENTORY_NUMBER_COLUMN, None, False),
            FieldItem(FIELD_NAME_COLLECTION.QUANTITY_COLUMN, None, False),
        )

    class AD:
        COMPUTER_DESCRIPTION: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.NAME, "Имя компьютера"),
            FieldItem(FIELD_NAME_COLLECTION.DESCRIPTION, "Описание"),
            FieldItem(FIELD_NAME_COLLECTION.PROPERTIES, "Свойства", visible=False),
        )

        USER_ACTION: FieldItemList = FieldItemList(
            FieldItem(USER_PROPERTIES.TELEPHONE_NUMBER, "Изменить номер телефона"),
            FieldItem(USER_PROPERTIES.PASSWORD, "Изменить пароль"),
            FieldItem(USER_PROPERTIES.USER_STATUS, "Активировать или деактивировать"),
        )

        SERVER: FieldItemList = FieldItemList(
            COMPUTER_DESCRIPTION,
            FieldItem(FIELD_NAME_COLLECTION.ACCESSABLE, "Доступен"),
        )

        WORKSTATION: FieldItemList = FieldItemList(
            SERVER,
            FieldItem(FIELD_NAME_COLLECTION.LOGIN, "Имя залогированного пользователя"),
        )

        SEARCH_ATTRIBUTE: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.SEARCH_ATTRIBUTE_LOGIN, "Логин"),
            FieldItem(FIELD_NAME_COLLECTION.SEARCH_ATTRIBUTE_NAME, "Имя"),
        )

        CONTAINER: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.NAME, "Название"),
            FieldItem(FIELD_NAME_COLLECTION.DESCRIPTION, "Описание"),
        )

        USER_NAME: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.NAME, "Полное имя пользователя")
        )

        TEMPLATED_USER: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.DESCRIPTION, "Описание")
        )

        USER: FieldItemList = (
            FieldItemList(
                CONTAINER,
                FieldItem(FIELD_NAME_COLLECTION.LOGIN, "Логин"),
                FieldItem(FIELD_NAME_COLLECTION.TELEPHONE_NUMBER, "Телефон"),
                FieldItem(USER_PROPERTIES.EMAIL, "Электронная почта"),
                FieldItem(FIELD_NAME_COLLECTION.DN, "Размещение"),
                FieldItem("userAccountControl", "Свойства аккаунта", False),
            )
            .position(FIELD_NAME_COLLECTION.DESCRIPTION, 4)
            .caption(
                FIELD_NAME_COLLECTION.NAME,
                USER_NAME.get_item_by_name(FIELD_NAME_COLLECTION.NAME).caption,
            )
        )

        CONTAINER_TYPE: FieldItemList = FieldItemList(
            FieldItem(
                FIELD_NAME_COLLECTION.TEMPLATE_USER_CONTAINER, "Шаблонный пользователь"
            ),
            FieldItem(FIELD_NAME_COLLECTION.CONTAINER, "Контейнер"),
        )

    class POLIBASE:
        CARD_REGISTRY_FOLDER: FieldItem = FieldItem(
            FIELD_NAME_COLLECTION.CARD_REGISTRY_FOLDER,
            "Папка карты пациента",
            default_value="Не зарегистрирована в реестре карт пациентов",
        )

        PERSON_BASE: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.PIN, "Идентификационный номер пациента"),
            FieldItem(FIELD_NAME_COLLECTION.FULL_NAME, "ФИО пациента"),
            FieldItem(FIELD_NAME_COLLECTION.TELEPHONE_NUMBER, "Телефон"),
        )

        PERSON_VISIT: FieldItemList = FieldItemList(
            PERSON_BASE,
            FieldItem(FIELD_NAME_COLLECTION.REGISTRATION_DATE, "Дата регистрации"),
            FieldItem(FIELD_NAME_COLLECTION.DOCTOR_FULL_NAME, "Имя доктора"),
        )

        PERSON: FieldItemList = FieldItemList(
            PERSON_BASE,
            FieldItem(
                FIELD_NAME_COLLECTION.BIRTH,
                "День рождения",
                True,
                "datetime",
                data_formatter=f"{DATA.FORMATTER.MY_DATE.value}",
            ),
            FieldItem(
                FIELD_NAME_COLLECTION.EMAIL,
                "Электронная почта",
                default_value="Нет электронной почты",
            ),
            CARD_REGISTRY_FOLDER,
            FieldItem(FIELD_NAME_COLLECTION.COMMENT, "Комментарий"),
        )

    class POLICY:
        PASSWORD_TYPE: FieldItemList = FieldItemList(
            # FieldItem("EMAIL", "Для почты"),
            # FieldItem("SIMPLE", "Простой"),
            FieldItem("NORMAL", "Стандартный"),
            FieldItem("STRONG", "Сложный"),
        )

    class PRINTER:
        ITEM: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.NAME, "Name"),
            FieldItem("serverName", "Server name"),
            FieldItem(FIELD_NAME_COLLECTION.PORT_NAME, "Host name"),
            FieldItem(FIELD_NAME_COLLECTION.DESCRIPTION, "Description"),
            FieldItem("adminDescription", "Admin description", False),
            FieldItem("driverName", "Driver name"),
        )

    class INDICATIONS:
        CT_VALUE: FieldItemList = FieldItemList(
            FIELD_ITEM_COLLECTION.TEMPERATURE,
            FieldItem(
                FIELD_NAME_COLLECTION.HUMIDITY, "Влажность", data_formatter="{data}%"
            ),
        )

        CHILLER_VALUE: FieldItemList = FieldItemList(
            FIELD_ITEM_COLLECTION.TEMPERATURE, FIELD_ITEM_COLLECTION.INDICATORS
        )

        CT_VALUE_CONTAINER: FieldItemList = FieldItemList(
            CT_VALUE, FIELD_ITEM_COLLECTION.INDICATION_TIMESTAMP
        )

        CHILLER_VALUE_CONTAINER: FieldItemList = FieldItemList(
            CHILLER_VALUE, FIELD_ITEM_COLLECTION.INDICATION_TIMESTAMP
        )


class FieldCollectionAliases(Enum):
    TIME_TRACKING: FieldItem = FIELD_COLLECTION.ORION.TIME_TRACKING
    PERSON: FieldItem = FIELD_COLLECTION.ORION.PERSON
    TEMPORARY_MARK: FieldItem = FIELD_COLLECTION.ORION.TEMPORARY_MARK
    POLIBASE_PERSON: FieldItem = FIELD_COLLECTION.POLIBASE.PERSON
    POLIBASE_PERSON_VISIT: FieldItem = FIELD_COLLECTION.POLIBASE.PERSON_VISIT
    PERSON_DIVISION: FieldItem = FIELD_COLLECTION.ORION.PERSON_DIVISION
    PERSON_EXTENDED: FieldItem = FIELD_COLLECTION.ORION.PERSON_EXTENDED
    COMPUTER_DESCRIPTION: FieldItem = FIELD_COLLECTION.AD.COMPUTER_DESCRIPTION
    WORKSTATION: FieldItem = FIELD_COLLECTION.AD.WORKSTATION
    SERVER: FieldItem = FIELD_COLLECTION.AD.SERVER
    VALUE: FieldItem = FIELD_COLLECTION.VALUE
    VALUE_LIST: FieldItem = FIELD_COLLECTION.VALUE_LIST


class PolibasePersonInformationQuestStatus(Enum):
    UNKNOWN: int = -1
    GOOD: int = 0
    EMAIL_IS_EMPTY: int = 1
    EMAIL_IS_WRONG: int = 2
    EMAIL_IS_NOT_ACCESSABLE: int = 4


class PolibasePersonVisitNotificationType(Enum):
    GREETING: int = auto()
    REMINDER: int = auto()
    DEFAULT: int = auto()


class PolibasePersonReviewQuestStep(Enum):
    BEGIN: int = auto()
    #
    ASK_GRADE: int = auto()
    ASK_FEEDBACK_CALL: int = auto()
    ASK_INFORMATION_WAY: int = auto()
    #
    COMPLETE: int = auto()


LINK_EXT = "lnk"


class PrinterCommands(Enum):
    REPORT: str = "report"
    STATUS: str = "status"


class PASSWORD_GENERATION_ORDER:
    SPECIAL_CHARACTER: str = "s"
    LOWERCASE_ALPHABET: str = "a"
    UPPERCASE_ALPHABET: str = "A"
    DIGIT: str = "d"
    DEFAULT_ORDER_LIST: list[str] = [
        SPECIAL_CHARACTER,
        LOWERCASE_ALPHABET,
        UPPERCASE_ALPHABET,
        DIGIT,
    ]


class PASSWORD:
    class SETTINGS:
        SIMPLE: PasswordSettings = PasswordSettings(
            3, "", PASSWORD_GENERATION_ORDER.DEFAULT_ORDER_LIST, 0, 3, 0, 0, False
        )
        NORMAL: PasswordSettings = PasswordSettings(
            8, "!@#", PASSWORD_GENERATION_ORDER.DEFAULT_ORDER_LIST, 3, 3, 1, 1, False
        )
        STRONG: PasswordSettings = PasswordSettings(
            10,
            "#%+\-!=@()_",
            PASSWORD_GENERATION_ORDER.DEFAULT_ORDER_LIST,
            3,
            3,
            2,
            2,
            True,
        )
        DEFAULT: PasswordSettings = NORMAL
        PC: PasswordSettings = NORMAL
        EMAIL: PasswordSettings = NORMAL

    def get(name: str) -> SETTINGS:
        return PASSWORD.__getattribute__(PASSWORD.SETTINGS, name)


class COMMAND_TYPE(Enum):
    POLIBASE: tuple[str] = (
        "Запрос к базе данный Polibase (Oracle)",
        "polibase",
        "полибейс",
        "oracle",
    )
    DATA_SOURCE: tuple[str] = ("Запрос к базе данных DataSource (DS)", "ds")
    CMD: tuple[str] = ("Консольную команду", "cmd")
    PYTHON: tuple[str] = ("Скрипт Python", "py", "python")
    SSH: tuple[str] = ("Команда SSH", "ssh")


class LogMessageChannels(Enum):
    BACKUP: int = auto()
    POLIBASE: int = auto()
    POLIBASE_BOT: int = auto()
    DEBUG: int = auto()
    DEBUG_BOT: int = auto()
    SERVICES: int = auto()
    SERVICES_BOT: int = auto()
    HR: int = auto()
    HR_BOT: int = auto()
    IT: int = auto()
    IT_BOT: int = auto()
    RESOURCES: int = auto()
    RESOURCES_BOT: int = auto()
    PRINTER: int = auto()
    POLIBASE_ERROR: int = auto()
    POLIBASE_ERROR_BOT: int = auto()
    CARD_REGISTRY: int = auto()
    CARD_REGISTRY_BOT: int = auto()
    NEW_EMAIL: int = auto()
    NEW_EMAIL_BOT: int = auto()
    TIME_TRACKING: int = auto()
    JOURNAL: int = auto()
    JOURNAL_BOT: int = auto()
    DEFAULT: int = DEBUG


class LogMessageFlags(Enum):
    NORMAL: int = 1
    ERROR: int = 2
    NOTIFICATION: str = 4
    DEBUG: str = 8
    SAVE: int = 16
    SILENCE: str = 32
    RESULT: int = 64
    WHATSAPP: int = 128
    ALERT: int = 256
    TASK: int = 512
    SAVE_ONCE: int = 1024
    DEFAULT: str = NORMAL


POLIBASE_BASE: ServiceDescription = ServiceDescription(
    host=CONST.HOST.POLIBASE.NAME,
    pyton_executor_path=r"C:\Users\adm\AppData\Local\Programs\Python\Python310\python.exe",
    run_from_system_account=True,
)


class ServiceRoles(Enum):
    @staticmethod
    def description(
        value: Enum | str | ServiceInformationBase, get_source_description: bool = False
    ) -> ServiceInformationBase | None:
        def isolated_name(value: ServiceInformationBase | None) -> str | None:
            if value is None:
                return None
            value.name = (
                ":".join(("isolated", value.name))
                if value.isolated and value.name.find("isolated") == -1
                else value.name
            )
            return value

        if isinstance(value, str):
            for service_role in ServiceRoles:
                if ServiceRoles.description(service_role).name == value:
                    return isolated_name(service_role.value)
            return None
        if isinstance(value, ServiceInformationBase):
            return isolated_name(
                ServiceRoles.description(value.name)
                if get_source_description
                else value
            )
        return isolated_name(value.value)

    SERVICE_ADMIN: ServiceDescription = ServiceDescription(
        name="ServiceAdmin",
        description="Service admin",
        host=CONST.HOST.DC1.NAME,
        port=CONST.RPC.PORT(20),
        host_changeable=False,
        commands=[
            ServiceCommands.on_service_starts,
            ServiceCommands.on_service_stops,
            ServiceCommands.get_service_information_table,
            ServiceCommands.heart_beat,
        ],
    )

    EVENT_AND_LOG: ServiceDescription = ServiceDescription(
        name="EventAndLog",
        description="Log and Event service",
        host=CONST.HOST.BACKUP_WORKER.NAME,
        commands=[ServiceCommands.send_log_message, ServiceCommands.send_event],
    )

    DS: ServiceDescription = ServiceDescription(
        name="DataSource",
        description="Data storage and source service",
        host=CONST.HOST.BACKUP_WORKER.NAME,
        host_changeable=True,
        commands=[
            ServiceCommands.register_polibase_person_information_quest,
            ServiceCommands.search_polibase_person_information_quests,
            ServiceCommands.update_polibase_person_information_quest,
            #
            ServiceCommands.update_polibase_person_visit_to_data_stogare,
            ServiceCommands.search_polibase_person_visits_in_data_storage,
            #
            ServiceCommands.register_polibase_person_visit_notification,
            ServiceCommands.search_polibase_person_visit_notifications,
            #
            ServiceCommands.register_delayed_message,
            ServiceCommands.search_delayed_messages,
            ServiceCommands.update_delayed_message,
            #
            ServiceCommands.get_settings_value,
            ServiceCommands.set_settings_value,
            #
            ServiceCommands.search_polibase_person_notification_confirmation,
            ServiceCommands.update_polibase_person_notification_confirmation,
            #
            ServiceCommands.get_storage_value,
            ServiceCommands.set_storage_value,
            #
            ServiceCommands.get_ogrn_value,
            ServiceCommands.get_fms_unit_name,
            #
            ServiceCommands.register_chiller_indications_value,
            ServiceCommands.register_ct_indications_value,
            ServiceCommands.get_last_ct_indications_value_container_list,
            ServiceCommands.get_last_сhiller_indications_value_container_list,
            #
            ServiceCommands.get_gkeep_item_list_by_any,
            ServiceCommands.add_gkeep_item,
            #
            ServiceCommands.register_event,
            ServiceCommands.get_event,
            ServiceCommands.remove_event,
            #
            ServiceCommands.execute_data_source_query,
            ServiceCommands.joke,
        ],
    )

    FILE_WATCHDOG: ServiceDescription = ServiceDescription(
        name="FileWatchdog",
        description="FileWatchdog service",
        host=CONST.HOST.BACKUP_WORKER.NAME,
        commands=[ServiceCommands.listen_for_new_files],
    )

    MAIL: ServiceDescription = ServiceDescription(
        name="Mail",
        description="Mail service",
        host=CONST.HOST.WS255.NAME,
        commands=[
            ServiceCommands.check_email_accessibility,
            ServiceCommands.send_email,
            ServiceCommands.get_email_information,
        ],
    )

    BACKUP: ServiceDescription = ServiceDescription(
        name="Backup",
        description="Backup service",
        host=CONST.HOST.BACKUP_WORKER.NAME,
        commands=[
            ServiceCommands.robocopy_start_job,
            ServiceCommands.robocopy_get_job_status_list,
        ],
    )

    AD: ServiceDescription = ServiceDescription(
        name="ActiveDirectory",
        description="Active directory service",
        host=CONST.HOST.DC2.NAME,
        commands=[
            ServiceCommands.authenticate,
            ServiceCommands.check_user_exists_by_login,
            ServiceCommands.get_user_by_full_name,
            ServiceCommands.get_users_by_name,
            ServiceCommands.get_user_by_login,
            ServiceCommands.get_user_by_telephone_number,
            ServiceCommands.get_template_users,
            ServiceCommands.get_containers,
            ServiceCommands.get_user_list_by_job_position,
            ServiceCommands.get_user_list_by_group,
            ServiceCommands.get_printer_list,
            ServiceCommands.get_computer_list,
            ServiceCommands.get_computer_description_list,
            ServiceCommands.get_workstation_list_by_user_login,
            ServiceCommands.get_user_by_workstation,
            ServiceCommands.create_user_by_template,
            ServiceCommands.create_user_in_container,
            ServiceCommands.set_user_telephone_number,
            ServiceCommands.set_user_password,
            ServiceCommands.set_user_status,
            ServiceCommands.remove_user,
            ServiceCommands.drop_user_cache,
            ServiceCommands.drop_workstaion_cache,
        ],
    )
    WS: ServiceDescription = ServiceDescription(
        name="WS",
        description="Workstation service",
        host=CONST.HOST.BACKUP_WORKER.NAME,
        commands=[
            ServiceCommands.reboot,
            ServiceCommands.shutdown,
            ServiceCommands.send_message_to_user_or_workstation,
            ServiceCommands.kill_process,
        ],
    )

    PRINTER: ServiceDescription = ServiceDescription(
        name="Printer",
        description="Printer service",
        host=CONST.HOST.DC2.NAME,
        commands=[ServiceCommands.printers_report, ServiceCommands.printer_snmp_call],
    )

    DOCS: ServiceDescription = ServiceDescription(
        name="Docs",
        description="Documents service",
        host=CONST.HOST.DC2.NAME,
        commands=[
            ServiceCommands.get_inventory_report,
            ServiceCommands.create_user_document,
            ServiceCommands.save_time_tracking_report,
            ServiceCommands.create_barcodes_for_inventory,
            ServiceCommands.create_barcode_for_polibase_person,
            ServiceCommands.create_qr_code,
            ServiceCommands.check_inventory_report,
            ServiceCommands.save_inventory_report_item,
            ServiceCommands.close_inventory_report,
            ServiceCommands.create_note,
            ServiceCommands.get_note,
            ServiceCommands.get_note_list_by_label,
            ServiceCommands.create_statistics_chart,
            ServiceCommands.save_xlsx,
            ServiceCommands.drop_note_cache,
        ],
    )

    MARK: ServiceDescription = ServiceDescription(
        name="Mark",
        description="Mark service",
        host=CONST.HOST.BACKUP_WORKER.NAME,
        commands=[
            ServiceCommands.get_free_mark_list,
            ServiceCommands.get_temporary_mark_list,
            ServiceCommands.get_mark_person_division_list,
            ServiceCommands.get_time_tracking,
            ServiceCommands.get_mark_list,
            ServiceCommands.get_mark_by_tab_number,
            ServiceCommands.get_mark_by_person_name,
            ServiceCommands.get_free_mark_group_statistics_list,
            ServiceCommands.get_free_mark_list_by_group_id,
            ServiceCommands.get_owner_mark_for_temporary_mark,
            ServiceCommands.get_mark_list_by_division_id,
            ServiceCommands.set_full_name_by_tab_number,
            ServiceCommands.set_telephone_by_tab_number,
            ServiceCommands.check_mark_free,
            ServiceCommands.create_mark,
            ServiceCommands.make_mark_as_free_by_tab_number,
            ServiceCommands.make_mark_as_temporary,
            ServiceCommands.remove_mark_by_tab_number,
            ServiceCommands.door_operation,
        ],
    )

    POLIBASE: ServiceDescription = ServiceDescription(
        name="Polibase",
        description="Polibase service",
        host=POLIBASE_BASE.host,
        pyton_executor_path=POLIBASE_BASE.pyton_executor_path,
        run_from_system_account=POLIBASE_BASE.run_from_system_account,
        commands=[
            ServiceCommands.get_polibase_person_by_pin,
            ServiceCommands.get_polibase_persons_by_pin,
            ServiceCommands.get_polibase_persons_by_telephone_number,
            ServiceCommands.get_polibase_persons_by_name,
            ServiceCommands.get_polibase_persons_by_card_registry_folder_name,
            ServiceCommands.get_polibase_person_registrator_by_pin,
            ServiceCommands.get_polibase_person_pin_list_with_old_format_barcode,
            #
            ServiceCommands.get_polibase_persons_pin_by_visit_date,
            #
            ServiceCommands.search_polibase_person_visits,
            ServiceCommands.get_polibase_person_visits_last_id,
            #
            ServiceCommands.set_polibase_person_card_folder_name,
            ServiceCommands.set_polibase_person_email,
            ServiceCommands.set_barcode_for_polibase_person,
            ServiceCommands.check_polibase_person_card_registry_folder_name,
            ServiceCommands.set_polibase_person_telephone_number,
            ServiceCommands.get_polibase_person_operator_by_pin,
            ServiceCommands.get_polibase_person_by_email,
            #
            ServiceCommands.execute_polibase_query,
            ServiceCommands.update_person_change_date,
            ServiceCommands.get_polibase_person_pin_by_login,
            ServiceCommands.get_polibase_person_user_login_and_worstation_name_pair_list,
            ServiceCommands.get_bonus_list,
        ],
    )

    POLIBASE_DATABASE: ServiceDescription = ServiceDescription(
        name="PolibaseDatabase",
        description="Polibase database service",
        host=POLIBASE_BASE.host,
        pyton_executor_path=POLIBASE_BASE.pyton_executor_path,
        run_from_system_account=POLIBASE_BASE.run_from_system_account,
        commands=[ServiceCommands.create_polibase_database_backup],
    )

    POLIBASE_APP: ServiceDescription = ServiceDescription(
        name="PolibaseApp",
        description="Polibase Application service",
        host=POLIBASE_BASE.host,
        pyton_executor_path=POLIBASE_BASE.pyton_executor_path,
        run_from_system_account=POLIBASE_BASE.run_from_system_account,
    )

    MESSAGE_QUEUE: ServiceDescription = ServiceDescription(
        name="MessageQueue",
        description="Message queue service",
        host=CONST.HOST.BACKUP_WORKER.NAME,
        commands=[ServiceCommands.add_message_to_queue],
    )

    POLIBASE_PERSON_NOTIFICATION: ServiceDescription = ServiceDescription(
        name="PolibasePersonNotification",
        description="Polibase Person Notification service",
        host=CONST.HOST.BACKUP_WORKER.NAME,
    )

    POLIBASE_PERSON_INFORMATION_QUEST: ServiceDescription = ServiceDescription(
        name="PolibasePersonInformationQuest",
        description="Polibase Person Information Quest service",
        host=CONST.HOST.BACKUP_WORKER.NAME,
        commands=[ServiceCommands.start_polibase_person_information_quest],
    )

    POLIBASE_PERSON_REVIEW_NOTIFICATION: ServiceDescription = ServiceDescription(
        name="PolibasePersonReviewNotification",
        description="Polibase Person Review Notification service",
        host=CONST.HOST.BACKUP_WORKER.NAME,
    )

    MESSAGE_RECEIVER: ServiceDescription = ServiceDescription(
        name="MessageReceiver",
        description="Message service",
        host=CONST.HOST.BACKUP_WORKER.NAME,
        host_changeable=False,
    )

    SSH: ServiceDescription = ServiceDescription(
        name="SSH",
        description="SSH service",
        host=CONST.HOST.BACKUP_WORKER.NAME,
        commands=[
            ServiceCommands.execute_ssh_command,
            ServiceCommands.get_certificate_information,
            ServiceCommands.get_unix_free_space_information_by_drive_name,
        ],
    )

    WS735: ServiceDescription = ServiceDescription(
        name="ws735",
        description="ws-735 service",
        host=CONST.HOST.WS735.NAME,
        login="{" + LINK.DEVELOPER_LOGIN + "}",
        password="{" + LINK.DEVELOPER_PASSWORD + "}",
        commands=[ServiceCommands.print_image],
        host_changeable=False,
    )

    RECOGNIZE: ServiceDescription = ServiceDescription(
        name="Recognize",
        description="Recognize service",
        host=CONST.HOST.WS255.NAME,
        host_changeable=False,
        commands=[
            ServiceCommands.get_barcode_list_information,
            ServiceCommands.document_type_exists,
            ServiceCommands.recognize_document,
        ],
    )

    FILE_OGANIZER: ServiceDescription = ServiceDescription(
        name="FileOrganizer",
        description="File organizer service",
        host=CONST.HOST.WS255.NAME,
    )

    RECOGNIZE_TEST: ServiceDescription = ServiceDescription(
        name="RecognizeTest",
        description="Recognize test service",
        host=CONST.HOST.WS255.NAME,
        auto_start=False,
        auto_restart=False,
        visible_for_admin=False,
    )

    """INDICATIONS: ServiceDescription = ServiceDescription(
        name="Indications",
        description="Indications service",
        host=CONST.HOST.WS255.NAME,
    )"""

    WEB_SERVER: ServiceDescription = ServiceDescription(
        name="WebServer",
        description="Web server service",
        host=CONST.HOST.WS255.NAME,
    )

    CHECKER: ServiceDescription = ServiceDescription(
        name="Checker",
        description="Checker service",
        host=CONST.HOST.BACKUP_WORKER.NAME,
        commands=[ServiceCommands.get_resource_status_list],
    )

    AUTOMATION: ServiceDescription = ServiceDescription(
        name="Automation",
        description="Automation service",
        host=HOSTS.BACKUP_WORKER.NAME,
    )

    MOBILE_HELPER: ServiceDescription = ServiceDescription(
        name="MobileHelper",
        description="Mobile helper service",
        host=CONST.HOST.WS255.NAME,
        commands=[ServiceCommands.send_mobile_helper_message],
        auto_restart=True,
        support_servers=(HOSTS.DEVELOPER.NAME,),
    )

    REGISTRATOR_HELPER: ServiceDescription = ServiceDescription(
        name="RegistratorHelper",
        description="Registrator mobile helper service",
        host=HOSTS.BACKUP_WORKER.NAME,
    )

    DEVELOPER: ServiceDescription = ServiceDescription(
        name="Developer",
        description="Developer service",
        host=CONST.HOST.DEVELOPER.NAME,
        port=CONST.RPC.PORT(1),
        visible_for_admin=False,
        auto_start=False,
        auto_restart=False,
        commands=[ServiceCommands.test],
    )

    STUB: ServiceDescription = ServiceDescription(
        name="Stub",
        visible_for_admin=False,
    )


class SubscribtionTypes:
    ON_PARAMETERS: int = 1
    ON_RESULT: int = 2
    ON_RESULT_SEQUENTIALLY: int = 4


class WorkstationMessageMethodTypes(Enum):
    REMOTE: int = auto()
    LOCAL_MSG: int = auto()
    LOCAL_PSTOOL_MSG: int = auto()


class MessageTypes(Enum):
    WHATSAPP: int = auto()
    TELEGRAM: int = auto()
    WORKSTATION: int = auto()


class MessageStatuses(Enum):
    REGISTERED: int = 0
    COMPLETE: int = 1
    AT_WORK: int = 2
    ERROR: int = 3
    ABORT: int = 4


class PolibasePersonVisitStatus:
    CONFIRMED: int = 107
    CANCELED: int = 102


"""
102 - отмена		
99 прошу перенести
101 - пришел			
102 - отказался	
103 - на приеме
104 - окончен
105 - не пришел	
106 - предварительно
107 - подверждено
108 - оказано
109 к оплате
"""


class SCAN:
    SPLITTER_DATA: str = "1"

    class Sources(Enum):
        POLICLINIC: tuple[str, str, str] = ("poly", "Поликлиника", PATH_SCAN.VALUE)
        DIAGNOSTICS: tuple[str, str, str] = (
            "diag",
            "Приёмное отделение",
            PATH_SCAN.VALUE,
        )
        TEST: tuple[str, str, str] = ("test", "Тестовый", PATH_SCAN_TEST.VALUE)
        WS_816: tuple[str, str, str] = (
            HOSTS.WS816,
            "Дневной стационар",
            PATH_WS_816_SCAN.VALUE,
        )


class SETTINGS(Enum):

    REVIEW_ACTION_URL: StorageVariableHolder = StorageVariableHolder(
        "REVIEW_ACTION_URL",
        CONST.POLIBASE.REVIEW_ACTION_URL,
    )

    REVIEW_ACTION_URL_FOR_INPATIENT: StorageVariableHolder = StorageVariableHolder(
        "REVIEW_ACTION_URL_FOR_INPATIENT",
        CONST.POLIBASE.REVIEW_ACTION_URL_FOR_INPATIENT,
    )

    USER_RESPONSIBLE_FOR_PATIENT_MARK: StorageVariableHolder = StorageVariableHolder(
        "USER_RESPONSIBLE_FOR_PATIENT_MARK",
        "baa",
    )

    WIFI_VIP_PASSWORD: StorageVariableHolder = StorageVariableHolder(
        "WIFI_VIP_PASSWORD", "ilovepacific"
    )

    PLAIN_FORMAT_AS_DEFAULT_LOGIN_LIST: StorageVariableHolder = StorageVariableHolder(
        "PLAIN_FORMAT_AS_DEFAULT_LOGIN_LIST", ["bar", "rob", "ptyu"]
    )

    CHILLER_RECOGNIZE_LOG_LEVEL: IntStorageVariableHolder = IntStorageVariableHolder(
        "CHILLER_RECOGNIZE_LOG_LEVEL", 0
    )

    HEART_BEAT_IS_ON: BoolStorageVariableHolder = BoolStorageVariableHolder(
        "HEART_BEAT_IS_ON", True
    )

    CT_INDICATIONS_VALUE_TEMPERATURE_CORRECTION: IntStorageVariableHolder = (
        IntStorageVariableHolder("CT_INDICATIONS_VALUE_TEMPERATURE_CORRECTION", 0.7)
    )
    CT_INDICATIONS_VALUE_SAVE_PERIOD_IN_MINUTES: IntStorageVariableHolder = (
        IntStorageVariableHolder("CT_INDICATIONS_VALUE_SAVE_PERIOD_IN_MINUTES", 60)
    )

    CHILLER_INDICATIONS_VALUE_SAVE_PERIOD_IN_MINUTES: IntStorageVariableHolder = (
        IntStorageVariableHolder("CHILLER_INDICATIONS_VALUE_SAVE_PERIOD_IN_MINUTES", 60)
    )

    HOSPITAL_WORK_DAY_START_TIME: TimeStorageVariableHolder = TimeStorageVariableHolder(
        "HOSPITAL_WORK_DAY_START_TIME", "8:00"
    )
    HOSPITAL_WORK_DAY_END_TIME: TimeStorageVariableHolder = TimeStorageVariableHolder(
        "HOSPITAL_WORK_DAY_END_TIME", "20:00"
    )
    OFFICE_WORK_DAY_START_TIME: TimeStorageVariableHolder = TimeStorageVariableHolder(
        "OFFICE_WORK_DAY_START_TIME", "8:30"
    )
    OFFICE_WORK_DAY_END_TIME: TimeStorageVariableHolder = TimeStorageVariableHolder(
        "OFFICE_WORK_DAY_END_TIME", "17:00"
    )

    INDICATION_CT_NOTIFICATION_START_TIME: DateListStorageVariableHolder = (
        DateListStorageVariableHolder(
            "INDICATION_CT_NOTIFICATION_START_TIME", ["8:00", "12:00", "15:00", "17:00"]
        )
    )

    USER_USE_CACHE: BoolStorageVariableHolder = BoolStorageVariableHolder(
        "USER_USE_CACHE", True
    )

    POLIBASE_PERSON_INFORMATION_QUEST_IS_ON: BoolStorageVariableHolder = (
        BoolStorageVariableHolder("POLIBASE_PERSON_INFORMATION_QUEST_IS_ON", False)
    )
    #
    POLIBASE_PERSON_REVIEW_NOTIFICATION_IS_ON: BoolStorageVariableHolder = (
        BoolStorageVariableHolder("POLIBASE_PERSON_REVIEW_NOTIFICATION_IS_ON", True)
    )

    POLIBASE_PERSON_REVIEW_NOTIFICATION_ASK_WITHOUT_CHECK_FOR_CONFIRMATION: BoolStorageVariableHolder = BoolStorageVariableHolder(
        "POLIBASE_PERSON_REVIEW_NOTIFICATION_ASK_WITHOUT_CHECK_FOR_CONFIRMATION", True
    )

    POLIBASE_PERSON_REVIEW_NOTIFICATION_DAY_DELTA: StorageVariableHolder = (
        StorageVariableHolder("POLIBASE_PERSON_REVIEW_NOTIFICATION_DAY_DELTA", 0)
    )

    POLIBASE_PERSON_REVIEW_NOTIFICATION_TEXT_FOR_CONFIRMED_NOTIFICATION: StorageVariableHolder = StorageVariableHolder(
        "POLIBASE_PERSON_REVIEW_NOTIFICATION_TEXT_FOR_CONFIRMED_NOTIFICATION",
        CONST.POLIBASE.PERSON_REVIEW_NOTIFICATION_TEXT_FOR_CONFIRMED_NOTIFICATION,
    )

    POLIBASE_PERSON_REVIEW_NOTIFICATION_TEXT: StorageVariableHolder = (
        StorageVariableHolder(
            "POLIBASE_PERSON_REVIEW_NOTIFICATION_TEXT",
            CONST.POLIBASE.PERSON_REVIEW_NOTIFICATION_TEXT,
        )
    )

    TIME_TRACKING_FOR_POLYCLINIC: StorageVariableHolder = StorageVariableHolder(
        "TIME_TRACKING_FOR_POLYCLINIC",
        [
            "190",
            "035",
            "058",
            "064",
            "101-0-",
            "125",
            "131",
            "134",
            "139",
            "156",
            "177",
            "199",
            "124",
            "183",
        ],
    )

    POLIBASE_PERSON_REVIEW_NOTIFICATION_START_TIME: TimeStorageVariableHolder = (
        TimeStorageVariableHolder(
            "POLIBASE_PERSON_REVIEW_NOTIFICATION_START_TIME", "21:00"
        )
    )
    #
    RESOURCE_MANAGER_CHECK_SITE_CERTIFICATE_START_TIME: TimeStorageVariableHolder = (
        TimeStorageVariableHolder(
            "RESOURCE_MANAGER_CHECK_SITE_CERTIFICATE_START_TIME", "8:00"
        )
    )
    #
    POLIBASE_CREATION_DB_DUMP_START_TIME: TimeStorageVariableHolder = (
        TimeStorageVariableHolder("POLIBASE_CREATION_DB_DUMP_START_TIME", "20:30")
    )
    #
    RESOURCE_MANAGER_CHECK_SITE_FREE_SPACE_PERIOD_IN_MINUTES: IntStorageVariableHolder = IntStorageVariableHolder(
        "RESOURCE_MANAGER_CHECK_SITE_FREE_SPACE_PERIOD_IN_MINUTES", 15
    )
    #
    PRINTER_REPORT_PERIOD_IN_MINUTES: IntStorageVariableHolder = (
        IntStorageVariableHolder("PRINTER_REPORT_PERIOD_IN_MINUTES", 5)
    )
    #
    POLIBASE_PERSON_VISIT_GREETING_NOTIFICATION_TEXT_WITHOUT_DATE_FOR_CONFIRMED_NOTIFICATION: StorageVariableHolder = StorageVariableHolder(
        "POLIBASE_PERSON_VISIT_GREETING_NOTIFICATION_TEXT_WITHOUT_DATE_FOR_CONFIRMED_NOTIFICATION",
        CONST.POLIBASE.PERSON_VISIT_GREETING_NOTIFICATION_TEXT_FOR_CONFIRMED_NOTIFICATION
        + CONST.POLIBASE.SEND_TELEGRAM_BOT_TEXT,
    )

    POLIBASE_PERSON_VISIT_GREETING_NOTIFICATION_TEXT_WITHOUT_DATE: StorageVariableHolder = StorageVariableHolder(
        "POLIBASE_PERSON_VISIT_GREETING_NOTIFICATION_TEXT_WITHOUT_DATE",
        CONST.POLIBASE.PERSON_VISIT_GREETING_NOTIFICATION_TEXT_WITHOUT_TEXT,
    )

    POLIBASE_PERSON_VISIT_GREETING_NOTIFICATION_TEXT_FOR_CONFIRMED_NOTIFICATION: StorageVariableHolder = StorageVariableHolder(
        "POLIBASE_PERSON_VISIT_GREETING_NOTIFICATION_TEXT_FOR_CONFIRMED_NOTIFICATION",
        CONST.POLIBASE.PERSON_VISIT_GREETING_NOTIFICATION_TEXT_FOR_CONFIRMED_NOTIFICATION
        + CONST.POLIBASE.PERSON_VISIT_NOTIFICATION_WITH_TIME_TEXT
        + CONST.POLIBASE.SEND_TELEGRAM_BOT_TEXT
        + CONST.POLIBASE.HAVE_A_GOOD_DAY,
    )

    POLIBASE_PERSON_VISIT_GREETING_NOTIFICATION_TEXT: StorageVariableHolder = (
        StorageVariableHolder(
            "POLIBASE_PERSON_VISIT_GREETING_NOTIFICATION_TEXT",
            CONST.POLIBASE.PERSON_VISIT_GREETING_NOTIFICATION_TEXT_BASE
            + CONST.POLIBASE.PERSON_VISIT_NOTIFICATION_WITH_TIME_TEXT
            + CONST.POLIBASE.ASK_TO_SEND_TELEGRAM_BOT_URL_TEXT
            + CONST.POLIBASE.HAVE_A_GOOD_DAY,
        )
    )

    PERSON_VISIT_NOTIFICATION_HEADER: StorageVariableHolder = StorageVariableHolder(
        "PERSON_VISIT_NOTIFICATION_HEADER",
        CONST.POLIBASE.PERSON_VISIT_NOTIFICATION_HEADER,
    )

    POLIBASE_PERSON_VISIT_NOTIFICATION_TEXT: StorageVariableHolder = (
        StorageVariableHolder(
            "POLIBASE_PERSON_VISIT_NOTIFICATION_TEXT",
            CONST.POLIBASE.PERSON_VISIT_NOTIFICATION_HEADER
            + CONST.POLIBASE.PERSON_VISIT_NOTIFICATION_APPOINTMENT_INFORMATION
            + CONST.POLIBASE.PERSON_VISIT_NOTIFICATION_WITH_TIME_TEXT
            + CONST.POLIBASE.HAVE_A_GOOD_DAY,
        )
    )

    POLIBASE_PERSON_VISIT_REMINDER_TEXT: StorageVariableHolder = StorageVariableHolder(
        "POLIBASE_PERSON_VISIT_REMINDER_TEXT",
        CONST.POLIBASE.PERSON_VISIT_NOTIFICATION_HEADER
        + "*{name}*, напоминаем Вам о записи сегодня {visit_time}. Вы записаны на {appointment_information}."
        + CONST.POLIBASE.PERSON_VISIT_NOTIFICATION_TEXT_CANCEL_OR_REPLACE_RECEPTION
        + CONST.POLIBASE.HAVE_A_GOOD_DAY,
    )

    POLIBASE_PERSON_TAKE_TELEGRAM_BOT_URL_TEXT: StorageVariableHolder = (
        StorageVariableHolder(
            "POLIBASE_PERSON_TAKE_TELEGRAM_BOT_URL_TEXT",
            CONST.POLIBASE.TAKE_TELEGRAM_BOT_URL_TEXT,
        )
    )

    POLIBASE_PERSON_TAKE_REVIEW_ACTION_URL_TEXT: StorageVariableHolder = (
        StorageVariableHolder(
            "POLIBASE_PERSON_TAKE_REVIEW_ACTION_URL_TEXT",
            CONST.POLIBASE.TAKE_REVIEW_ACTION_URL_TEXT,
        )
    )

    POLIBASE_PERSON_REVIEW_NOTIFICATION_DOCTOR_PERSON_PIN_LIST: IntListStorageVariableHolder = IntListStorageVariableHolder(
        "POLIBASE_PERSON_REVIEW_NOTIFICATION_DOCTOR_PERSON_PIN_LIST",
        [
            51087,
            24727,
            8846,
            97078,
            104498,
            97967,
            103731,
            95357,
            105688,
            102561,
            12411,
            101363,
            2290,
            40903,
            79233,
            20261,
            51858,
            1121,
            100669,
            100728,
            2455,
            99537,
            8975,
            1226,
            35208,
            54098,
            67558,
            89566,
            55956,
            38784,
            2231,
            86363,
            12097,
            43476,
            12146,
            22142,
            4497,
            5471,
            92761,
            3004,
            9207,
            86909,
            102114,
            106721,
            436,
            33636,
            102852,
            7202,
            34388,
            5960,
            29451,
            108037,
            47502,
            111110,
            6772,
            118252,
            120547,
        ],
    )

    POLIBASE_DOCTEMPLATE_THRESHOLD: IntStorageVariableHolder = IntStorageVariableHolder(
        "POLIBASE_DOCTEMPLATE_THRESHOLD", 100
    )

    POLIBASE_PERSON_YES_ANSWER_VARIANTS: StorageVariableHolder = StorageVariableHolder(
        "POLIBASE_PERSON_YES_ANSWER_VARIANTS", CONST.POLIBASE.YES_ANSWER
    )

    POLIBASE_PERSON_NO_ANSWER_VARIANTS: StorageVariableHolder = StorageVariableHolder(
        "POLIBASE_PERSON_NO_ANSWER_VARIANTS", CONST.POLIBASE.NO_ANSWER
    )

    POLIBASE_PERSON_NO_ANSWER_ON_NOTIFICATION_CONFIRMATION_TEXT: StorageVariableHolder = StorageVariableHolder(
        "POLIBASE_PERSON_NO_ANSWER_ON_NOTIFICATION_CONFIRMATION_TEXT",
        "Хорошего дня",
    )

    POLIBASE_PERSON_REVIEW_QUEST_WAIT_TIME: IntStorageVariableHolder = (
        IntStorageVariableHolder("POLIBASE_PERSON_REVIEW_QUEST_WAIT_TIME", 15)
    )

    POLIBASE_PERSON_VISIT_NEED_REGISTER_GREETING_NOTIFICATION: BoolStorageVariableHolder = BoolStorageVariableHolder(
        "POLIBASE_PERSON_VISIT_NEED_REGISTER_GREETING_NOTIFICATION", True
    )

    POLIBASE_PERSON_VISIT_NEED_REGISTER_REMINDER_NOTIFICATION: BoolStorageVariableHolder = BoolStorageVariableHolder(
        "POLIBASE_PERSON_VISIT_NEED_REGISTER_REMINDER_NOTIFICATION", True
    )

    POLIBASE_PERSON_VISIT_TIME_BEFORE_REMINDER_NOTIFICATION_IN_MINUTES: IntStorageVariableHolder = IntStorageVariableHolder(
        "POLIBASE_PERSON_VISIT_TIME_BEFORE_REMINDER_NOTIFICATION_IN_MINUTES", 120
    )

    POLIBASE_PERSON_VISIT_NOTIFICATION_TEST_TELEPHONE_NUMBER: StorageVariableHolder = (
        StorageVariableHolder(
            "POLIBASE_PERSON_VISIT_NOTIFICATION_TEST_TELEPHONE_NUMBER", None
        )
    )

    POLIBASE_PERSON_REVIEW_NOTIFICATION_TEST_TELEPHONE_NUMBER: StorageVariableHolder = (
        StorageVariableHolder(
            "POLIBASE_PERSON_REVIEW_NOTIFICATION_TEST_TELEPHONE_NUMBER", None
        )
    )

    WHATSAPP_SENDING_MESSAGES_VIA_WAPPI_IS_ON: BoolStorageVariableHolder = (
        BoolStorageVariableHolder("WHATSAPP_SENDING_MESSAGES_VIA_WAPPI_IS_ON", True)
    )

    WHATSAPP_BUFFERED_MESSAGE_MIN_DELAY_IN_MILLISECONDS: IntStorageVariableHolder = (
        IntStorageVariableHolder(
            "WHATSAPP_BUFFERED_MESSAGE_MIN_DELAY_IN_MILLISECONDS", 6000
        )
    )

    WHATSAPP_BUFFERED_MESSAGE_MAX_DELAY_IN_MILLISECONDS: IntStorageVariableHolder = (
        IntStorageVariableHolder(
            "WHATSAPP_BUFFERED_MESSAGE_MAX_DELAY_IN_MILLISECONDS", 12000
        )
    )

    WHATSAPP_MESSAGE_SENDER_USER_LOGIN: StorageVariableHolder = StorageVariableHolder(
        "WHATSAPP_MESSAGE_SENDER_USER_LOGIN", "Administrator"
    )

    POLIBASE_WAS_EMERGENCY_CLOSED_NOTIFICATION_TEXT: StorageVariableHolder = StorageVariableHolder(
        "POLIBASE_WAS_EMERGENCY_CLOSED_NOTIFICATION_TEXT",
        "к сожалениию наш Полибейс поломался и был аварийно закрыт, ожидайте сообщение о просьбе переоткрыть его!",
    )

    POLIBASE_WAS_RESTARTED_NOTIFICATION_TEXT: StorageVariableHolder = (
        StorageVariableHolder(
            "POLIBASE_WAS_RESTARTED_NOTIFICATION_TEXT",
            "Полибейс перезагружен, можете переоткрыть его.",
        )
    )

    WORKSTATION_SHUTDOWN_TIME: TimeStorageVariableHolder = TimeStorageVariableHolder(
        "WORKSTATION_SHUTDOWN_TIME", "21:00"
    )

    WORKSTATION_REBOOT_TIME: TimeStorageVariableHolder = TimeStorageVariableHolder(
        "WORKSTATION_REBOOT_TIME", "21:00"
    )

    EMAIL_VALIDATION_IS_ON: BoolStorageVariableHolder = BoolStorageVariableHolder(
        "EMAIL_VALIDATION_IS_ON", True
    )
    EMAIL_VALIDATION_TEST: BoolStorageVariableHolder = BoolStorageVariableHolder(
        "EMAIL_VALIDATION_TEST", False
    )

    CHILLER_ALERT_TEMPERATURE: FloatStorageVariableHolder = FloatStorageVariableHolder(
        "CHILLER_ALERT_TEMPERATURE", 17.0
    )

    CHILLER_COUNT_DEFAULT: FloatStorageVariableHolder = FloatStorageVariableHolder(
        "CHILLER_COUNT_DEFAULT", 3
    )

    CHILLER_MAX_TEMPERATURE: IntStorageVariableHolder = IntStorageVariableHolder(
        "CHILLER_MAX_TEMPERATURE", 17
    )

    CHILLER_MIN_TEMPERATURE: IntStorageVariableHolder = IntStorageVariableHolder(
        "CHILLER_MIN_TEMPERATURE", 10
    )

    CHILLER_ACTION_MAX_TEMPERATURE: IntStorageVariableHolder = IntStorageVariableHolder(
        "CHILLER_ACTION_MAX_TEMPERATURE", 15
    )

    CHILLER_ACTION_MIN_TEMPERATURE: IntStorageVariableHolder = IntStorageVariableHolder(
        "CHILLER_ACTION_MIN_TEMPERATURE", 12
    )

    CT_ROOM_MAX_TEMPERATURE: IntStorageVariableHolder = IntStorageVariableHolder(
        "CT_ROOM_MAX_TEMPERATURE", 24
    )

    CT_ROOM_MIN_TEMPERATURE: IntStorageVariableHolder = IntStorageVariableHolder(
        "CT_ROOM_MIN_TEMPERATURE", 20
    )

    CT_ROOM_MAX_HUMIDITY: IntStorageVariableHolder = IntStorageVariableHolder(
        "CT_ROOM_MAX_HUMIDITY", 60
    )

    CT_ROOM_MIN_HUMIDITY: IntStorageVariableHolder = IntStorageVariableHolder(
        "CT_ROOM_MIN_HUMIDITY", 30
    )


class PARAM_ITEMS:
    NAME: ParamItem = ParamItem(FIELD_NAME_COLLECTION.NAME, "")
    IP_ADDRESS: ParamItem = ParamItem(FIELD_NAME_COLLECTION.IP_ADDRESS, "")
    VALUE: ParamItem = ParamItem(FIELD_NAME_COLLECTION.VALUE, "")
    PID: ParamItem = ParamItem(FIELD_NAME_COLLECTION.PID, "")
    PIN: ParamItem = ParamItem(FIELD_NAME_COLLECTION.PIN, "")
    STATUS: ParamItem = ParamItem(FIELD_NAME_COLLECTION.STATUS, "")
    PERSON_PIN: ParamItem = ParamItem(
        FIELD_NAME_COLLECTION.PERSON_PIN, "Идентификационный номер пациента"
    )
    PERSON_NAME: ParamItem = ParamItem(FIELD_NAME_COLLECTION.PERSON_NAME, "")
    REGISTRATOR_PERSON_NAME: ParamItem = ParamItem(
        FIELD_NAME_COLLECTION.REGISTRATOR_PERSON_NAME, ""
    )
    REGISTRATOR_PERSON_PIN: ParamItem = ParamItem(
        FIELD_NAME_COLLECTION.REGISTRATOR_PERSON_PIN, ""
    )
    CARD_REGISTRY_FOLDER: ParamItem = ParamItem(
        FIELD_NAME_COLLECTION.CARD_REGISTRY_FOLDER, ""
    )
    DESCRIPTION: ParamItem = ParamItem(FIELD_NAME_COLLECTION.DESCRIPTION, "")
    DESTINATION: ParamItem = ParamItem(FIELD_NAME_COLLECTION.DESTINATION, "")
    COUNT: ParamItem = ParamItem(FIELD_NAME_COLLECTION.COUNT, "Количество")
    TELEPHONE_NUMBER: ParamItem = ParamItem(
        FIELD_NAME_COLLECTION.TELEPHONE_NUMBER, "Телефонный номер"
    )
    TAB_NUMBER: ParamItem = ParamItem(
        FIELD_NAME_COLLECTION.TAB_NUMBER, "Табельный номер"
    )
    PASSWORD: ParamItem = ParamItem(FIELD_NAME_COLLECTION.PASSWORD, "")
    ID: ParamItem = ParamItem(FIELD_NAME_COLLECTION.ID, "Id")
    LOGIN: ParamItem = ParamItem(USER_PROPERTIES.LOGIN, "Login of user")
    FULL_NAME: ParamItem = ParamItem(FIELD_NAME_COLLECTION.FULL_NAME, "Name of user")
    TYPE: ParamItem = ParamItem(FIELD_NAME_COLLECTION.TYPE, "Type")
    SERVICE_NAME: ParamItem = ParamItem("service_name", "Name of service")
    PARAMETERS: ParamItem = ParamItem("parameters", "Parameters", optional=True)
    TAG: ParamItem = ParamItem("tag", "Tag")
    EMAIL: ParamItem = (ParamItem(FIELD_NAME_COLLECTION.EMAIL, ""),)
    INPATIENT: ParamItem = ParamItem("inpatient", "")
    PATH: ParamItem = ParamItem("path", "Путь к файлу")
    DOCUMENT_NAME: ParamItem = ParamItem("document_name", "Имя документа")


class Events(Enum):
    DEBUG: EventDescription = EventDescription(
        "It is a debug event", LogMessageChannels.POLIBASE, LogMessageFlags.DEBUG.value
    )

    PRINTER_REPORT: EventDescription = EventDescription(
        "Принтер {printer_name} ({location}):\n {printer_report}",
        LogMessageChannels.PRINTER,
        LogMessageFlags.NORMAL,
        (
            ParamItem("printer_name", "Name of printer"),
            ParamItem("location", "Location"),
            ParamItem("printer_report", "Printer report"),
        ),
    )
    #
    ADD_JOURNAL_RECORD: EventDescription = EventDescription(
        "{tag_string}. {type_string}. {samAccountName} сделал запись в журнале. {title}: {text}.",
        LogMessageChannels.JOURNAL,
        (LogMessageFlags.NORMAL, LogMessageFlags.SAVE),
        (
            PARAM_ITEMS.TAG,
            PARAM_ITEMS.TYPE,
            PARAM_ITEMS.LOGIN,
            ParamItem("title", "Title"),
            ParamItem("text", "Text"),
            ParamItem("tag_string", "Tag string"),
            ParamItem("type_string", "Type string"),
            PARAM_ITEMS.PARAMETERS,
        ),
        invisible_list=(5, 6),
    )
    #
    LOG_IN: EventDescription = EventDescription(
        "Пользователь {} ({}) вошел с компьютера {}",
        LogMessageChannels.IT,
        LogMessageFlags.NORMAL,
        (
            PARAM_ITEMS.FULL_NAME,
            PARAM_ITEMS.LOGIN,
            ParamItem("computer_name", "Name of computer"),
        ),
    )

    SESSION_STARTED: EventDescription = EventDescription(
        "Пользователь {} ({}) начал пользоваться программой {}.\nВерсия: {}.\nНазвание компьютера: {}",
        LogMessageChannels.IT,
        LogMessageFlags.NORMAL,
        (
            PARAM_ITEMS.FULL_NAME,
            PARAM_ITEMS.LOGIN,
            ParamItem("app_name", "Name of user"),
            ParamItem("version", "Version"),
            ParamItem("computer_name", "Name of computer"),
        ),
    )

    SERVICE_WAS_STARTED: EventDescription = EventDescription(
        "Сервис {service_name} запущен!\nИмя хоста: {host_name}\nПорт: {port}\nИдентификатор процесса: {pid}\n",
        LogMessageChannels.SERVICES,
        LogMessageFlags.NORMAL,
        (
            PARAM_ITEMS.SERVICE_NAME,
            ParamItem("host_name", "Name of host"),
            ParamItem("port", "Port"),
            ParamItem("pid", "PID"),
            ParamItem("service_information", "Service information"),
        ),
    )

    SERVICE_WAS_STOPPED: EventDescription = EventDescription(
        "Сервис {service_name} остановлен!",
        LogMessageChannels.SERVICES,
        LogMessageFlags.NORMAL,
        (
            PARAM_ITEMS.SERVICE_NAME,
            ParamItem("service_information", "Service information"),
        ),
    )

    SERVICE_WAS_NOT_STARTED: EventDescription = EventDescription(
        "Сервис {service_name} не запущен!\nИмя хоста: {host_name}\nПорт: {port}\nОшибка:{error}",
        LogMessageChannels.SERVICES,
        LogMessageFlags.ERROR,
        (
            PARAM_ITEMS.SERVICE_NAME,
            ParamItem("host_name", "Name of host"),
            ParamItem("port", "Port"),
            ParamItem("error", "Error"),
            ParamItem("service_information", "Service information"),
        ),
    )

    SERVICE_IS_INACCESIBLE_AND_WILL_BE_RESTARTED: EventDescription = EventDescription(
        "Сервис {service_name} недоступен и будет перезапущен!",
        LogMessageChannels.SERVICES,
        LogMessageFlags.ERROR,
        (
            PARAM_ITEMS.SERVICE_NAME,
            ParamItem("service_information", "Service  information"),
        ),
    )

    WHATSAPP_MESSAGE_RECEIVED: EventDescription = EventDescription(
        "Получено сообщение",
        LogMessageChannels.POLIBASE,
        LogMessageFlags.SILENCE,
        (ParamItem("message", "Сообщение"),),
    )

    NEW_FILE_DETECTED: EventDescription = EventDescription(
        "Новый файл",
        LogMessageChannels.IT,
        LogMessageFlags.SILENCE,
        (PARAM_ITEMS.PATH,),
    )

    NEW_POLIBASE_DOCUMENT_DETECTED: EventDescription = EventDescription(
        lambda args: [
            "Новый Polibase документ: {path}",
            "Polibase документ: {path} обработан",
        ][args[PARAM_ITEMS.STATUS.name]],
        LogMessageChannels.POLIBASE,
        (LogMessageFlags.NOTIFICATION, LogMessageFlags.SAVE_ONCE),
        (
            PARAM_ITEMS.PERSON_PIN,
            PARAM_ITEMS.PATH,
            PARAM_ITEMS.DOCUMENT_NAME,
            PARAM_ITEMS.STATUS,
        ),
        (PARAM_ITEMS.PATH.name,),
    )

    COMPUTER_WAS_STARTED: EventDescription = EventDescription(
        "Компьютер {name} загрузился",
        LogMessageChannels.IT,
        LogMessageFlags.NORMAL,
        (ParamItem("name", "Название компьютера"),),
    )

    SERVER_WAS_STARTED: EventDescription = EventDescription(
        "Сервер {name} загрузился",
        LogMessageChannels.IT,
        LogMessageFlags.NORMAL,
        (ParamItem("name", "Название сервера"),),
    )

    RESOURCE_INACCESSABLE: EventDescription = EventDescription(
        "Ресурс {resource_name} недоступен. {reason_string}",
        LogMessageChannels.RESOURCES,
        LogMessageFlags.ERROR,
        (
            ParamItem("resource_name", "Название ресурса"),
            ParamItem("resource", "Ресурс"),
            ParamItem("at_first_time", "Признак первого раза"),
            ParamItem("reason_string", "Строка причины"),
            ParamItem("reason", "Причины", optional=True),
        ),
    )

    RESOURCE_ACCESSABLE: EventDescription = EventDescription(
        "Ресурс {resource_name} доступен",
        LogMessageChannels.RESOURCES,
        LogMessageFlags.NORMAL,
        (
            ParamItem("resource_name", "Название ресурса"),
            ParamItem("resource", "Ресурс"),
            ParamItem("at_first_time", "Признак первого раза"),
        ),
    )

    #
    BACKUP_ROBOCOPY_JOB_WAS_STARTED: EventDescription = EventDescription(
        "Robocopy: Начато выполнение задания: {name}. PID процесса: {pid}",
        LogMessageChannels.BACKUP,
        (LogMessageFlags.NOTIFICATION, LogMessageFlags.SAVE_ONCE),
        (PARAM_ITEMS.NAME, PARAM_ITEMS.PID),
        (PARAM_ITEMS.NAME.name,),
    )

    BACKUP_ROBOCOPY_JOB_WAS_COMPLETED: EventDescription = EventDescription(
        "Robocopy: Завершено выполнение задания: {name}. Статус: {status_string}",
        LogMessageChannels.BACKUP,
        (LogMessageFlags.NOTIFICATION, LogMessageFlags.SAVE),
        (PARAM_ITEMS.NAME, ParamItem("status_string", ""), PARAM_ITEMS.STATUS),
    )
    #
    POLIBASE_CREATION_DB_DUMP_START: EventDescription = EventDescription(
        "Базы данных Polibase: Начато создание дампа",
        LogMessageChannels.BACKUP,
        (LogMessageFlags.NORMAL, LogMessageFlags.SAVE),
    )

    POLIBASE_CREATION_DB_DUMP_COMPLETE: EventDescription = EventDescription(
        "Базы данных Polibase: Завершено создание дампа. Размер: {size}",
        LogMessageChannels.BACKUP,
        (LogMessageFlags.NORMAL, LogMessageFlags.SAVE),
        (ParamItem("size", ""),),
    )

    POLIBASE_CREATION_ARCHIVED_DB_DUMP_START: EventDescription = EventDescription(
        "Базы данных Polibase: Начато архивирование дампа",
        LogMessageChannels.BACKUP,
        LogMessageFlags.NORMAL,
    )

    POLIBASE_CREATION_ARCHIVED_DB_DUMP_COMPLETE: EventDescription = EventDescription(
        "Базы данных Polibase: Завершено архивирование дампа. Размер: {size}",
        LogMessageChannels.BACKUP,
        (LogMessageFlags.NORMAL, LogMessageFlags.SAVE),
        (ParamItem("size", ""),),
    )

    POLIBASE_COPING_ARCHIVED_DB_DUMP_START: EventDescription = EventDescription(
        "Базы данных Polibase: Начато копирование архивированного дампа на {}",
        LogMessageChannels.BACKUP,
        LogMessageFlags.NORMAL,
        [PARAM_ITEMS.DESTINATION],
    )

    POLIBASE_COPING_ARCHIVED_DB_DUMP_COMPLETE: EventDescription = EventDescription(
        "Базы данных Polibase: Завершено копирование архивированного дампа на {}",
        LogMessageChannels.BACKUP,
        LogMessageFlags.NORMAL,
        [PARAM_ITEMS.DESTINATION],
    )

    POLIBASE_COPING_DB_DUMP_START: EventDescription = EventDescription(
        "Базы данных Polibase: Начато копирование дампа на {}",
        LogMessageChannels.BACKUP,
        LogMessageFlags.NORMAL,
        [PARAM_ITEMS.DESTINATION],
    )

    POLIBASE_COPING_DB_DUMP_COMPLETE: EventDescription = EventDescription(
        "Базы данных Polibase: Завершено копирование дампа на {}",
        LogMessageChannels.BACKUP,
        LogMessageFlags.NORMAL,
        [PARAM_ITEMS.DESTINATION],
    )
    #
    HR_NOTIFY_ABOUT_NEW_EMPLOYEE: EventDescription = EventDescription(
        "День добрый, {hr_given_name}.\nДокументы для нового сотрудника: {employee_full_name} готовы!\nЕго корпоративная почта: {employee_email}.",
        LogMessageChannels.HR,
        LogMessageFlags.NOTIFICATION.value,
        (
            ParamItem("hr_given_name", "Имя руководителя отдела HR"),
            ParamItem("employee_full_name", "ФИО нового сотрудника"),
            ParamItem("employee_email", "Корпаротивная почта нового сотрудника"),
        ),
    )
    #
    IT_NOTIFY_ABOUT_CREATE_USER: EventDescription = EventDescription(
        "Добрый день, отдел Информационных технологий.\nДокументы для нового пользователя: {} готовы!\nОписание: {}\nЛогин: {}\nПароль: {}\nТелефон: {}\nЭлектронная почта: {}\nДополнительная информация: {}",
        LogMessageChannels.IT,
        LogMessageFlags.NOTIFICATION.value,
        (
            PARAM_ITEMS.NAME,
            ParamItem("description", ""),
            PARAM_ITEMS.LOGIN,
            PARAM_ITEMS.PASSWORD,
            PARAM_ITEMS.TELEPHONE_NUMBER,
            ParamItem("email", ""),
            ParamItem("information", ""),
        ),
    )

    IT_NOTIFY_ABOUT_CREATE_PERSON: EventDescription = EventDescription(
        "Добрый день, отдел Информационных технологий.\nДокументы для новой персоны: {name} готовы!\nОписание: {description}\nЭлектронная почта: {email}\nПароль: {password}\nТелефон: {telephoneNumber}",
        LogMessageChannels.IT,
        LogMessageFlags.NOTIFICATION.value,
        (
            PARAM_ITEMS.NAME,
            ParamItem("description", ""),
            ParamItem("email", ""),
            PARAM_ITEMS.PASSWORD,
            PARAM_ITEMS.TELEPHONE_NUMBER,
        ),
    )

    IT_NOTIFY_ABOUT_CREATE_MARK: EventDescription = EventDescription(
        "Добрый день, отдел Информационных технологий.\nКарта доступа для новой персоны: {name} готова!\nТелефон: {telephoneNumber}\nНомер карты доступа: {TabNumber}\nГруппа доступа: {group_name}",
        LogMessageChannels.IT,
        LogMessageFlags.NOTIFICATION.value,
        (
            PARAM_ITEMS.NAME,
            PARAM_ITEMS.TELEPHONE_NUMBER,
            PARAM_ITEMS.TAB_NUMBER,
            ParamItem("group_name", ""),
        ),
    )

    IT_NOTIFY_ABOUT_CREATE_TEMPORARY_MARK: EventDescription = EventDescription(
        "Добрый день, отдел Информационных технологий.\nВременная карта доступа для персоны: {name} готова!\nНомер карты: {TabNumber}\nТелефон: {telephoneNumber}",
        LogMessageChannels.IT,
        LogMessageFlags.NOTIFICATION.value,
        (PARAM_ITEMS.NAME, PARAM_ITEMS.TAB_NUMBER, PARAM_ITEMS.TELEPHONE_NUMBER),
    )

    IT_NOTIFY_ABOUT_TEMPORARY_MARK_RETURN: EventDescription = EventDescription(
        "Добрый день, отдел Информационных технологий.\nВременная карта доступа для персоны: {name} возвращена!\nНомер карты: {TabNumber}",
        LogMessageChannels.IT,
        LogMessageFlags.NOTIFICATION.value,
        (PARAM_ITEMS.NAME, PARAM_ITEMS.TAB_NUMBER),
    )

    IT_NOTIFY_ABOUT_MARK_RETURN: EventDescription = EventDescription(
        "Добрый день, отдел Информационных технологий.\nКарта доступа для персоны: {name} возвращена!\nНомер карты: {TabNumber}",
        LogMessageChannels.IT,
        LogMessageFlags.NOTIFICATION.value,
        (PARAM_ITEMS.NAME, PARAM_ITEMS.TAB_NUMBER),
    )

    IT_TASK_AFTER_CREATE_USER: EventDescription = EventDescription(
        "Добрый день, {it_user_name}.\nНеобходимо создать ящик электронной почту для пользователя: {name}\nАдресс электронной почты: {mail}\nПароль: {password}",
        LogMessageChannels.IT,
        LogMessageFlags.TASK.value,
        (
            ParamItem("it_user_name", ""),
            PARAM_ITEMS.NAME,
            ParamItem("mail", ""),
            PARAM_ITEMS.PASSWORD,
        ),
    )

    IT_TASK_AFTER_CREATE_PERSON: EventDescription = EventDescription(
        "Добрый день, {it_user_name}.\nНеобходимо создать ящик электронной почты почту для персоны: {name}\nАдресс электронной почты: {mail}\nПароль: {password}",
        LogMessageChannels.IT,
        LogMessageFlags.TASK.value,
        (
            ParamItem("it_user_name", ""),
            PARAM_ITEMS.NAME,
            ParamItem("mail", ""),
            PARAM_ITEMS.PASSWORD,
        ),
    )

    WATCHABLE_WORKSTATION_IS_NOT_ACCESSABLE: EventDescription = EventDescription(
        "Компьютер {} вне сети",
        LogMessageChannels.RESOURCES,
        LogMessageFlags.ERROR,
        [PARAM_ITEMS.NAME],
    )

    WATCHABLE_WORKSTATION_IS_ACCESSABLE: EventDescription = EventDescription(
        "Компьютер {} в сети",
        LogMessageChannels.RESOURCES,
        LogMessageFlags.NORMAL,
        [PARAM_ITEMS.NAME],
    )

    SERVER_IS_NOT_ACCESSABLE: EventDescription = EventDescription(
        "Сервер {} вне сети",
        LogMessageChannels.RESOURCES,
        (LogMessageFlags.ERROR, LogMessageFlags.SAVE_ONCE),
        (PARAM_ITEMS.NAME,),
    )

    SERVER_IS_ACCESSABLE: EventDescription = EventDescription(
        "Сервер {} в сети",
        LogMessageChannels.RESOURCES,
        (LogMessageFlags.NORMAL, LogMessageFlags.SAVE_ONCE),
        (PARAM_ITEMS.NAME,),
    )

    # INDICATION_DEVICES

    INDICATION_DEVICES_WAS_REGISTERED: EventDescription = EventDescription(
        "Устройство индикации: {} ({}) зарегистрировано. Адресс: {}",
        LogMessageChannels.RESOURCES,
        (LogMessageFlags.NOTIFICATION, LogMessageFlags.SAVE_ONCE),
        (PARAM_ITEMS.NAME, PARAM_ITEMS.DESCRIPTION, PARAM_ITEMS.IP_ADDRESS),
        (PARAM_ITEMS.NAME.name,),
    )

    # MRI

    MRI_CHILLER_FILTER_WAS_CHANGED: EventDescription = EventDescription(
        "Фильтр водяного охлаждения МРТ был заменён. Количество оставшихся фильтров: {}",
        LogMessageChannels.RESOURCES,
        (LogMessageFlags.NOTIFICATION, LogMessageFlags.SAVE),
        (PARAM_ITEMS.COUNT,),
    )

    MRI_CHILLER_TEMPERATURE_ALERT_WAS_FIRED: EventDescription = EventDescription(
        "Превышена температура чиллера",
        LogMessageChannels.RESOURCES,
        (LogMessageFlags.ERROR, LogMessageFlags.SAVE),
    )

    MRI_CHILLER_TEMPERATURE_ALERT_WAS_RESOLVED: EventDescription = EventDescription(
        "Проблема повышенной температуры чиллера была решена",
        LogMessageChannels.RESOURCES,
        (LogMessageFlags.NOTIFICATION, LogMessageFlags.SAVE),
    )

    MRI_CHILLER_WAS_TURNED_OFF: EventDescription = EventDescription(
        "Чиллер был выключен",
        LogMessageChannels.RESOURCES,
        (LogMessageFlags.NOTIFICATION, LogMessageFlags.SAVE),
    )

    MRI_CHILLER_WAS_TURNED_ON: EventDescription = EventDescription(
        "Чиллер был включен",
        LogMessageChannels.RESOURCES,
        (LogMessageFlags.NOTIFICATION, LogMessageFlags.SAVE),
    )

    # POLIBASE

    POLIBASE_PERSON_DUPLICATION_WAS_DETECTED: EventDescription(
        "Регистратор {registrator_person_name} создал персону {person_name} ({person_pin}), которая дублирует {duplicated_person_name} ({duplicated_person_pin})",
        LogMessageChannels.POLIBASE_ERROR,
        LogMessageFlags.SAVE,
        (
            ParamItem("person_name", ""),
            PARAM_ITEMS.PERSON_PIN,
            ParamItem("duplicated_person_name", ""),
            ParamItem("duplicated_person_pin", ""),
            ParamItem("registrator_person_name", ""),
        ),
    )

    POLIBASE_PERSON_VISIT_WAS_REGISTERED: EventDescription = EventDescription(
        "Зарегистрировано новое посещение: {name} ({type_string})",
        LogMessageChannels.POLIBASE,
        LogMessageFlags.NOTIFICATION,
        (PARAM_ITEMS.NAME, ParamItem("type_string", ""), ParamItem("visit", "")),
    )

    POLIBASE_PERSON_WAS_CREATED: EventDescription = EventDescription(
        "Создана полибейс персона: {name} ({pin})",
        LogMessageChannels.POLIBASE,
        LogMessageFlags.NOTIFICATION,
        (PARAM_ITEMS.NAME, PARAM_ITEMS.PIN, PARAM_ITEMS.VALUE),
    )

    MAIL_TO_POLIBASE_PERSON_WAS_SENT: EventDescription = EventDescription(
        "Почта с медицинской записью {id} была отправлена пациенту: {pin}",
        LogMessageChannels.POLIBASE,
        LogMessageFlags.NOTIFICATION,
        (PARAM_ITEMS.ID, PARAM_ITEMS.PIN),
    )

    POLIBASE_PERSON_WAS_UPDATED: EventDescription = EventDescription(
        "Обновлена полибейс персона: {name} ({pin})",
        LogMessageChannels.POLIBASE,
        LogMessageFlags.SILENCE,
        (PARAM_ITEMS.NAME, PARAM_ITEMS.PIN, PARAM_ITEMS.VALUE),
    )

    POLIBASE_PERSON_VISIT_NOTIFICATION_WAS_REGISTERED: EventDescription = (
        EventDescription(
            "Зарегистрировано новое уведомление о посещении: {name} ({type_string})",
            LogMessageChannels.POLIBASE,
            LogMessageFlags.SILENCE,
            (
                PARAM_ITEMS.NAME,
                ParamItem("type_string", ""),
                ParamItem("notification", ""),
            ),
        )
    )

    POLIBASE_PERSON_REVIEW_NOTIFICATION_WAS_REGISTERED: EventDescription = (
        EventDescription(
            None,
            LogMessageChannels.POLIBASE,
            (LogMessageFlags.SAVE_ONCE, LogMessageFlags.SILENCE),
            (PARAM_ITEMS.PERSON_PIN, PARAM_ITEMS.INPATIENT),
            (PARAM_ITEMS.PERSON_PIN.name,),
        )
    )

    POLIBASE_PERSON_REVIEW_NOTIFICATION_WAS_ANSWERED: EventDescription = (
        EventDescription(
            "Пациент ({}) ответил на уведомление об отзыве: {}",
            LogMessageChannels.POLIBASE,
            LogMessageFlags.SAVE_ONCE,
            (PARAM_ITEMS.PERSON_PIN, PARAM_ITEMS.STATUS),
            (PARAM_ITEMS.PERSON_PIN.name,),
        )
    )

    POLIBASE_PERSONS_WITH_OLD_FORMAT_BARCODE_WAS_DETECTED: EventDescription = EventDescription(
        "Полибейс: обнаружены пациенты со старым форматом или отсутствующим штрих-кодом",
        LogMessageChannels.POLIBASE,
        LogMessageFlags.SILENCE,
        (PARAM_ITEMS.PERSON_PIN,),
    )

    POLIBASE_PERSON_BARCODES_WITH_OLD_FORMAT_WERE_CREATED: EventDescription = (
        EventDescription(
            "Полибейс: все новые штрих-коды созданы",
            LogMessageChannels.POLIBASE,
            LogMessageFlags.SILENCE,
            [PARAM_ITEMS.PERSON_PIN],
        )
    )

    POLIBASE_PERSON_WITH_INACCESSABLE_EMAIL_WAS_DETECTED: EventDescription = EventDescription(
        "Пациент {} ({}) имеет недоступную электронную почту: {}. Регистратор: {}, компьютер: {} ({})",
        LogMessageChannels.POLIBASE_ERROR,
        LogMessageFlags.SAVE,
        [
            ParamItem(FIELD_NAME_COLLECTION.PERSON_NAME, ""),
            PARAM_ITEMS.PERSON_PIN,
            PARAM_ITEMS.EMAIL,
            PARAM_ITEMS.REGISTRATOR_PERSON_NAME,
            ParamItem(FIELD_NAME_COLLECTION.WORKSTATION_NAME, ""),
            ParamItem(FIELD_NAME_COLLECTION.WORKSTATION_DESCRIPTION, ""),
        ],
    )

    POLIBASE_PERSON_EMAIL_WAS_ADDED: EventDescription = EventDescription(
        "Электронная почта пациента {} ({}): {} была добавлена",
        LogMessageChannels.POLIBASE,
        (LogMessageFlags.RESULT, LogMessageFlags.SAVE),
        [
            ParamItem(FIELD_NAME_COLLECTION.PERSON_NAME, ""),
            PARAM_ITEMS.PERSON_PIN,
            PARAM_ITEMS.EMAIL,
        ],
    )

    POLIBASE_PERSON_BONUSES_WAS_UPDATED: EventDescription = EventDescription(
        # "Бонусы пациента {} ({}) обновились",
        "Бонусы пациента {} обновились",
        LogMessageChannels.POLIBASE,
        (LogMessageFlags.NOTIFICATION),
        [
            # PARAM_ITEMS.PERSON_NAME,
            PARAM_ITEMS.PERSON_PIN,
        ],
    )

    ACTION_WAS_DONE: EventDescription = EventDescription(
        'Совершено действие {} ("{}").\nДействие совершил: {} ({}).\nПараметры действия: {}.\nПринудительное действие: {}.',
        LogMessageChannels.DEBUG,
        LogMessageFlags.SAVE,
        [
            ParamItem(FIELD_NAME_COLLECTION.ACTION_DESCRIPTION, ""),
            ParamItem(FIELD_NAME_COLLECTION.ACTION_NAME, ""),
            ParamItem(FIELD_NAME_COLLECTION.NAME, ""),
            ParamItem(FIELD_NAME_COLLECTION.LOGIN, ""),
            ParamItem(FIELD_NAME_COLLECTION.PARAMETERS, ""),
            ParamItem(FIELD_NAME_COLLECTION.FORCED, ""),
        ],
    )

    ACTION_HAVE_TO_BE_DONE: EventDescription = EventDescription(
        "Необходимо совершить действие {}: {}",
        LogMessageChannels.DEBUG,
        LogMessageFlags.SAVE,
        [
            ParamItem(FIELD_NAME_COLLECTION.ACTION_NAME, ""),
            ParamItem(FIELD_NAME_COLLECTION.ACTION_DESCRIPTION, ""),
        ],
    )

    NEW_EMAIL_MESSAGE_WAS_RECEIVED: EventDescription = EventDescription(
        "Почтовый ящик: {mailbox}\nНовое письмо было получено от {from}: {title}.",
        LogMessageChannels.NEW_EMAIL,
        LogMessageFlags.NOTIFICATION,
        [
            ParamItem("mailbox", ""),
            ParamItem(FIELD_NAME_COLLECTION.TITLE, ""),
            ParamItem("from", ""),
            PARAM_ITEMS.VALUE,
        ],
    )

    CARD_REGISTRY_FOLDER_WAS_SET_FOR_POLIBASE_PERSON: EventDescription = (
        EventDescription(
            'Карта пациента: {} добавлена в папку "{}".\nДействие совершил: {} ({})',
            LogMessageChannels.CARD_REGISTRY,
            LogMessageFlags.SAVE_ONCE,
            [
                PARAM_ITEMS.PERSON_PIN,
                PARAM_ITEMS.CARD_REGISTRY_FOLDER,
                PARAM_ITEMS.REGISTRATOR_PERSON_NAME,
                PARAM_ITEMS.REGISTRATOR_PERSON_PIN,
            ],
            (PARAM_ITEMS.PERSON_PIN.name,),
        )
    )

    CARD_REGISTRY_FOLDER_WAS_SET_NOT_FROM_POLIBASE_FOR_POLIBASE_PERSON: EventDescription = EventDescription(
        "Карта пациента: {} добавлена не с помощью Полибейс",
        LogMessageChannels.CARD_REGISTRY,
        LogMessageFlags.SAVE_ONCE,
        (PARAM_ITEMS.PERSON_PIN,),
    )

    CARD_REGISTRY_SUITABLE_FOLDER_WAS_SET_FOR_POLIBASE_PERSON: EventDescription = EventDescription(
        'Карта пациента: {} добавлена в подходящую папку "{}".\nДействие совершил: {} ({})',
        LogMessageChannels.CARD_REGISTRY,
        LogMessageFlags.NOTIFICATION,
        [
            PARAM_ITEMS.PERSON_PIN,
            PARAM_ITEMS.CARD_REGISTRY_FOLDER,
            PARAM_ITEMS.REGISTRATOR_PERSON_NAME,
            PARAM_ITEMS.REGISTRATOR_PERSON_PIN,
        ],
    )

    CARD_REGISTRY_FOLDER_WAS_REGISTERED: EventDescription = EventDescription(
        "Папка с картами пациентов: {} добавлена в реестр карт пациентов. Положение: шкаф: {}; полка: {}; место на полке: {}",
        LogMessageChannels.CARD_REGISTRY,
        LogMessageFlags.SAVE_ONCE,
        (
            PARAM_ITEMS.CARD_REGISTRY_FOLDER,
            ParamItem("p_a", ""),
            ParamItem("p_b", ""),
            ParamItem("p_c", ""),
        ),
        (PARAM_ITEMS.CARD_REGISTRY_FOLDER.name,),
    )

    CARD_REGISTRY_FOLDER_START_CARD_SORTING: EventDescription = EventDescription(
        'Начат процесс сортировки карта пациентов в папке реестра карт "{}"',
        LogMessageChannels.CARD_REGISTRY,
        LogMessageFlags.SAVE,
        [PARAM_ITEMS.CARD_REGISTRY_FOLDER],
    )

    CARD_REGISTRY_FOLDER_COMPLETE_CARD_SORTING: EventDescription = EventDescription(
        'Закончен процесс сортировки карта пациентов в папке реестра карт "{}"',
        LogMessageChannels.CARD_REGISTRY,
        LogMessageFlags.SAVE,
        [PARAM_ITEMS.CARD_REGISTRY_FOLDER],
    )

    EMPLOYEE_CHECKED_IN: EventDescription = EventDescription(
        "Сотрудник {} отметился на приход",
        LogMessageChannels.TIME_TRACKING,
        LogMessageFlags.NOTIFICATION,
        [PARAM_ITEMS.NAME],
    )

    EMPLOYEE_CHECKED_OUT: EventDescription = EventDescription(
        "Сотрудник {} отметился на выход",
        LogMessageChannels.TIME_TRACKING,
        LogMessageFlags.NOTIFICATION,
        [PARAM_ITEMS.NAME],
    )


class Actions(Enum):
    CHILLER_FILTER_CHANGING: ActionDescription = ActionDescription(
        "CHILLER_FILTER_CHANGING",
        ("filter",),
        "Замена фильтра очистки воды",
        "Заменить фильтр очистки воды",
    )

    SWITCH_TO_EXTERNAL_WATER_SOURCE: ActionDescription = ActionDescription(
        "SWITCH_TO_EXTERNAL_WATER_SOURCE",
        ("external_ws",),
        "Переход на внешнее (городское) водоснабжение",
        "Перейти на внешнее (городское) водоснабжение",
    )

    SWITCH_TO_INTERNAL_WATER_SOURCE: ActionDescription = ActionDescription(
        "SWITCH_TO_INTERNAL_WATER_SOURCE",
        ("internal_ws",),
        "Переход на внутреннее водоснабжение",
        "Перейти на внутреннее водоснабжение",
    )

    VALENTA_SYNCHRONIZATION: ActionDescription = ActionDescription(
        "VALENTA_SYNCHRONIZATION",
        ("valenta", "валента"),
        "Синхронизация Валенты",
        "Совершить синхронизацию для Валенты",
        False,
        True,
        forcable=True,
    )

    TIME_TRACKING_REPORT: ActionDescription = ActionDescription(
        "TIME_TRACKING_REPORT",
        ("tt", "урв"),
        "Отчеты по учёту рабочего времени",
        "Создать",
        False,
        False,
    )

    DOOR_OPEN: ActionDescription = ActionDescription(
        "DOOR_OPEN",
        ("door_open",),
        "Открытие дверей",
        "Открыть",
        False,
        False,
    )

    DOOR_CLOSE: ActionDescription = ActionDescription(
        "DOOR_CLOSE",
        ("door_close",),
        "Закрытие дверей",
        "Закрыть",
        False,
        False,
    )

    ATTACH_SHARED_DISKS: ActionDescription = ActionDescription(
        "ATTACH_SHARED_DISKS",
        ("attach",),
        "Присоединить сетевые диски",
        "Присоединить",
        False,
        True,
    )

    ACTION: ActionDescription = ActionDescription(
        "ACTION",
        ("action",),
        "Неспециализированное действие",
        None,
        False,
        True,
        forcable=True,
    )


class EMAIL:
    SPLITTER: str = "@"


class EMAIL_COLLECTION:
    MAIL_RU_NAME: str = "mail.ru"
    MAIL_RU_DAEMON: str = f"mailer-daemon@corp.{MAIL_RU_NAME}"
    MAIL_RU_IMAP_SERVER: str = f"imap.{MAIL_RU_NAME}"

    NAS: str = EMAIL.SPLITTER.join(("nas", CONST.SITE_ADDRESS))
    IT: str = EMAIL.SPLITTER.join(("it", CONST.SITE_ADDRESS))
    EXTERNAL_MAIL: str = f"mail.{CONST.SITE_NAME}{EMAIL.SPLITTER}{MAIL_RU_NAME}"

    EXTERNAL_MAIL_SERVER: str = MAIL_RU_IMAP_SERVER


class STATISTICS:
    class Types(Enum):
        CT: str = "CT"
        CT_DAY: str = "CT_DAY"
        CT_WEEK: str = "CT_WEEK"
        CT_MONTH: str = "CT_MONTH"
        CHILLER_FILTER: str = MATERIALIZED_RESOURCES.TYPES.CHILLER_FILTER.name
        MRI_COLDHEAD: str = "MRI_COLDHEAD"
        POLIBASE_DATABASE_DUMP: str = "POLIBASE_DATABASE_DUMP"
        POLIBASE_PERSON_REVIEW_NOTIFICATION: str = "POLIBASE_PERSON_REVIEW_NOTIFICATION"


class JournalType(tuple[int, OrderedNameCaptionDescription], Enum):
    TEST: tuple[int, OrderedNameCaptionDescription] = (
        0,
        OrderedNameCaptionDescription("test", "Тест"),
    )
    COMPUTER: tuple[int, OrderedNameCaptionDescription] = (
        1,
        OrderedNameCaptionDescription("computer", "Компьютер"),
    )
    MRI_CHILLER: tuple[int, OrderedNameCaptionDescription] = (
        2,
        OrderedNameCaptionDescription("mri_chiller", "Чиллер МРТ"),
    )
    MRI_GRADIENT_CHILLER: tuple[int, OrderedNameCaptionDescription] = (
        3,
        OrderedNameCaptionDescription("mri_gradient_chiller", "Чиллер градиентов МРТ"),
    )
    MRI_CLOSET_CHILLER: tuple[int, OrderedNameCaptionDescription] = (
        4,
        OrderedNameCaptionDescription("mri_closet_chiller", "Чиллер кабинета МРТ"),
    )
    CHILLER: tuple[int, OrderedNameCaptionDescription] = (
        5,
        OrderedNameCaptionDescription("chiller", "Чиллер"),
    )
    COMMUNICATION_ROOM: tuple[int, OrderedNameCaptionDescription] = (
        6,
        OrderedNameCaptionDescription("communication_room", "Коммутационная комната"),
    )
    SERVER_ROOM: tuple[int, OrderedNameCaptionDescription] = (
        7,
        OrderedNameCaptionDescription("server_room", "Серверная комната"),
    )
    MRI_TECHNICAL_ROOM: tuple[int, OrderedNameCaptionDescription] = (
        8,
        OrderedNameCaptionDescription("mri_technical_room", "Техническая комната МРТ"),
    )
    MRI_PROCEDURAL_ROOM: tuple[int, OrderedNameCaptionDescription] = (
        9,
        OrderedNameCaptionDescription("mri_procedural_room", "Процедурная комната МРТ"),
    )
    PRINTER: tuple[int, OrderedNameCaptionDescription] = (
        10,
        OrderedNameCaptionDescription("printer", "Принтер"),
    )
    SERVER: tuple[int, OrderedNameCaptionDescription] = (
        11,
        OrderedNameCaptionDescription("server", "Сервер"),
    )
    OUTSIDE_SERVER: tuple[int, OrderedNameCaptionDescription] = (
        12,
        OrderedNameCaptionDescription("outside_server", "Внешний сервер"),
    )
    AGREEMENT: tuple[int, OrderedNameCaptionDescription] = (
        13,
        OrderedNameCaptionDescription("agreement", "Договор и счет"),
    )
    XRAY: tuple[int, OrderedNameCaptionDescription] = (
        14,
        OrderedNameCaptionDescription("xray", "Рентген"),
    )
    CASH_REGISTER: tuple[int, OrderedNameCaptionDescription] = (
        15,
        OrderedNameCaptionDescription("cash_register", "Касса"),
    )


class Tag(tuple[int, IconedOrderedNameCaptionDescription], Enum):
    SERVICE: tuple[int, IconedOrderedNameCaptionDescription] = (
        auto(),
        IconedOrderedNameCaptionDescription(
            None, "Обслуживание", None, 4, CONST.VISUAL.GOOD
        ),
    )
    ERROR: tuple[int, IconedOrderedNameCaptionDescription] = (
        auto(),
        IconedOrderedNameCaptionDescription(
            None, "Ошибка", None, 2, CONST.VISUAL.ERROR
        ),
    )
    WARNING: tuple[int, IconedOrderedNameCaptionDescription] = (
        auto(),
        IconedOrderedNameCaptionDescription(
            None, "Внимание", None, 3, CONST.VISUAL.WARNING
        ),
    )
    NOTIFICATION: tuple[int, IconedOrderedNameCaptionDescription] = (
        auto(),
        IconedOrderedNameCaptionDescription(
            None, "Уведомление", None, 1, CONST.VISUAL.NOTIFICATION
        ),
    )
    TASK: tuple[int, IconedOrderedNameCaptionDescription] = (
        auto(),
        IconedOrderedNameCaptionDescription(
            None,
            "Задача",
            None,
            6,
            CONST.VISUAL.TASK,
        ),
    )
    INSPECTION: tuple[int, IconedOrderedNameCaptionDescription] = (
        auto(),
        IconedOrderedNameCaptionDescription(
            None,
            "Осмотр",
            None,
            5,
            CONST.VISUAL.EYE,
        ),
    )
    INFORMATION: tuple[int, IconedOrderedNameCaptionDescription] = (
        auto(),
        IconedOrderedNameCaptionDescription(
            None,
            "Информация",
            None,
            0,
            CONST.VISUAL.INFORMATION,
        ),
    )
