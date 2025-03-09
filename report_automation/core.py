import pandas as pd
import spacy
from collections import Counter
import matplotlib.pyplot as plt
from fpdf import FPDF

def clean_messages(df: pd.DataFrame, text_column: str) -> pd.DataFrame:
    """
    Cleans social media messages in a DataFrame by removing stopwords and unnecessary characters.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame containing social media messages.
    text_column (str): The column name containing the messages.
    
    Returns:
    pd.DataFrame: A new DataFrame with an additional column 'cleaned_text' containing processed messages.
    """
    # Load the English NLP model from spaCy
    nlp = spacy.load("en_core_web_sm")
    
    def process_text(text):
        """Processes a single message by removing stopwords and non-alphabetic characters."""
        doc = nlp(text)
        cleaned_tokens = [token.lemma_.lower() for token in doc if not token.is_stop and token.is_alpha]
        return " ".join(cleaned_tokens)
    
    # Apply text processing to each message in the DataFrame
    df["cleaned_text"] = df[text_column].astype(str).apply(process_text)
    
    return df

def get_top_words(df: pd.DataFrame, text_column: str, top_n: int = 10) -> dict:
    """
    Extracts the most frequent words from the cleaned messages.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame containing cleaned social media messages.
    text_column (str): The column name containing the cleaned messages.
    top_n (int): The number of top frequent words to return.
    
    Returns:
    dict: A dictionary where keys are words and values are their frequency count.
    """
    all_words = " ".join(df[text_column]).split()
    word_freq = Counter(all_words)
    return dict(word_freq.most_common(top_n))

def plot_word_distribution(word_freq: dict, title:str, x_label:str, y_label:str, color:str, filename: str = "word_distribution.png"):
    """
    Plots and saves the distribution of word frequencies.
    
    Parameters:
    word_freq (dict): A dictionary with words as keys and their frequency count as values.
    filename (str): The filename to save the plot as an image.
    """
    plt.figure(figsize=(10, 5))
    plt.bar(word_freq.keys(), word_freq.values(), color=color)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def save_report(dict_info: dict, pdf_filename: str = "report.pdf"):
    """
    Generates a PDF report with the top words frequency distribution and saves it.
    
    Parameters:
    dict_info (dict): Dictionary containing sections with titles, analysis, and graph filenames.
    pdf_filename (str): The filename to save the PDF report.
    """
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=16)  # H1 Style: Bold and Larger

    for key, value in dict_info.items():
        # Insert title (H1, bold, centered)
        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(200, 10, value["context"], ln=True, align="C")
        pdf.ln(10)

        # Insert image
        png_filename = value["filename_graph"]
        pdf.image(png_filename, x=10, w=180)
        pdf.ln(10)

        # Insert analysis as a paragraph (wrapped text)
        pdf.set_font("Arial", size=12)  # Normal text
        pdf.multi_cell(0, 10, value["analysis"])  # Multi-line text support
        pdf.ln(10)

    pdf.output(pdf_filename)




