from flask import Flask, render_template, request
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

def generate_bio(name, color_palette):
    prompt = f"""Generate a short, engaging bio for {name}. 
    Use a friendly and professional tone. 
    The bio should be 2-3 sentences long and highlight personal branding.
    Consider this color palette: {color_palette} in the personality."""
    
    response = model.generate_content(prompt)
    return response.text

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form['name']
    color_palette = request.form['colors']
    
    links = []
    for i in range(5):
        title = request.form[f'link_title_{i}']
        url = request.form[f'link_url_{i}']
        if title and url:
            links.append({'title': title, 'url': url})
    
    bio = generate_bio(name, color_palette)
    
    return render_template('result.html', 
                         name=name, 
                         bio=bio, 
                         links=links, 
                         colors=color_palette)

if __name__ == '__main__':
    app.run(debug=True) 