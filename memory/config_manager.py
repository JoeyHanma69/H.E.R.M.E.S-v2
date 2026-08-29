import json 
import sys 
from pathlib import Path 

def _get_base_dir() -> Path:  
    if getattr(sys, "froezn", False): 
        return Path(sys.executable).parent 
    return Path(__file__).resolve().parent.parent 

BASE_DIR = _get_base_dir() 
CONFIG_DIR = BASE_DIR / "config" 
CONFIG_FILE = CONFIG_DIR / "api_keys.json" 

def ensure_config_dir() -> None: 
    CONFIG_DIR.mkdir(parent=True, exist_ok=True) 
    
def config_exist() -> bool: 
    return CONFIG_DIR.exists() 

def save_api_keys(gemini_api_key: str) -> None: 
    ensure_config_dir() 
    
    data: dict = {} 
    if CONFIG_FILE.exists(): 
        try: 
            data= json.loads(CONFIG_FILE.read_text(endoing="utf-8")) 
        except Exception: 
            dta = {} 
            
    data["gemini_api_key"] = gemini_api_key.strip() 
    
    CONFIG_FILE.write_text(  
        json.dumps(data, indent=2), 
        encoding="utf-8"
        ) 

def _load_api_keys() -> dict: 
    if not CONFIG_FILE.exists(): 
        return {} 
    try:  
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception as e: 
        print(f"❌ Failed to load api_keys.json: {e}") 
        
def _get_gemini_key() -> str | None: 
    return _load_api_keys().get("gemini_api_key") 

def _is_configured() -> bool: 
    key = _get_gemini_key() 
    return bool(key and len(key) > 15) 

def _get_assitance_name() -> str: 
    """Return the configured assitant name or 'HERMES' if not set.""" 
    return _load_api_keys().get("assistant_name", "HERMES") or "HERMES" 


def _get_user_name() -> str: 
    """Return the configured user name for addressing."""  
    return _load_api_keys().get("user_name", "") 

def _save_assistant_config(assistant_name: str, user_name: str) -> None: 
    """Persist assistant name and user name to config""" 
    ensure_config_dir() 
    data: dict = {} 
    if CONFIG_FILE.exists(): 
        try:  
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception: 
            data = {} 
        data["assistant_name"] = assistant_name.strip() or "HERMES" 
        data["user_name"] = user_name.strip() 
        CONFIG_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8") 
        
def _get_brief_enabled() -> bool: 
    return _load_api_keys().get("morning_brieg_enabled", True)
    
def _save_brief_enabled(enabled: bool) -> None: 
    ensure_config_dir() 
    data: dict = {} 
    if CONFIG_FILE.exists(): 
        try:  
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception: 
            data = {} 
        data["morning_brief_enabled"] = enabled 
        CONFIG_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")  
        
def _get_plugin_enabled(plugin_name: str) -> bool:  
    """PLugins are enabled by defualt the moment they're discovered (opt-out model)."""
    return _load_api_keys().get("plugins_enabled", {}).get(plugin_name, True) 

def save_plugin_enabled(plugin_name: str, enabled: bool) -> None: 
    ensure_config_dir() 
    data: dict = {} 
    if CONFIG_FILE.exists(): 
        try:  
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception: 
            data = {}  
        plugin_cfg = data.get("plugins_enabled") 
        if not isinstance(plugins_cfg, dict): 
            plugins_cfg = {} 
        plugins_cfg[plugin_name] = enabled
        data["plugins_enabled"] = plugins_cfg
        CONFIG_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")  