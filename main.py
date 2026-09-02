import requests
import pyttsx3
import os
import json

from dotenv import load_dotenv
from groq import Groq


# Load environment variables
load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not WEATHER_API_KEY:
    raise ValueError("WEATHER_API_KEY is not set in the environment variables.")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")


# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

model = "openai/gpt-oss-120b"


# Weather function
def get_weather(place):

    url = (
        f"http://api.weatherapi.com/v1/current.json"
        f"?key={WEATHER_API_KEY}&q={place}&aqi=no"
    )

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    wd = response.json()

    if "error" in wd:
        return {
            "error": wd["error"]["message"]
        }

    return {
        "location": wd["location"]["name"],
        "country": wd["location"]["country"],
        "temperature": wd["current"]["temp_c"],
        "condition": wd["current"]["condition"]["text"],
        "humidity": wd["current"]["humidity"],
        "wind_speed": wd["current"]["wind_kph"]
    }


# Tool definition for Groq
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather information for a specific location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "place": {
                        "type": "string",
                        "description": "The city or location to get weather for."
                    }
                },
                "required": ["place"]
            }
        }
    }
]


# Main program
if __name__ == "__main__":

    print("Welcome to the AI Weather Assistant!")

    # Initialize text-to-speech
    engine = pyttsx3.init()

    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1.0)

    voices = engine.getProperty("voices")

    if len(voices) > 1:
        engine.setProperty("voice", voices[1].id)

    # Conversation memory
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful weather assistant. "
                "When the user asks about weather, use the get_weather tool. "
                "Use previous conversation context when answering follow-up questions. "
                "Explain weather information clearly and briefly. "
                "Give practical advice when appropriate. "
                "Do not use Markdown, asterisks, bullet points, "
                "or special formatting."
            )
        }
    ]

    try:

        # Continuous conversation
        while True:

            # Get user question
            user_query = input("\nWhat would you like to know? ")

            # Exit commands
            if user_query.lower() in ["quit", "exit", "bye"]:
                print("Goodbye!")
                break

            # Add user question to conversation history
            messages.append(
                {
                    "role": "user",
                    "content": user_query
                }
            )

            # First LLM call
            llm_response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                max_tokens=150
            )

            # Get assistant message
            message = llm_response.choices[0].message

            # Check whether LLM requested a tool
            if message.tool_calls:

                tool_call = message.tool_calls[0]

                # Get arguments from tool call
                arguments = json.loads(
                    tool_call.function.arguments
                )

                place = arguments["place"]

                # Execute weather function
                weather_result = get_weather(place)

                print("\nTool executed successfully.")
                print("Weather data:", weather_result)

                # Add assistant tool request to conversation
                messages.append(message)

                # Add tool result to conversation
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(weather_result)
                    }
                )

                # Second LLM call
                final_response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=150
                )

                # Get final answer
                answer = final_response.choices[0].message.content

                # Add final assistant response to memory
                messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            else:

                # LLM answered without using a tool
                answer = message.content

                # Add assistant response to memory
                messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            # Display answer
            print("\nAI Weather Assistant:")
            print(answer)

            # Remove Markdown before speech
            speech_text = (
                answer
                .replace("**", "")
                .replace("*", "")
                .replace("#", "")
            )

            # Speak answer
            engine.say(speech_text)
            engine.runAndWait()

    except requests.exceptions.Timeout:

        print("Error: The weather service took too long to respond.")

    except requests.exceptions.ConnectionError:

        print("Error: Could not connect to the weather service.")

    except requests.exceptions.HTTPError:

        print("Error: Weather API returned an HTTP error.")

    except (KeyError, ValueError):

        print("Error: Unexpected response received.")

    except Exception as e:

        print(f"Unexpected error: {e}")

    finally:

        engine.stop()