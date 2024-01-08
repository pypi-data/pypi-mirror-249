import openai
import os
import pandas as pd
import fitz  # PyMuPDF
import pytesseract
import textstat
import re
from PIL import Image
from gensim import corpora, models
from nltk.tokenize import word_tokenize
from summarizer import Summarizer
import json
import copy
from flair.models import SequenceTagger
from flair.data import Sentence
from textblob import TextBlob
from gensim import corpora, models
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from importlib import resources

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
# print(openai.api_key)

def base_table_gen(filename=None):
    # If no filename is specified, use the packaged data
    if filename is None:
        # Open the file as a file-like object using resources.open_text
        with resources.open_text('autopipeline.data', 'base.csv') as file:
            base_table = pd.read_csv(file)
    else:
        # If a filename is specified, read from that file
        base_table = pd.read_csv(filename)
    enum = base_table.columns.tolist()
    description = "'id' column is the document ID, starts with 0; 'pdf_orig' column is the path to the pdf file of the document file; "
    return base_table, enum, description

def pdf_to_text(table, column, enum, description):
    def ocr(pdf_path):
        # Open the PDF file
        # with resources.path('autopipeline.data', pdf_file_name) as pdf_path:
        #     pdf_document = fitz.open(pdf_path)
        pdf_document = fitz.open(pdf_path)

        # Initialize an empty string to store text
        text = ""

        # Iterate over pages
        for page_number in range(pdf_document.page_count - 4):
            # Get the page
            page = pdf_document[page_number]

            # Convert the page to an image
            pix = page.get_pixmap()
            image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

            # Perform OCR on the image
            page_text = pytesseract.image_to_string(image, lang='eng')

            ls = page_text.split("\n\n")

            ls = ls[1:]

            ls = [line.replace("\n", " ") for line in ls]

            page_text = '\n'.join(ls)

            # Append the extracted text to the overall text
            text += page_text

        # Close the PDF document
        pdf_document.close()

        # print(text)

        return text
    
    def pdf_extract(pdf_path):
        # Open the PDF file
        pdf_document = fitz.open(pdf_path)

        # Initialize an empty string to store text
        text = ""

        # Iterate over pages
        for page_number in range(pdf_document.page_count):
            # Get the page
            page = pdf_document[page_number]

            # Get text from the page
            page_text = page.get_text("text")

            # Append the extracted text to the overall text
            text += page_text

        # Close the PDF document
        pdf_document.close()

        # print(text)

        return text
    table[column+'_text'] = table[column].apply(ocr)
    enum.append(column+'_text')
    description += " "+"'"+column+"_text' column is the plain text content of the '" + column +"' column; "
    return table, enum, description

# break into paragraphs: this might pose challenge in our mapping since every row might have different number
# "I want to know the attitude of MORITZ, Circuit Judge"
def para_sep(table, column, enum, description):
    def sep(row):
        # Tokenize and preprocess the document
        paragraphs = [paragraph.strip() for paragraph in row[column].split('\n') if paragraph.strip()]
        rows = []
        for para_id, paragraph in enumerate(paragraphs):
            new_row = copy.deepcopy(row)
            new_row[column+'_segment'] = paragraph
            new_row[column+'_segmentid'] = para_id
            rows.append(new_row)
        res = pd.DataFrame(rows)
        #print(res)
        return res

    # Apply the function to each row and collect the results in a list
    result_df = pd.concat(table.apply(lambda row: sep(row), axis=1).tolist())

    table[column+'_segmentid'] = -1
    table[column+'_segment'] = ""
    # Concatenate the original DataFrame and the result
    table = pd.concat([table, result_df])
    enum.append(column+'_segment')
    description += " "+f"'{column}_segment' column stores the paragraph segments of the '" + column +"column', the original text has empty value; "
    enum.append(column+'_segmentid')
    description += " "+f"'{column}_segmentid' column stores the paragraph index according to the order of the '" + column +"_segment' column, starts with 0, and the original text has value -1 (should be removed when performing functions related to paragraphs); "

    # # Apply the sep function to the specified column
    # segments = table[column].apply(sep)

    # # Create new columns for each segment
    # for i in range(len(segments[0])):
    #     col_name = f"{column}_segment{i + 1}"
    #     enum.append(column+'_segment'+str(i+1))
    #     description += " "+f"'{column}_segment{i + 1}' column is the {i+1}-th segment of the '" + column +"' column; "
    #     table[col_name] = segments.apply(lambda x: x[i] if i < len(x) else None)

    return table, enum, description

def get_ner(table, column, enum, description):
    def ner(row):
        document = row[column]
        # Load the pre-trained Flair NER model for English
        ner_model = SequenceTagger.load('ner')

        # Create a Flair Sentence
        sentence = Sentence(document)

        # Run NER on the sentence
        ner_model.predict(sentence)

        rows = []

        for entity in sentence.get_spans('ner'):
            new_row = copy.deepcopy(row)
            new_row[column+'_ner_type'] = entity.get_labels()[0].value
            new_row[column+'_ner_val'] = entity.text
            rows.append(new_row)
        res = pd.DataFrame(rows)
        #print(res)
        return res

        # Apply the function to each row and collect the results in a list
    result_df = pd.concat(table.apply(lambda row: ner(row), axis=1).tolist())

    table[column+'_ner_type'] = ""
    table[column+'_ner_val'] = ""
    # Concatenate the original DataFrame and the result
    table = pd.concat([table, result_df])
    enum.append(column+'_ner_type')
    description += " "+"'"+column+"_ner_type' column gives the type of the name entities recognized (NER) in the "+column+" column. IMPORTANT: all the NER in the '" +column+"_ner_type' column are in the form of three letters: 'PER' (person), 'LOC' (location), 'GPE' (geopolitical entities), etc."
    enum.append(column+'_ner_val')
    description += " "+"'"+column+"_ner_val' column gives the value of the name entities recognized (NER) in the "+column+" column. e.g. 'UNITED STATES', 'MOHAMED BAK'."
    return table, enum, description

def get_summary(table, column, enum, description):
    def summary(document):
        # Create a BERT Extractive Summarizer
        bertsum_model = Summarizer()
        # Summarize the legal document
        if isinstance(document, list):
            summary = [bertsum_model(doc) for doc in document]
        else:
            summary = bertsum_model(document)
        return summary

    table[column+'_summary'] = table[column].apply(summary)
    enum.append(column+"_summary")
    description += " " + "'"+column+"_summary' column provides summaries of the '"+column+"' column;"
    return table, enum, description

def get_fk(table, column, enum, description):
    def fk(document):
        return textstat.flesch_kincaid_grade(document)

    table[column+'_fk'] = table[column].apply(fk)
    enum.append(column+"_fk")
    description += " " + "'"+column+"_fk' column calculates the Flesch-Kincaid (F-K) readability score of the '"+column+"' column, with a higher score representing lower readability;"
    return table, enum, description

def get_ttr(table, column, enum, description):
    def ttr(document):
        tokens = re.findall(r'\b\w+\b', document.lower())
        types = set(tokens)
        ttr = len(types) / len(tokens) if tokens else 0
        return ttr

    table[column+'_ttr'] = table[column].apply(ttr)
    enum.append(column+"_ttr")
    description += " " + "'"+column+"_ttr' column calculates the Type-Token Ratio (TTR) of the '"+column+"' column, with a higher score representing greater lexical diversity;"
    return table, enum, description

def get_similarity(table, column, enum, description, primary_id, secondary_id):
    def similarity(doc1):
        # Locate the document in the table using doc_id and para_id
        doc2 = table.loc[(table['id'] == int(primary_id)) & (table[column+'id'] == int(secondary_id)), column].values[0]
        
        # If doc2 is not found or empty, return 0
        if not doc2:
            return 0

        vectorizer = TfidfVectorizer()

        # Vectorize the documents
        tfidf_matrix = vectorizer.fit_transform([doc1, doc2])

        # Calculate cosine similarity
        sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

        return sim[0][0]

    # Apply the similarity function to each row in the specified column
    table[column + '_similarity_' + str(primary_id) + '_' + str(secondary_id)] = table[column].apply(similarity)

    # Update the enum and description
    enum.append(column + '_similarity_' + str(primary_id) + '_' + str(secondary_id))
    description += f" '{column}_similarity_{primary_id}_{secondary_id}' column calculates the cosine similarity between the '{column}' column of all the documents and the reference document specified by id={primary_id} and {column}_id={secondary_id};"

    return table, enum, description

def get_keyword(table, column, enum, description):
    def lda(document):
        if document == "":
            return ""
        # Preprocessing the document
        stop_words = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(word) for word in word_tokenize(document.lower()) if word.isalpha() and word not in stop_words]
        
        # Creating a dictionary and corpus for LDA
        dictionary = corpora.Dictionary([tokens])
        corpus = [dictionary.doc2bow(tokens)]

        # Applying LDA model
        lda_model = models.LdaModel(corpus, num_topics=1, id2word=dictionary, passes=10)

        # Extracting keywords from the topic
        topic_words = lda_model.show_topic(0, topn=5)
        keywords = [word for word, _ in topic_words]
        return ', '.join(keywords)

    table[column+'_keyword'] = table[column].apply(lda)
    enum.append(column+"_keyword")
    description += " '" + column + "_keyword' column provides LDA-based keyword identification of the '" + column + "' column;"

    return table, enum, description

def get_sentiment(table, column, enum, description):
    def sentiment(document):
        blob = TextBlob(document)
        polarity = blob.sentiment.polarity
        
        if polarity > 0:
            return 'Positive'
        elif polarity < 0:
            return 'Negative'
        else:
            return 'Neutral'

    table[column+'_sentiment'] = table[column].apply(sentiment)
    enum.append(column+"_sentiment")
    description += " "+"'"+column+"_sentiment' column is the sentiment of the content of the '" + column +"' column. IMPORTANT: sentiment values of '" +column+"_sentiment' column can only be either 'Positive', 'Negative', or 'Neutral'; "
    #description += " Correct Example: table[table['"+column+"_sentiment'] == 'Positive']; Incorrect Example: table[table['"+column+"_sentiment'] == 'positive']; "
    return table, enum, description

# using function call APIs
def schema_gpt(user_query, column_description, description):
    # Define the user's query as an argument
    functions = [
        {
            "name": "para_sep",
            "description": "This function takes in one of the columns as input, split the text according to paragraphs, and generates an additional rows and columns to store the list of paragraphs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "column": {
                        "type": "string",
                        "description": "The column to apply paragraph split. You have to select one column in the 'enum' field to apply paragraph-level split based on the description: "+description,
                        "enum": column_description
                    }
                },
                "required": ["column"]
            }
        },
        {
            "name": "pdf_to_text",
            "description": 
            ''' 
            This function takes in one of the columns as input, transforms the pdf in that column into plain text, and generate an additional column to store the plain text. Don't select this if none of the columns match the user query.
            ''',
            "parameters": {
                "type": "object",
                "properties": {"column": {
                    "type": "string",
                    "description": "the column to apply pdf to text transformation, you have to select one column in the 'enum' field to apply pdf to text transformation based on the description: "+description,
                    "enum": column_description,

                }
                }
            },
            "required": ["column"]
        },
        {
            "name": "get_summary",
            "description": 
            ''' 
            This function takes in one of the columns as input, summarizes the contents in that column, and generate an additional column to include those. Don't select this if none of the columns matches the user query.
            ''',
            "parameters": {
                "type": "object",
                "properties": {"column": {
                    "type": "string",
                    "description": "the column to summarize, you have to select one in the 'enum' field to summarize based on the description: "+description,
                    "enum": column_description,
                }
                }
            },
            "required": ["column"]
        },
        {
            "name": "get_ner",
            "description": 
            ''' 
            This function takes in one of the columns as input, get the name entities recognized in that column, and generate additional rows and columns to include those. NER are in the form of three letters, e.g., PER, LOC, GPE.
            ''',
            "parameters": {
                "type": "object",
                "properties": {"column": {
                    "type": "string",
                    "description": "the column to apply NER analysis, you have to select one column in the 'enum' field to apply NER analysis based on the description: "+description,
                    "enum": column_description,

                }
                }
            },
            "required": ["column"]
        },
        {
            "name": "get_fk",
            "description": 
            ''' 
            This function takes in one of the columns as input, get the Flesch-Kincaid (F-K) readability score of that column, and generate an additional columns to store the score.
            ''',
            "parameters": {
                "type": "object",
                "properties": {"column": {
                    "type": "string",
                    "description": "the column to calculate Flesch-Kincaid (F-K) readability score, you have to select one column in the 'enum' field to calculate F-K readability score based on the description: "+description,
                    "enum": column_description,

                }
                }
            },
            "required": ["column"]
        },
        {
            "name": "get_ttr",
            "description": 
            ''' 
            This function takes in one of the columns as input, get the Type-Token Ratio (TTR) of that column, and generate an additional columns to store the score.
            ''',
            "parameters": {
                "type": "object",
                "properties": {"column": {
                    "type": "string",
                    "description": "the column to calculate Type-Token Ratio (TTR), you have to select one column in the 'enum' field to calculate TTR based on the description: "+description,
                    "enum": column_description,

                }
                }
            },
            "required": ["column"]
        },
        {
            "name": "get_similarity",
            "description": 
            ''' 
            This function calculates the cosine similarity between a specified column and a reference document identified by primary_id and secondary_id.
            ''',
            "parameters": {
                "type": "object",
                "properties": {"column": {
                    "type": "string",
                    "description": "the column to calculate similarity between the reference doc, you have to select one column in the 'enum' field to calculate similarity based on the description: "+description,
                    "enum": column_description,
                },
                "primary_id": {
                    "type": "string",
                    "description": "the index in the 'id' column",
                },
                "secondary_id": {
                    "type": "string",
                    "description": "the index of corresponding to the selected column",
                },

                }
            },
            "required": ["column", "primary_id", "secondary_id"]
        },
        {
            "name": "get_keyword",
            "description": 
            ''' 
            This function takes in one of the columns as input, get the top 5 keywords recognized in that column, and generate an additional column to include those.
            ''',
            "parameters": {
                "type": "object",
                "properties": {"column": {
                    "type": "string",
                    "description": "the column to apply keyword recognition, you have to select one column in the 'enum' field to apply keyword recognition based on the description: "+description,
                    "enum": column_description,

                }
                }
            },
            "required": ["column"]
        },
        {
            "name": "get_sentiment",
            "description": "This function takes in one of the columns as input, applies sentiment analysis on the content of that column, and generates an additional column labeling the content as 'Positive', 'Negative', and/or 'Neutral'. Don't select this if none of the columns matches the user query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "column": {
                        "type": "string",
                        "description": "The column to apply sentiment analysis. You have to select one column in the 'enum' field to apply sentiment analysis based on the description: "+description,
                        "enum": column_description
                    }
                },
                "required": ["column"]
            }
        },
        {
            "name": "null",
            "description": "This function should be called when the table already contains all the necessary information to complete the user query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "column": {
                        "type": "string",
                        "description": "The placeholder parameter. It can only be 'null'",
                        "enum": ["null"]
                    }
                },
                "required": ["column"]
            }
        }
    ]
    messages = [
        {
            "role": "user",
            "content": "I want to count the number of positive paragraphs in the PDF document. 'id' column is the document ID; 'pdf_orig' column is the path to the pdf file of the document file;"
        },
        {
            "role": "assistant",
            "content": "To count the number of positive paragraphs in the PDF document, the user should first transform the PDF file into plain text, break the text into paragraphs, and then get the sentiment of these paragraphs. Among all the columns, the user is given the PDF file in 'pdf_orig', and is not given the plain text of the document, thus the first function to apply is 'pdf_to_text' on the 'pdf_orig' column to get the plain text of the PDF file.",
            "function_call": {
                "name": "pdf_to_text",
                "arguments": "{\n  \"column\": \"pdf_orig\"\n}"
            }
        },
        {
            "role": "user",
            "content": "I want to count the number of positive paragraphs in the PDF document. 'id' column is the document ID; 'pdf_orig' column is the path to the pdf file of the document file; 'pdf_orig_text' column is the plain text content of the 'pdf_orig' column;"
        },
        {
            "role": "assistant",
            "content": "To count the number of positive paragraphs in the PDF document, the user should first transform the PDF file into plain text, break the text into paragraphs, and then get the sentiment of these paragraphs. Among all the columns, the user is given the plain text of the PDF file in 'pdf_orig_text', and is not given the paragraph-wise segments of the document, thus the first function to apply is 'para_sep' on the 'pdf_orig_text' column to get the paragraph-level splits of the plain text.",
            "function_call": {
                "name": "para_sep",
                "arguments": "{\n  \"column\": \"pdf_orig_text\"\n}"
            }
        },
        {
            "role": "user",
            "content": "I want to count the number of positive paragraphs in the PDF document. 'id' column is the document ID; 'pdf_orig' column is the path to the pdf file of the document file; 'pdf_orig_text' column is the plain text content of the 'pdf_orig' column; 'pdf_orig_text_segment' stores the paragraph segments of the 'pdf_orig_text' column, the original text has empty value; 'pdf_orig_text_segmentid' column stores the paragraph index according to the order of the 'pdf_orig_text_segment' column, starts with 0, and the original text has value -1;"
        },
        {
            "role": "assistant",
            "content": "To count the number of positive paragraphs in the PDF document, the user should first transform the PDF file into plain text, break the text into paragraphs, and then get the sentiment of these paragraphs. Among all the columns, the user is given the paragraphs of the PDF file in 'pdf_orig_text_segments', and is not given the sentimental analysis for the paragraphs, thus the first function to apply is 'get_sentiment' on the 'pdf_orig_text_segments' column to get the sentiment for the paragraphs.",
            "function_call": {
                "name": "pdf_to_text",
                "arguments": "{\n  \"column\": \"pdf_orig_text_segment\"\n}"
            }
        },
        {
            "role": "user",
            "content": "I want to count the number of positive paragraphs in the PDF document. 'id' column is the document ID; 'pdf_orig' column is the path to the pdf file of the document file; 'pdf_orig_text' column is the plain text content of the 'pdf_orig' column; 'pdf_orig_text_segment' stores the paragraph segments of the 'pdf_orig_text' column, the original text has empty value; 'pdf_orig_text_segmentid' column stores the paragraph index according to the order of the 'pdf_orig_text_segment' column, starts with 0, and the original text has value -1; 'pdf_orig_text_segment_sentiment' column is the sentiment of the content of the 'pdf_orig_text_segment' column; "
        },
        {
            "role": "assistant",
            "content": "To count the number of positive paragraphs in the PDF document, the user should first transform the PDF file into plain text, break the text into paragraphs, and then get the sentiment of these paragraphs. Among all the columns, the user is already given the paragraph-level sentiment analysis in the 'pdf_orig_text_segment_sentiment' column. Thus the first function to apply is 'null' to end the function chain.",
            "function_call": {
                "name": "null",
                "arguments": "{\n  \"column\": \"null\"\n}"
            }
        },
        {
            "role": "user",
            "content": user_query  # Use the user's query
        }
    ]

    response = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo-16k",
        model="gpt-4-0613",
        messages=messages,
        functions = functions,
        function_call = "auto",
    )

    return response.choices[0].message

def table_gen_pd(user_query, table, enum, description, status):
    while True:
        response = schema_gpt(user_query + " I am given a table with the following columns: " + description, enum, description)
        # print(response)
        if "function_call" not in response:
            if "content" in response:
                feedback = response["content"]
            else:
                feedback = ""
            return table, enum, description, True, feedback
        func = response["function_call"]
        f = func["name"]
        if f == "null":
            break
        function_dict = json.loads(func["arguments"])
        col = function_dict["column"]
        if col == "null":
            break
        if f == "get_similarity":
            primary_id = function_dict["primary_id"]
            secondary_id = function_dict["secondary_id"]
            table, enum, description = globals()[f](table, col, enum, description, primary_id, secondary_id)
        else:
            table, enum, description = globals()[f](table, col, enum, description)
    print(table)
    # print(description)
    status.append("table augmented")
    return table, enum, description, False, ""

if __name__ == "__main__":
    # query = "I want to remove biases."
    table, enum, description = base_table_gen()
    # status = []
    # table, enum, description, _ = table_gen_pd(query, table, enum, description, status)
    # print(table)
    # print(enum)
    # # # print(description)
    table, enum, description = pdf_to_text(table, 'pdf_orig', enum, description)
    table, enum, description = get_keyword(table, 'pdf_orig_text', enum, description)
    print(table)
    # # print(table)
    # print(enum)
    # # print(description)
    # table, enum, description = para_sep(table, 'pdf_orig_text', enum, description)
    # print(table)
    # print(enum)
    # # print(description)
    # # table, enum, description = get_summary(table, 'pdf_orig_text_segment1', enum, description)
    # # print(table)
    # # print(enum)
    # # print(description)



