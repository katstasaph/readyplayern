'''
Created on Nov 23, 2020

@author: Katherine Morayati
'''

import json
import random
import re

import spacy
import tracery
from text_to_num import alpha2digit
from text_to_num import text2num
from tracery.modifiers import base_english

import tkinter as tk
from tkinter import filedialog

nlp = spacy.load("en_core_web_sm")

from spacy.matcher import Matcher

import html_formatter

matcher = Matcher(nlp.vocab)
tracery_tokens = []

def get_referential_density():
    while True:
        density = input("How lovingly nostalgic and wildly referential a story would you like? (0-100)").strip()
        if density.isdigit():
            break
        print("Please enter a number from 0 to 100.")
    return int(density)

def assemble_matcher_patterns(corpora):
    for key in corpora:
        if(any(char.isdigit() for char in key)): 
            continue #numbers are handled separately
        tracery_pattern = "#" + key + "#"    
        matcher_pattern = None  
        match_word = key[:-5] # 4 characters plus the underscore
        if ("noun" in key): #only keys of the form word_pos are used for matcher
            matcher_pattern = [{'LOWER': match_word, 'POS': {'IN': ['NOUN', 'PROPN']}}] 
        elif ("verb" in key):
            matcher_pattern = [{'LOWER': match_word, 'POS': 'VERB'}] 
        elif ("adjc" in key):
            matcher_pattern = [{'LOWER': match_word, 'POS': 'ADJ'}] 
        elif ("advb" in key):
            matcher_pattern = [{'LOWER': match_word, 'POS': 'ADV'}]     
        if (matcher_pattern):
            matcher.add(tracery_pattern, [matcher_pattern])        
    number_pattern = [{'POS': 'NUM', 'ENT_TYPE': {"NOT_IN": ['DATE']}}]
    matcher.add("numeral", [number_pattern])


def convert_to_origin(matcher, content, density):
    matches = matcher(content)
    for match_id, start, end in matches:
        span = content[start:end]
        match_string = nlp.vocab.strings[match_id]
        if(match_string == "numeral"):
            if(span.text != "1" and span.text.lower() != "one"): # relatively unlikely to be used as a number
                new_token = "#" + span.text + "#"
                tracery_tokens.append((span.text, new_token))           
        else:
            tracery_tokens.append((span.text, match_string))
    filtered_tokens = list(dict.fromkeys(tracery_tokens)) #remove duplicates
    with content.retokenize() as retokenizer:
        retokenizer.merge(content[start:end])
    new_text = content.text
    for token in filtered_tokens:
        new_text = re.sub(r"\b%s\b" % token[0], lambda match: token[1] if random.randint(0,100) <= density else match.group(0), new_text)
    return new_text

def fix_final_text(content):
    new_text = re.sub(r'[\,\.\-]+(?=[\,\.\?\!\;])', '', content) # Get rid of double punctuation introduced
    new_text = re.sub('[aA] 100', '100', new_text) #alpha2digit misses "a hundred," etc.
    new_text = re.sub('[aA] 1000', '1000', new_text)
    new_text = re.sub('[aA] 1,000', '1000', new_text)
    return new_text

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
with open('texts/corpora.json', encoding="utf16") as f:
    corpora = json.load(f)
density = get_referential_density()
rules = corpora
assemble_matcher_patterns(rules)
base_text = open(file_path, 'r', encoding="utf8")
base_text = alpha2digit(base_text.read(), "en") # Ensuring compound numbers work in matcher
content = nlp(base_text)
content = convert_to_origin(matcher, content, density)
origin = {"origin": content}
rules.update(origin)
grammar = tracery.Grammar(rules)
grammar.add_modifiers(base_english)
f = open("story.txt", "w+")
new_text = grammar.flatten("#origin#")
new_text = fix_final_text(new_text)
f.write(new_text)
html_formatter.create_html_page(new_text)
f.close()