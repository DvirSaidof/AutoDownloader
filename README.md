## AutoDownloader

The AutoDownloader Application is a simple tool that provides a GUI interface to automate the process of downloading a movie (via utorrent) and subtitles. The project is composed of 3 main components: gui, piratebay_api, and subtitles_api.

### **Disclaimer**
This script only triggers the download of given URLs. I'm not responsible for the usage you do with this software, for any damage that might result from using it, and I'm certainly not encouraging piracy in any form.

### **Prerequisites:**
  
  ###### For Windows
1. Install [WSL](https://learn.microsoft.com/en-us/windows/wsl/install/)

  ###### OpenSubtitles Api Key:
  
1. Register at [opensubtitles](https://www.opensubtitles.com/en/home/)
2. Go to - https://www.opensubtitles.com/en/consumers and create Api Key.
3. Save the key.

  ###### UTorrentWeb:
  
1. Download and install [UTorrentWeb](https://www.utorrent.com/web/)
2. Go to Settings in the upper right corner.

   
   <img src="https://user-images.githubusercontent.com/34963960/205316252-8e329d83-0135-4670-9420-579ea90cefe9.png" width="800" height="550">

3. Disable "Show add torrent dialog" and set your desired download_folder
    
   <img src="https://user-images.githubusercontent.com/34963960/205316376-3c7fe307-4bb0-4b8d-b4ef-184aca0e8496.png" width="800" height="550">

### **Steps to run the app:**

```
1. # Open your zsh/bash/wsl terminal and navigate to your projects dir
2. git clone https://github.com/DvirSaidof/AutoDownloader.git
2. cd AutoDownloader
4. mv config/config.json.sample config/config.json
5. # Fill all the empty values in config/config.json. Make sure the download_folder is the same as set in utorrentweb and that logs_folder exists.
6. sudo bash auto_download.sh $(whoami)
```

### **Credits** 
In order to parse a torrent name I used code from [parse-torrent-name](https://github.com/divijbindlish/parse-torrent-name) repository
