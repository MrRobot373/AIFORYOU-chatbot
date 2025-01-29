import streamlit as st
import google.generativeai as genai

# Step 1: Configure the API client with your API key
genai.configure(api_key="AIzaSyCIhzKAOCeRUL-GX2q0jbJL6-vgxUMPIeM")  # Replace with your actual API key

# Step 2: Initialize the model (e.g., gemini-1.5-flash)
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to call the generative model and get a response
def get_advice(prompt: str) -> str:
    """
    Function to get advice or response from the generative model.
    """
    try:
        # Step 3: Send a request to the model to generate content based on the prompt
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error occurred while calling the model: {str(e)}"

# Step 3: Streamlit UI setup
def main():
    st.title("Counseling Chatbot")
    st.write("Welcome to the Counseling Chatbot. I'm here to help you with your thoughts, feelings, or any other concerns.")

    # User input for the chatbot
    user_input = st.text_area("What is bothering you?", "")

    # When the user clicks the "Send" button
    if st.button("Get Advice"):
        if user_input:
            st.write(f"You: {user_input}")

            # Get advice from the model
            bot_response = get_advice(user_input)

            # Display the bot's response
            st.write(f"Bot: {bot_response}")
        else:
            st.write("Please enter something for me to respond to.")

if __name__ == "__main__":
    main()
