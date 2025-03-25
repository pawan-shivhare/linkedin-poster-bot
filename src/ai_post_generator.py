import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-3.5-turbo" 

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_post(topic, tone="Professional", word_limit=200):
    """Generates a LinkedIn post using GPT-3.5 Turbo."""
    prompt = f"""
    Write a LinkedIn post about "{topic}" in a {tone} tone.
    - Keep it engaging and insightful.
    - Use bullet points if necessary.
    - Add a compelling call-to-action at the end.
    - Stay within {word_limit} words.
    """

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Error generating AI post: {e}")
        return None

if __name__ == "__main__":
    topic = input("Enter the topic for your LinkedIn post: ")
    generated_post = generate_post(topic)
    if generated_post:
        print("\n📝 AI-Generated LinkedIn Post:\n")
        print(generated_post)
