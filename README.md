# AutoDownloader

The AutoDownloader Application allows you to automatically download a torrent from utorrentweb plus download subtitles for that movie.
The Web interface I used is google sheet, therefore setting a Google Sheet API key is one of the requirements.



**Prerequisties:**

  **OpenSubtitles Api Key:**
  
    1. Register in https://www.opensubtitles.com/en/home
    2. Go to https://www.opensubtitles.com/en/consumers and create Api Key.
    
    ![opensub_example](https://user-images.githubusercontent.com/34963960/205314076-445fe646-c8e9-48c6-869c-02d2b199e6d7.PNG)

    ![opensubs_example2](https://user-images.githubusercontent.com/34963960/205314085-e6f42298-ea88-410a-8877-9fe6fe5c825b.PNG)


    3. Save the key.

  **UTorrentWeb:**


**Steps to run the app:**

1. git clone https://github.com/DvirSaidof/AutoDownloader.git
2. pip install -r requirements.txt
4. change config.json.sample to config.json and fill all empty values.

{
  "user_preferences": {
    "language": ["English"], # Your prefered subtitles language
    "folder": "" # Subtitles will be downloaded to this folder 
  },
  "google_credentials": { # Your google credentials
    "type": "",
    "project_id": "",
    "private_key_id": "",
    "private_key": "",
    "client_email": "",
    "client_id": "",
    "auth_uri": "",
    "token_uri": "",
    "auth_provider_x509_cert_url": "",
    "client_x509_cert_url": ""
  },
  "opensubtitles_credentials": { # Your open subtitles api key
    "api_key": ""
  }
}
