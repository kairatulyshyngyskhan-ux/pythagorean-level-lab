# Right Triangle Level Lab

A Streamlit web app for **AI for Differentiated Learning**.

## Main idea
The app starts from one core **Pythagorean theorem** problem and adapts it into:
- Foundation
- Standard
- Advanced

Each level provides an adapted task, hint, solution, and a short check question.

## Why this is different
Instead of a general all-topic generator, this project focuses on one clear foundational concept: **identifying and using the hypotenuse in a right triangle**. The interface is designed like a small learning lab rather than a generic chatbot.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Add AI on Streamlit Cloud
In **App settings → Secrets**, add:
```toml
OPENAI_API_KEY = "your_api_key_here"
```

The source uses the OpenAI Responses API. If no API key is available, the app still runs in a checked demo mode.

## Deploy
1. Create a public GitHub repository.
2. Upload `app.py`, `requirements.txt`, `.streamlit/config.toml`, and this README.
3. Go to Streamlit Community Cloud.
4. Create an app from the GitHub repository.
5. Set `app.py` as the main file.
6. Add the API key in Streamlit Secrets.
7. Deploy and submit the live URL plus GitHub link.
