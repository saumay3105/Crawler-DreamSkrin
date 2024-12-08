from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import asyncio
import json
from crawl4ai import AsyncWebCrawler
import google.generativeai as genai
from django.conf import settings
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def validate_url(url):
    validator = URLValidator()
    try:
        validator(url)
        return True
    except ValidationError:
        return False

async def extract_contacts(url):
    async with AsyncWebCrawler(verbose=True) as crawler:
        try:
            result = await crawler.arun(url)
            return result.markdown
        except Exception as e:
            raise Exception(f"Failed to crawl URL: {str(e)}")

def process_with_gemini(text):
    try:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        llm_prompt = f"""
        Extract contact information from the following text and return in JSON format.
        Text: {text}
        
        Required format:
        {{
            "contactDetails": {{
                "phoneNumbers": [],
                "email": "",
                "additionalContact": ""
            }}
        }}
        
        Rules:
        1. Phone numbers should be properly formatted
        2. Email addresses should be validated
        3. Include any additional contact methods in additionalContact
        4. If a field is empty, return an empty string or empty array
        """
        
        response = model.generate_content(llm_prompt)
        json_str = response.text[response.text.find("{"):response.text.rfind("}") + 1]
        return json.loads(json_str)
    except Exception as e:
        raise Exception(f"Error processing text with Gemini: {str(e)}")

@api_view(['POST'])
def extract_contacts_view(request):
    url = request.data.get('url')
    
    if not url:
        return Response(
            {'error': 'URL is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not validate_url(url):
        return Response(
            {'error': 'Invalid URL format'},
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