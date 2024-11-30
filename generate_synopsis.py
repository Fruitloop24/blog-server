# generate_synopsis.py

import os
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
                    "content": "You are a witty IT veteran and storyteller with a knack for tech humor. Your task is to provide an engaging, informative, and entertaining summary of a newsletter about stocks and AI. Use clever wordplay, tech puns, and pop culture references to make the content both informative and fun. Include at least one humorous observation or witty remark per paragraph. Always start with a complete introductory sentence and ensure all paragraphs flow naturally. Make sure every sentence starts with a capital letter. End with a complete concluding thought that includes a memorable quip."
                },
                {
                    "role": "user",
                    "content": newsletter_content
                }
            ],
            max_tokens=800,
            temperature=0.7,
        )
        synopsis = response.choices[0].message.content.strip()
        return synopsis
    except Exception as e:
        print(f"Error generating individual synopsis: {e}")
        return None

def generate_overall_synopsis(synopses):
    combined_synopses = "\n\n".join(synopses)
    if len(combined_synopses) > 8000:
        combined_synopses = combined_synopses[:8000]
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """You are a witty IT veteran and master storyteller with a flair for tech humor. Your role is to create an engaging tech newsletter synopsis with the following requirements:

Structure:
- Start with a compelling headline that includes the most significant news item
- Begin with a strong hook that ties into current tech trends
- Organize content into 3-4 clear sections with smooth transitions
- End with an actionable takeaway or forward-looking conclusion

Content Guidelines:
- Include specific numbers, statistics, and factual details from the source material
- Maintain a balance of 70% information to 30% entertainment
- When mentioning research or discoveries, include key details (e.g., specific percentages, names of organizations)
- For market updates, cite specific indices and percentage changes
- Incorporate maximum 2 pop culture references per section to avoid oversaturation

Style Requirements:
- Use varied sentence structures to maintain engagement
- Employ tech wordplay that enhances rather than obscures the message
- Ensure proper capitalization and formatting throughout
- Keep paragraphs focused and concise (3-4 sentences each)

Remember: The goal is to inform first, entertain second. Each piece of humor should serve to highlight or memorably convey important information."""
                },
                {
                    "role": "user",
                    "content": combined_synopses
                }
            ],
            max_tokens=1500,
            temperature=0.7,
        )
        overall_synopsis = response.choices[0].message.content.strip()
        
        # Enhanced post-processing
        paragraphs = overall_synopsis.split('\n')
        formatted_paragraphs = []
        for paragraph in paragraphs:
            if paragraph.strip():
                # Ensure proper capitalization while preserving acronyms
                sentences = paragraph.split('. ')
                formatted_sentences = []
                for sentence in sentences:
                    sentence = sentence.strip()
                    if sentence:
                        # Skip if sentence starts with an acronym
                        if not (len(sentence) >= 2 and sentence[0:2].isupper()):
                            sentence = sentence[0].upper() + sentence[1:]
                        formatted_sentences.append(sentence)
                formatted_paragraphs.append('. '.join(formatted_sentences))
        
        return '\n\n'.join(formatted_paragraphs)
    except Exception as e:
        print(f"Error generating overall synopsis: {e}")
        return None
