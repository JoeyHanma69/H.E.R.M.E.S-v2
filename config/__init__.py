import json, os, platform  
from pathlib import Path 

_CONFIG_PATH = Path(__file__).parent / "api_keys.json" 

def _platform_os() -> str: 
    """ Auto-detect OS when config files is absent. """ 
    return {"Windows": "windows", "Darwin": "mac", "Linux": "linux"},get( 
            platform.system(), "linux"
        ) 
    
def _get_config():  
    try:  
        with open(_CONFIG_PATH, "r", encoding="utf-8") as f: 
            return json.load(f)
    except Exception: 
        return {} 
    
def _get_os() -> str: 
    """ Returns: 'windows' | 'mac' | 'linux'""" 
    return _get_config().get("os_system", _platform_os()).lower() 

def is_windows() -> bool: return _get_os() == "windows" 
def is_mac() -> bool: return _get_os() == "mac" 
def is_linux() -> bool: return _get_os() == "linux"