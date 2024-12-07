import ollama
import random
import json

# Configure Ollama to use GPU
def setup_ollama_gpu():
    try:
        # Set GPU configuration when creating chat messages
        gpu_config = {
            'numa': True,  # Enable NUMA optimization
            'gpu_layers': -1,  # Use all available GPU layers (-1 means use all)
            'context_size': 5048,  # Adjust based on your GPU memory
        }
        return gpu_config
    except Exception as e:
        print(f"Warning: GPU setup failed - {str(e)}")
        return {}

def ceo_generate_title(model="llama3.2:latest",story_titles=[]):

    themes = [
        "space exploration", "ancient myths", "romance in dystopia",
        "time travel mysteries", "epic fantasy", "urban legends",
        "cyberpunk futurism", "post-apocalyptic survival",
        "supernatural mysteries", "dark academia", "steampunk adventures",
        "mythical creatures", "psychological thrillers", "utopian societies",
        "cosmic horror", "revenge tales", "epic war stories",
        "forbidden love", "magic realism", "lost civilizations",
        "environmental dystopia", "parallel universes",
        "artificial intelligence revolts", "heists and schemes",
        "heros journey", "underwater worlds", "historical retellings",
        "ancient curses", "alien invasions", "shape-shifters and doppelgängers",
        "ethereal love stories", "time loops", "rogue outlaws",
        "lost artifacts", "space westerns", "fae realms"
        ]
    theme_choice = random.choice(themes)
    
    prompt = f"""You are a creative CEO, and your task is to generate a unique story title based on the theme "{theme_choice}". 
        Ensure the title adheres to the following guidelines:

        Guidelines:
            - Avoid patterns like "Echoes of", "The Last...", "Beyond the..."
            - Use creative structures (single words, questions, metaphors, action statements)
            - Limit the title to 3-7 words
            - Create strong emotions and vivid imagery
            - The title must NOT repeat or closely resemble any of the following existing titles: {story_titles}
            - Return ONLY the title, no explanations

        Example structures (do not copy):
            - The Memory Thieves
            - Who Dreams of Tomorrow?
            - A Symphony of Shadows
            - Chasing the Crimson Sky
            - Scarlet Algorithms"""

    gpu_config = setup_ollama_gpu()
    response = ollama.chat(
        model=model,
        messages=[{'role': 'user', 'content': prompt}],
        options=gpu_config  # Add GPU configuration
    )
    return response['message']['content'],theme_choice
def Create_storeis_team_effort(title):
    print(f"Creating story with title: {title}")
    agents = {
        "World_Builder": {
            "prompt": f"""You are the World Builder agent.
            For the story titled "{title}", create the setting and atmosphere in exactly 25 words.
            Focus on the world, environment, and mood.
            Return only your 100-word contribution."""
        },
        
        "Character_Creator": {
            "prompt": f"""You are the Character Creator agent.
            For the story titled "{title}", introduce the main characters in exactly 25 words.
            Focus on their personalities and conflicts.
            make sure the charecters are gender neutral
            Previous text: {{previous_text}}
            Return only your 100-word contribution."""
        },
        
        "Plot_Developer": {
            "prompt": f"""You are the Plot Developer agent.
            For the story titled "{title}", develop the main action in exactly 25 words.
            Focus on the central conflict and events.
            Previous text: {{previous_text}}
            Return only your 100-word contribution."""
        },
        
        "Story_Resolver": {
            "prompt": f"""You are the Story Resolver agent.
            For the story titled "{title}", create the conclusion in exactly 25 words.
            Focus on resolving the conflict and ending.
            Previous text: {{previous_text}}
            Return only your 100-word contribution."""
        }
    }
    story_parts = []
    for agent_name, prompt_data in agents.items():
        gpu_config = setup_ollama_gpu()
        response = ollama.chat(
            model="llama3.2:latest",
            messages=[{'role': 'user', 'content': prompt_data["prompt"].format(previous_text=" ".join(story_parts))}],
            options=gpu_config
        )
        story_parts.append(response['message']['content'].strip())

        # Combine all parts into final story
    final_story = " ".join(story_parts)
    return final_story  
def Create_storeis_single_agents(title,theme_choice):
    print(f"Creating story with title: {title}\n")
    agents = {
    "Agent_1": {
        "prompt": f"""You are a storytelling AI. Write a short and complete story inspired by the title '{{title}}' and the theme '{{theme_choice}}'.
        1. Create a vivid and imaginative world that reflects the theme '{{theme_choice}}'.
        2. Introduce unique, gender-neutral characters who enhance the emotional depth of the story.
        
        4. Conclude with a twist or a meaningful resolution that aligns with the title and theme.
        5. Use rich, engaging language to captivate the reader.
        6make sure the story is  approxemtely 500 words long and in one paragprh not less than 400 words """
    },
    
    "Agent_2": {
        "prompt": f"""You are a storytelling AI. Write a complete and concise short story based on the title '{{title}}' and the theme '{{theme_choice}}'.
        1. Create a compelling conflict or central event tied to the theme '{{theme_choice}}'.
        2. Immerse the reader in an imaginative setting that aligns with the title '{{title}}'.
        3. Develop gender-neutral characters that drive the narrative forward.
        5. Use vivid descriptions and emotional depth to leave a lasting impression.
        6:make sure the story is  approxemtely 500 words long and in one paragprh not less than 400 words """
    },
    
    "Agent_3": {
        "prompt": f"""You are a storytelling AI tasked with crafting a unique short story inspired by the title '{{title}}' and the theme '{{theme_choice}}'.
        1. Create a concise, impactful narrative that fully explores the world suggested by '{{theme_choice}}'.
        2. Focus on character actions and decisions that reveal the emotional core of the story.
        3. Ensure the story has a clear structure, including a beginning, a central conflict, and a resolution.
        4. The story must be complete, engaging, and   approxemtely 500 words and in one paragraph and not less than 400 words.
        """
    },
    
    "Agent_4": {
        "prompt": f"""You are a storytelling AI. Write a complete and engaging short story inspired by the title '{{title}}' and the theme '{{theme_choice}}'.
        1. Develop a concise narrative that reflects the essence of '{{theme_choice}}'.
        2. Highlight imaginative settings and meaningful character actions to create a strong emotional connection.
        3. Conclude the story with a twist or a thought-provoking ending that aligns with the title '{{title}}'.
        4. Keep the story within  approxemtely 500 words but not less than 400 words, ensuring it feels complete and impactful and in one paragraph.
         """
    }
}


    story_parts = []
    for agent_name, agent_data in agents.items():
        print(f"\n=== {agent_name}'s Version ===")
        gpu_config = setup_ollama_gpu()
        response = ollama.chat(
            model="llama3.2:latest",
            messages=[{'role': 'user', 'content': agent_data["prompt"].format(title=title, theme_choice=theme_choice)}],
            options=gpu_config
        )
        story = response['message']['content'].strip()
       # story_parts.append(response['message']['content'].strip())
       
       
        story_parts.append(story)
        story_parts.append("\n")
        #print(story)
        #print("-" * 50)  # Separator line


    

    # Optionally, you could return all stories
    return story_parts
def CEO_choose_from4_stories(model,stories,title):
     
        print("choosing the best story from the 4 ai agents")
        
        prompt = f"""You are a the CEO of a publishing book company,and a story choosing expert and your task is to choose the best story from the 4 that are in {stories}

        make sure to choose the best story based on the title{title} ONLY OUTPUT THE STORY THAT YOU CHOOSE"""


        response = ollama.chat(model=model, messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ])
       
        return response['message']['content'].strip()

def CEO_final_decision(model,stories,story,title,theme):
        print("choosing the best story from the 4 ai agents and the team effort")
       
        prompt = f"""
            You are the CEO of a leading publishing company and an expert in selecting compelling stories. 
            Your task is to evaluate two stories and choose the best one based on the given title "{title}" and their alignment with the selected theme: "{theme}".
            DO NOT CREATE A NEW STORY JUST CHOOSE THE BEST ONE
            The stories you need to choose from are:

            Story 1: {story}
            Story 2: {stories}

            Instructions:
            1. Reflect thoroughly on both stories to assess how well each aligns with the title "{title}" and the theme "{theme}".
            2. Evaluate the creativity, coherence, and emotional impact of each story.
            3. Consider which story will resonate more deeply with the audience and has stronger market potential.
            4. Once the best story is selected, return ONLY the story that you choose and dont tell me if its story 1 or 2. and DONT output the title or theme
              Do NOT provide any explanations, reflections, or assessments in your output. 
            """


        response = ollama.chat(model=model, messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ])
        return response['message']['content'].strip()

story_titles = []
model="llama3.2:latest"
output_data = {}
for n in range(5000):
        title,theme_choice=ceo_generate_title(model,story_titles=story_titles)
        print(title)
        print(theme_choice)
        story=Create_storeis_team_effort(title)
        print(f"The team effort story is ...........\n{story}")
        stories=Create_storeis_single_agents(title,theme_choice)
        
       
        best_story_from_4_agents=CEO_choose_from4_stories(model, stories,title)
        print(best_story_from_4_agents)

        final_story=CEO_final_decision(model,best_story_from_4_agents,story,title,theme_choice)
        print(final_story)
                
        # Add this new code to save to JSON
        try:
            # Try to load existing data
            with open('stories.json', 'r') as f:
                stories_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # If file doesn't exist or is empty, start with empty list
            stories_data = []
        
        # Append new story
        stories_data.append({
            "title": title,
            "story": final_story
        })
        
        # Save updated data
        with open('stories.json', 'w') as f:
            json.dump(stories_data, f, indent=4)
                
               
file_path = "stories.json"  # Replace with the actual file path

# Open and parse the JSON file
with open(file_path, "r") as f:
    stories_data = json.load(f)

# Count the number of titles
number_of_titles = len(stories_data)

# Display the result
print(f"Number of titles: {number_of_titles}")
#391 stories