import streamlit as st
from google import genai
from google.genai import types, Client

#Initialize Gemini client
api_key=st.secrets["api_key"]
client = Client(api_key=api_key)

#Page title
st.title("Data Science AI Assistant")

#Initialize session state with system prompt
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """You are a data science expert assistant. 
            -Help with analysis, visualization, and statistical insights.
            Tone: Professional, technical 
            Format: Clear, structured responses"""
        }
    ]

#Display all previous messages 
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

#Get user input
prompt = st.chat_input("Ask about data science...")

if prompt:
    #Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to session state
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    
   
    system_instruction = st.session_state.messages[0]["content"]
    
    contents = [
        {"role": m["role"], "parts": [{"text": m["content"]}]}
        for m in st.session_state.messages
        if m["role"] != "system"
    ]
    
    # Configure the model using the system instruction
    config = types.GenerateContentConfig(
        system_instruction=system_instruction
    )
    
    #Call Gemini API
    completion = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=contents, 
        config=config # Pass the system instruction here
    )
    
    #Extract assistant response
    response = completion.text

    #Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
    
    #Add assistant response to session state
    st.session_state.messages.append({
        "role": "assistant",
        "content": response 
    })