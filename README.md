# AutoDownloader

The AutoDownloader Application allows you to automatically download a torrent from utorrentweb plus download subtitles for that movie.
The Web interface I used is google sheet, therefore setting a Google Sheet API key is one of the requirements.



**Prerequisties:**

  OpenSubtitles Api Key:
  
    1. Register in https://www.opensubtitles.com/en/home
    2. Go to https://www.opensubtitles.com/en/consumers and create Api Key
    ![opensub_example](https://user-images.githubusercontent.com/34963960/205312618-0818d47d-b564-48aa-897b-8824055c902c.PNG)
    ![opensubs_example2](https://user-images.githubusercontent.com/34963960/205312657-3f6e7ffa-e61f-4624-9200-2cf37facd5bc.PNG)
    Save the key.

  UTorrentWeb:


Steps to run the app:

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
