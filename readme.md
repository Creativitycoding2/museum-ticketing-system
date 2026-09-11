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
