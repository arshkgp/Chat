import streamlit as st
import spacy
import requests

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Predefined travel data
DESTINATIONS = {
    "japan": {
        "places": ["Tokyo", "Kyoto", "Mt. Fuji", "Osaka", "Hiroshima"],
        "best_time": "March - May (Spring, Cherry Blossoms) & September - November (Autumn)",
        "avg_cost": "$2000 - $4000 per person (flight, stay, food, sightseeing)",
    },
    "paris": {
        "places": ["Eiffel Tower", "Louvre Museum", "Notre Dame", "Seine River"],
        "best_time": "April - June & September - October",
        "avg_cost": "$1500 - $3000 per person",
    },
    "bali": {
        "places": ["Ubud", "Kuta Beach", "Tanah Lot Temple", "Tegallalang Rice Terraces"],
        "best_time": "April - October",
        "avg_cost": "$1000 - $2500 per person",
    },
}

# Function to get weather data (Free API)
def get_weather(city):
    api_key = "YOUR_OPENWEATHER_API_KEY"  # Get from https://openweathermap.org/api
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    
    if response.get("main"):
        temp = response["main"]["temp"]
        condition = response["weather"][0]["description"]
        return f"{temp}°C, {condition}"
    return "Weather data unavailable."

# Function to extract destination from user query
def extract_destination(text):
    doc = nlp(text.lower())
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"]:  # Geographical locations
            return ent.text
    return None

# Streamlit UI
st.title("✈️ AI Travel Planner")
st.markdown("Plan your dream trip with AI-powered travel suggestions!")

user_input = st.text_input("Ask me about travel destinations, itineraries, or costs:")

if user_input:
    destination = extract_destination(user_input)

    if destination in DESTINATIONS:
        data = DESTINATIONS[destination]
        st.write(f"🌍 **{destination.capitalize()} Travel Guide**")
        st.write(f"📍 **Must-Visit Places:** {', '.join(data['places'])}")
        st.write(f"🗓️ **Best Time to Visit:** {data['best_time']}")
        st.write(f"💰 **Estimated Cost:** {data['avg_cost']}")

        # Weather info
        st.write(f"☀️ **Current Weather in {destination.capitalize()}:** {get_weather(destination)}")
    
    else:
        st.write("🤖 Sorry, I don't have information on that location yet! Try Japan, Paris, or Bali.")

st.sidebar.markdown("💡 **Try asking:**")
st.sidebar.write("👉 'I want to visit Japan in April. What are some must-visit places?'")
st.sidebar.write("👉 'How much does a trip to Bali cost?'")
st.sidebar.write("👉 'Best time to visit Paris?'")
