import sys
import importlib.util
from enum import Enum
from collections import defaultdict
from typing import Callable

pih_is_exists = importlib.util.find_spec("pih") is not None
if not pih_is_exists:
    sys.path.append("//pih/facade")
from pih import A
from pih.const import ARGUMENT_PREFIX
from MobileHelperService.api import (
    MobileOutput,
    MobileSession,
    Flags,
    format_given_name,
)
from MobileHelperService.collection import MobileHelperUserSettings
from MobileHelperService.const import (
    MOBILE_HELPER_USER_SETTINGS_NAME,
    MODULE_NAME,
    VERSION,
    ADMIN_ALIAS,
)
from pih.tools import ne, e, n, j, js
from pih import Output, ServiceListener
from pih.tools import ParameterList
from pih.collection import WhatsAppMessage

ANSWER: dict[str, list[str]] = defaultdict(list)


class MOBILE_HELPER:
    @staticmethod
    def start(
        host: bool, admin: bool, standalone: bool, pih_install: bool | None = None
    ) -> bool:
        if pih_install or standalone:
            A.U.install_module(A.root.NAME, A.V.value, True, host)
        if standalone:
            A.U.install_module(MODULE_NAME, VERSION, True, host)
            returncode: bool | None = A.EXC.extract_returncode(
                A.EXC.execute(
                    A.EXC.create_command_for_psexec(
                        [MODULE_NAME, j((ARGUMENT_PREFIX, ADMIN_ALIAS)) if admin else None],
                        host,
                    ),
                    show_output=True,
                ),
                check_on_success=True,
            )
            if n(returncode):
                result: str = str(
                    A.R_SSH.execute(
                        js((MODULE_NAME, j((ARGUMENT_PREFIX, ADMIN_ALIAS)) if admin else "")), host
                    ).data
                )
                return result
            return returncode
        else:
            return A.SRV_A.start(
                A.CT_SR.MOBILE_HELPER,
                False,
                True,
                j((ARGUMENT_PREFIX, ADMIN_ALIAS)) if admin else None,
                host=host
            )

    @staticmethod
    def create_output(recipient: str | Enum) -> Output:
        recipient = recipient if isinstance(recipient, str) else A.D.get(recipient)
        session: MobileSession = MobileSession(recipient, A.D.get(Flags.SILENCE))
        recipient_as_whatsapp_group: bool = recipient.endswith(A.CT_ME_WH.GROUP_SUFFIX)
        output: MobileOutput = MobileOutput(session)
        session.output = output
        if not recipient_as_whatsapp_group:
            output.user.get_formatted_given_name = lambda: format_given_name(
                session, output
            )
            session.say_hello(recipient)
        return output

    @staticmethod
    def waiting_for_input_from(
        recipient: str,
        handler: Callable[[str, Callable[[None], None]], None] | None = None,
    ) -> str | None:
        def internal_handler(
            message: str, close_handler: Callable[[None], None]
        ) -> None:
            ANSWER[recipient].append(message)
            if e(handler):
                close_handler()
            else:
                handler(message, close_handler)

        MOBILE_HELPER.waiting_for_mobile_helper_message_input(
            recipient, internal_handler
        )
        return ANSWER[recipient][-1]

    @staticmethod
    def waiting_for_mobile_helper_message_input(
        recipient: str, handler: Callable[[str, Callable[[None], None]], None]
    ) -> None:
        def internal_handler(
            parameter_list: ParameterList, listener: ServiceListener
        ) -> None:
            message: WhatsAppMessage = A.D_Ex_E.whatsapp_message(parameter_list)
            if ne(message) and A.D_F.telephone_number(
                message.sender
            ) == A.D_F.telephone_number(recipient):
                handler(message.message, listener.close)

        A.E.on_event(internal_handler)

    class SETTINGS:
        class USER:
            @staticmethod
            def get(login: str) -> MobileHelperUserSettings:
                value: MobileHelperUserSettings = MobileHelperUserSettings()
                result: MobileHelperUserSettings | None = A.S_U.get(
                    login, MOBILE_HELPER_USER_SETTINGS_NAME, value
                )
                if n(result):
                    MOBILE_HELPER.SETTINGS.USER.set(login, value)
                    result = value
                return result

            @staticmethod
            def set(login: str, value: MobileHelperUserSettings) -> bool:
                return A.S_U.set(login, MOBILE_HELPER_USER_SETTINGS_NAME, value)
