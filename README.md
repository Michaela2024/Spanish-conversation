## Testing

This project includes unit tests and Selenium integration tests.

### Running Tests

**Run all tests:**
```bash
python manage.py test
```

**Run specific test files:**
```bash
# Database tests
python test_direct.py

# Gemini API tests
python test_gemini.py

# UI tests with Selenium
python test_ui.py
```

**Note:** Selenium tests require a web browser driver (ChromeDriver, GeckoDriver, etc.) to be installed.# Spanish Learning App

An interactive Spanish learning application that combines structured phrase practice with AI-powered conversation scenarios. Built to help learners progress from beginner fundamentals to confident real-world conversations.

## Features

### 📚 Phrase Practice
Perfect for beginners! Learn key Spanish phrases with color-coded grammar tags that help you understand sentence structure.

- **Structured learning**: Progress through carefully curated phrases
- **Grammar visualization**: Color-coded tags show parts of speech and grammar patterns
- **Audio pronunciation**: Hear native pronunciation for every phrase
- **Beginner friendly**: Built with new learners in mind

### 💬 Conversation Practice
Have real conversations with AI in different scenarios. Practice what you've learned in context and get instant feedback.

- **Real-world scenarios**: Restaurant ordering, travel situations, casual conversations, and more
- **Instant feedback**: Get corrections and suggestions as you practice
- **Performance assessment**: Track your progress and identify areas for improvement
- **All levels**: Adapts to your proficiency level


## Tech Stack

- **Backend**: Django 5.2 (Python)
- **AI Model**: Google Gemini 2.0 Flash
- **Database**: SQLite (default Django database)
- **Frontend**: Django Templates with HTML/CSS/JavaScript

## Prerequisites

- [Python](https://www.python.org/) (version 3.8 or higher)
- [pip](https://pip.pypa.io/en/stable/) (Python package installer)
- A Google AI Studio API key for Gemini

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- A Google AI Studio API key

### Step-by-Step Setup

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/spanish-learning-app.git
cd spanish-learning-app
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt` file yet, install these packages:
```bash
pip install django python-dotenv google-generativeai
```

3. **Set up your environment variables:**
   
   Create a `.env` file in the project root (same directory as `manage.py`):
```bash
# On Windows PowerShell
notepad .env

# On Mac/Linux
nano .env
```

   Add your Google API key to the `.env` file:
```
GOOGLE_API_KEY=your_actual_google_api_key_here
```
   
   **Important:** Do not use quotes around the key, and make sure there are no extra spaces.

4. **Run database migrations:**
```bash
python manage.py migrate
```

5. **Start the development server:**
```bash
python manage.py runserver
```

6. **Open your browser and navigate to:**
```
http://127.0.0.1:8000
```

The application should now be running!

## Getting a Google API Key

This app uses Google's Gemini 2.0 Flash model for AI-powered conversation practice and feedback.

### Steps to get your API key:

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API key"**
4. Choose **"Create API key in new project"** (recommended)
5. Copy the generated API key
6. Paste it into your `.env` file as shown above

**Note:** Google Gemini offers a generous free tier suitable for personal learning use. For pricing details, visit [Google AI Pricing](https://ai.google.dev/pricing).

### Troubleshooting API Key Issues

If you get an "Invalid API key" error:
- Make sure there are no quotes around the key in your `.env` file
- Ensure there are no extra spaces before or after the key
- Verify the API key is from a valid Google Cloud project
- Check that the Generative Language API is enabled in your project
- Try regenerating a new API key if the issue persists

## Usage

### Starting the Application

1. Make sure you're in the project directory
2. Activate your virtual environment (if using one)
3. Start the Django development server:
```bash
python manage.py runserver
```
4. Open your browser and go to `http://127.0.0.1:8000`

### Phrase Practice Mode
1. From the home page, select **"Phrase Practice"**
2. Browse through Spanish phrases with color-coded grammar tags
3. Click the audio icon (🔊) to hear native pronunciation
4. Study how sentences are constructed before moving to conversations

### Conversation Practice Mode
1. From the home page, select **"Conversation Practice"**
2. Choose your proficiency level (beginner, intermediate, advanced)
3. Select a conversation scenario:
   - Restaurant ordering
   - Travel situations  
   - Casual conversations
   - And more!
4. Type your responses in Spanish
5. Receive instant AI feedback on your grammar and phrasing
6. View your performance assessment after the conversation

### Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.


## Acknowledgments

- Powered by Google Gemini 2.0 Flash API
- Built as a self-directed learning project to explore Django and AI integration
- Spanish language content curated for educational purposes


Built with ❤️ for Spanish learners
