import streamlit as st
import google.generativeai as genai
from streamlit.components.v1 import html

# Configure the API client
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# System Prompt
system_prompt = """
Your name is Alex. You are an empathetic counselor providing thoughtful, 
supportive, and uplifting responses. Maintain a warm, conversational tone,
offer positive guidance and encouragement. Keep responses concise and focused.
"""

# Custom CSS for styling
def inject_custom_css():
    st.markdown("""
    <style>
        /* Main container styling */
        .stApp {
            background-color: #f5f5f5;
            padding-bottom: 100px !important;
        }
        
        /* Sticky header styling */
        .sticky-header {
            position: sticky;
            top: 0;
            background: #f5f5f5;
            z-index: 1001;
            padding: 15px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 15px;
        }
        
        .header-content {
            max-width: 800px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        .sticky-header h1 {
            margin: 0;
            font-size: 1.8rem;
            color: #1a1a1a;
        }
        
        .sticky-header p {
            margin: 5px 0 0;
            font-size: 0.9rem;
            color: #666;
        }
        
        /* Chat history container */
        .stElementContainer {
            max-width: 800px;
            margin: 0 auto;
            # padding: 20px;
        }
        
        .chat-history {
            # min-height: calc(100vh - 250px);
            padding: 20px 0;
        }
        
        /* Message bubbles */
        .message {
            margin: 10px 0;
            padding: 15px 20px;
            border-radius: 25px;
            max-width: 80%;
            animation: fadeIn 0.3s ease-in;
        }
        
        .user-message {
            background-color: #007bff;
            color: white;
            margin-left: auto;
            border-bottom-right-radius: 5px;
        }
        
        .bot-message {
            background-color: #e9ecef;
            color: black;
            margin-right: auto;
            border-bottom-left-radius: 5px;
        }
        
        /* Input area styling */
        .input-container {
            position: sticky;
            bottom: 0px;
            left: 50%;
            transform: translateX(-50%);
            width: 80%;
            max-width: 800px;
            background: white;
            padding: 15px;
            border-radius: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            z-index: 1000;
        }
        
        /* Send button styling */
        .stButton>button {
            background-color: #007bff;
            color: white;
            border-radius: 20px;
            padding: 10px 25px;
            border: none;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: #0056b3;
            transform: scale(1.05);
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

                .stForm {
                    position: sticky;
                    bottom:15px;
                    background-color: #00000;
                }
    </style>
    """, unsafe_allow_html=True)

def get_response(user_input):
    try:
        conversation = [{"role": "user", "parts": [system_prompt]}]
        for msg in st.session_state.history:
            if msg["type"] == "user":
                conversation.append({"role": "user", "parts": [msg["content"]]})
            else:
                conversation.append({"role": "model", "parts": [msg["content"]]})
        
        response = model.generate_content(conversation)
        return response.text
    except Exception as e:
        return f"Sorry, I'm having trouble responding right now. Error: {str(e)}"

def scroll_bottom():
    html(
        f"""
        <script>
            window.parent.document.querySelector('.chat-history').scrollTop = window.parent.document.querySelector('.chat-history').scrollHeight;
        </script>
        """,
        height=0,
    )

def main():
    inject_custom_css()
    
    # Sticky header
    st.markdown("""
    <div class="sticky-header">
        <div class="header-content">
            <h1>🤖 Alex - Your Counseling Companion</h1>
            <h5>A safe space to share your thoughts and feelings</h5>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if "history" not in st.session_state:
        st.session_state.history = []
    
    # Chat history container
    with st.container():
        st.markdown("""
        <div class="stElementContainer">
            <div class="chat-history">
        """, unsafe_allow_html=True)
        
        for message in st.session_state.history:
            if message["type"] == "user":
                st.markdown(
                    f'<div class="message user-message">{message["content"]}</div>', 
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="message bot-message">{message["content"]}</div>', 
                    unsafe_allow_html=True
                )
        
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Input area
    with st.form("chat_input", clear_on_submit=True):
        cols = st.columns([8, 1])
        with cols[0]:
            user_input = st.text_input(
                "Type your message...",
                key="input",
                label_visibility="collapsed",
                placeholder="How are you feeling today?", 

            )
        with cols[1]:
            send_button = st.form_submit_button("➤")
        
        if send_button and user_input:
            st.session_state.history.append({"type": "user", "content": user_input})
            
            with st.spinner("Alex is thinking..."):
                bot_response = get_response(user_input)
            
            st.session_state.history.append({"type": "bot", "content": bot_response})
            st.rerun()
    
    scroll_bottom()

if __name__ == "__main__":
    main()
