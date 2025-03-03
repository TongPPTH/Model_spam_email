import streamlit as st
from tensorflow.keras.models import load_model
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
import nltk
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tensorflow.keras.preprocessing.text import Tokenizer
from tran import translate_bulk
import asyncio

# Load model and tokenizer
model = load_model(r"models/my_model.keras")
with open(r"models/tokenizer.pkl", 'rb') as handle:
    tokenizer = pickle.load(handle)

# Download necessary NLTK resources
nltk.download('stopwords')
nltk.download('punkt')

# Set up stopwords and stemmer
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

def process(text):
    words = word_tokenize(text)
    words = [word for word in words if word not in stop_words]
    words = [ps.stem(word) for word in words]
    return ' '.join(words)

def main():
    st.set_page_config(page_title="SPAM Email Detector", page_icon="📧", layout="centered")
    st.title("📩 SPAM Email Detector")
    st.markdown("### Enter an email text below to check if it's spam or not.")
    
    user_input = st.text_area("Enter your email content:", height=150)
    
    # if st.button("Translate to English"):
    #     if user_input:
    #         translated_text = asyncio.run(translate_bulk(user_input))
    #         st.text_area("Translated Text:", translated_text, height=150)
    #         user_input = translated_text  # Use translated text for further processing
    #     else:
    #         st.warning("Please enter text to translate.")
    
    if st.button("Analyze"): 
        if user_input:
            try:
                translated_text = asyncio.run(translate_bulk(user_input))
                # st.text_area("Translated Text:", translated_text, height=150)
                user_input = translated_text
                
                new_text_cleaned = [re.sub(r"[^a-zA-Z]+", ' ', user_input).lower()]
                new_text_processed = [process(doc) for doc in new_text_cleaned]

                new_sequences = tokenizer.texts_to_sequences(new_text_processed)
                new_padded = pad_sequences(new_sequences, maxlen=11776)

                prediction = model.predict(new_padded)
                predicted_label = 'Spam' if prediction[0][0] > 0.5 else 'Not Spam'
                probability = prediction[0][0]

                st.subheader("Prediction Result:")
                st.markdown(f"**Prediction Probability:** {probability:.4f}")
                st.markdown(f"**Predicted Label:** :{'red' if predicted_label == 'Spam' else 'green'}[{predicted_label}]")
            
            except:
                st.warning('Can not analyze this language')
        else:
            st.warning("Please enter some text to analyze.")

if __name__ == "__main__":
    main()
