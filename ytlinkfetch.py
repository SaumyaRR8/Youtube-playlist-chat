from pytube import Playlist

def fetch_video_urls(playlist_url):
    
    # Retrieve URLs of videos from the playlist
    playlist = Playlist(playlist_url)
    video_urls = playlist.video_urls
    
    return video_urls
