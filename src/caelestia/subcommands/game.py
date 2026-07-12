import os
import sys
import subprocess
import shlex
from pathlib import Path
import configparser

def get_xdg_data_dirs():
    dirs = os.environ.get('XDG_DATA_DIRS', '/usr/local/share/:/usr/share/')
    data_home = os.environ.get('XDG_DATA_HOME', os.path.expanduser('~/.local/share'))
    return [data_home] + dirs.split(':')

def get_games():
    desktop_files = {}
    
    # Iterate in reverse order so higher priority directories overwrite lower ones
    for data_dir in reversed(get_xdg_data_dirs()):
        app_dir = Path(data_dir) / 'applications'
        if not app_dir.exists():
            continue
            
        for path in app_dir.rglob('*.desktop'):
            desktop_files[path.name] = path

    games = []
    
    for filename, filepath in desktop_files.items():
        try:
            config = configparser.ConfigParser(interpolation=None)
            config.read(filepath, encoding='utf-8')
            
            if 'Desktop Entry' not in config:
                continue
                
            entry = config['Desktop Entry']
            
            if entry.get('NoDisplay', 'false').lower() == 'true':
                continue
                
            categories = entry.get('Categories', '')
            if 'game' not in categories.lower():
                continue
                
            name = entry.get('Name')
            exec_cmd = entry.get('Exec')
            
            if name and exec_cmd:
                games.append((name, exec_cmd))
                
        except Exception:
            pass

    # Sort perfectly alphabetically to match the user's expected indexing
    games.sort(key=lambda x: x[0].lower())
    return games

class Command:
    def __init__(self, args):
        self.args = args

    def run(self):
        if not getattr(self.args, 'number', None):
            print("Usage: caelestia game <number>")
            sys.exit(1)
            
        try:
            index = int(self.args.number) - 1
        except ValueError:
            print("Please provide a valid number.")
            sys.exit(1)
        
        if index < 0:
            print("Index must be 1 or greater.")
            sys.exit(1)
            
        games = get_games()
        
        if not games:
            subprocess.run(["notify-send", "Game Launcher", "No games found on your system!"])
            sys.exit(1)
            
        if index >= len(games):
            subprocess.run(["notify-send", "Game Launcher", f"You only have {len(games)} games!"])
            sys.exit(1)
            
        target_game = games[index]
        subprocess.run(["notify-send", "Game Launcher", f"Launching: {target_game[0]}"])
        
        raw_cmd = target_game[1]
        for code in ["%U", "%F", "%u", "%f", "%c", "%k"]:
            raw_cmd = raw_cmd.replace(code, "")
            
        cmd_parts = shlex.split(raw_cmd)
        
        # Execute the game detached
        subprocess.Popen(cmd_parts, start_new_session=True)
