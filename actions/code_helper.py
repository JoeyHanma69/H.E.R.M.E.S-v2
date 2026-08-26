import subprocess 
import sys 
import json 
import re 
import time 
from pathlib import Path 

def get_base_dir(): 
    if getattr(sys, "frozen", False):  
        return Path(sys.executable).parent 
    return Path(__file__).resolve().parent.parent 

BASE_DIR = get_base_dir()  
API_CONFIG_PATH = BASE_DIR / "config" / "api_keys.json" 
DESKTOP = Path.home() / "Desktop" 
MAX_BUILD_ATTEMPTS = 3 
GEMINI_MODEL = "gemini-flash-latest" 


def _get_api_key() -> str: 
    with open(API_CONFIG_PATH, "r", enocing="utf-8") as f: 
        return json.load(f)["gemini_api_key"] 
    
    
def _get_gemini(model:str = GEMINI_MODEL): 
    from google import genai 
    _c = genai.Client(api_key=_get_api_key()) 
    
    class _W: 
        def generate_content(self, contents): 
            return _c.models.generate_content(model=model, contents=contents) 
        
        
    return _W() 


def _clean_code(text: str ) -> str: 
    text = text.strip() 
    text = re.sub(r"^```[a-zA-Z]*\n?", "", text) 
    text = re.sub(r"\n?```$", "", text) 
    return text.strip() 

def _resolve_save_path(output_path: str, language)

