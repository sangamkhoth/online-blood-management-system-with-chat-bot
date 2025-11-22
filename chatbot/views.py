from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
import re
from textblob import TextBlob
from geopy.geocoders import Nominatim
import requests
import spacy

from .models import ChatMessage
from api.models import Donor, Hospital


# Load spaCy NER model
nlp = spacy.load("en_core_web_sm")


# ----------------------------
# CHAT PAGE
# ----------------------------
@login_required(login_url='/accounts/login/')
def chat_page(request):
    return render(request, "chatbot/chat.html")


# ----------------------------
# BLOOD GROUP DETECTION
# ----------------------------
def detect_blood_group(message):
    pattern = r"\b(A|B|AB|O)[+-]\b"
    match = re.search(pattern, message.upper())
    return match.group(0) if match else None


# ----------------------------
# LOCATION DETECTION (NER)
# ----------------------------
def detect_location(message):
    doc = nlp(message)
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"]:
            return ent.text
    return None


# ----------------------------
# HOSPITAL LOOKUP – OPENSTREETMAP
# ----------------------------
def find_hospitals(city):
    try:
        geolocator = Nominatim(user_agent="bloodms_app")
        loc = geolocator.geocode(city)

        if not loc:
            return ["Unable to find this location."]

        lat, lon = loc.latitude, loc.longitude
        overpass_url = "https://overpass-api.de/api/interpreter"

        query = f"""
        [out:json];
        node["amenity"="hospital"](around:5000,{lat},{lon});
        out;
        """

        res = requests.get(overpass_url, params={"data": query}, timeout=30)
        data = res.json()

        if "elements" not in data or len(data["elements"]) == 0:
            return ["No hospitals found nearby."]

        hospitals = [
            h["tags"].get("name", "Unnamed Hospital")
            for h in data["elements"][:5]
        ]

        return hospitals

    except:
        return ["Hospital service unavailable."]


# ----------------------------
# MAIN CHATBOT LOGIC
# ----------------------------
@api_view(["POST"])
def chatbot_api(request):

    message = request.data.get("message", "").strip()

    if not message:
        return Response({"response": "Please type something."})

    # Sentiment
    score = TextBlob(message).sentiment.polarity
    sentiment = (
        "Positive" if score > 0.3 else
        "Negative" if score < -0.3 else
        "Neutral"
    )

    # Extract info
    blood_group = detect_blood_group(message)
    location = detect_location(message)

    # ----------------------------
    # 1️⃣ Donor Search
    # ----------------------------
    if blood_group:

        donors = Donor.objects.filter(blood_group=blood_group)

        if location:
            donors = donors.filter(city__icontains=location)

        if donors.exists():
            lst = [
                f"{d.name} ({d.blood_group}) - {d.city}, {d.phone}"
                for d in donors
            ]
            reply = "🩸 Available Donors:\n" + "\n".join(lst)

        else:
            reply = f"❌ No {blood_group} donors found."

    # ----------------------------
    # 2️⃣ Emergency / Hospital Lookup
    # ----------------------------
    elif any(w in message.lower() for w in ["urgent", "emergency", "hospital", "accident", "help", "blood"]):

        if location:
            hospitals = find_hospitals(location)
            reply = "🚑 Nearby hospitals:\n" + "\n".join(hospitals)
        else:
            reply = "⚠️ Please mention a city (Example: 'help in Delhi')."

    # ----------------------------
    # 3️⃣ General Chat
    # ----------------------------
    else:
        if sentiment == "Positive":
            reply = "😊 Glad to hear that!"
        elif sentiment == "Negative":
            reply = "😔 I’m sorry you feel this way. I’m here to help."
        else:
            reply = "🤖 I can help you find donors or hospitals. Try: 'I need O+ blood in Delhi'."

    # Save chat
    ChatMessage.objects.create(
        user=request.user,
        message=message,
        response=reply,
        sentiment=sentiment
    )

    return Response({"response": reply})
