import streamlit as st
import ollama
from gtts import gTTS
import os

st.title("Story Creator")

# Character management in the sidebar
with st.sidebar:
    st.header("Manage Characters")
    num_characters = st.number_input("Number of Characters", min_value=1, value=2)

characters = []

# Dynamic character input using the main page
for i in range(num_characters):
    st.subheader(f"Character {i+1}")
    character_name = st.text_input(f"Character {i+1} Name", key=f"name_{i}")
    traits = st.text_area(f"Character {i+1} Traits", key=f"traits_{i}")
    habits = st.text_area(f"Character {i+1} Habits", key=f"habits_{i}")
    desires = st.text_area(f"Character {i+1} Desires", key=f"desires_{i}")
    relations = st.text_area(f"Character {i+1} Relations", key=f"relations_{i}")
    characters.append({
        "name": character_name,
        "traits": traits,
        "habits": habits,
        "desires": desires,
        "relations": relations
    })

# Story setting and tone input
setting = st.text_input("Setting")
tone = st.selectbox("Tone", ["Humorous", "Dramatic", "Mysterious", "Adventurous"])

def generate_story(characters, setting, tone):
    character_descriptions = []
    for character in characters:
        desc = (f"{character['name']} is characterized by {character['traits']}. "
                f"They have the habit of {character['habits']} and desire {character['desires']}. "
                f"They are related to others as follows: {character['relations']}.")
        character_descriptions.append(desc)

    # Combine character descriptions into a single prompt
    character_prompt = " ".join(character_descriptions)
    prompt = f"Create a {tone} story set in {setting} featuring the following characters: {character_prompt}"

    # Call the chat function with the prompt
    response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
    
    # Extract the generated story from the response
    story = response['message']['content']
    
    return story

def generate_image_prompt(characters, setting, tone):
    character_descriptions = []
    for character in characters:
        desc = (f"{character['name']} is characterized by {character['traits']}. "
                f"They have the habit of {character['habits']} and desire {character['desires']}. "
                f"They are related to others as follows: {character['relations']}.")
        character_descriptions.append(desc)

    # Combine character descriptions into a single detailed prompt
    character_prompt = " ".join(character_descriptions)
    
    # Define the image prompt
    prompt = (f"Generate a flat, vibrant illustration capturing a key moment from a {tone} story set in {setting}. "
              f"The scene features the following characters: {character_prompt}. "
              f"Focus on depicting the essence of their traits, interactions, and desires in a single frame. "
              f"The illustration should be clear and minimalistic, using clean lines and a cohesive style to convey the tone of the story. "
              f"Include visual elements that reflect the ambiance of the setting, with appropriate lighting and color schemes to match the {tone} nature of the narrative. "
              f"Make sure the image is detailed, visually cohesive, and suitable for use in a video adaptation of the story, with a modern and engaging artistic style.")

    return prompt


# Function to convert text to speech
def convert_to_audio(text, language="en"):
    tts = gTTS(text=text, lang=language)
    tts.save("story.mp3")
    return "story.mp3"

# Story generation button
if st.button("Generate Story"):
    if all(char['name'] and char['traits'] and char['habits'] and char['desires'] and char['relations'] for char in characters) and setting:
        story = generate_story(characters, setting, tone)
        st.write(story)
        
        # Generate the image prompt
        image_prompt = generate_image_prompt(characters, setting, tone)
        st.write("Prompt for Image Generation:", image_prompt)
        
        # Convert the story to audio
        audio_file = convert_to_audio(story)
        st.audio(audio_file)
        
        # Optionally, offer a download link
        with open(audio_file, "rb") as file:
            btn = st.download_button(
                label="Download Audio",
                data=file,
                file_name="story.mp3",
                mime="audio/mp3"
            )
    else:
        st.write("Please fill out all the fields for each character to generate the story.")
