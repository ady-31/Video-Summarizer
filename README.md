﻿# Video-Summarizer
Project Overview
YouTube Video Summarizer

This project is a web application built with Streamlit that allows users to input a YouTube video URL and receive a summarized version of its transcript. The application uses the OpenAI GPT model to generate the summary and incorporates a horror-themed design for an engaging user experience.

Libraries Used
Streamlit: A Python library for creating interactive web applications with ease. It is used here to build the user interface of the application, allowing users to input video links, view progress, and display the summary.

Installation: pip install streamlit
OpenAI: The official Python client for OpenAI’s API, used to interact with OpenAI’s GPT models. This library is essential for generating summaries of the video transcripts.

Installation: pip install openai
YouTube Transcript API: A Python library for fetching transcripts of YouTube videos. It handles both manually created and auto-generated transcripts.

Installation: pip install youtube-transcript-api
Langchain: A library for splitting long texts into smaller chunks, which is useful for processing and summarizing large transcripts.

Installation: pip install langchain
python-dotenv: A library for loading environment variables from a .env file. It is used to securely manage and access the OpenAI API key.

Installation: pip install python-dotenv
Key Features
Transcript Fetching: Retrieves transcripts from YouTube videos, preferring manually created transcripts and falling back to auto-generated ones if necessary.
Text Summarization: Uses OpenAI’s GPT model to summarize the video transcript, providing a concise and informative summary.
Horror-Themed Interface: The application features a custom horror-themed design with dark colors, spooky fonts, and eerie visual effects.
