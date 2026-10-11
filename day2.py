
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "openai/gpt-oss-20b"


def build_client():
    if not API_KEY:
        raise RuntimeError("GROQ_API_KEY is missing from your .env file")

    return Groq(api_key=API_KEY)


def call_llm(client, messages):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    return response.choices[0].message.content or ""


#version a

def version_a(client, question):
    messages = [
        {
            "role": "user",
            "content": question
        }
    ]

    return call_llm(client, messages)


#version b

def version_b(client, question):
    system_instruction = """
    You are an AI assistant for employees.
    Follow the user's request directly.
    Keep answers simple, clear, and professional.
    Do not invent company policies or internal facts.
    If information is missing, acknowledge it.
    If a request is ambiguous, ask for clarification
    instead of making unsupported assumptions.
    """

    messages = [
        {
            "role": "system",
            "content": system_instruction
        },
        {
            "role": "user",
            "content": question
        }
    ]

    return call_llm(client, messages)


#version c

def version_c(client, question, context):
    system_instruction = """
    You are an AI assistant for employees.
    Follow the user's request directly.
    Keep answers simple, clear, and professional.
    Do not invent company policies or internal facts.
    Use the supplied context for company-specific questions.
    If information is missing, acknowledge it.
    If a request is ambiguous, ask for clarification
    instead of making unsupported assumptions.
    """

    user_message = f"""
Relevant information:

{context}

Question:
{question}
"""

    messages = [
        {
            "role": "system",
            "content": system_instruction
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    return call_llm(client, messages)


def main():
    client = build_client()

    question = input("Enter your test question: ")

    print("\n--- VERSION A ---")
    print(version_a(client, question))

    print("\n--- VERSION B ---")
    print(version_b(client, question))

    context = input(
        "\nEnter relevant context for Version C "
        "(leave blank if not required):\n"
    )

    print("\n--- VERSION C ---")
    print(version_c(client, question, context))


if __name__ == "__main__":
    main()
