from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import pytube
import os
import shutil
import math
import datetime
from pytube import YouTube
import cv2

DEVELOPER_KEY="AIzaSyADZxh712P3wWPRkr7VvJzcT30UYbfzo20"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
SEARCH_PHRASES = ['looking down smarthphone', 'text neck', \
                  'tech neck', 'children using smarthphone','smartphone Addiction']

def youtube_search(q, max_results=50,order="relevance", token=None, location=None, location_radius=None):

  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  search_response = youtube.search().list(
    q=q,
    type="video",
    pageToken=token,
    order = order,
    part="id,snippet",
    maxResults=max_results,
    location=location,
    locationRadius=location_radius

  ).execute()


  videos = []

  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append(search_result)
  try:
      nexttok = search_response["nextPageToken"]
      return(nexttok, videos)
  except Exceoauth2clientption as e:
      nexttok = "last_page"
      return(nexttok, videos)

def video_exists(target_dir, video_id):
  files = os.listdir(target_dir + '/videos')
  if (video_id + '.mp4' ) in files:
    print('Video=', video_id, '.mp4 already exists. Continue.')
    return True
  else:
    return False

def download_youtube_video(target_dir, video_id):
  yt_url = 'https://www.youtube.com/watch?v=' + video_id
  print(yt_url)
  yt = YouTube(yt_url) 
  video_filename = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download(target_dir+'/videos/')
  target_filename = target_dir+'/videos/'+video_id+".mp4"
  os.rename(video_filename, target_filename)

if __name__=='__main__':
  response = None
  target_dir ='./data'
  for i in range(10):
    
    if i !=0:
      response = youtube_search('children using smarthphone',token=response[0])
      nexttok = response[0]
      print('Next tocken = ', nexttok)
    else:
      response = youtube_search('children using smarthphone')

    for search_res in response[1]:
      video_id = search_res['id']['videoId']
      print(video_id)
      if not video_exists(target_dir, video_id):
        print('video=', video_id, ' does not exist')
        try:
          download_youtube_video('./data',video_id)
        except (http.client.IncompleteRead) as e:
          print('Could not read video_id=', video_id)
          
          

