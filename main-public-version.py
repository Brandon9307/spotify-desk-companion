import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# spotify access information from the developer dashboard
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REDIRECT_URI = "http://127.0.0.1:8888/callback"

SCOPE = "user-read-currently-playing user-read-playback-state user-modify-playback-state user-library-modify"

# spotify object
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

last_volume = 50


# displays the current song playing
def show_now_playing(sp):
    current = sp.current_user_playing_track()

    if current is None or current["item"] is None:
        print("\nNothing is playing right now.\n")
    else:
        track = current["item"]

        song_name = track["name"]
        artists = [artist["name"] for artist in track["artists"]]
        artist_names = ", ".join(artists)
        album_name = track["album"]["name"]

        print("\nNow playing:")
        print(song_name)
        print("by", artist_names)
        print("Album:", album_name)
        print()


# plays a searched song
def play_song(sp, query):
    query = query.strip()

    if query == "":
        print("Tell me what song to play.")
    else:
        if " by " in query:
            song, artist = query.split(" by ", 1)
            search_query = f"track:{song.strip()} artist:{artist.strip()}"
        else:
            search_query = query

        results = sp.search(q=search_query, limit=1, type="track")
        tracks = results["tracks"]["items"]

        if len(tracks) == 0:
            print("No song found.")
        else:
            track = tracks[0]
            track_uri = track["uri"]

            sp.start_playback(uris=[track_uri])

            artists = [artist["name"] for artist in track["artists"]]
            artist_names = ", ".join(artists)

            print("Playing:")
            print(track["name"])
            print("by", artist_names)


show_now_playing(sp)

# commands the program takes
while True:
    command = input("Type command: ").lower().strip()

    try:
        if command in [
            "pause",
            "pause music",
            "pause the music",
            "pause song",
            "pause the song",
            "stop",
            "stop music",
            "stop the music",
            "stop song",
            "stop the song",
            "shut up",
            "hold on",
            "hold the music",
            "freeze music",
            "freeze the music",
            "shut up",
            "quiet",
            "be quiet"
        ]:
            sp.pause_playback()
            print("Paused.")

        elif command in [
            "start",
            "start music",
            "start the music",
            "play",
            "play music",
            "play the music",
            "resume",
            "resume music",
            "resume the music",
            "continue",
            "continue music",
            "continue the music",
            "keep playing",
            "keep the music playing"
        ]:
            sp.start_playback()
            print("Playing.")
            time.sleep(0.2)
            show_now_playing(sp)

        elif command in [
            "skip",
            "skip song",
            "skip the song",
            "next",
            "next song",
            "next the song",
            "play next",
            "play the next",
            "play next song",
            "play the next song",
            "go next",
            "go to next song",
            "go to the next song",
            "change song",
            "change the song",
            "switch song",
            "switch the song"
        ]:
            sp.next_track()
            print("Skipped.")
            time.sleep(0.3)
            show_now_playing(sp)

        elif command in [
            "back",
            "go back",
            "previous",
            "previous song",
            "previous the song",
            "last song",
            "last the song",
            "go to previous song",
            "go to the previous song",
            "play previous song",
            "play the previous song",
            "go to last song",
            "go to the last song",
            "play last song",
            "play the last song"
        ]:
            sp.seek_track(0)
            time.sleep(0.2)
            sp.previous_track()
            print("Went to previous track.")
            time.sleep(0.3)
            show_now_playing(sp)

        elif command in [
            "restart",
            "restart song",
            "restart the song",
            "start over",
            "start the song over",
            "start song over",
            "play from beginning",
            "play from the beginning",
            "restart music",
            "restart the music",
            "go to beginning",
            "go to the beginning"
        ]:
            sp.seek_track(0)
            print("Restarted song.")
            time.sleep(0.2)
            show_now_playing(sp)

        elif command in [
            "now playing",
            "what is playing",
            "what's playing",
            "what song is this",
            "what is this song",
            "what's this song",
            "song name",
            "the song name",
            "current song",
            "the current song",
            "show song",
            "show the song",
            "show current song",
            "show the current song"
        ]:
            show_now_playing(sp)

        elif command.startswith("set volume") or command.startswith("set the volume") or command.startswith("set music") or command.startswith("set the music"):
            playback = sp.current_playback()

            if playback is None:
                print("No active playback device.")
            else:
                words = command.replace("%", "").split()

                volume_value = None

                for word in words:
                    if word.isdigit():
                        volume_value = int(word)

                if volume_value is None:
                    print("Tell me a number between 0 and 100.")
                else:
                    if volume_value < 0:
                        volume_value = 0
                    if volume_value > 100:
                        volume_value = 100

                    try:
                        sp.volume(volume_value)
                        print("Volume set to", volume_value, "%")
                    except Exception:
                        device_name = playback["device"]["name"]
                        device_type = playback["device"]["type"]
                        print("Volume control may not work on this device:", device_name, "-", device_type)

        elif command in [
            "volume up",
            "increase volume",
            "increase the volume",
            "louder",
            "make it louder",
            "make the music louder",
            "turn up volume",
            "turn up the volume",
            "turn volume up",
            "turn the volume up",
            "turn up music",
            "turn up the music",
            "turn music up",
            "turn the music up",
            "raise volume",
            "raise the volume",
            "music louder",
            "the music louder"
        ]:
            playback = sp.current_playback()

            if playback is None:
                print("No active playback device.")
            else:
                device_name = playback["device"]["name"]
                device_type = playback["device"]["type"]
                current_volume = playback["device"]["volume_percent"]

                if current_volume is None:
                    print("Volume control may not work on this device:", device_name, "-", device_type)
                else:
                    new_volume = current_volume + 10

                    if new_volume > 100:
                        new_volume = 100

                    try:
                        sp.volume(new_volume)
                        print("Volume set to", new_volume, "%")
                    except Exception:
                        print("Volume control may not work on this device:", device_name, "-", device_type)

        elif command in [
            "volume down",
            "decrease volume",
            "decrease the volume",
            "quieter",
            "make it quieter",
            "make the music quieter",
            "turn it down",
            "turn down volume",
            "turn down the volume",
            "turn volume down",
            "turn the volume down",
            "turn down music",
            "turn down the music",
            "turn music down",
            "turn the music down",
            "lower volume",
            "lower the volume",
            "music quieter",
            "the music quieter"
        ]:
            playback = sp.current_playback()

            if playback is None:
                print("No active playback device.")
            else:
                device_name = playback["device"]["name"]
                device_type = playback["device"]["type"]
                current_volume = playback["device"]["volume_percent"]

                if current_volume is None:
                    print("Volume control may not work on this device:", device_name, "-", device_type)
                else:
                    new_volume = current_volume - 10

                    if new_volume < 0:
                        new_volume = 0

                    try:
                        sp.volume(new_volume)
                        print("Volume set to", new_volume, "%")
                    except Exception:
                        print("Volume control may not work on this device:", device_name, "-", device_type)

        elif command in [
            "mute",
            "mute music",
            "mute the music",
            "mute volume",
            "mute the volume",
            "mute sound",
            "mute the sound",
            "silence",
            "silence music",
            "silence the music",
            "shut off sound",
            "shut off the sound",
            "turn off sound",
            "turn off the sound"
        ]:
            playback = sp.current_playback()

            if playback is None:
                print("No active playback device.")
            else:
                current_volume = playback["device"]["volume_percent"]

                if current_volume is None:
                    print("Volume control not supported on this device.")
                else:
                    last_volume = current_volume
                    sp.volume(0)
                    print("Muted.")

        elif command in [
            "unmute",
            "unmutes",
            "unmute music",
            "unmute the music",
            "unmute volume",
            "unmute the volume",
            "unmute sound",
            "unmute the sound",
            "restore volume",
            "restore the volume",
            "bring back sound",
            "bring back the sound",
            "turn sound back on",
            "turn the sound back on"
        ]:
            playback = sp.current_playback()

            if playback is None:
                print("No active playback device.")
            else:
                try:
                    sp.volume(last_volume)
                    print("Unmuted. Volume restored to", last_volume, "%")
                except Exception:
                    print("Volume control may not work on this device.")

        elif command in [
            "forward",
            "go forward",
            "skip forward",
            "skip the song forward",
            "fast forward",
            "fast forward the song",
            "forward 10 seconds",
            "forward ten seconds",
            "go forward 10 seconds",
            "go forward ten seconds",
            "skip ahead",
            "skip the song ahead",
            "go ahead",
            "move forward",
            "move the song forward",
            "skip ten seconds",
            "skip 10 seconds"
        ]:
            playback = sp.current_playback()

            if playback is None or playback["item"] is None:
                print("No active playback.")
            else:
                current_position = playback["progress_ms"]
                duration = playback["item"]["duration_ms"]

                new_position = current_position + 10000

                if new_position > duration:
                    new_position = duration - 1000

                    if new_position < 0:
                        new_position = 0

                sp.seek_track(new_position)
                print("Skipped forward 10 seconds.")

        elif command in [
            "rewind",
            "rewind song",
            "rewind the song",
            "go backward",
            "go backwards",
            "backward",
            "backwards",
            "go back 10 seconds",
            "go back ten seconds",
            "rewind 10 seconds",
            "rewind ten seconds",
            "skip back",
            "skip the song back",
            "skip backward",
            "skip backwards",
            "move backward",
            "move backwards",
            "move the song backward",
            "move the song backwards"
        ]:
            playback = sp.current_playback()

            if playback is None or playback["item"] is None:
                print("No active playback.")
            else:
                current_position = playback["progress_ms"]

                new_position = current_position - 10000

                if new_position < 0:
                    new_position = 0

                sp.seek_track(new_position)
                print("Went back 10 seconds.")

        elif command in [
            "shuffle",
            "start shuffling",
            "start the shuffle",
            "turn on shuffle",
            "turn on the shuffle",
            "shuffle on",
            "enable shuffle",
            "enable the shuffle",
            "randomize",
            "randomize music",
            "randomize the music",
            "mix it up",
            "mix the music up"
        ]:
            playback = sp.current_playback()

            if playback is None:
                print("No active playback device.")
            else:
                sp.shuffle(True)
                print("Shuffle on.")

        elif command in [
            "stop shuffling",
            "stop the shuffle",
            "stop shuffle",
            "turn off shuffle",
            "turn off the shuffle",
            "shuffle off",
            "disable shuffle",
            "disable the shuffle",
            "no shuffle",
            "no more shuffle"
        ]:
            playback = sp.current_playback()

            if playback is None:
                print("No active playback device.")
            else:
                sp.shuffle(False)
                print("Shuffle off.")

        elif command in [
            "like song",
            "like the song",
            "like this song",
            "save song",
            "save the song",
            "save this song",
            "add song to library",
            "add the song to library",
            "add this song to library",
            "add song to the library",
            "add the song to the library",
            "add this song to the library",
            "heart song",
            "heart the song",
            "heart this song"
        ]:
            current = sp.current_user_playing_track()

            if current is None or current["item"] is None:
                print("No song is playing.")
            else:
                track_id = current["item"]["id"]
                sp.current_user_saved_tracks_add([track_id])
                print("Song liked.")

        elif command in [
            "unlike song",
            "unlike the song",
            "unlike this song",
            "remove like",
            "remove the like",
            "remove this like",
            "remove song",
            "remove the song",
            "remove this song",
            "unsave song",
            "unsave the song",
            "unsave this song",
            "remove song from library",
            "remove the song from library",
            "remove this song from library",
            "remove song from the library",
            "remove the song from the library",
            "remove this song from the library"
        ]:
            current = sp.current_user_playing_track()

            if current is None or current["item"] is None:
                print("No song is playing.")
            else:
                track_id = current["item"]["id"]
                sp.current_user_saved_tracks_delete([track_id])
                print("Song unliked.")

        elif command.startswith("play song "):
            query = command.replace("play song ", "", 1).strip()
            play_song(sp, query)

        elif command.startswith("play the song "):
            query = command.replace("play the song ", "", 1).strip()
            play_song(sp, query)

        elif command.startswith("play track "):
            query = command.replace("play track ", "", 1).strip()
            play_song(sp, query)

        elif command.startswith("play the track "):
            query = command.replace("play the track ", "", 1).strip()
            play_song(sp, query)

        elif command.startswith("put on "):
            query = command.replace("put on ", "", 1).strip()
            play_song(sp, query)

        elif command.startswith("put the song on "):
            query = command.replace("put the song on ", "", 1).strip()
            play_song(sp, query)

        elif command.startswith("play "):
            query = command.replace("play ", "", 1).strip()
            play_song(sp, query)

        elif command in [
            "quit",
            "exit",
            "close",
            "close program",
            "close the program",
            "end program",
            "end the program",
            "goodbye",
            "bye",
            "stop program",
            "stop the program"
        ]:
            print("Exiting...")
            break

        else:
            print("Unknown command.")

    except Exception as error:
        print("\nCommand failed.")
        print("Make sure Spotify is open and a device is active.")
        print("Error:", error)
        print()