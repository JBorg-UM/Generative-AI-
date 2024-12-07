import streamlit as st
import json
import openai


def load_stories():
    """Load existing stories from JSON file"""
    try:
        with open('stories.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_stories(stories):
    """Save updated stories to JSON file"""
    with open('stories.json', 'w') as f:
        json.dump(stories, f, indent=4)

def generate_story(prompt, stories):
    """Generate a new story using GPT-3.5"""
    client = openai.OpenAI(api_key=OPENAI)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a creative storyteller. Create a story with a title and approximately 100 words of content."},
            {"role": "user", "content": f"Create a new story based on: {prompt}"}
        ],
        temperature=1.0
    )
    
    # Extract title and story from response
    content = response.choices[0].message.content
    try:
        parts = content.split('\n', 2)
        title = parts[0].replace('Title:', '').strip()
        story = parts[2].replace('Story:', '').strip()
        return title, story
    except:
        return "Untitled", content

def setup_page():
    """Setup the initial page layout"""
    st.title("Story Generator")
    st.write("Enter a prompt to generate a new story using GPT-3.5.")

def handle_story_generation(prompt, stories):
    """Handle the story generation and display"""
    if prompt.strip():
        with st.spinner("Generating story..."):
            title, story = generate_story(prompt, stories)
            stories.append({"title": title, "story": story})
            save_stories(stories)

            # Display the new story
            st.subheader(f"Title: {title}")
            st.write(story)
            
            # Display the image
            st.image("NYC Desktop Wallpaper 3.png", caption="NYC Wallpaper")
    else:
        st.error("Please enter a valid prompt.")
    return title,story

def run_app():
    """Main function to run the application"""
    setup_page()
    stories = load_stories()
    prompt = st.text_input("Enter a story prompt:")
    
    story = None
    title = None
    
    if st.button("Generate Story"):
        title, story = handle_story_generation(prompt, stories)
        
        # Print to terminal only when story is generated
        if title and story:
            print("\nGenerated Story:")
            print(f"Title: {title}")
            print(f"Story: {story}")
    
    return story, title

# Start the application
story, title = run_app()
print(title)
print(story)
