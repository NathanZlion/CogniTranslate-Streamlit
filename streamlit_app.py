from transformers import MarianMTModel, MarianTokenizer
import pdfplumber
import requests
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import streamlit as st
from io import BytesIO
import os
import streamlit.components.v1 as components

# Function to extract text from a PDF
def extract_pdf_text(pdf_path):
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

# Function to scrape text from a website
def scrape_website(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = " ".join([p.get_text() for p in paragraphs])
        return text
    except Exception as e:
        return f"Error scraping website: {str(e)}"

# Function to translate text
def translate_text(text, model_name="Helsinki-NLP/opus-mt-en-fr"):
    try:
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        max_length = 500
        text_chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
        translated_chunks = []
        for chunk in text_chunks:
            if chunk.strip():
                inputs = tokenizer([chunk], return_tensors="pt", padding=True, truncation=True, max_length=512)
                translated = model.generate(**inputs)
                translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
                translated_chunks.append(translated_text)
        return " ".join(translated_chunks)
    except Exception as e:
        return f"Error translating text: {str(e)}"

# Function to export translated text as PDF in memory
def export_to_pdf(text):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = [Paragraph(text.replace('\n', '<br/>'), styles['Normal'])]
    doc.build(story)
    buffer.seek(0)
    return buffer

# Function to copy text to clipboard using JavaScript
def copy_to_clipboard(text, key):
    # Create a unique ID for the textarea and button
    textarea_id = f"textarea_{key}"
    button_id = f"copy_button_{key}"
    
    # HTML and JavaScript for copying text
    html = f"""
    <textarea id="{textarea_id}" style="position: absolute; left: -9999px;">{text}</textarea>
    <button id="{button_id}" onclick="copyText('{textarea_id}')">Copy Full Text</button>
    <script>
    function copyText(textareaId) {{
        var textarea = document.getElementById(textareaId);
        textarea.select();
        document.execCommand('copy');
        alert('Text copied to clipboard!');
    }}
    </script>
    """
    components.html(html, height=50)

# Modular function to display translation results
def display_translation(translated_text, source_key):
    if not translated_text.startswith("Error"):
        st.write("**Translated Text Preview:**")
        st.write(translated_text)

        # Button to copy full text to clipboard
        copy_to_clipboard(translated_text, source_key)
        
        # Download PDF
        pdf_buffer = export_to_pdf(translated_text)
        st.download_button(
            label="Download Translated PDF",
            data=pdf_buffer,
            # file_name="translated.pdf",
            mime="application/pdf",
            key=f"pdf_download_{source_key}"
        )
    else:
        st.error(translated_text)

# Streamlit interface
st.title("CogniTranslate: Cognitive Science Research Translator")
st.write("Translate cognitive science content from PDFs or websites into another language.")

source = st.selectbox("Choose Source", ["PDF", "Website"])
target_language = st.selectbox("Target Language", ["fr (French)", "es (Spanish)", "pt (Portuguese)"])
lang_code = target_language.split()[0]  # Extract 'fr', 'es', or 'pt'

if source == "PDF":
    uploaded_file = st.file_uploader("Upload a PDF (e.g., cognitive science paper)", type="pdf")
    if uploaded_file and st.button("Translate", key="translate_pdf"):
        with st.spinner("Processing PDF..."):
            # Save uploaded PDF temporarily
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.read())
            text = extract_pdf_text("temp.pdf")
            if not text.startswith("Error"):
                translated_text = translate_text(text, f"Helsinki-NLP/opus-mt-en-{lang_code}")
                display_translation(translated_text, "pdf")
            else:
                st.error(text)
            # Remove temporary PDF file
            if os.path.exists("temp.pdf"):
                os.remove("temp.pdf")
else:
    url = st.text_input("Enter Website URL (e.g., https://neurosciencenews.com/)")
    if url and st.button("Translate", key="translate_web"):
        with st.spinner("Processing Website..."):
            text = scrape_website(url)
            if not text.startswith("Error"):
                translated_text = translate_text(text, f"Helsinki-NLP/opus-mt-en-{lang_code}")
                display_translation(translated_text, "web")
            else:
                st.error(text)
