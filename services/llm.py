import ollama


class LLMService:

    def __init__(self):

        self.model = "llama3.1:latest"

        print(f"Using LLM : {self.model}")

    def generate_response(self, prompt):

        print("\nGenerating response...\n")

        response = ollama.chat(

            model=self.model,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]