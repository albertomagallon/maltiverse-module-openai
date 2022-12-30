# -*- coding: utf-8 -*-
from maltiverse import Maltiverse
import json
import argparse
import re
import requests
 
try:
    import openai
except ImportError:
    print("OpenAI module not installed.")

api_key_openAI = "PUT_YOUR_OPENAI_API_KEY_HERE"
#api_key_maltiverse = Maltiverse(auth_token="PUT_YOUR_MALTIVERSE_API_KEY_HERE")
# Use Maltiverse with requests
api_key_maltiverse_requests= "PUT_YOUR_MALTIVERSE_API_KEY_HERE"

# Beautifier function for OpenAI
def replace_last(string, delimiter, replacement):
    start, _, end = string.rpartition(delimiter)
    return start + replacement + end

def get_openai_answer(prompt, api_key):

    # Set up the OpenAI API client
    openai.api_key = api_key
    print("[+] Question to OpenAI: " + prompt)

    # Set up the model and prompt; this can also be moved to the module config
    model_engine = "text-davinci-003"
    max_tokens = 1024
    max_n = 10
    frequency_penalty = 0.7
    top_p = 1
    temperature = 0.0

    # Generate a response ; alternative use n=max_n instead of top_p
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        frequency_penalty=frequency_penalty,
        max_tokens=max_tokens,
        top_p=top_p,
        stop=None,
        temperature=temperature,
    )

    ai_response = ""
    for el in completion.choices:
        if len(ai_response) > 0:
            ai_response = "{} {}".format(ai_response, el.text)
        else:
            ai_response = el.text

    return ai_response

def create_openAI_Question(IOC, IOC_Type, threats):
    attribute_type = IOC_Type
    attribute_value = IOC
    attribute_threats = threats

    base_prompt_1 = "I'm a cyber threat analyst, give me a short report about what I have to do with the malicious"
    base_prompt_2 = "used in campaigns"
    base_prompt_3 = "and a list of recomendations for IT administrators should take to prevent traffic to this"
    
    prompt = base_prompt_1 + " " + attribute_type + " " + attribute_value + " " + base_prompt_2 + " " + attribute_threats + " " + base_prompt_3 + " " + attribute_type  + "."
    return prompt

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("--ip", "-i", type=str, help="IOC is a IP parameter")
# Other possibilities
#group.add_argument("--domain", "-d", type=str, help="IOC is a domain")

# Parse the arguments
args = parser.parse_args()

attribute_value = ""
threat_description_list = []
result = ""


if args.ip:
    attribute_value =  str(args.ip)
    # Without using requests
    #result = api_key_maltiverse.ip_get(attribute_value)
    # Using requests
    url = 'https://api.maltiverse.com/ip/' + attribute_value
    headers = { 'Authorization':'Bearer ' + api_key_maltiverse_requests }
    #Ask Maltiverse
    response = requests.get(url, headers=headers)
    result = json.loads(response.text)
#  Other possibilities
# if args.domain:
#    attribute_value =  str(args.domain)
#    result = api_key_maltiverse.hostname_get(attribute_value)

print("[+] Looking for " + str(attribute_value))

threat_type =  result["type"]

# Iterate through the attributes
for attribute in result["blacklist"]:
    threat_description_list.append(attribute["description"])

# Remove duplicates
threat_description_list = list(set(threat_description_list))

#Beatiful presenteation for OpenAI :)
threat_description_text = ', '.join(threat_description_list)
threat_description_text = replace_last(threat_description_text, ', ', ' and ')

print("[+] Maltiverse response: IOC type " + threat_type + " with the follow threats associated " + threat_description_text)

# Prepare question for openAI
prompt = create_openAI_Question(attribute_value, threat_type, threat_description_text)
# Ask openAI
response = get_openai_answer(prompt, api_key_openAI)

print("[+] Recomendation from OpenAI: " + response)