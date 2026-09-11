# Museum Online Chatbot Ticketing System

A Django-based prototype inspired by **Smart India Hackathon problem statement SIH1648 — Online Chatbot Based Ticketing System**.

The project explores how a conversational AI assistant can be integrated with a museum's backend to help visitors discover exhibitions and events, check availability, and manage bookings.

## Features

* Museum exhibitions and events
* General museum visit booking
* Event ticket booking
* Booking cancellation
* QR-code tickets
* Staff ticket verification and check-in
* User authentication and booking isolation
* Gemini-powered conversational assistant
* Function/tool calling for backend operations
* Session-based conversation context
* Confirmation before AI performs state-changing actions

## AI Architecture

```text
Visitor
   ↓
Gemini AI Assistant
   ↓
Tool Call
   ↓
Django AI Tool Layer
   ↓
Confirmation for state-changing actions
   ↓
Django Service Layer
   ↓
Database
```

The AI model does not directly access the database. Django remains responsible for validation, authorization, and state changes.

## Tech Stack

* Python
* Django
* SQLite
* Google Gemini API
* JavaScript
* Tailwind CSS
* QR Code

## Purpose

This project was primarily built as a learning and prototyping exercise around **LLM function calling and safe AI-backend integration**.

It focuses on the chatbot and backend interaction described in SIH1648 rather than implementing the complete expected solution. Features such as payment gateway integration, multilingual support, analytics, and a fully production-ready deployment are outside the current scope.

AI assistance was used extensively during development as an implementation and learning partner. The resulting system was manually tested for booking validation, user authorization, confirmation handling, replay/tampering scenarios, conversation context, and ticket lifecycle.
## Running Locally

1. Clone the repository and enter the project folder.

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Set the required environment variables.
   ```bash
   $env:DJANGO_SECRET_KEY="your-generated-secret-key"
   $env:GEMINI_API_KEY="your-gemini-api-key"
4. For a fresh setup, delete db.sqlite3 if it exists.
5. Apply migrations:
   ```bash
   python manage.py migrate
6. Create a new admin account:
   ```bash
   python manage.py createsuperuser
7. Start the development server:
   ```bash
   python manage.py runserver
8. Open http://127.0.0.1:8000/.

The project uses SQLite, so no separate database setup is required.
A Gemini API key is required for the AI assistant.
For a clean installation, starting with a fresh database is recommended.
