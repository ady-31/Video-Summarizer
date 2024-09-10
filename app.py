import os
import openai
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/home/USER/.env/openai_api')
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_transcript(youtube_url):
    
    # Fetches the transcript of a YouTube video. 
    
    video_id = youtube_url.split("v=")[-1]
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    try:
        transcript = transcript_list.find_manually_created_transcript()
    except:
        try:
            generated_transcripts = [trans for trans in transcript_list if trans.is_generated]
            transcript = generated_transcripts[0]
        except:
            raise Exception("No suitable transcript found.")
    
    full_transcript = " ".join(part['text'] for part in transcript.fetch())
    return full_transcript, transcript.language_code

def summarize_with_openai(transcript, language_code, model_name='gpt-3.5-turbo'):
    
    # Summarizes the transcript using OpenAI's GPT model.
    
    # Split the transcript into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
    texts = text_splitter.split_text(transcript)
    text_to_summarize = " ".join(texts[:4])  # Adjust as needed

    prompt = f'''
    Summarize the following text in {language_code}.
    Text: {text_to_summarize}

    Add a title to the summary in {language_code}. 
    Include an INTRODUCTION, BULLET POINTS if possible, and a CONCLUSION in {language_code}.
    '''

    response = openai.ChatCompletion.create(
        model=model_name,
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': prompt}
        ],
        temperature=1,
        max_tokens=1500,  # Adjust token limit as needed
        n=1
    )
    
    return response.choices[0].message['content'].strip()

def main():
    
    # Streamlit app main function for summarizing YouTube video transcripts.
    
    # Custom CSS for a horror theme
    st.markdown("""
        <style>
        .main {
            background-color: #000000;
            color: #ffffff;
            font-family: 'Creepster', cursive; /* Adding a creepy font */
        }
        .sidebar .sidebar-content {
            background-color: #222222;
        }
        .stButton>button {
            background-color: #c8102e; /* Blood red */
            color: #ffffff;
            border: none;
            border-radius: 5px;
            box-shadow: 0 0 10px #ff0000; /* Red glow */
        }
        .stTextInput>div>input {
            background-color: #333333;
            color: #ffffff;
            border: 1px solid #666666;
        }
        .stMarkdown {
            color: #ffffff;
        }
        /* Custom font */
        @import url('https://fonts.googleapis.com/css2?family=Creepster&display=swap');
        </style>
    """, unsafe_allow_html=True)

    st.title('🦇 YouTube Video Summarizer 🦇')
    youtube_link = st.text_input('Enter the link of the YouTube video you want to summarize:')

    if st.button('Start'):
        if youtube_link:
            try:
                progress = st.progress(0)
                status_text = st.empty()

                status_text.text('Loading the transcript...')
                progress.progress(25)

                # Fetch transcript and language code
                transcript, language_code = get_transcript(youtube_link)

                status_text.text('Creating summary...')
                progress.progress(75)

                summary = summarize_with_openai(transcript, language_code)

                status_text.text('Summary:')
                st.markdown(summary)
                progress.progress(100)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning('Please enter a valid YouTube link.')

if __name__ == "__main__":
    main()
