from typing import List, Dict, Iterator
from google.genai import types, Client
import streamlit as st

class AIAssistant:
    """Simple wrapper around an AI/chat model.
    In your real project, connect this to OpenAI or another provider.
    """
    def __init__(self, system_prompt: str, model_name: str, temperature: float):
        api_key = st.secrets["api_key"]
        self._client = Client(api_key=api_key)
        self._model_name = model_name
        self._temperature = temperature
        self._system_prompt = system_prompt
        self._history: List[Dict[str, str]] = []
    def set_system_prompt(self, prompt: str) :
        self._system_prompt = prompt
    def send_message_stream(self, messages: List[Dict[str, str]]) -> Iterator[types.GenerateContentResponse]:
        """Sends the full conversation history to the Gemini API and returns a
        streaming response iterator.
        """
        contents = self.format_history(messages)
        config = self.get_gemini_config()
        response_stream = self._client.models.generate_content_stream(
            model=self._model_name,
            contents=contents,
            config=config
        )
        return response_stream
    def clear_history(self):
        self._history.clear()
