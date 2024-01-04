import json

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage
)


def get_metadata(prompt: str, chat: ChatOpenAI):
    metadata = f"""
    
    Instructions
    
    Please consider the following prompt. Before you answer, please provide the following.
    
    1) A Summarized Prompt of 10 words or less.
    
    2) A Restated Prompt.
    
    3) A Classification of the prompt as Creative Writing, Information Retrieval, Calculation, or Reasoning. You may provide more than one classification. Please return a list.
    4) Entities references in the prompt returned as a list.
    
    5) A score of the Difficulty of this prompt from 1 to 10 where 1 is easiest and 10 is hardest/
    
    6) A score of the Time Sensitivity of this prompt from 1 to 10 where 1 means the response does NOT change with time and 10 means the response changes frequently.
    
    7) A list of Presumptions that must be true in the response.
    
    8) A list of Aspects of the Prompt which should be included in the response.
    
    9) If a list of possible answers is provided use it. If the possible answers are labeled, please show the label and the answer. Otherwise, develop a list of possible answers if you can.
    
    10) A liat of Relevant Website from which we can get some relevant information about the prompt.
    
    11) A list of Related Search Terms.
    
    12) An Algorithm for creating the response.
    
    13) If the classification list includes "Calculation", then write and execute a python script to calculate the response.
    
    
    Response Format:
    "summarized_prompt": response to 1
    "restated_prompt": response to 2
    "classification": response to 3
    "entities": response to 4
    "difficulty_score": response to 5
    "time_sensitivity_score": response to 6
    "presumptions": response to 7
    "aspects_to_include": response to 8
    "possible_answers": response to 9
    "relevant_website": response to 10
    "related_search_terms": response to 11
    "algorithm": response to 12
    
    Prompt:
    {prompt}

    """
    output_prompt = "Return the results in a JSON format only. Do not include any other commentary, only JSON."
    messages = [
        SystemMessage(content=metadata),
        SystemMessage(content=output_prompt)
    ]

    res = chat(messages)
    json_data = res.content.replace('```json', '').replace('```', '').strip()
    rsp = json.loads(json_data)
    return rsp
