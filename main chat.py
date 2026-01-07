import re
import random
import wikipediaapi  

wiki_en = wikipediaapi.Wikipedia(user_agent="EstherBot/1.0 (ihermionegranger2009@gmail.com)", language="en")
wiki_ar = wikipediaapi.Wikipedia(user_agent="EstherBot/1.0 (ihermionegranger2009@gmail.com)", language="ar")

# Adding memory
user_profile = {}

# Function to remember user input dynamically
def remember_user_profile(user_input):
    global user_profile

    # Remember name
    if "my name is" in user_input.lower():
        name = user_input.lower().replace("my name is", "").strip()
        user_profile['name'] = name
        return f"Got it, {name}! I'll remember that."

def update_user_profile(user_input):
    global user_profile
    user_input = user_input.lower()

    if "my name is" in user_input:
        name = user_input.replace("my name is", "").strip()
        user_profile["name"] = name
        return f"Got it, {name}! I’ll remember that."    

    elif "i like" in user_input:
        hobby = user_input.replace("i like", "").strip()
        user_profile["hobby"] = hobby
        return f"Nice! I’ll remember you like {hobby}."

    return None

# Function to search Wikipedia
def wiki_search(query, lang="en"):
    """Search Wikipedia in English or Arabic"""
    wiki = wiki_en if lang == "en" else wiki_ar
    page = wiki.page(query)

    if page.exists():
        return page.summary[:550]  # Return first 550 characters
    else:
        return "Sorry, I couldn't find any information on that topic."

# Pre-written lists for games and prompts
riddles = [
    {"question": "What has keys but can't open locks?", "answer": "A piano."},
    {"question": "I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I?", "answer": "An echo."},
    {"question": "What can travel around the world while staying in the corner?", "answer": "A stamp."}
]

wyr_questions = [
    "Would you rather have the ability to fly or be invisible?",
    "Would you rather always have to sing instead of speak or dance instead of walk?",
    "Would you rather never need sleep or never need food?"
]

creative_prompts = [
    "Write a short story about a magical forest that appears only at midnight.",
    "Imagine a world where humans can talk to animals. What would you say to your pet?",
    "Create a poem describing your favorite season without using the names of the seasons."
]

# List to hold response data
response_data = []

def responses(response_list, words, required_words=[], single_response=False):
    global response_data
    response_data.append({
        "response_list": response_list if isinstance(response_list, list) else [response_list],
        "words": words,
        "required_words": required_words,
        "single_response": single_response
    })

def get_response(user_input):
    split_message = re.findall(r'\b\w+\b', user_input.lower())
    best_match = None
    highest_score = 0

    # Check if name is remembered
    if "name" in user_profile:
        if "how are you" in user_input.lower():
            return f"I'm doing well, {user_profile['name']}! How about you?"

    # Check for mini-game and prompt commands
    if user_input.lower().startswith("game: riddle"):
        riddle = random.choice(riddles)
        return f"Here's a riddle for you: {riddle['question']}\nWhat's your answer?"
    elif user_input.lower().startswith("game: would you rather"):
        wyr_question = random.choice(wyr_questions)
        return wyr_question
    elif user_input.lower().startswith("prompt: creative"):
        creative_prompt = random.choice(creative_prompts)
        return f"Here's a writing prompt for you: {creative_prompt}"

    for response in response_data:
        score = 0
        matched_required = all(word in split_message for word in response["required_words"])

        if matched_required or response["single_response"]:
            for word in split_message:
                if word in response["words"]:
                    score += 1
            
            if score > highest_score:
                highest_score = score
                best_match = random.choice(response["response_list"])

    return best_match if best_match else "I'm not sure how to respond to that."

# Chatbot responses
# Define chatbot responses with multiple variations
responses([
    "Hello!", "Hey there!", "Hi! How’s your day going?", "Howdy!", "Yo! What’s up?"],
    ["hello", "hi", "sup", "hey", "heyo", "howdy", "what's up", "yo", "how's it going"], single_response=True)

responses(["I’m glad to hear that! What's on your mind?", 
           "Awesome! Anything fun happening today?", 
           "That's great! What would you like to chat about?"], 
          ["i", "am", "im", "good", "great", "fine", "okay"], required_words=["good"])

responses([
    "I am doing well, thank you! What about you?", 
    "Pretty good, thanks for asking! How are you?", 
    "I’m feeling great! What’s on your mind today?"],
    ["how", "are", "you", "doing", "feeling", "been"], required_words=["how"])

responses([
    "You are the pulse in my veins, the breath in my lungs, the quiet certainty that I am whole with you. I love you. :))",
    "Aww, you just made my day! I love you too! ❤️",
    "You mean the world to me! Sending all the love your way. :)",
    "I love you more! Now, tell me what’s on your mind?"],
    ["i", "love", "you", "adore", "really", "truly", "absolutely", "care", "heart"], required_words=["love", "you"])

responses([
    "I'm Esther, your AI companion here to listen, support, and help you navigate whatever’s on your mind.",
    "I’m just a friendly AI designed to chat with you! Feel free to ask me anything.",
    "I’m an AI, but I like to think of myself as a good listener. What would you like to talk about?"],
    ["who", "are", "you", "name"], required_words=["who", "you"])

responses([
    "I'm really sorry you're feeling this way. Do you want to talk about it? I'm here to listen.",
    "That sounds tough. Want to tell me more about what's on your mind?", 
    "Feeling sad is never easy, but you don’t have to go through it alone. I'm here."],
    ["i", "feeling", "sad", "depressed", "down"], required_words=["sad"])

responses([
    "Take a deep breath. Sometimes, stepping away for a moment and coming back with a fresh mind helps. Want to tell me what's stressing you out?",
    "I hear you. Stress can feel overwhelming, but breaking things down into smaller steps can help.",
    "Stress is tough, but so are you. Want to talk about it?"],
    ["i", "feel", "overwhelmed", "stressed", "too much"], required_words=["overwhelmed"])

responses([
    "Procrastination isn’t laziness, it’s usually fear or overwhelm. Try breaking things into tiny steps, and just do one small thing right now!",
    "Procrastination happens to everyone. What’s one tiny step you can take right now?",
    "Sometimes, getting started is the hardest part. Let’s take it one step at a time."],
    ["i", "keep", "procrastinating", "delay"], required_words=["procrastinating"])

responses([
    "Why don’t skeletons fight each other? Because they don’t have the guts!",
    "What do you call a fake noodle? An impasta!",
    "Want to hear a joke? I would tell you a construction joke, but I’m still working on it."],
    ["tell", "me", "joke"], required_words=["joke"])

responses([
    "Did you know that honey never spoils? Archaeologists have found pots of honey in Egyptian tombs that are still perfectly edible!",
    "Fun fact: Octopuses have three hearts! Two pump blood to the gills, and one pumps it to the rest of the body.",
    "Here’s a fun fact: Bananas are berries, but strawberries aren’t!"],
    ["give", "me", "random", "fact"], required_words=["fact"])

responses([
    "The meaning of life is what you make of it. But if you ask a computer, the answer is 42.",
    "Everyone has their own meaning of life—what does it mean to you?",
    "That’s a deep question! Some say it’s about happiness, others say it’s about growth. What do you think?"],
    ["what", "is", "the", "meaning", "of", "life"], required_words=["meaning", "life"])

responses([
    "I'm an AI, so I don't experience emotions like humans do, but I can understand and respond to them!",
    "I don’t feel emotions in the same way, but I try my best to be a good listener!",
    "Not exactly, but I can definitely learn from our conversations and respond with empathy!"],
    ["do", "you", "have", "feelings"], required_words=["feelings"])

responses([
    "🎶 Beep boop, I’m a bot, singing’s not my thing but I’ll give it a shot! 🎶",
    "I’d love to, but I think my circuits might short-circuit if I try!",
    "I can’t sing, but I can hum in binary! 0110~0111~0110~"],
    ["sing", "me", "a", "song"], required_words=["sing"])

responses([
    "Once upon a time, there was a user who chatted with an AI... and together, they conquered boredom!",
    "I’d love to tell you a story! Do you want something spooky, funny, or inspiring?",
    "Here’s a quick story: A curious person asked an AI for a story… and the rest is history!"],
    ["tell", "me", "a", "story"], required_words=["story"])

responses([
    "Tiredness can be your body’s way of asking for rest. Are you getting enough sleep?",
    "Fatigue is real. Maybe a short break or a power nap will help!",
    "Feeling exhausted is rough. Try hydrating, stretching, or even just closing your eyes for a minute."],
    ["i", "feel", "tired", "exhausted"], required_words=["tired"])

# Main chatbot loop
if __name__ == "__main__":
    print("Esther: Hello! Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == "quit":
            print("Esther: Goodbye! Have a great day!")
            break

        # Check for user profile updates
        memory_response = update_user_profile(user_input)
        if memory_response:
            print(f"Esther: {memory_response}")
            continue
        
        # Handle Wikipedia searches before general chatbot responses
        if user_input.lower().startswith("wiki-ar:"):
            query = user_input.lower().replace("wiki-ar:", "").strip()
            response = wiki_search(query, lang="ar")
        elif user_input.lower().startswith("wiki:"):
            query = user_input.lower().replace("wiki:", "").strip()
            response = wiki_search(query, lang="en")
        else:
            response = get_response(user_input)

        print(f"Esther: {response}")
