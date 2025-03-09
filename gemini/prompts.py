def google_sheet_task_classifier(user_input):

    prompt = f""" 
            ### Role  
                You are an expert in interpreting user instructions related to Google Sheets. Your task is to determine whether the user is requesting to **fill columns** or **analyze** the spreadsheet.  

                ### Task  
                Analyze the user input and classify it into one of the following categories:  
                - **"Fill columns"** → If the user is requesting to complete, populate, or update specific columns in a Google Sheet.  
                - **"Analyze"** → If the user is requesting an analysis, summary, insights, or reports from the Google Sheet.  

                ### Instructions  
                - Carefully examine the user's request.  
                - If the user asks to **fill, complete, or update columns**, return `"Fill columns"`.  
                - If the user asks to **analyze, summarize, or generate insights**, return `"Analyze"`.  
                - **Return only the classification (`"Fill columns"` or `"Analyze"`) without any additional explanation.**  

                ### Example  
                **Input:**  
                `"Complete the column B with the Sentiment for each message from spreadsheet https://docs.google.com/spreadsheets/d/17fmC8BAm3sL7oG3UkypuqrYnrT4aXJ5DFsSdZsi9928/edit?gid=0#gid=0"`  

                **Output:**  
                `Fill columns`  

                **Input:**  
                `"Analyze the following Google Sheet and generate a report with graphs with the most important insights from the following spreadsheet: https://docs.google.com/spreadsheets/d/17fmC8BAm3sL7oG3UkypuqrYnrT4aXJ5DFsSdZsi9928/edit?gid=0#gid=0"`  

                **Output:**  
                `Analyze` 

            ### User's input: {user_input}


            """
    return prompt

def identify_text_column(column_names):
    prompt = f"""
               ### Role  
            You are an expert data analyst specialized in text processing and data structures.  

            ### Task  
            Analyze a given list of column names from a Pandas dataframe and return only the column name that is most likely to contain text messages.  

            ### Instructions  
            - Evaluate each column name carefully.  
            - Identify the one that is most related to text messages (e.g., "message", "text", "content").  
            - **Return only the column name** without any additional explanation.  
 
            ### Example  
            **Input:**  
            `["name", "message", "sentiment", "emotion"]`  

            **Output:**  
            `message`

            ### The column names are: {column_names}
    """
    return prompt

def sentiment_emotion_analysis_expert(message):
    prompt = f"""
        ### Role  
        You are an expert sentiment and emotion analyst specializing in analyzing messages from social media. You have deep expertise in understanding tone, context, sentiment, and emotions in text.  

        ### Task  
        Analyze a given message and classify:  
        - **Sentiment** as **Positive, Negative, or Neutral**  
        - **Emotion** as **Joy, Anger, Sadness, Fear, Surprise, or Disgust**  

        ### Instructions  
        - Carefully evaluate the emotional tone and sentiment of the message.  
        - Identify the sentiment (**Positive, Negative, or Neutral**).  
        - Identify the emotion (**Joy, Anger, Sadness, Fear, Surprise, or Disgust**).  
        - **Return only the sentiment and emotion, separated by a comma, without any additional explanation.**  

        ### Example  
        **Input:**  
        `"I love this product! It's amazing!"`  

        **Output:**  
        `Positive, Joy`  

        **Input:**  
        `"This is the worst experience I've ever had."`  

        **Output:**  
        `Negative, Anger`  

        **Input:**  
        `"It's okay, nothing special."`  

        **Output:**  
        `Neutral, None`  

        ### The message is: {message}
    """
    return prompt


def identify_sentiment_column(column_names):
    prompt = f"""
          ### Role  
            You are an expert data analyst specializing in text classification and sentiment analysis. Your task is to identify the column that contains **sentiment information** from a given list of column names.  

            ### Task  
            Analyze a list of column names and return only **one** column name that represents the **sentiment of messages**.  

            ### Instructions  
            - Identify the column that is most likely to contain **sentiment classification** (e.g., `"Sentiment"`, `"Sentiment of message"`, `"sentiment_score"`).  
            - **Return only one column name** without duplicates, newlines, or additional explanations.  
            - If there are multiple columns that could represent sentiment, choose the **most relevant one**.  

            ### Example  
            **Input:**  
            `["name", "message", "Sentiment", "emotion"]`  

            **Output:**  
            `Sentiment`  

            **Input:**  
            `["user_id", "review_text", "sentiment_score", "timestamp"]`  

            **Output:**  
            `sentiment_score`  

            **Input:**  
            `["Message", "Sentiment", "Emotion"]`  

            **Output:**  
            `Sentiment`  

            ### The column names are: {column_names}
    """
    return prompt

def identify_emotion_column(column_names):
    prompt = f"""
          ### Role  
            You are an expert data analyst specializing in text classification and emotion analysis. Your task is to identify the column that contains **emotion information** from a given list of column names.  

            ### Task  
            Analyze a list of column names and return only **one** column name that represents the **emotion of messages**.  

            ### Instructions  
            - Identify the column that is most likely to contain **emotion classification** (e.g., `"Emotion"`, `"Emotion of message"`, `"emotion_score"`).  
            - **Return only one column name**, without duplicates, newlines, or additional explanations.  
            - If multiple columns seem relevant, choose the **most appropriate** one.  

            ### Example  
            **Input:**  
            `["name", "message", "Sentiment", "emotion"]`  

            **Output:**  
            `emotion`  

            **Input:**  
            `["user_id", "review_text", "emotion_score", "timestamp"]`  

            **Output:**  
            `emotion_score`  

            **Input:**  
            `["Message", "Sentiment", "Emotion"]`  

            **Output:**  
            `Emotion`  

            ### The column names are: {column_names}
    """
    return prompt


def frequency_word_analyzer_with_context(context, frequency_dict):
    prompt = f"""
          ### Role  
            You are an expert data analyst specializing in text analysis and frequency word detection, particularly for speech analysis. Your task is to analyze the most frequent words from a given set of messages, considering a specific context (all messages, positive messages, or negative messages). You will evaluate the frequency of words based on the context and provide a detailed, clear, and concise analysis of why those words are relevant within the context.

            ### Task  
            Analyze the provided dictionary of the most frequent words and identify the words that appear most often, based on the specified context. Provide a thorough explanation in a paragraph form, focusing on why these words are relevant to the context of the messages, considering whether they belong to positive, negative, or general contexts.

            ### Instructions  
            - You will receive a dictionary with words and their frequencies.  
            - You will also receive a context that defines which messages to analyze (e.g., all messages, positive messages, or negative messages).  
            - **Return the most frequent words** according to the specified context, and **provide an analysis** explaining why these words are most frequent in the given context.  
            - Focus on how these words are related to the context (positive, negative, or general messages), and explain their relevance based on frequency and meaning in a concise paragraph.

            ### Context Examples:  
            - `"most frequent words of all messages"`  
            - `"most frequent words of all positive messages"`  
            - `"most frequent words of all negative messages"`  

            ### Example  
            **Input:**  
            - Dictionary: `'borderland': 82, 'borderlands': 66, 'play': 37, 'fun': 34, 'game': 34, 'get': 31, 'good': 31, 'stream': 29, 'drop': 29, 'come': 24`  
            - Context: `"most frequent words of all messages"`  

            **Analysis:**  
            The frequent appearance of words like "borderland", "borderlands", "play", "fun", and "game" indicates that the messages likely revolve around a game or activity, with a positive sentiment. Words like "get", "good", "stream", and "come" further emphasize participation and enjoyment in this activity. These words together paint a picture of people engaged in a fun, game-related experience.

            ---

            **Input:**  
            - Dictionary: `'happy': 42, 'sad': 30, 'joy': 28, 'play': 24, 'rain': 20`  
            - Context: `"most frequent words of all positive messages"`  

            **Analysis:**  
            In the context of positive messages, the most frequent words "happy" and "joy" strongly align with positive emotions, indicating the messages convey feelings of contentment and satisfaction. "Play" further emphasizes an activity that people enjoy. Although "rain" might initially seem neutral, it could have a positive connotation in certain situations, such as bringing calmness or a pleasant atmosphere, hence its inclusion, albeit less frequent.

            ---

            **Input:**  
            - Dictionary: `'anger': 58, 'frustration': 47, 'sad': 34, 'dislike': 32, 'fail': 28`  
            - Context: `"most frequent words of all negative messages"`  

            **Analysis:**  
            These words are all associated with negative emotions and outcomes, fitting the context of negative messages. "Anger" and "frustration" are intense emotional responses often tied to dissatisfaction or conflict, while "sad" reflects feelings of sorrow. "Dislike" and "fail" indicate negative experiences or outcomes, contributing to an overall tone of discontent, disappointment, and emotional distress within the messages.

            ### Dictionary of word frequencies: {frequency_dict}  
            ### Context: {context}


    """
    return prompt

def analysis_sentimient_emotion(context, dict_distribution):
    prompt = f"""
                ### Role  
                    You are an expert in sentiment and emotion analysis, specializing in analyzing the distribution of sentiments and emotions in social media messages. Your task is to examine the given distribution of sentiment or emotion and provide a clear, concise analysis in a paragraph format.  

                    ### Task  
                    Analyze the provided dictionary that contains the distribution of sentiment or emotion categories in messages. Depending on the specified context, your analysis should focus on either sentiment (Neutral, Positive, Negative) or emotions (e.g., Happiness, Sadness, Anger, Fear). Your response should be a well-structured paragraph that highlights the key insights from the distribution, explaining the overall tone of the messages and any significant trends.  

                    ### Instructions  
                    - You will receive:  
                    1. A **context** that specifies whether the analysis should focus on **sentiment distribution** or **emotion distribution**.  
                    2. A **dictionary** containing sentiment or emotion categories along with their respective frequencies.  
                    - Your response must be a **concise paragraph** analyzing the distribution based on the given context.  
                    - Consider the dominance of certain categories, the balance between them, and what this implies about the general tone of the messages.  
                    - If the distribution is skewed toward one sentiment or emotion, highlight its significance.  

                    ### Context Examples:  
                    - `"Sentiment distribution of messages"` → Analyze sentiments (Neutral, Positive, Negative).  
                    - `"Emotion distribution of messages"` → Analyze emotions (Happiness, Sadness, Anger, etc.).  

                    ### Example  

                    #### **Input:**  
                    - **Context:** `"Sentiment distribution of messages"`  
                    - **Dictionary:** `'Neutral': 248, 'Negative': 6, 'Positive': 4`  

                    #### **Output:**  
                    The sentiment distribution reveals that the majority of messages (248) are neutral, suggesting that most discussions lack strong emotional expressions. Positive (4) and negative (6) sentiments are minimal, indicating a generally balanced yet emotionally subdued conversation. The low presence of emotional polarity suggests that users are either providing factual information or engaging in neutral discourse rather than expressing strong opinions.  

                    ---

                    #### **Input:**  
                    - **Context:** `"Emotion distribution of messages"`  
                    - **Dictionary:** `'Happiness': 120, 'Sadness': 40, 'Anger': 30, 'Fear': 10`

                    #### **Output:**  
                    The emotion distribution highlights that happiness is the dominant emotion, appearing in 120 messages, which suggests that users generally express positive experiences or uplifting sentiments. Sadness (40) and anger (30) are present but significantly lower, indicating that negative emotions are not prevalent in the discourse. Fear (10) is the least expressed emotion, further reinforcing the notion that the overall conversation maintains a predominantly positive or neutral emotional tone.  

                    ### Dictionary of sentiment or emotion distribution: {dict_distribution}  
                    ### Context: {context}  
            """
    
    return prompt