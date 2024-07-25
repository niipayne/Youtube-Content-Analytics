from googleapiclient.discovery import build
import json
import os 
import pandas as pd
import visualizer
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv('api_key')

# Getting the channel upload Id
def get_channel_details(channel_id):
    youtube = build('youtube', 'v3', developerKey='AIzaSyAyh0L1ib80S1ezQs-onDhAsvH1ZDDUjoI')
    request = youtube.channels().list(
        part = 'contentDetails, snippet, statistics',
        id = channel_id)
    response = request.execute()

    uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    

# Get the 50 most recent videos in the uploads playlist

    playlist_items = []
    page_token = None
    while len(playlist_items)  < 50:
        playlist_response = youtube.playlistItems().list(
            part = 'snippet',
            maxResults = 5,
            playlistId = uploads_playlist_id,
            pageToken = page_token
        ).execute()
        playlist_items += playlist_response['items']
        page_token = playlist_response.get('nextPageToken')

        if not page_token:
            break
   
    videos_data = []
    for item in playlist_items[:50]:
        video_id = item['snippet']['resourceId']['videoId']
        title = item['snippet']['title']
        published_at = item['snippet']['publishedAt'][0:10]
        tags, view_count, thumbnail, duration = get_video_details(video_id, api_key)

        videos_data.append(
            {'title':title,
             'published' :published_at,
             'tags':tags,
             'views': view_count,
             'thumbnail':thumbnail,
             'duration':duration
            }
        )
    return videos_data


def get_video_details(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)

    video_reponse = youtube.videos().list(
        part='snippet,contentDetails,statistics',
        id = video_id
    ).execute()

    video = video_reponse['items'][0]
    tags = video['snippet'].get('tags', [])
    view_count = video['statistics']['viewCount']
    thumbnail  = video['snippet']['thumbnails']['high']['url']
    duration = video['contentDetails']['duration']

    return tags, view_count, thumbnail, duration

data = (get_channel_details(channel_id= 'UCBJycsmduvYEL83R_U4JriQ'))

# Saving the data to a json file
with open('data.json', 'w')as f:
    json.dump(data, f, indent=2)

# Using panda to organise the data from a json file

data_frame = pd.read_json('data.json')

visualizer.display()