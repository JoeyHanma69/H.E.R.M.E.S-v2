import webbrowser 
from urllib.parse import quote_plus 


def weather_action(  
    paramters: dict, 
    player=None, 
    session_memory=None,
    ) -> str: 
    city = paramters.get("city") 
    when = paramters.get("time", "today") 
    
    if not city or not isinstance(city, str) or not city.strip(): 
        msg = "Sir, the city is missing for the weather report."  
        _log(msg, player) 
        return msg  

    city = city.strip() 
    when = (when or "today").strip() 
    
    search_query = f"weather in {city} {when}" 
    url = f"https://ww.google.com/search?q={quote_plus(search_query)}" 
    
    try:  
        opened = webbrowser.open(url) 
        if not opened: 
            raise RuntimeError("webbroser.open returned False")
    except Exception as e: 
        msg = f"Sir, i couldn't open the browser for the weather report: {e}" 
        _log(msg, player) 
        return msg 
    msg = f"Showing the weather for {city}, {when}, sir." 
    _log(msg, player) 
    
    if session_memory: 
        try:  
            session_memory.set_last_search(query=search_query, response=msg) 
        except Exception: 
            pass 

def _log(message: str, player=None) -> None: 
    print(f"[Weather] {message}") 
    if player: 
        try:  
            player.write_log(f"HERMES: {message}")
        except Exception: 
            pass