from flask import Flask, request, render_template
import openai
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key  = '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'

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def format_result(raw_result):
    # Split the raw result into lines
    lines = raw_result.split('\n')

    # Initialize the formatted result as an empty string with starting styles
    formatted_result = '<div style="text-align: left; margin: 0 auto; max-width: 800px; font-family: Arial, sans-serif;">'

    # Process each line
    for line in lines:
        # If the line is empty, skip it
        if line == '':
            continue
        # If the line starts with a number and a closing parenthesis, assume it's a section header
        elif line[1:3] == ') ':
            formatted_result += f'<h2 style="color: #333; border-bottom: 1px solid #ddd;"><strong>{line}</strong></h2>'
        # If the line starts with a dash, assume it's an item in a list
        elif line[0] == '-':
            formatted_result += f'<p>{line[2:]}</p>'
        # Otherwise, assume it's a regular paragraph
        else:
            formatted_result += f'<p style="text-indent: 2em; text-align: justify;">{line}</p>'

    formatted_result += '</div>'
    return formatted_result



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code_snippet = request.form['code']
        prompt = f"""
        Your task is to generate a concise and comprehensive
        description of the code input for the purposes of algorithm audits.

        Generate the detailed description in technical laguage at a iq level of 130 
        and include the following aspects, always list them beginning with the numbers in your response:
        1) All variables (type and name)
        2) All inputs (distinguish the stage of the code in which they're input)
        3) All stages of the code and thier logical function
        4) All outputs (distinguish the stage of the code in which they're output)
        5) Any audit/regulatory related comments that come to mind

        Here is the code: ```{code_snippet}```

        Here is an example of a correct response: 
        ```1) Variables:
- incurred_triangle: input data for incurred loss triangle
- paid_triangle: input data for paid loss triangle
- incurred_model: model fitted using incurred loss triangle data
- paid_model: model fitted using paid loss triangle data
- test_model: model fitted using RAA data
- calc_stats: function to calculate desired statistics
- mean_val: mean value of simulations
- sd_val: standard deviation of simulations
- cv_val: coefficient of variation of simulations
- min_val: minimum value of simulations
- max_val: maximum value of simulations
- quantiles: quantiles of simulations

2) Inputs:
- incurred_triangle and paid_triangle: input data for incurred and paid loss triangles respectively

3) Stages of the code and their logical function:
- Stage 1: Fitting a bootstrap model for incurred and paid triangles using BootChainLadder function with gamma distribution
- Stage 2: Fitting a bootstrap model for RAA data using BootChainLadder function with gamma distribution
- Stage 3: Defining a function to calculate desired statistics using simulations
- Stage 4: Calculating mean, standard deviation, coefficient of variation, minimum, maximum, and quantiles of simulations using the calc_stats function

4) Outputs:
- mean_val, sd_val, cv_val, min_val, max_val, and quantiles: output of the calc_stats function

5) Audit/regulatory related comments:
- The code appears to be fitting bootstrap models and calculating statistics for loss triangles, which may be relevant for insurance or risk management purposes. However, without additional context it is difficult to assess the accuracy or appropriateness of the models or statistics being calculated.```

        Respond in exactly the same format.

        Let's think this through step by step.
        """
        result = get_completion(prompt)
        formatted_result = format_result(result)
        return render_template('result.html', result=formatted_result)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
