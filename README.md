#AI-Weather-Assistant
# AI Weather Assistant

An AI-powered weather assistant built with Python and Groq LLMs. The application uses LLM tool calling to retrieve real-time weather information through the WeatherAPI REST API and generate natural-language responses.

## Features

- Real-time weather information
- LLM-powered conversational interaction
- Function/tool calling with Groq
- Weather data retrieval using WeatherAPI
- Conversational context
- Secure API key management using environment variables
- Error handling for external API requests
- Command-line interface

## Tech Stack

- Python
- Groq API
- GPT-OSS-120B
- WeatherAPI
- REST APIs
- python-dotenv
- Requests

## Architecture

```text
User Query
    ↓
Groq LLM
    ↓
Tool Selection
    ↓
Weather Tool
    ↓
WeatherAPI
    ↓
Structured Weather Data
    ↓
Groq LLM
    ↓
Natural Language Response
