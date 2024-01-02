import pandas as pd
from .PipelineGen import pipeline_gen
from .Mapping import base_table_gen

def load_data(dataframe, desc, desc_file=True):
    # Load DataFrame
    try:
        table = pd.read_csv(dataframe)  # or pd.read_excel for Excel files
    except Exception as e:
        print(f"Failed to load DataFrame: {e}")
        return
    if desc_file:
        try:
            with open(desc, 'r') as file:
                description = file.read()
        except:
            print(f"Failed to load description: {e}")
            return
    else:
        description = desc
    
    return table, description

def pipeline(query, table, description):
    require_new, feedback = pipeline_gen(query, table, description, table_type="pd")
    if require_new:
        print("##########Feedback: ", feedback)
        print("Please Be More Detailed on Query.")
    else:
        print("Succeed!")

def interactive_pipeline(table, description):
    require_new = True
    # table, enum, description = base_table_gen()
    while require_new:
        print("-----------------------------")
        query = str(input("Please enter your query: "))
        require_new, feedback = pipeline_gen(query, table, description, table_type="pd")
        if require_new:
            print("##########Feedback: ", feedback)


def _interactive_pipeline():
    # Prompt user for file path
    file_path = input("Please enter the file path for your DataFrame: ")

    # Load DataFrame
    try:
        table = pd.read_csv(file_path)  # or pd.read_excel for Excel files
    except Exception as e:
        print(f"Failed to load DataFrame: {e}")
        return
    
    # Prompt user for file path
    file_path = input("Please enter the description for your DataFrame: ")

    # Load DataFrame
    try:
        with open(file_path, 'r') as file:
            description = file.read()
    except:
        description = file_path
    require_new = True
    # table, enum, description = base_table_gen()
    while require_new:
        print("-----------------------------")
        query = str(input("Please enter your query: "))
        require_new, feedback = pipeline_gen(query, table, description, table_type="pd")
        if require_new:
            print("##########Feedback: ", feedback)

if __name__ == "__main__":
    interactive_pipeline()