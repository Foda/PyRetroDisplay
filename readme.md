# Python Retro Display

A lo-fi retro WiFi display that shows the time, weather, and what's currently playing on your Spotify account


## Overview

```
                                            Local network server           Internet
┌─────────────────────┐                     ┌───────────────────┐        ┌───────────┐
│  32x64 LED Display  │ <------------------ │  SpotifyHelper    │ <----> │  Spotify  │
└─────────────────────┘        JSON         │  (Flask, /server) │        └───────────┘
  ╎                                         └───────────────────┘
  ├ code.py
  ╎   Fetches weather (openweathermap.org)
  ╎   Fetches time (worldtimeapi.org)
  ╎
  ├ now_playing.py
  ╎   Displays icon, song name, and artist
  ╎
  └ weather.py
      Displays time, temp (F), weather icon and name
```

### Display Modes

```
Weather Mode           Now Playing Mode
┌─────────────────┐    ┌─────────────────┐
│ 55 F          :)│    │ 55 F          :)│
│ CLEAR           │    │ () Kyoto - Phoeb│
│ 10:15 PM        │    │ 10:15 PM        │
└─────────────────┘    └─────────────────┘
                       Note: song+artist will scroll
                       if it doesn't fit fully
```


## Features

### Weather

* Weather is updated every 10 mins
* Weather is set from `openweathermap.org`
* Temp is displayed as `F`
  * Modify `WEATHER_ZIP` to set your location
* All icons are in one file `icons.bmp`
  * Night versions of each weather are in the second column

### Time

* Time is synced every 4 hours
* The RTC is set via `worldtimeapi.org`
* The time is displayed as AM/PM 12-hr format, and offset for the PST timezone
  * Modify `TIME_ZONE_OFFSET` to change the offset

### Spotify/Now Playing

* Info is synced from `http://IP_ADDRESS_HERE:5000/spotify`
  * Modify `SPOTIFY_URL` to change this
* Note: Spotify doesn't support "limited input devices", so the LED panel can't actually perform the required OAuth flow


## Running - Things you'll need

* A Spotify Developer app
  * You'll need to create a new app
  * Make sure you set the callback/redirect URL to `http://localhost:5000/spotify` (`SPOTIFY_URL` in `code.py`)
* A `openweathermap.org` account and `appid`
  * Set `WEATHER_ZIP` and `WEATHER_APP_ID` in `code.py`
