# Spotify Now Playing Helper

## What

This is a dead simple Flask app that serves the current song and artist name from Spotify. You should be able to access it on the local network without messing around with your router

Example
```
> curl http://192.168.1.105:5000/spotify

{
  "name": "Kyoto",
  "artist": "Phoebe Bridgers"
}
```

## Why

Spotify doesn't support "limited input devices", so the LED panel can't actually perform the required OAuth flow.

* First, create an app in the Spotify Developer Dashboard
* Set the callback/redirect uri in the Spotify App to the URL of the Flask app: `http://localhost:5000/spotify_callback`
* Add the `client_id` and `client_secret` to `server/server.py`

## Building

* Install venv
  * `python -m venv venv`
* Activate Powershell env
  * `venv\Scripts\activate.ps1`
* Install requirements
  * `pip3 install -r requirements.txt`
* Export PS var for Flask app
  * `$env:FLASK_APP = "server"`
* Start Flask
  * `flask run --host=0.0.0.0`