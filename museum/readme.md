# Museum Platform with Gemini AI Assistant

A Django-based museum platform built as a learning project to understand **LLM tool calling, conversational state, and safe integration of AI with a backend application**.

## Features

* Museum exhibitions and events
* Event and general visit booking
* Booking cancellation
* QR-code tickets and staff check-in
* User authentication and booking isolation
* Gemini-powered AI assistant
* Function/tool calling for museum operations
* Session-based conversation context
* Confirmation before state-changing AI actions

## AI Architecture

```text
User
 ↓
Gemini AI Assistant
 ↓
Tool Call
 ↓
Django AI Tool Layer
 ↓
Confirmation (for writes)
 ↓
Django Service Layer
 ↓
Database
```

The AI model does not directly access or modify the database. Django remains responsible for authorization, validation, and state changes.

## Tech Stack

* Django
* Python
* SQLite
* Google Gemini API
* Tailwind CSS
* JavaScript
* QR Code

## Purpose

This project was built primarily to learn how an LLM can interact with an existing backend through controlled tools rather than directly controlling application logic.

AI assistance was used extensively during development as an implementation and learning partner. The project was tested manually, including booking validation, authorization, confirmation replay, session state, and ticket lifecycle scenarios.
    