"""
PaLM - Google's LLM - to build generative AI applications like content generation, dialog agents, summarization, classification, and more.
pip install -q google-generativeai

Google Translator - offers several other translators - translate the text to desired language
pip install deep_translator 

Taipy - a friendly simplified gui to create applications in much simplified way
pip install taipy
"""

# imports down here
from deep_translator import GoogleTranslator
from taipy.gui import Gui
import google.generativeai as palm
import sys
sys.path.insert(0, '/')  # Add the directory path to config.py
import config

# API Key
palm.configure(api_key=config.API_KEY)
prompt, completion = '', ''

# Use the palm.list_models function to find available models
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name


# translate to desired language 
def translate(target_lang, source_text):
    translator = GoogleTranslator(source='auto', target=target_lang)
    target_text = translator.translate(source_text)
    return target_text


# Use the palm.generate_text method to generate text
def generate_response(prompt):
    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0,
        # The maximum length of the response
        max_output_tokens=800,
    )
    return completion.result

# list of languages for conversion
langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)
langs_list = list(langs_dict.keys())


# parameters
language = ''
source = ''
target = ''


# triggered on chnage of any state variable
def on_change(state, var_name):
    if var_name == 'language':
        if state.language:
            state.target =  translate(state.language, state.source)

def translate_onclick(state):
    if state.language:
            state.target =  translate(state.language, state.source)


# invoked when button is clicked
def generate_summary_onclick(state):
    prompt = "Generate meaning or summary of following context: "
    context = state.target
    context = translate('en', context)
    response = generate_response(prompt+context)
    if response:
        state.completion = response
    else:
        state.completion = "Couldn't generate a summary for it, or the API might be down, try in later!"

# page
my_page = '''
<|toggle|theme|class_name=relative nolabel|>

<|Choose a language|>

<|{language}|selector|lov={langs_list}|dropdown|> 

<br/>


<|Write something|>

<|{source}|input|>

<br/>

<|translate|button|on_action=translate_onclick|>

<br/>

<|Translation in {language}|>

<br/>

<|{target}|>

<br/>

<|summarize|button|on_action=generate_summary_onclick|>

<br/>

<|{completion}|>
'''

app = Gui(page=my_page)
app.run(use_reloader=True)
