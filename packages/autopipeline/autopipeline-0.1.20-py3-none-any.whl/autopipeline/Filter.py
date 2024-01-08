import openai
import pandas as pd
import os

OPENAI_ORGANIZATION = "org-5rFbX7p7v2H4Sk1C8xb17aea"
os.environ["OPENAI_ORG"] = OPENAI_ORGANIZATION
openai.organization=os.environ["OPENAI_ORG"]

def check_vague(user_query, columns, description):
    functions = '''
    "para_sep": "This function takes in one of the columns as input, split the text according to paragraphs, and generates an additional rows and columns to store the list of paragraphs.",
    "pdf_to_text": "This function takes in one of the columns as input, transforms the pdf in that column into plain text, and generate an additional column to store the plain text.",
    "get_summary": "This function takes in one of the columns as input, summarizes the contents in that column, and generate an additional column to include those.",
    "get_ner": "This function takes in one of the columns as input, get the name entities recognized in that column, and generate additional rows and columns to include those.",
    "get_fk": "This function takes in one of the columns as input, get the Flesch-Kincaid (F-K) readability score of that column, and generate an additional columns to store the score.",
    "get_ttr": "This function takes in one of the columns as input, get the Type-Token Ratio (TTR) of that column, and generate an additional columns to store the score.",
    "get_similarity": "This function calculates the cosine similarity between a specified column and a reference document identified by primary_id and secondary_id.",
    "get_keyword": "This function takes in one of the columns as input, get the top 5 keywords recognized in that column, and generate an additional column to include those.",
    "get_sentiment": "This function takes in one of the columns as input, applies sentiment analysis on the content of that column, and generates an additional column labeling the content as 'Positive', 'Negative', and/or 'Neutral'."
    '''
    messages = [
        {
            "role": "system",
            "content": "Given a table with columns: " + columns 
            + " where " + description 
            + " You are also given functions to be applied to different columns: " + functions 
            + '''Your task is 
                (1) Check if user query is specific enough; 
                (2) If it is specific (True), provide the function chain to be performed to generate the table required to answer users' query; 
                If it is not specific (False), provide alternative queries that are specific enough to be answered with a function chain of provided function.

                Your output format can ONLY be "True"/"False" + "#" + "{function chain}"/"{alternative queries}"
                '''
        },
        {
            "role": "user",
            "content": "I want to count the number of positive paragraphs in the PDF document. 'id' column is the document ID; 'pdf_orig' column is the path to the pdf file of the document file;"
        },
        {
            "role": "assistant",
            "content": "True#To count the number of positive paragraphs in the PDF document, the user should first transform the PDF file into plain text, break the text into paragraphs, and then get the sentiment of these paragraphs. Thus the function call chain should be ['pdf_to_text', 'para_sep', 'get_sentiment']",
        },
        {
            "role": "user",
            "content": "I want to find paragraph(s) dictating a specific outcome or reasoning. 'id' column is the document ID; 'pdf_orig' column is the path to the pdf file of the document file;"
        },
        {
            "role": "assistant",
            "content": "False#Your query is too vague. Alternatively, you can ask 'I want to get the summary for each paragraph in the pdf file.'",
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
    )

    return response.choices[0].message

if __name__ == "__main__":
    # query = "I want to remove biases."
    table = pd.read_csv("./data/base.csv")
    columns = str(table.columns.tolist())
    description = "'id' column is the document ID, starts with 0; 'pdf_orig' column is the path to the pdf file of the document file; "
    user_query = "I want to remove adversarial examples."
    user_query = "Hi."
    user_query = "I want to count the number of positive, negative, and neutral paragraphs for each document."
    response = check_vague(user_query, columns, description)
    print(response)
    