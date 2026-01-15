import os 
import subprocess
from pathlib import Path
from typing import Optional

class PiperTTS:
    """ Text to Speech service using Piper """

    def __init__(self, model_path: Optional[str] = None, output_dir: str = "output"):
        """ Intialize Piper TTS service """
        self.model_path = model_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def text_to_speech(self, text: str, output_filename: str) -> str:
        """ Convert text to speech using Piper """
        output_path = self.output_dir / f"{output_filename}.wav"

        try:
            cmd = ["piper"]
            if self.model_path: cmd.extend(["--model", self.model_path])

            cmd.extend(["--output_file", str(output_path)])

            process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            stdout, stderr = process.communicate(input=text)

            if process.returncode != 0:
                raise Exception(f"Piper TTS failed: {stderr}")

            print(f"Audio generated: {output_path}")
            return str(output_path)
        except FileNotFoundError:
            raise Exception("Piper TTS not found. Please install Piper first.")
        except Exception as e:
            raise Exception(f"Error generating speech: {str(e)}")
    
    def text_to_speech_from_file(self, text_file: str, output_filename: str) -> str:
        """ Convert text from a file to speech """

        with open(text_file, 'r') as f:
            text = f.read()

        return self.text_to_speech(text, output_filename)