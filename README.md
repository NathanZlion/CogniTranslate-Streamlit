# 🌐 CogniTranslate

CogniTranslate is a Streamlit app for seamless text translation, PDF document processing, and web content extraction. Translate text across languages, extract and translate content from PDFs, or scrape and translate web pages—all in one place!

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cognitranslate-app.streamlit.app)


### 🚀 Features

- Text Translation: Translate text between multiple languages using state-of-the-art NLP models.
- PDF Processing: Extract text from PDFs and translate it with ease.
- Web Scraping: Scrape content from web pages and translate it instantly.
- User-Friendly Interface: Built with Streamlit for a smooth, interactive experience.

### 🛠️ Methods
CogniTranslate leverages cutting-edge technologies:

- Translation: Powered by transformers (Hugging Face) with MarianMTModel and MarianTokenizer for accurate translations.
- PDF Extraction: Uses pdfplumber to extract text from PDF documents.
- Web Scraping: Employs requests and BeautifulSoup to fetch and parse web content.
- Document Generation: Creates translated PDFs using reportlab.
- Visualization: Enhanced with altair for interactive data displays.

### To run CogniTranslate locally:

Install Dependencies
   ```
   $ pip install -r requirements.txt
   ```

Run the App
   ```
   $ streamlit run streamlit_app.py
   ```

### 🌍 Try It Out
Visit cognitranslate-app.streamlit.app to test the app live! Translate text, upload PDFs, or input URLs to see CogniTranslate in action. Currently there's only supports English to fr (French), es (Spanish) and, pt (Portugues). More coming soon...


🤝 Contribute
⭐ Star this repo if you’ve ever whispered “just work” to your code like it’s listening!, 🥺 ... 😆
