# generate_synopsis.py

import os
from hello import hello
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_individual_synopsis(newsletter_content):
    # Truncate newsletter content to a manageable length (e.g., 3000 characters)
    if len(newsletter_content) > 3000:
        newsletter_content = newsletter_content[:3000]
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a seasoned IT veteran who provides a concise, humorous, and insightful summary of a newsletter about stocks and AI."
                },
                {
                    "role": "user",
                    "content": newsletter_content
                }
            ],
            max_tokens=250,
            temperature=0.5,
        )
        synopsis = response.choices[0].message.content.strip()
        return synopsis
    except Exception as e:
        print(f"Error generating individual synopsis: {e}")
        return None

def generate_overall_synopsis(synopses):
    combined_synopses = "\n\n".join(synopses)
    # Ensure the combined synopses do not exceed context length
    if len(combined_synopses) > 8000:
        combined_synopses = combined_synopses[:8000]
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a seasoned IT veteran who combines multiple summaries into a single, cohesive, and engaging blog post, maintaining a humorous and insightful tone."
                },
                {
                    "role": "user",
                    "content": combined_synopses
                }
            ],
            max_tokens=750,
            temperature=0.5,
        )
        overall_synopsis = response.choices[0].message.content.strip()
        return overall_synopsis
    except Exception as e:
        print(f"Error generating overall synopsis: {e}")
        return None

