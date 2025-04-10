﻿import json                # for create the json file
import re                  # for using pattern matching to find questions, answers and options
from docx import Document  # for reading word file

def doc_tojson(file_path):
    '''
    Using try catch block to load the file so that errors can handle
    '''
    
    try:
        doc=Document(file_path)
    except Exception as e:
        print(f"Error opening document: {e}")
        return 
    
    
    '''
    Using List Data Structure to store questions.
    '''
    
    question=[]   # store all questions dictionaries
    c_question={} # current question
    
    '''
    Using re module to find patterns.
    Generating patterns for finding questions, answers and options.
    
    '''
    q_pattern=re.compile(r'^\d+\.\s+(.*)')          # regular expression pattern for question matching
    opt_pattern=re.compile(r'^([A-D])\.\s+(.*)')      # regular expression pattern for option matching
    anw_pattern=re.compile(r'^Answer:\s*([A-D])')   # regular expression pattern for answer matching 
    
    
    '''
    Iterating through the file data.
    '''
    for i in doc.paragraphs:
        text=i.text.strip()                         # removing whitespaces
        if not text:
            continue
        question_match=q_pattern.match(text)
        option_match=opt_pattern.match(text)
        answer_match=anw_pattern.match(text) 
        
        if question_match: 
            if c_question:                          # if question and already present current question, save it
                question.append(c_question)
            c_question={
                "question":question_match.group(1),
                "answer":None,
                "options":{}
            }
        elif option_match and c_question:
            c_question["options"][option_match.group(1)]=option_match.group(2)  # save option under corresponding question
        
        elif answer_match and c_question:
            c_question["answer"]=answer_match.group(1)                          # we use group 1 not 0 as we need only the fisrt match with the regular expression pattern
        
    if  c_question:
        question.append(c_question)
            
    
    '''
    After iteration finally iteration json file is created using json.dump method
    '''        
    
    output_file=file_path.replace('.docx',".json")                              # using same file name and changing its extension to json as straing operation.
    try:
        with open(output_file,"w",encoding='utf-8') as f:                       # using 'with' so that the we don't need to close the file opend 
            json.dump(question,f,indent=4)                                      # using dump method to add data to json
            print(f"Json output stored to {output_file}")
    except Exception as e:
        print(f"Error occured at {e}")                                          # Log the error occured
                
    
'''
For the example usage of this converting function use
doc_tojson('file_name.docx')
note: 
    1. replace the file_name.docx with actuall file path to the word document 
    2. if not installed please install python-docx for using this function.
'''
        
