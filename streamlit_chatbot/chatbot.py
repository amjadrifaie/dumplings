import streamlit as st
import google.generativeai as genai


persona_instructions = """
You are a cheerful, expert, and encouraging **Food Hunting Study Buddy**. 🍽️
Your goal is to help the user find the best food and recipes.
- ALWAYS use a cheerful, encouraging tone.
- Give suggestions based on location, cuisine, or craving.
- Always offer a fun fact or helpful tip about the food or a similar dish.
- Emojis are strongly encouraged.
"""

# --- SIDEBAR WIDGETS ---
with st.sidebar:
    st.title("Hunger Hunt")
    
    # These variables MUST be defined outside the main function or within the sidebar block
    # so they are accessible to the get_gemini_response call later.
    location = st.text_input("Your Current Location (City/Zip):", "Kuala Lumpur")
    budget = st.select_slider("Select Max Budget (per person)", 
                              options=["$", "$$", "$$$", "$$$$"], 
                              value="$$")
    cuisine = st.multiselect("Cuisine Cravings:", ["Asian", "Western", "Italian", "Fusion", "Dessert", "Cafe",], default=["Asian"])

    st.markdown("---") 
    st.radio("Radio-button select", ["Friendly", "Formal", "Funny"], index=0)


user_emoji = "😹" 
robot_img = "robot.jpg" 


# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyDZ8u2bcSszOsAT_UUwJ0X95jaXMZabDIY"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

# --- CORRECTED & CONSOLIDATED GEMINI FUNCTION ---
def get_gemini_response(prompt, persona_instructions, location, budget, cuisine):
    """
    Generates the Gemini response by combining user input and sidebar filters
    into a powerful system prompt.
    """
    # Define Context (using the new sidebar variables)
    context = (
        f"The user is currently in **{location}** and their max budget is **{budget}**."
        f"They are primarily interested in the following cuisines: **{', '.join(cuisine)}**."
        "Please keep these constraints and preferences in mind for all suggestions, making sure to acknowledge them."
    )
    
    # Build the full prompt to send to the AI
    full_prompt = (
        f"{persona_instructions}\n"
        f"--- CONTEXT ---\n"
        f"{context}\n"
        f"--- USER QUERY ---\n"
        f"{prompt}\n" # Use the local 'prompt' variable here, not the old 'PROMPT'
        f"--- ASSISTANT RESPONSE ---\n"
    )
    
    # Call the Gemini API
    response = model.generate_content(full_prompt)
    
    # Return the text content of the response
    return response.text

# --- MAIN STREAMLIT APPLICATION ---
def main():
    st.title("Grub Grab 🍜")
    st.markdown("Your cheerful AI hungry buddy for finding the best local eateries and delicacies! Use the sidebar filters to refine your hunt. 🕵️‍♀️")

    initialize_session_state()

    # Display previous messages
    for message in st.session_state.messages:
        avatar = robot_img if message["role"] == "assistant" else user_emoji
        with st.chat_message(message["role"], avatar=avatar):
            st.write(f"{message['content']}")


    # Chat input
    if prompt := st.chat_input("Chat with Gemini"):
        
        # 1. Display user message and add to history
        with st.chat_message("user", avatar=user_emoji):
            st.write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # 2. Get Gemini response, passing ALL context variables
        with st.spinner('Thinking up some delicious ideas...'):
            # The 'response' variable is defined HERE.
            response = get_gemini_response(
                prompt, 
                persona_instructions, 
                location, 
                budget, 
                cuisine
            )

        # 3. Display assistant response
        # This block is now correctly inside the main function AND the 'if prompt' block,
        # ensuring 'response' is defined when st.write(response) is called.
        with st.chat_message("assistant", avatar=robot_img):
            st.write(response)
          
        # 4. Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()