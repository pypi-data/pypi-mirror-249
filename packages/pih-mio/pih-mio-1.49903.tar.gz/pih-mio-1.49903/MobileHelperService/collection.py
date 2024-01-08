#from MobileHelperService.const import MOBILE_HELPER_USER_SETTINGS_NAME
from dataclasses import dataclass

@dataclass
class MobileHelperUserSettings:
    #name: str = MOBILE_HELPER_USER_SETTINGS_NAME
    flags: int = 0
    

