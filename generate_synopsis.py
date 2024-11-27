# generate_synopsis.py

import os
import logging
from openai import OpenAI
from typing import Optional, List

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
if not os.environ.get("OPENAI_API_KEY"):
    logger.error("OPENAI_API_KEY not found in environment variables!")

def generate_individual_synopsis(newsletter_content: str) -> Optional[str]:
    """
    Generate a synopsis for an individual newsletter with the personality of a tech veteran.
    
    Args:
        newsletter_content (str): The content to summarize
        
    Returns:
        Optional[str]: The generated synopsis or None if generation fails
    """
    # Truncate newsletter content to a manageable length (e.g., 3000 characters)
    if len(newsletter_content) > 3000:
        newsletter_content = newsletter_content[:3000]
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a grizzled IT veteran with decades of experience in the trenches of tech. You've seen it all - from the dot-com bubble to the AI revolution. With a passion for technology, markets, and the occasional whiskey, you transform complex tech news into engaging stories. Your summaries are insightful, slightly irreverent, and peppered with references to your extensive experience in the field. Make the content engaging and accessible, but maintain the depth that tech professionals expect."
                },
                {
                    "role": "user",
                    "content": f"Here's some tech news to analyze. Break it down like you're sharing insights over a good bourbon: {newsletter_content}"
                }
            ],
            max_tokens=500,
            temperature=0.5,
        )
        synopsis = response.choices[0].message.content.strip()
        return synopsis
    except Exception as e:
        logger.error(f"Error generating individual synopsis: {str(e)}", exc_info=True)
        return None

def generate_overall_synopsis(synopses: List[str]) -> Optional[str]:
    """
    Combine multiple synopses into a cohesive narrative with veteran tech insight.
    
    Args:
        synopses (List[str]): List of individual synopses to combine
        
    Returns:
        Optional[str]: The combined synopsis or None if generation fails
    """
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
                    "content": "You're a battle-hardened tech veteran who's survived countless system migrations, market crashes, and technology shifts. Drawing from your deep experience in AI, stock trading, and enterprise architecture, weave these summaries into a compelling narrative. Share your wisdom like you're holding court at the developer's bar after hours - with wit, wisdom, and the occasional war story. Make connections between different pieces of news, point out market implications, and don't shy away from technical depth when it matters."
                },
                {
                    "role": "user",
                    "content": combined_synopses
                }
            ],
            max_tokens=1000,
            temperature=0.5,
        )
        overall_synopsis = response.choices[0].message.content.strip()
        return overall_synopsis
    except Exception as e:
        logger.error(f"Error generating overall synopsis: {str(e)}", exc_info=True)
        return None

