import random
from pathlib import Path
from moviepy import VideoFileClip, AudioFileClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
import whisper

class VideoProcessor:
    def __init__(self, background_dir = "backgrounds", output_dir = "output/videos"):
        """ Initiate Video Processing Assembly """
        self.background_dir = Path(background_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.whisper_model = whisper.load_model("base")

    def get_random_background_montage(self) -> str:
        """ Receive a Random Background Montage """
        videos = list(self.background_dir.glob(".mp4"))
        if not videos:
            raise Exception("No background videos found")
        return str(random.choice(videos))
     
    def generate_subtitles(self, audio_path: str) -> str:
        """ Transcribe audio and create """
        result = self.whisper_model.transcribe(audio_path, word_timestamps = True)

        srt_path = audio_path.replace(".wav", ".srt")

        with open(srt_path, 'w', encoding='utf-8') as f:
            counter = 1
            for segment in result['segment']:
                words = segment.get('words', [])
                if words:
                    for word in words:
                        start = word['start']
                        end = word['end']
                        text = word['word'].strip()

                        f.write(f"{counter}\n")
                        f.write(f"{self._format_timestamp(start)} --> {self._format_timestamp(end)}\n")
                        f.write(f"{text}\n\n")
                        counter += 1
                else:
                    start = segment['start']
                    end = segment['end']
                    text = segment['text'].strip()

                    f.write(f"{counter}\n")
                    f.write(f"{self._format_timestamp(start)} --> {self._format_timestamp(end)}")
                    f.write(f"{text}\n\n")
                    counter += 1
        return srt_path

    def _format_timestamp(self, seconds: float) -> str:
        """ Convert seconds to SRT timestamp format """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600)// 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def create_video(self, audio_path: str, output_filename: str) -> str:
        """ Combine Video, Audio and Subtitles """
        from moviepy.video.VideoClip import TextClip
        from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

        bg_video_path = self.get_random_background_montage()
        bg_video = VideoFileClip(bg_video_path)

        audio =  AudioFileClip(audio_path)
        audio_duration = audio.duration;

        if bg_video.duration < audio.duration:
            n_loops = int(audio_duration / bg_video.duration) + 1
            bg_video = bg_video.loop(n_loops)
        bg_video = bg_video.subclip(0, audio.duration)

        target_width, target_height = 1080, 1920
        bg_video = bg_video.resize(height=target_height) 
        

    
