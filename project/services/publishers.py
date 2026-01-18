from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import requests

class YouTubePublisher:
    def __init__(self, credentials_path: str):
        self.credentials = Credentials.from_authorized_user_file(credentials_path)
        self.youtube = build('youtube', 'v3', credentials=self.credentials)

    def upload_short(self, video_path: str, title: str, description: str) -> str:
        """ Upload video as youtube short """
        body = {
            'snippet': {
                'title': title[:100],  
                'description': f"{description}\n\n#Shorts",
                'tags': ['shorts', 'reddit', 'story'],
                'categoryId': '24'  
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }

        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)

        request = self.youtube.videos().insert(
            part='snippet,status',
            body=body,
            media_body=media
        )

        response = request.execute()
        video_id = response['id']

        print(f"Uploaded to Youtube: https://youtube.com/shorts/{video_id}")
        return video_id