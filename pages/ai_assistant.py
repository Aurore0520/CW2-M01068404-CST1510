from google import genai
from google.genai import types, Client
import streamlit as st
from services.AI_assistant import AIAssistant

system_prompt = """You are a data science expert assistant. 
            -Help with analysis, visualization, and statistical insights.
            Tone: Professional, technical 
            Format: Clear, structured responses"""

# Initialize Gemini Client
api_key=st.secrets["api_key"] 


# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []    

if 'ai_service' not in st.session_state:
    st.session_state.ai_service = AIAssistant(
        model_name="gemini-flash-lite-latest",
        temperature=0.7,
        system_prompt=system_prompt
    )
# --- Sidebar with controls ---
with st.sidebar:
    st.subheader("Chat Controls")

    # Display message count 
    message_count = len([m for m in st.session_state.messages if m["role"] != "system"])
    st.metric("Messages", message_count)

    # Clear chat button
    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # Model selection (using stable official names)
    model_name = st.selectbox(
        "Model",
        ["gemini-flash-lite-latest", "gemini-2.5-pro"], 
        index=0 
    )

    # Temperature slider 
    temperature = st.slider(
       "Temperature",
        min_value=0.0,
        max_value=1.0, 
        value=0.7,
        step=0.1,
        help="Higher values make output more random"
    )
     # Update the service instance with the new model and temperature settings
    st.session_state.ai_service._model_name = model_name
    st.session_state.ai_service._temperature = temperature

# Display all previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
prompt = st.chat_input("Ask about data science...")

if prompt and prompt.strip():
    
    # 1. Display user message and add to session state
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })


    # 2. Call Gemini API with streaming 
    with st.spinner("Thinking..."):
        # Pass the model name, the full history (contents), and the config
        response = st.session_state.ai_service.send_message_stream(
            messages=st.session_state.messages
        )

    # 3. Display streaming response
    with st.chat_message("assistant"):
        container = st.empty()
        full_reply=""

        for chunk in response:
            if chunk.text:
                full_reply += chunk.text
                container.markdown(full_reply + "▌") 
            
        # Remove cursor and show final response
        container.markdown(full_reply)
        
    # 6. Save assistant response
    st.session_state.messages.append({
        "role": "model",
        "content": full_reply
    })
    st.rerun()