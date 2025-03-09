import os

from google import genai
from google.genai import types
from gemini.prompts import *

from core.settings import settings
from core.logger import get_logger
from google_sheet_settings.google_sheet_connector import read_google_sheet
from google_sheet_settings.utils import extract_url_from_message
from report_automation.core import clean_messages, get_top_words, save_report, plot_word_distribution
import time

logger = get_logger()

class GeminiConnector:
    def __init__(self, input, message_history):
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model_name = 'gemini-2.0-flash'
        self.input = input
        self.message_history = message_history
        self.response = ""

    def generate_content(self, contents):
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=types.GenerateContentConfig(
                                    tools=[types.Tool(google_search=types.GoogleSearchRetrieval(dynamic_retrieval_config=types.DynamicRetrievalConfig(dynamic_threshold=1.0)))] 
                                )
                )
            return response.text
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            raise e
        
        
    def run(self):

        prompt_task_classifier = google_sheet_task_classifier(self.input)
        task_classifier = self.generate_content(prompt_task_classifier)

        # Read Google Sheet
        df, worksheet = self.read_sheet()
        df = df.reset_index(drop=True)

        # Get column with messages
        contents = identify_text_column(", ".join(df.columns.to_list()))
        columna_message = self.generate_content(contents)
        columna_message = columna_message.replace("\n", "").replace(".", "").strip()

        # Get sentiment column
        sentiment_column_prompt = identify_sentiment_column(", ".join(df.columns.to_list()))
        sentiment_column = self.generate_content(sentiment_column_prompt)
        sentiment_column = sentiment_column.replace("\n", "").replace(".", "").strip()
        index_column_sent = df.columns.get_loc(sentiment_column) + 1

        # Get emotion column
        emotion_column_prompt = identify_emotion_column(", ".join(df.columns.to_list()))
        emotion_column = self.generate_content(emotion_column_prompt)
        emotion_column = emotion_column.replace("\n", "").replace(".", "").strip()
        index_column_emo = df.columns.get_loc(emotion_column) + 1

        if "fill column" in task_classifier.lower():

            logger.info(f"""
                            Info Google Sheet:
                            
                            - length: {len(df)}
                            - Column names:  {', '.join(df.columns.to_list())}
                        """)
            
            for i in df.index[:]:
                message = df.loc[i, columna_message]
                prompt = sentiment_emotion_analysis_expert(message)
                response_sentiment = self.generate_content(prompt)

                sentiment, emotion = response_sentiment.split(",")[0].strip().replace("\n", ""), response_sentiment.split(",")[1].strip().replace("\n", "")

                while True:
                    try:
                        # Save santiment
                        worksheet.update_cell(i+2, index_column_sent, sentiment)

                        # Save emotion
                        worksheet.update_cell(i+2, index_column_emo, emotion)
                        
                        break
                    except:
                        pass

                time.sleep(1)
            
            self.response = f"Update Google Sheet"
            
        elif "analyze" in task_classifier.lower():

            # Clean message
            df = clean_messages(df, columna_message)

            # Extracts the most frequent words from the cleaned messages
            # General words
            general_words = get_top_words(df, "cleaned_text")

            # Positive words
            positive_words = get_top_words(df[df[sentiment_column].str.contains("positive", case=False, na=False)], "cleaned_text")

            # Negative words
            negative_words = get_top_words(df[df[sentiment_column].str.contains("negative", case=False, na=False)], "cleaned_text")

            # Value counts of sentiment column
            sentiment_distribution = df[sentiment_column].value_counts().to_dict()

            # Value counts of emotion column
            emotion_distribution = df[emotion_column].value_counts().to_dict()

            dict_to_processing = {
                "general_words": general_words,
                "positive_words": positive_words,
                "negative_words": negative_words,
                "sentiment_distribution": sentiment_distribution,
                "emotion_distribution": emotion_distribution
            }
            
            dict_info = {}
            count = 0
            colors = ["blue", "green", "red", "yellow", "orange"]
            for key, value in dict_to_processing.items():

                if key == "general_words":
                    context = "Most frequent words of all messages"

                elif key == "positive_words":
                    context = "Most frequent words of all positive messages"

                elif key == "negative_words":
                    context = "Most frequent words of all negative messages"                  

                elif key == "sentiment_distribution":
                    context = "Sentiment distribution of messages"

                elif key == "emotion_distribution":
                    context = "Emotion distribution of messages"
                
                if key != "sentiment_distribution" or key != "emotion_distribution":
                    prompt = frequency_word_analyzer_with_context(context, value)
                    analysis = self.generate_content(prompt)
                else:
                    prompt = analysis_sentimient_emotion(context, value)
                    analysis = self.generate_content(prompt)
                
                # Save graph
                x_label = "Words"
                y_label = "Frequency"
                
                filename = os.path.join(os.getcwd(), "report_automation", "images", f"{key}_distribution.png")
                plot_word_distribution(value, context, x_label, y_label, colors[count], filename)
                count += 1

                dict_info[key] = {
                    "context": context,
                    "analysis": analysis,
                    "filename_graph": filename
                }

            # save report
            save_report(dict_info)

            self.response = "Report generated"


    def read_sheet(self):
        sheet_url = extract_url_from_message(self.input)
        df, worksheet = read_google_sheet(sheet_url["full_link"], sheet_url["gid"])
        return df, worksheet


# def main(
#     column_names
# ) -> str:

#     client = genai.Client(api_key=settings.gemini_api_key)
    
#     try:

#         response = client.models.generate_content(
#             model='gemini-2.0-flash',
#             contents=identify_text_column(column_names),
#             config=types.GenerateContentConfig(
#                 tools=[types.Tool(google_search=types.GoogleSearchRetrieval(dynamic_retrieval_config=types.DynamicRetrievalConfig(dynamic_threshold=1.0)))] 
#             )
#         )
#         response = response.text

#         return f"{response}"
#     except Exception as e:
#         raise e
    


