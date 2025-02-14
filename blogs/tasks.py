from celery import shared_task
from django.apps import apps
from dotenv import load_dotenv
import os
from openai import OpenAI, completions

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key from environment variable
OpenAI.api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY")
)

@shared_task
def auto_post_blog():
    # Import the model here to avoid it being accessed before app loading
    Blog = apps.get_model('blogs', 'Blog')
    business_info = "Our company offers innovative IT solutions for various industries."
    title = "Business Update"
    content = get_api_response(business_info)  # Generate AI content using OpenAI API

    # Now use the Blog model to create a new blog post
    #title = "Business Information"
    #content = "Generated content about business"
    blog = Blog(title=title, content=content)
    blog.save()




def get_api_response(prompt: str) -> str:
    """Generate content using OpenAI API."""
    try:
        # Use openai.ChatCompletion.create for OpenAI API request
       completion = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {"role": "user", "content": "Write a short content (max line 3) about " + prompt},
            ]
        )
        # Extract the response text
        #print(completion.choices[0].message.content)
    
    except Exception as e:
        print('ERROR:', e)
        return "Error generating content"
    return completion.choices[0].message.content
