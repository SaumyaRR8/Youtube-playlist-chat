from urllib.parse import urlparse, parse_qs
from contextlib import suppress
from youtube_transcript_api import YouTubeTranscriptApi
import jsonlines

def get_yt_id(url, ignore_playlist=False):
    # Examples:
    # - http://youtu.be/SA2iWivDJiE
    # - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    # - http://www.youtube.com/embed/SA2iWivDJiE
    # - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    query = urlparse(url)
    if query.hostname == 'youtu.be': return query.path[1:]
    if query.hostname in {'www.youtube.com', 'youtube.com', 'music.youtube.com'}:
        if not ignore_playlist:
        # use case: get playlist id not current video in playlist
            with suppress(KeyError):
                return parse_qs(query.query)['list'][0]
        if query.path == '/watch': return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/watch/': return query.path.split('/')[1]
        if query.path[:7] == '/embed/': return query.path.split('/')[2]
        if query.path[:3] == '/v/': return query.path.split('/')[2]
   # returns None for invalid YouTube url
        
def get_transcript(urls):
    # Create a JSON Lines file
    with jsonlines.open('transcript.jsonl', mode='w') as writer:
        for i in urls:
            try:
                ida = get_yt_id(i)
                ts = YouTubeTranscriptApi.get_transcript(ida)
                output=''
                for x in ts:
                    sentence = x['text']
                    output += f' {sentence}\n'
                writer.write({'transcript': output})
                print(f"Transcript for URL: {i} retrieved successfully")
                print(f"Transcript: {output}")
            except Exception as e:
                print(f"Error retrieving transcript for URL: {i}")
                print(f"Error message: {str(e)}")
    return "transcript.jsonl"