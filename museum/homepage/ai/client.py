import os

from google import genai
from google.genai import types

from .prompts import SYSTEM_PROMPT
from .tools import TOOL_REGISTRY, TOOL_DECLARATIONS

WRITE_TOOLS = {
    "book_event",
    "book_general_visit",
    "cancel_booking",
}

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)


def ask_gemini(message, user=None, conversation_history=None):

    if conversation_history is None:
        conversation_history = []
    config = {
        "tools": [
            {
                "function_declarations": TOOL_DECLARATIONS
            }
        ]
    }

    contents = [SYSTEM_PROMPT]

    for item in conversation_history:
        contents.append(
            f"{item['role']}: {item['content']}"
        )

    contents.append(
        f"user: {message}"
    )

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=contents,
        config=config,
    )

    part = response.candidates[0].content.parts[0]

    if not part.function_call:
        return response.text

    function_call = part.function_call

    function = TOOL_REGISTRY.get(function_call.name)

    if not function:
        raise ValueError(
            f"Unknown tool: {function_call.name}"
        )

    arguments = dict(function_call.args)

    if function_call.name in {
        "get_my_bookings",
        "book_event",
        "book_general_visit",
        "cancel_booking",
    }:
        if user is None:
            raise ValueError(
                "User context is required for this tool."
            )

        arguments["user"] = user

    if function_call.name in WRITE_TOOLS:
        return {
            "confirmation_required": True,
            "action": function_call.name,
            "arguments": dict(function_call.args),
        }

    result = function(**arguments)

    function_response_part = types.Part.from_function_response(
        name=function_call.name,
        response={
            "result": result
        },
    )

    final_response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=[
            SYSTEM_PROMPT,
            message,
            response.candidates[0].content,
            types.Content(
                role="user",
                parts=[function_response_part],
            ),
        ],
        config=config,
    )

    return final_response.text
