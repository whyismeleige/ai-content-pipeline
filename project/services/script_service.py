import random
from ollama import Client
from prompts import reddit_prompts

class ScriptGenerator:
    def __init__(self):
        self.ollama = Client()

    async def generate_random_script(self):
        """ Generate a random script using a random prompt from reddit_prompts """
        prompt = random.choice(reddit_prompts)

        response = self.ollama.chat(
            model='llama3.2',
            messages=[
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )
        
        return response