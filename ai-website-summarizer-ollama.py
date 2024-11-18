# imports
import os
import requests
from bs4 import BeautifulSoup
from IPython.display import Markdown, display

import ollama

OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL = "llama3.2"


# Class of the webpage
# This class will be used to extract the text from a webpage, removing irrelevant tags
class WebPage:
    def __init__(self, url):
        self.url = url
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        # Remove (.decompose) irrelevant tags
        for irrelevant in soup(["script", "style", "img", "input", "button"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)

# Test the WebPage class
# cnn = WebPage("https://cnn.com/")
# print(cnn.title)
# print(cnn.text)

# Tells the LLM what task to perform and what tone to use
system_prompt = "You are an assistant that analyzes content of a website and provides a shor summary, ignoring text that might be navigation related. Respond in markdown."

# Making the prompt
def user_prompt_for(website):
    user_prompt = f"You are looking at a website title '{website.title}'"
    user_prompt += "\nThe contents of this website is as follows; \ please provide a short summary of this website in markdown \ If it includes news or announcements, then summarize these too. \n\n"
    user_prompt += website.text
    return user_prompt

# Test the user_prompt_for function
# print(user_prompt_for(cnn))

# Function to get the messages for the AI
# Creates the structure of the messages that will be sent to the AI, as it is expected
def messages_for(website):
    return [
        {"role": "user", "content": user_prompt_for(website)}
    ]

# Function to summarize the website
# This function will use the OpenAI API, using the model given, to summarize the website
def summarize(url):
    website = WebPage(url)
    response = ollama.chat(
        model=MODEL, 
        messages = messages_for(website)
    )
    return print(response['message']['content'])

# Test the summarize function
    # This will charge your account on OpenAI
#summarize("https://cnn.com/")

# Function to display the markdown
# This function will display the markdown summary of the website
    # This will charge your account on OpenAI   
def display_markdown(url):
    summary = summarize(url)
    # display(Markdown(summary)) for jupyter notebook
    print(summary)

# Main
display_markdown("https://cnn.com/")