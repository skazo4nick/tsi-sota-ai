import os
from dotenv import load_dotenv
load_dotenv()
from mistralai import Mistral

def main():
    try:
        # Retrieve the Mistral API key from environment variables
        api_key = os.environ["MISTRAL_API_KEY"]
        model = "mistral-small-latest"

        # Initialize the Mistral client
        client = Mistral(api_key=api_key)

        # Send a test chat message
        chat_response = client.chat.complete(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": "What is the best French cheese?",
                },
            ]
        )

        # Print the response from the Mistral API
        print(chat_response.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
