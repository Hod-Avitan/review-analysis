import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_reply(review_text):

    prompt = f"""
You are a customer support agent for a mobile app.

Write a short friendly response to this review.

Rules:
- Do not promise fixes or dates
- Be empathetic
- Encourage contacting support if needed
- Keep it under 50 words

Follow app store review guidelines.
Never:
- ask for personal information
- promise refunds
- blame the user
- disclose internal issues
- provide unsupported claims

Review:
{review_text}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content