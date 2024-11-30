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
    # Ensure the combined synopses do not exceed context length
    if len(combined_synopses) > 8000:
        combined_synopses = combined_synopses[:8000]
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a witty IT veteran and master storyteller with a flair for tech humor. Your role is to combine multiple summaries into a single, cohesive, and entertaining blog post. Every paragraph must start with a capital letter and maintain proper sentence case throughout. Begin with an attention-grabbing introduction that sets the context for today's tech and market updates, incorporating a clever tech-related hook or pun. Each paragraph should flow naturally into the next, maintaining a consistent narrative voice while weaving in humor, pop culture references, and tech-savvy observations. Include at least one witty remark or humorous analogy per section. End with a punchy concluding paragraph that ties the main points together with a memorable tech-themed quip. Remember: proper capitalization, smooth transitions, and engaging humor are key!"
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
        # Enhanced post-processing for proper capitalization and formatting
        sentences = overall_synopsis.split(". ")
        formatted_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                # Ensure first letter is capitalized while preserving existing caps
                if not sentence[0].isupper():
                    sentence = sentence[0].upper() + sentence[1:]
                formatted_sentences.append(sentence)
        overall_synopsis = ". ".join(formatted_sentences)
        return overall_synopsis
    except Exception as e:
        print(f"Error generating overall synopsis: {e}")
        return None
