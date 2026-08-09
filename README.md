# Review Intelligence Agent

## Overview

Review Intelligence Agent is a proof-of-concept application that analyzes app store reviews using AI and presents aggregated insights for product teams.

The goal of the tool is to help identify recurring issues, understand user sentiment, detect potential release-related problems, and prioritize reviews that may require human attention.

Instead of reviewing feedback manually one review at a time, the system processes reviews, extracts structured information, and groups similar issues into meaningful themes.

---

## Features

### AI Review Analysis

Each review is analyzed and enriched with:
- Category
- Theme
- Issue summary
- Sentiment
- Severity
- Suggested action
- Human reply recommendation

Example insights:
- Crash-related issues
- Performance complaints
- Payment problems
- Feature requests
- Account-related issues

---

### Issue Aggregation

The application groups similar user feedback into common themes.
For example:
- "App crashes on startup"
- "Game closes immediately"
- "Crash after update"

are grouped under a common theme such as:
`Crash`
This helps identify recurring problems instead of isolated reviews.
---

### Product Insights Dashboard

The dashboard provides different views of the analyzed reviews:
- Review-level analysis
- Issues by application
- Issues by release version
- Common themes
- Severity distribution
- Reviews requiring human attention
- AI-generated reply suggestions

---

## Project Structure
.
├── app.py                  # Streamlit application
├── review_agent.py         # AI review analysis logic
├── insights_agent.py       # Aggregation and insights generation
├── reply_agent.py          # AI reply suggestions
├── requirements.txt
└── sample_reviews.xlsx     # Example input dataset

---

## Technology Stack
- Python
- Streamlit
- OpenAI API
- Pandas
- OpenPyXL
- python-dotenv

---

## Running the Project

### 1. Clone the repository
git clone <repository-url>

### 2. Create a virtual environment
python -m venv venv

Activate:
Mac/Linux:
source venv/bin/activate

Windows:
venv\Scripts\activate


### 3. Install dependencies
pip install -r requirements.txt


### 4. Configure environment variables
Create a `.env` file:
OPENAI_API_KEY=api_key

### 5. Run the application
streamlit run app.py

---

## Input Format
The application accepts an Excel file containing app store reviews.
Required columns:
| Column | Description |
|---|---|
| app | Application name |
| country | Review country |
| date | Review date |
| version | Application version |
| rating | Review rating |
| language | Review language |
| review_text | Review content |

## Status
This project is a proof-of-concept implementation.