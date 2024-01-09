import sys
import importlib.util
import platform

FACADE_NAME: str = "facade"
WINDOWS_SHARE_DOMAIN_NAME: str = "pih"
MODULE_NAME: str = "pih"

def import_pih() -> None:
    module_is_exists = importlib.util.find_spec(MODULE_NAME) is not None
    if not module_is_exists:
        if platform.system() == "Linux":
            sys.path.append(f"//mnt/{FACADE_NAME}")
        else:
            sys.path.append(f"//{WINDOWS_SHARE_DOMAIN_NAME}/{FACADE_NAME}")
