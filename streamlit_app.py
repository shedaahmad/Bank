import streamlit as st
import os
from mistralai import Mistral
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="🏦 Banking Bot - Mistral AI",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .stChatMessage {
        padding: 1rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
    }
    
    .header-container {
        text-align: center;
        padding: 2rem 0;
        color: white;
    }
    
    .header-title {
        font-size: 2.5rem;
        margin: 0;
    }
    
    .header-subtitle {
        font-size: 1rem;
        opacity: 0.9;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "bot" not in st.session_state:
    @st.cache_resource
    def load_bot():
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            return None
        
        client = Mistral(api_key=api_key)
        return client
    
    st.session_state.client = load_bot()

# Header
with st.container():
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("""
        <div class="header-container">
            <h1 class="header-title">🏦 Banking Bot</h1>
            <p class="header-subtitle">Powered by Mistral Large AI</p>
        </div>
        """, unsafe_allow_html=True)

# System prompt
system_prompt = """You are a friendly, professional banking assistant. Your goal is to help customers with their banking needs in a clear, conversational manner.

You can help with:
- Account questions (savings, checking, credit cards)
- Money transfers and payments
- Loan and credit information
- Banking products and services
- General financial questions

Guidelines:
1. Keep responses concise and easy to understand (2-3 sentences)
2. Use simple language, avoid jargon
3. For sensitive matters, recommend secure verification
4. Never ask for passwords or PIN numbers
5. Be warm and helpful while maintaining professionalism
6. Format responses clearly
7. Always be ready to escalate to a human agent if needed

Remember: You're here to make banking easier and more pleasant!"""

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Quick action buttons
if not st.session_state.messages:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💳 Open Account", use_container_width=True):
            st.session_state.user_input = "How do I open a new account?"
    with col2:
        if st.button("💸 Transfer Money", use_container_width=True):
            st.session_state.user_input = "How do I transfer money?"
    
    col3, col4 = st.columns(2)
    with col3:
        if st.button("🏦 Loan Info", use_container_width=True):
            st.session_state.user_input = "What loan options do you offer?"
    with col4:
        if st.button("💰 Fees & Charges", use_container_width=True):
            st.session_state.user_input = "What are your fees?"

# Chat input
user_input = st.chat_input("Ask me anything about banking...")

# Process user input
if user_input and st.session_state.client:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            try:
                response = st.session_state.client.chat.complete(
                    model="mistral-large-latest",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *st.session_state.messages[:-1],  # Exclude current user message for context
                        {"role": "user", "content": user_input}
                    ]
                )
                
                bot_message = response.choices[0].message.content
                
                # Clean up formatting
                bot_message = bot_message.replace("**", "").replace("###", "").strip()
                
                st.markdown(bot_message)
                
                # Add to chat history
                st.session_state.messages.append({"role": "assistant", "content": bot_message})
                
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

elif not st.session_state.client:
    st.error("⚠️ MISTRAL_API_KEY not configured. Please set it in your secrets.")

# Clear chat button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; margin-top: 2rem; color: #666;">
    <small>🏦 Banking Bot | Powered by Mistral Large AI | Built with Streamlit</small>
</div>
""", unsafe_allow_html=True)
