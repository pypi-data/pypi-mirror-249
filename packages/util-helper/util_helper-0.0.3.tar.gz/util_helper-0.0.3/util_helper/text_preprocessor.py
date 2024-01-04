import os
import re




def split_by_letters(text, max_letters=1):
    # split text into separate characters
    chars = list(text)
    # split into batches of max_chars_per_batch
    batches = ["".join(chars[i:i + max_letters]) for i in range(0, len(chars), max_letters)]
    return batches

def split_by_words(text, max_words=1):
    # split text into separate words
    words = text.split(" ")
    # split into batches of max_words_per_batch
    batches = [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]
    return batches

def split_by_lines(text):
    # split text into separate lines
    lines = text.split("\n")
    return lines

def split_by_double_lines(text):
    # split text into separate double lines
    double_lines = text.split("\n\n")
    return double_lines

def split_by_dot(text):
    # split text into separate sentences
    sentences = text.split(".")
    return sentences

def remove_non_letters(string):
    print(string)
    pattern = r'[^a-zA-Z\s]'
    string =  re.sub(pattern, '', string)
    pattern = r'\s+'
    string = re.sub(pattern, ' ', string)
    string = string.strip()
    return string

def remove_list_formatting(string):
    pattern = r'\n[0-9]+\. '
    string = re.sub(pattern, '', string)
    pattern = r'\n[0-9]+\) '
    string = re.sub(pattern, '', string)
    pattern = r'\s[0-9]+\. '
    string = re.sub(pattern, '', string)
    pattern = r'\s[0-9]+\) '
    string = re.sub(pattern, '', string)
    pattern = r'\s{2,}'
    string = re.sub(pattern, ' ', string)
    string = string.strip()
    return string

