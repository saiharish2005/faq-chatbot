import streamlit as st
import pandas as pd
from fuzzywuzzy import process

# Streamlit UI
st.title("Admin Chatbot - FAQ System")

# File Upload Section
uploaded_file = st.file_uploader("Upload FAQ CSV", type=["csv"])

if uploaded_file is not None:
    # Read CSV File
    faq_data = pd.read_csv(uploaded_file)

    # Ensure 'Question' and 'Answer' columns exist
    if "Question" in faq_data.columns and "Answer" in faq_data.columns:
        st.success("FAQ Data Loaded Successfully! ✅")

        # User Input for Query
        user_query = st.text_input("Ask a question:")

        if user_query:
            # Convert 'Question' column to list & remove NaN values
            questions_list = faq_data["Question"].dropna().tolist()

            # Fuzzy Matching to Find the Best Match
            match = process.extractOne(user_query, questions_list)

            if match:  # Check if a match is found
                best_match, score = match
                answer = faq_data.loc[faq_data["Question"] == best_match, "Answer"].values

                if len(answer) > 0:
                    st.write(f"**Answer:** {answer[0]} (Confidence: {score}%)")
                else:
                    st.write("Sorry, I couldn't find an answer. 😕")
            else:
                st.write("No similar question found.")
    else:
        st.error("CSV file must have 'Question' and 'Answer' columns!")
