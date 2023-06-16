import gui.gui as gui
import json
import sys

config_file = sys.argv[1]
port = sys.argv[2]
ip_address = sys.argv[3]

with open(config_file, 'r') as f:
    config = json.loads(f.read())

opensubtitles_key = config.get('opensubtitles_credentials').get('api_key')
download_folder = config.get('user_preferences').get('download_folder')
language_preferences = config.get('user_preferences').get('language')
logs_folder = config.get('user_preferences').get('logs_folder')

system_os = "linux"

if sys.platform.startswith("win"):
    print("Running on Windows OS")
    system_os = "windows"
else:
    print("Running on Linux/Mac OS")

gui.run(opensubtitles_key=opensubtitles_key,
        language_preferences=language_preferences,
        download_folder=download_folder,
        logs_folder=logs_folder,
        system_os=system_os,
        port=port,
        ip_address=ip_address)
