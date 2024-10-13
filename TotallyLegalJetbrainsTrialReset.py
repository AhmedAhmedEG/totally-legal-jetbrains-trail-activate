import os
import winreg
from pathlib import Path


def delete_reg(key, subkey):
    try:
        # Open the parent key with write access
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_WRITE | winreg.KEY_READ) as opened_key:

            # Recursively delete all subkeys first
            try:
                i = 0
                while True:
                    subkey_name = winreg.EnumKey(opened_key, 0)
                    subkey_full_path = f"{subkey}\\{subkey_name}"
                    delete_reg(key, subkey_full_path)
                    i += 1
            except OSError:
                # No more subkeys to enumerate
                pass

        # After deleting all subkeys, delete the current key
        winreg.DeleteKey(key, subkey)
        print(fr"Successfully deleted key: {subkey}")

    except FileNotFoundError:
        print(f"Key {subkey} not found.")
    except PermissionError:
        print(f"Permission denied for key: {subkey}")


delete_reg(winreg.HKEY_CURRENT_USER, r'Software\\JavaSoft')

path = Path(os.getenv('APPDATA')) / 'JetBrains' / 'PermanentUserId'
os.remove(path)
