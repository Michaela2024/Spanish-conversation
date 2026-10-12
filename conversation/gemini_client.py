from django.conf import settings
from google import genai


class ConversationAI:
    def __init__(self):
        api_key = settings.GOOGLE_API_KEY
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in settings")

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3.5-flash-lite"

    def start_conversation(self, scenario, user_level):
        prompt = f"""
You are a native {scenario.language} speaker playing the role of {getattr(scenario, 'role', 'a helpful person')}.
Scenario: {scenario.name}
Context: {scenario.context}
User level: {user_level}

IMPORTANT:
- Choose a specific gender for yourself and stick to it throughout the conversation
- Use masculine OR feminine forms consistently for yourself
- Do NOT use dual gender forms like "señor/señora" or "perdido/perdida" - pick one
- Example: Say "¿En qué puedo ayudarte?" not "¿En qué puedo ayudarte, señor/señora?"

Give a brief, welcoming greeting in {scenario.language} (1-2 sentences).
Wait for the user to start their request.
Respond ONLY in {scenario.language}.
"""
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return {"roleplay_response": response.text}

    def continue_conversation(self, scenario, conversation_history, user_message, user_level="beginner"):
        history_text = "\n".join(
            f"{msg['role'].capitalize()}: {msg['content']}" for msg in conversation_history
        )

        # 1. Roleplay response
        roleplay_prompt = f"""
You are a native {scenario.language} speaker in the role of {getattr(scenario, 'role', 'a helpful person')}.
Scenario: {scenario.name}
Context: {scenario.context}

Conversation so far:
{history_text}
User: {user_message}

Continue the conversation naturally in {scenario.language}, staying in character.
Respond in 2-3 sentences.
Respond ONLY in {scenario.language}.
"""
        roleplay_response = self.client.models.generate_content(
            model=self.model,
            contents=roleplay_prompt
        ).text

        # 2. Feedback on user's Spanish
        feedback_prompt = f"""
You are a {scenario.language} language teacher speaking directly to a {user_level} student.

The student just said: "{user_message}"

Analyze their Spanish CAREFULLY. Only provide feedback if there are ACTUAL errors.

If their Spanish is correct or mostly correct:
- "Great! That's perfectly correct."
- "Excellent! Very natural phrasing."
- "Well done! You expressed that correctly."

If there ARE real errors:
- Point out the SPECIFIC mistake
- Show the correct form
- Give ONE tip for improvement

Be accurate and encouraging. Do NOT invent errors that aren't there.
Give 2-3 sentences in English, speaking directly to them using "you".
"""
        feedback_response = self.client.models.generate_content(
            model=self.model,
            contents=feedback_prompt
        ).text

        return {
            "roleplay_response": roleplay_response,
            "feedback": feedback_response
        }

    def generate_assessment(self, scenario, conversation_history, user_level):
        # Your assessment method here if you have one
        pass
