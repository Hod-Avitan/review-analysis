import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def analyze_review(review_text, rating, version=None):

    prompt = f"""
You are an app store review analyst.

Analyze this app store review and return ONLY JSON.

Return this exact structure:

{{
  "category": "",
  "theme": "",
  "issue_summary": "",
  "sentiment": "",
  "severity": "",
  "requires_human_reply": false,
  "suggested_action": ""
}}

Rules:

category:
Choose one:
- Bug
- Feature Request
- Performance
- Payment
- Account/Login
- Positive Feedback
- Other


theme:
This must be a broad recurring issue category.
Use consistent names across reviews.

Examples:

Review:
"App crashes on startup"
"App crashes after update"
"Game closes immediately"

theme:
"Crash"


Review:
"App freezes"
"Game is very slow"
"Performance dropped after update"

theme:
"Performance"


Review:
"Cannot sign in"
"Login stopped working"

theme:
"Login Issue"


issue_summary:
Provide a short description of the specific user complaint.
Do not use this field for grouping.
Example:
"Crash occurs immediately after launching the app"


sentiment:
Choose one:
- Positive
- Neutral
- Negative


severity:
Choose one:
- Low
- Medium
- High
- Critical


requires_human_reply:
Set to true only when:
- user is extremely frustrated
- rating is 1 star
- mentions losing money, progress, or account access
- requires empathy or personal handling


suggested_action:
Examples:
- Investigate bug
- Prepare auto reply
- Escalate to support
- Monitor


App Version:
{version}


Review:
{review_text}


Rating:
{rating}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={
            "type": "json_object"
        }
    )

    return json.loads(
        response.choices[0].message.content
    )
