from google import genai
from google.genai import types, Client
import streamlit as st

# Initialize Gemini Client
api_key=st.secrets["api_key"]


client = Client(api_key=api_key) 

# Page configuration
st.set_page_config(
    page_title="Data Science AI Assistant",
    page_icon="💬",
    layout="wide"
)

# Title
st.title("💬 Data Science AI Assistant with Streaming ")
st.caption("Powered by Gemini")

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = [{
            "role": "system",
            "content": """You are a data science expert assistant. 
            -Help with analysis, visualization, and statistical insights.
            Tone: Professional, technical 
            Format: Clear, structured responses"""
        }]

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

    # 2. History Transformation
    genai_chat_history = []
    for message in st.session_state.messages:
        role = 'model' if message["role"] == 'assistant' else message["role"]

        content = message.get("content", "")
        if content:
            genai_chat_history.append({
                "role": role,
                "parts": [{"text": content}] 
            })

    # All messages, including the latest user prompt
    contents = genai_chat_history 
    
    # 3. Model Setup and Configuration
    
    model_config = types.GenerateContentConfig( 
        temperature=temperature
    )
    
    
    # 4. Call Gemini API with streaming 
    with st.spinner("Thinking..."):
        # Pass the model name, the full history (contents), and the config
        response = client.models.generate_content_stream(
            model=model_name,
            contents=contents, # This includes the full conversation history
            config=model_config
        )

    # 5. Display streaming response
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
        "role": "assistant",
        "content": full_reply
    })