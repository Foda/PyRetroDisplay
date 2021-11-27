import time
import rtc
import board
import displayio
import adafruit_requests as requests
from adafruit_bitmap_font import bitmap_font
from adafruit_matrixportal.matrixportal import MatrixPortal
import weather
import now_playing

SPOTIFY_URL = "http://192.168.1.25:5000/spotify"

WEATHER_ZIP = "94608"
WEATHER_APP_ID = ""
WEATHER_URL = f"https://api.openweathermap.org/data/2.5/weather?zip={WEATHER_ZIP},us&appid={WEATHER_APP_ID}&units=imperial"

TIME_URL = "http://worldtimeapi.org/api/ip"
TIME_ZONE_OFFSET = 8 * 60 * 60 # UTC-8:00, in seconds

# Fonts
glyphs = b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
tiny_font = bitmap_font.load_font('/pixel-3x5.bdf')
tiny_font.load_glyphs(glyphs)

med_font = bitmap_font.load_font('/Tamzen8x16b.bdf')
med_font.load_glyphs(glyphs)

icons = displayio.OnDiskBitmap('/icons.bmp')

matrixportal = MatrixPortal()
weather_gfx = weather.Weather(matrixportal.display, icons, tiny_font, med_font)
now_playing_gfx = now_playing.NowPlaying(matrixportal.display, icons, tiny_font, med_font)

root_group = displayio.Group()
root_group.append(weather_gfx)
root_group.append(now_playing_gfx)

matrixportal.display.show(root_group)


def update_now_playing():
    print("Updating now playing\n")
    data = matrixportal.network.fetch(SPOTIFY_URL)
    now_playing = data.json()
    if now_playing:
        the_song = now_playing.get('name', None)
        the_artist = now_playing.get('artist', None)
        if the_song:
            show_now_playing(the_song, the_artist)
        else:
            hide_now_playing()


def show_now_playing(song, artist):
    weather_gfx.set_description_hidden(True)
    now_playing_gfx.update_now_playing(song, artist)
    now_playing_gfx.hidden = False
    now_playing_wait_sec = 10 # Update every 10 seconds


def hide_now_playing():
    weather_gfx.set_description_hidden(False)
    now_playing_gfx.hidden = True
    now_playing_wait_sec = 30 # Update every 30 sec


def update_time():
    print("Updating time\n")
    data = matrixportal.network.fetch(TIME_URL)
    rtc.RTC().datetime = time.localtime(data.json().get('unixtime') - TIME_ZONE_OFFSET)


def update_weather():
    # Subtrack 8 since we're 8 hrs behind UTC
    print("Updating weather\n")
    data = matrixportal.network.fetch(WEATHER_URL)
    the_weather = data.json()
    weather_gfx.update_weather(the_weather)


refresh_time = None
refresh_weather = None
now_playing_refresh_time = None
now_playing_wait_sec = 10
now_playing_fail_count = 0
while True:
    # Sync time every 4 hours
    if (not refresh_time) or (time.monotonic() - refresh_time) > 14400:
        refresh_time = time.monotonic()
        try:
            update_time()
        except Exception as e:
            print(e)
            continue

    # Update weather every 10 mins
    if (not refresh_weather) or (time.monotonic() - refresh_weather) > 600:
        refresh_weather = time.monotonic()
        try:
            update_weather()
        except Exception as e:
            print(e)
            continue

    # Update logic:
    #   Try and fetch now playing info every 10 seconds
    #   If we had valid info but fail 4 times backoff for 30 seconds
    #   If we get valid info reset update time to 10 seconds
    if (not now_playing_refresh_time) or (time.monotonic() - now_playing_refresh_time) > now_playing_wait_sec:
        now_playing_refresh_time = time.monotonic()
        try:
            update_now_playing()
            now_playing_fail_count = 0
        except Exception as e:
            print(e)
            now_playing_fail_count += 1
            if now_playing_fail_count > 4:
                hide_now_playing()
            continue

    weather_gfx.update_time()
    weather_gfx.update_scroll()
    now_playing_gfx.update_scroll()

    # Hold our scrolling info for 5 seconds
    time.sleep(5)
