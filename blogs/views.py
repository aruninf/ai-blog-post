import os
from django.shortcuts import render, redirect
from .models import Blog
import openai  # Correct import for openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

from openai import OpenAI, completions

client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY")
)

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
       print(completion.choices[0].message.content)
    
    except Exception as e:
        print('ERROR:', e)
        return "Error generating content"

    return completion.choices[0].message.content


def index(request):
    """Home page where users can create and view blogs."""
    #print("OpenAI API Key: ", os.getenv("OPENAI_API_KEY"))


    if request.method == 'POST':
        title = request.POST['title']
        # Generate content using OpenAI for the new blog post
        content = get_api_response(title)
        # Create a new blog post object and save it to the database
        blog = Blog(title=title, content=content)
        blog.save()
        
        # Redirect to the index page to view all blog posts
        return redirect('index')

    # Fetch all blog posts from the database and display them
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'blogs': blogs})

def blog_update(request, blog_id):
    """Update an existing blog post."""
    blog = Blog.objects.get(id=blog_id)
    
    if request.method == 'POST':
        title = request.POST['title']
        # Generate new content using OpenAI for the updated blog post
        content = get_api_response(title)
        
        # Update the blog post object with the new title and content
        blog.title = title
        blog.content = content
        blog.save()
        
        # Redirect to the index page to view all blog posts
        return redirect('index')
    
    # Render the update form with the existing blog data
    return render(request, 'update_blog.html', {'blog': blog})

def blog_delete(request, blog_id):
    """Delete a blog post."""
    blog = Blog.objects.get(id=blog_id)
    blog.delete()
    # Redirect to the index page after deleting the blog
    return redirect('index')
