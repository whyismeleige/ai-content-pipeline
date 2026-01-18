import asyncio
from services import ScriptGenerator, PiperTTS, VideoProcessor, YouTubePublisher
from datetime import datetime

class ContentPipeline:
    def __init__(self, model_path=None):
        """Intialize content pipeline with option TTS model path"""

        self.script_gen = ScriptGenerator()
        self.tts = PiperTTS(model_path=model_path, output_dir="output")
        self.video_processor = VideoProcessor()

        self.youtube = YouTubePublisher("credentials/youtube_token.json")
    async def run(self):
        """ Generate a random script using a random prompt """
        print("Starting daily content generation....")

        print("Step 1: Generate Script...")
        response = await self.script_gen.generate_random_script()

        script_text = response['message']['content']
        print(f"\n[Generated Script]: \n{script_text}\n")

        print("Step 2: Saving Script...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        script_filename = f"output/scripts/script_{timestamp}.txt"

        import os
        os.makedirs("output/scripts", exist_ok=True)

        with open(script_filename, 'w') as f:
            f.write(script_text)
        print(f"Script saved: {script_filename}")

        print("Step 3: Converting to Speech...")
        audio_filename = f"audio_{timestamp}"
        audio_path = self.tts.text_to_speech(script_text, audio_filename)

        print("Step 4: Assembling the Video...")
        video_path = self.video_processor.create_video(audio_path,f"video_{timestamp}")

        print("Step 5: Publishing...")
        title = script_text.split('\n')[0][:100]

        try:
            print("Publishing to YouTube...")
            yt_id = self.youtube.upload_short(video_path, title, script_text)
            
            print(f"\n Success in Publishing!!!")
            print(f"YouTube Link: https://youtube.com/shorts/{yt_id}")
        except Exception as e:
            print(f"Publishing Failed: {e}")

        print(f"\n{'='*50}")
        print(" Content Generation complete! ")
        print(f"Script: {script_filename}")
        print(f"Audio: {audio_path}")
        print(f"{'='*50}\n")

        return {
            'script': script_text, 
            'script_file': script_filename,
            'audio_file': audio_path
        }

async def main():
    """ Entry point for the application """

    model_path = "models/en_US-amy-medium.onnx"

    pipeline = ContentPipeline(model_path=model_path)
    await pipeline.run()

if __name__ == "__main__":
    asyncio.run(main()) 