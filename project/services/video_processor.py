import random
from pathlib import Path
from moviepy import VideoFileClip, AudioFileClip, CompositeVideoClip
from moviepy.video.VideoClip import TextClip
import whisper

class VideoProcessor:
    def __init__(self, background_dir="backgrounds", output_dir="output/videos"):
        """Initiate Video Processing Assembly"""
        self.background_dir = Path(background_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.whisper_model = whisper.load_model("base")

    def get_random_background_montage(self) -> str:
        """Receive a Random Background Montage"""
        videos = list(self.background_dir.glob("*.mp4"))
        if not videos:
            raise Exception("No background videos found")
        return str(random.choice(videos))
    
    def create_video(self, audio_path: str, output_filename: str) -> str:
        """Combine Video, Audio and Subtitles"""
        
        print("Loading background video...")
        bg_video_path = self.get_random_background_montage()
        bg_video = VideoFileClip(bg_video_path)

        print("Loading audio...")
        audio = AudioFileClip(audio_path)
        audio_duration = audio.duration

        # Loop and trim background video to match audio duration
        print("Processing background video...")
        if bg_video.duration < audio_duration:
            n_loops = int(audio_duration / bg_video.duration) + 1
            bg_video = bg_video.looped(n_loops)
        bg_video = bg_video.subclipped(0, audio_duration)

        # Resize and crop to 9:16 aspect ratio
        target_width, target_height = 1080, 1920
        bg_video = bg_video.resized(height=target_height)

        if bg_video.w > target_width:
            x_center = bg_video.w / 2
            x1 = x_center - target_width / 2
            bg_video = bg_video.cropped(x1=x1, width=target_width)

        bg_video = bg_video.with_audio(audio)

        # Generate subtitles using Whisper
        print("Transcribing audio with Whisper...")
        result = self.whisper_model.transcribe(audio_path, word_timestamps=True)
        
        # Create individual text clips for each word
        print("Creating subtitle clips...")
        subtitle_clips = []
        
        for segment in result['segments']:
            words = segment.get('words', [])
            if words:
                for word in words:
                    start_time = word['start']
                    end_time = word['end']
                    text = word['word'].strip().upper()
                    
                    print(f"The word is {text}")
                    if not text:
                        continue
                        
                    try:
                        # FIXED TEXT CLIP
                        txt_clip = TextClip(
                            text=text, 
                            font_size=120,     # Set a fixed, reasonable font size
                            color='yellow',
                            stroke_color='black',
                            stroke_width=6,    # Lower this, 15 is too thick for this size
                            method='label'     # 'label' creates text that fits the content, not a box
                        ).with_position('center').with_start(start_time).with_duration(end_time - start_time)
                        
                        subtitle_clips.append(txt_clip)
                    except Exception as e:
                        print(f"Warning: Failed to create text clip for '{text}': {e}")
                        continue
        
        print(f"Created {len(subtitle_clips)} subtitle clips")
        
        # Composite everything
        print("Compositing final video...")
        final_video = CompositeVideoClip([bg_video] + subtitle_clips)

        # Write to file
        output_path = self.output_dir / f"{output_filename}.mp4"
        print(f"Writing video to: {output_path}")
        
        final_video.write_videofile(
            str(output_path),
            fps=30,
            codec='libx264',
            audio_codec='aac',
            preset='medium',
            threads=4
        )

        # Cleanup
        print("Cleaning up...")
        bg_video.close()
        audio.close()
        final_video.close()

        return str(output_path)