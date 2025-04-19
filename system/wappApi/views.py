from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from .models import twilioModel
from google import genai
import os
from dotenv import load_dotenv
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Create your views here.
@csrf_exempt
def reply_whatsapp(req, message="", to=None, sender=None, action=None, method='POST', status_callback=None):
    response = MessagingResponse()
    WaID = req.POST.get("WaId")
    message = req.POST.get("Body").strip().lower()
    checkUser = twilioModel.objects.filter(WaID=WaID).first()
    profileName = req.POST.get("ProfileName")

    if not checkUser:
        welcome_message = response.message(
            "👋 Welcome to NextCare!\n"
            "I am your AI-powered health assistant. Here’s what I can do:\n\n"
            "📌 *Type 'help'* to get more information.\n"
            "📄 *Type 'pdf generate'* to generate your medical PDF.\n"
            "📝 *Type 'summary'* to get a summary of your health records.\n"
            "💬 *Type any health-related questions* to chat normally!\n\n"
            "I’m here to assist you with your health queries. Type *help* to get started!"
        )
        twilioModel.objects.create(WaID=WaID, profileName=profileName, message=message)
        return HttpResponse(str(response), content_type="application/xml")

    match message:
            case "help":
                help_message = response.message(
                    "🛠 *Help Menu*\n"
                    "Choose an option below:\n"
                    "1️⃣ *Type 'pdf generate'* to create your medical PDF.\n"
                    "2️⃣ *Type 'summary'* to get a detailed health summary.\n"
                    "3️⃣ *Ask any health-related question* and I will try to assist you!"
                )
                return HttpResponse(str(response), content_type="application/xml")

            case "pdf generate":
                response.message("Successfully Generated Report PDF!")
                return HttpResponse(str(response), content_type="application/xml")

            case "summary":
                summary = get_summary(WaID=WaID)
                response.message(f"📝 Here is your health summary:\n\n{summary}")
                return HttpResponse(str(response), content_type="application/xml")

            case _:
                reply = get_reply(WaID=WaID, profileName=profileName, message=message)
                response.message(reply)
                return HttpResponse(str(response), content_type="application/xml")

    return HttpResponse("Invalid Request", status=400)


def get_reply(WaID, profileName, message):
    twilioModel.objects.create(WaID=WaID, profileName=profileName, message=message)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Now I will ask all health related questions if the question is not health related then give a reply to user telling that please ask health related question! Now here is my question : "+message,
    )
    return response.text

def get_summary(WaID):
    messages = twilioModel.objects.all().filter(WaID=WaID)
    summaryStr = ""
    for msg in messages:
        summaryStr += msg.message
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Now Here are whole messages so pelase generate summary of what we have talked but select health related messages only and generate a summary! So here are complete messages" + summaryStr,
    )
    return response.text
