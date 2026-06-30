import google.generativeai as genai
from serpapi import GoogleSearch

# API Keys
gemini_key = "Put_Your_key"
serpapi_key = "Put_Your_serpapi_key"

# Configure Gemini
genai.configure(api_key=os.getenv("API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

chat_history = []


# Function for real-time search
def get_live_data(query):
    params = {
        "engine": "google",
        "q": query,
        "api_key": serpapi_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    if "organic_results" in results:
        return results["organic_results"][0]["snippet"]

    return "No live data found."


while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Bot: Goodbye!")
        break

    # Check for live queries
    if "bitcoin" in user_input.lower() or "weather" in user_input.lower():
        live_result = get_live_data(user_input)
        print("Bot (Live):", live_result)
        continue

    # Save user message
    chat_history.append({
        "role": "user",
        "content": user_input
    })

    # Build context
    context = ""

    for message in chat_history:
        context += f"{message['role']}: {message['content']}\n"

    # Gemini response
    response = model.generate_content(context)

    print("Bot:", response.text)

    # Save bot reply
    chat_history.append({
        "role": "assistant",
        "content": response.text
    })