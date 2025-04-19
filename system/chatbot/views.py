import base64
import io
import os
import requests
import logging
from dotenv import load_dotenv
from PIL import Image

from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

load_dotenv()

logger = logging.getLogger(__name__)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set in .env")

def chatbot_page(request):
    return render(request, "chatbot.html")

@csrf_exempt
def upload_and_query(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Only POST requests allowed.")

    image = request.FILES.get("image")
    query = request.POST.get("query")

    if not image or not query:
        return JsonResponse({"detail": "Image and query are required."}, status=400)

    try:
        image_content = image.read()
        encoded_image = base64.b64encode(image_content).decode("utf-8")

        # Check if image is valid
        try:
            img = Image.open(io.BytesIO(image_content))
            img.verify()
        except Exception as e:
            logger.error(f"Invalid image format: {e}")
            return JsonResponse({"detail": f"Invalid image: {str(e)}"}, status=400)

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": query},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
                ]
            }
        ]

        def make_api_request(model):
            response = requests.post(
                GROQ_API_URL,
                json={
                    "model": model,
                    "messages": messages,
                    "max_tokens": 1000
                },
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                timeout=30
            )
            return response

        llama_response = make_api_request("meta-llama/llama-4-scout-17b-16e-instruct")
        llava_response = make_api_request("meta-llama/llama-4-maverick-17b-128e-instruct")

        responses = {}
        for model, response in [("llama", llama_response), ("llava", llava_response)]:
            if response.status_code == 200:
                content = response.json()["choices"][0]["message"]["content"]
                responses[model] = content
            else:
                responses[model] = f"Error from {model} API: {response.status_code}"

        return JsonResponse(responses)

    except Exception as e:
        logger.exception("Error processing upload and query")
        return JsonResponse({"detail": f"Unexpected error: {str(e)}"}, status=500)
