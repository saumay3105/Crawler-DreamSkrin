from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import asyncio
import json
from crawl4ai import AsyncWebCrawler
import google.generativeai as genai
from django.conf import settings


async def extract_contacts(url):
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url)
        return result.markdown


def process_with_gemini(text):
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    llm_prompt = f"""
        You are provided with the following text: 

        {text}

        Check this text and find contact details, returning them in JSON format.
        Ensure the output follows this structure:
        {{"contactDetails": {{"phoneNumbers": ["+1 (434) 72-32964", "+91 432674 334328"], "email": "mail@abc.com"}}}}
    """
    response = model.generate_content(llm_prompt)
    start_idx = response.text.find("{")
    end_idx = response.text.rfind("}") + 1
    trimmed_response = response.text[start_idx:end_idx]
    parsed_json = json.loads(trimmed_response)
    print(parsed_json)
    return json.dumps(parsed_json, separators=(',', ':'))


@api_view(['POST'])
def extract_contacts_view(request):
    url = request.data.get('url')
    if not url:
        return Response(
            {'error': 'URL is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        text = asyncio.run(extract_contacts(url))
        contacts = process_with_gemini(text)
        return Response(contacts)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
