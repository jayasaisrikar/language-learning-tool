
#pip install streamlit googletrans==4.0.0-rc1 gtts SpeechRecognition pydub
'''
copy and paste the above requirements in your command prompt
'''



import streamlit as st
from googletrans import LANGUAGES, Translator
from gtts import gTTS, lang
import speech_recognition as sr

# Initialize the translator
translator = Translator()

# Get all languages supported by Google Translate and add Indian languages
ALL_LANGUAGES = {**LANGUAGES, **{
    'hi': 'Hindi',
    'bn': 'Bengali',
    'te': 'Telugu',
    'mr': 'Marathi',
    'ta': 'Tamil',
    'ur': 'Urdu',
    'gu': 'Gujarati',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'pa': 'Punjabi',
    'or': 'Odia',
    'as': 'Assamese',
    'ks': 'Kashmiri',
    'sd': 'Sindhi',
    'sa': 'Sanskrit'
}}

# Ensure 'English' is in the list with proper capitalization
ALL_LANGUAGES = {k: v.capitalize() for k, v in ALL_LANGUAGES.items()}
if 'en' in ALL_LANGUAGES:
    ALL_LANGUAGES['en'] = 'English'

# Get languages supported by gTTS
TTS_LANGUAGES = set(lang.tts_langs().keys())

# Function for text-to-speech
def text_to_speech(text, lang_code):
    if lang_code in TTS_LANGUAGES:
        tts = gTTS(text=text, lang=lang_code)
        tts.save("output.mp3")
        return "output.mp3"
    else:
        return None

# Function for speech-to-text
def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Speak now...")
        audio = r.listen(source)
        st.write("Processing...")
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand that."
    except sr.RequestError:
        return "Sorry, there was an error processing your request."

# Function to get language code
def get_language_code(language_name):
    return next((k for k, v in ALL_LANGUAGES.items() if v.lower() == language_name.lower()), None)

# Streamlit app
def main():
    st.title("Interactive Language Translator")

    # Sidebar for app mode selection
    app_mode = st.sidebar.selectbox("Choose the app mode",
        ["Text Translation", "Speech-to-Text Translation", "Text-to-Speech"])

    # Sort languages alphabetically
    sorted_languages = sorted(ALL_LANGUAGES.values())

    if app_mode == "Text Translation":
        # Text input
        text_input = st.text_area("Enter text to translate:", "Hello, how are you?")

        # Language selection
        source_lang = st.selectbox("Select source language:", sorted_languages, index=sorted_languages.index('English'))
        target_lang = st.selectbox("Select target language:", sorted_languages, index=sorted_languages.index('Hindi'))

        if st.button("Translate"):
            # Get language codes
            source_lang_code = get_language_code(source_lang)
            target_lang_code = get_language_code(target_lang)

            # Perform translation
            translated = translator.translate(text_input, src=source_lang_code, dest=target_lang_code)
            st.write("Translated text:")
            st.write(translated.text)

            # Text-to-speech for translated text
            audio_file = text_to_speech(translated.text, target_lang_code)
            if audio_file:
                st.audio(audio_file, format='audio/mp3')
            else:
                st.warning(f"Text-to-speech is not available for {target_lang}")

    elif app_mode == "Speech-to-Text Translation":
        st.write("Click the button and speak to translate")
        if st.button("Start Recording"):
            spoken_text = speech_to_text()
            st.write("You said:", spoken_text)

            # Language selection for translation
            source_lang = "English"  # Assuming speech input is in English
            target_lang = st.selectbox("Select target language for translation:", sorted_languages, index=sorted_languages.index('Hindi'))
            
            source_lang_code = get_language_code(source_lang)
            target_lang_code = get_language_code(target_lang)

            # Perform translation
            translated = translator.translate(spoken_text, src=source_lang_code, dest=target_lang_code)
            st.write("Translated text:")
            st.write(translated.text)

            # Text-to-speech for translated text
            audio_file = text_to_speech(translated.text, target_lang_code)
            if audio_file:
                st.audio(audio_file, format='audio/mp3')
            else:
                st.warning(f"Text-to-speech is not available for {target_lang}")

    elif app_mode == "Text-to-Speech":
        # Text input
        text_input = st.text_area("Enter text for speech synthesis:", "Hello, this is a test.")

        # Language selection
        lang = st.selectbox("Select language:", sorted_languages, index=sorted_languages.index('English'))
        lang_code = get_language_code(lang)

        if st.button("Generate Speech"):
            audio_file = text_to_speech(text_input, lang_code)
            if audio_file:
                st.audio(audio_file, format='audio/mp3')
            else:
                st.warning(f"Text-to-speech is not available for {lang}")

    # Interactive feature: Language Quiz
    st.sidebar.header("Language Quiz")
    if st.sidebar.button("Take a Quiz"):
        quiz_word = translator.translate("Exciting", dest='te').text
        user_answer = st.sidebar.text_input(f"What does '{quiz_word}' mean in English?")
        if user_answer.lower() == "exciting":
            st.sidebar.success("Correct! Great job!")
        elif user_answer:
            st.sidebar.error("Not quite. Try again!")

    # Interactive feature: Daily Phrase
    st.sidebar.header("Phrase of the Day")
    if st.sidebar.button("Get Daily Phrase"):
        daily_phrase = "When given lemons, make lemonade"
        translated_phrase = translator.translate(daily_phrase, dest='fr').text
        st.sidebar.write(f"English: {daily_phrase}")
        st.sidebar.write(f"French: {translated_phrase}")

if __name__ == "__main__":
    main()