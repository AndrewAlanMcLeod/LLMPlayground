#!/usr/bin/env python
# coding: utf-8

# # Code Reader Demo
# In notebook we'll set up the necessary parameters and prompts to intake code snippets and return a natural language description of the logic.
# 
# ## Setup

# In[10]:


import ipywidgets as widgets
from IPython.display import display


# In[11]:


import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = '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'


# In[12]:


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


# In[13]:


# Create text area widget for input
code_snippet = widgets.Textarea(
    value='',
    placeholder='Type code here...',
    description='Input:',
    disable=False
)

# Create button to trigger processing
button = widgets.Button(description="Analyze")

# Create output widget to display the result
output = widgets.Output()


# In[17]:


# Define button click event
def on_button_clicked(b):
    with output:
        output.clear_output()
        # Get value from text area and process
        result = get_completion(prompt)
        print(result)

# Set event handler for the button
button.on_click(on_button_clicked)


# In[18]:


prompt = f"""
Your task is to generate a concise and comprehensive
description of the code input for the purposes of algorithm audits.

Generate the detailed description in technical laguage at a iq level of 130 
and include the following aspects:
1) All variables (type and name)
2) All inputs (distinguish the stage of the code in which they're input)
3) All stages of the code and thier logical function
4) All outputs (distinguish the stage of the code in which they're output)
5) Any audit/regulatory related comments that come to mind


Here is the code: ```{code_snippet}```

Let's think this through step by step.
"""


# In[19]:


# Display everything
display(code_snippet, button, output)


# In[ ]:




