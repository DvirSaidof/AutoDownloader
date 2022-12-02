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


   **Google Sheet Api Key**
   
    1. Sign in to the Google Cloud console - https://console.developers.google.com/
    2. Select your Google's project (or create a new one)
    3. Search for the Google Sheets API and enable it
    4. On the main menu, select "APIs & Services" then "Credentials"
    5. Now create credentials with the "OAuth client ID" method
    6. Click on "Create"
    7. Go to service account
    8. Click on the email
     
   ![googleshit1](https://user-images.githubusercontent.com/34963960/205336584-71aa0c3c-9112-4e05-8412-098b0f31314b.png)
     
    9. Go to KEYS section and add a new key. This will download a credentials json file.
     
   ![googleshit2](https://user-images.githubusercontent.com/34963960/205337156-9c0420c7-f218-4d30-a3d6-6a1bdcd31813.png) 
   
    10. Open a google sheet and share it with the email generated for ur google service account.
    Google sheet should have 2 sheets that look like that
   ![image](https://user-images.githubusercontent.com/34963960/205352698-8ec30411-6450-4f1c-8f54-1877f04c5c3a.png)


**Steps to run the app:**

1. git clone https://github.com/DvirSaidof/AutoDownloader.git
2. pip install -r requirements.txt
3. change config.json.sample to config.json and fill all the empty values with the api keys generated in the prerequisites.

