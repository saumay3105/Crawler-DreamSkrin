# Crawler-DreamSkrin


A full-stack web application that extracts contact information from websites using web crawling and AI processing.

## Features

- Website crawling using AsyncWebCrawler
- Contact information extraction using Google's Gemini AI
- Clean and responsive React frontend
- RESTful Django backend API
- Real-time contact information display

## Tech Stack

### Frontend
- React
- CSS

### Backend
- Django
- Django REST Framework
- AsyncWebCrawler
- Google Gemini AI

## Prerequisites

- Python 3.8+
- Node.js 14+
- Google Gemini API key

## Installation

### Backend Setup

1. Clone the repository
```bash
git clone https://github.com/saumay3105/Crawler-DreamSkrin.git
cd backend
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```


3. Run migrations
```bash
python manage.py migrate
```

4. Start the server
```bash
python manage.py runserver
```

### Frontend Setup

1. Navigate to frontend directory
```bash
cd frontend
```

2. Install dependencies
```bash
npm install
```

3. Start the development server
```bash
npm run dev
```

## Usage

1. Open your browser and go to `http://localhost:5173`
2. Enter a website URL in the search bar
3. Click the search button
4. View the extracted contact information

## API Endpoints

### Extract Contacts
```
POST extract-contacts/

Request Body:
{
    "url": "https://example.com"
}

Response:
{
    // JSON formatted contact information
}
```

