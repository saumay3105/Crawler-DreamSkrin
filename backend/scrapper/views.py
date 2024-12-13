from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import asyncio
import json
from crawl4ai import AsyncWebCrawler
import google.generativeai as genai
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import logging
import os
from urllib.parse import urlparse, unquote
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

def validate_url(url):
    try:
       
        decoded_url = unquote(url)
        
       
        parsed = urlparse(decoded_url)
        
        
        if not all([parsed.scheme, parsed.netloc]):
            return False
            
        
        validator = URLValidator()
       
        base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        validator(base_url)
        
        return True
    except (ValidationError, ValueError) as e:
        logger.error(f"URL validation error: {str(e)}")
        return False

async def extract_contacts(url):
    async with AsyncWebCrawler(verbose=True) as crawler:
        try:
            
            decoded_url = unquote(url)
            result = await crawler.arun(decoded_url)
            if not result or not result.markdown:
                raise Exception("No content extracted from URL")
            return result.markdown
        except Exception as e:
            logger.error(f"Crawling error for URL {url}: {str(e)}")
            raise Exception(f"Failed to crawl URL: {str(e)}")

def process_with_gemini(text):
    try:
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise Exception("GEMINI_API_KEY not found in environment variables")

        genai.configure(api_key=api_key)
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
        if not response or not response.text:
            raise Exception("Empty response from Gemini")

        json_str = response.text[response.text.find("{"):response.text.rfind("}") + 1]
        result = json.loads(json_str)
        
        if "contactDetails" not in result:
            raise Exception("Invalid response structure from Gemini")
        
        return result
    except Exception as e:
        logger.error(f"Gemini processing error: {str(e)}")
        raise Exception(f"Error processing text with Gemini: {str(e)}")

@api_view(['POST'])
@csrf_exempt
def extract_contacts_view(request):
    try:
        
        if not request.data:
            logger.error("Empty request body")
            return Response(
                {'error': 'Request body is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )

        
        url = None
        if isinstance(request.data, dict):
            url = request.data.get('url')
        elif hasattr(request.data, 'get'):
            url = request.data.get('url')

        if not url:
            logger.error("URL not provided in request")
            return Response(
                {'error': 'URL is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        
        logger.info(f"Received URL for processing: {url}")

        if not validate_url(url):
            logger.error(f"Invalid URL format: {url}")
            return Response(
                {'error': 'Invalid URL format. Please provide a valid URL.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        logger.info(f"Processing validated URL: {url}")
        text = asyncio.run(extract_contacts(url))
        contacts = process_with_gemini(text)
        
        return Response(contacts)
    except Exception as e:
        logger.error(f"Error in extract_contacts_view: {str(e)}", exc_info=True)
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )