# AutoDownloader

The AutoDownloader Application allows you to automatically download a torrent from utorrentweb plus download subtitles for that movie.
The Web interface I used is google sheet, therefore setting a Google Sheet API key is one of the requirements.



**Prerequisties:**

  **OpenSubtitles Api Key:**
  
    1. Register in https://www.opensubtitles.com/en/home
    2. Go to https://www.opensubtitles.com/en/consumers and create Api Key.
    3. Save the key.

  **UTorrentWeb:**
  
    1. Download and install UTorrentWeb
    2. Go to Settings in the upper right corner.
    
   ![utorrentweb1](https://user-images.githubusercontent.com/34963960/205316252-8e329d83-0135-4670-9420-579ea90cefe9.png)

    3. Disable "Show add torrent dialog"
    
   ![utorrentweb2](https://user-images.githubusercontent.com/34963960/205316376-3c7fe307-4bb0-4b8d-b4ef-184aca0e8496.png)


**Steps to run the app:**

1. git clone https://github.com/DvirSaidof/AutoDownloader.git
2. pip install -r requirements.txt
3. change config.json.sample to config.json and fill all the empty values with the api keys generated in the prerequisites.
4. python app.py

