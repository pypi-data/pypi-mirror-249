# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 17:09:15 2023

@author: SOUMYAJIT
"""

import re, warnings
warnings.filterwarnings("ignore")
  
def prRed(skk):
    print("\033[31m{}\033[00m" .format(skk))

def tkeypos(keyword, text):
    text = text.lower()
    keyword = str(keyword).lower()
    positions = []
    for match in re.finditer(keyword, text):
        start = match.start()
        end = match.end()
        positions.append((start, end))
    return positions

def extract_sents(keyword, text, format='l'):
    keyword = str(keyword).lower()
    text = text.lower()
    sentences = text.split('.')
    keyword_sentences = [sentence.strip() for sentence in sentences if keyword in sentence]
    if format.lower() == 'l':
        return keyword_sentences
    elif format.lower == 'p':
        return '.'.join(keyword_sentences)
    else:
        pass

def extract_words(keyword, text, left=0, right=1):
    text = text.lower()
    keyword = str(keyword).lower()
    text_pieces = text.split(keyword)

    if len(text_pieces) == 1:
        return None

    split_words = [piece.split() for piece in text_pieces]
    occurrences = []

    for index in range(len(split_words) - 1):
        left_words = split_words[index][len(split_words[index]) - left:]
        right_words = split_words[index + 1][0: right]
        surrounded_text = " ".join(left_words + [keyword] + right_words)
        occurrences.append(surrounded_text)

    return occurrences

def extract_chars(keyword, text, left_chr=0, right_chr=1):
    keyword = str(keyword).lower()
    text = text.lower()
    key = re.finditer(keyword, text)
    pos_start_end = [(match.start(), match.end()) for match in key]
    extract_characters = []
    for pos in pos_start_end:
        user_need = text[pos[0] - left_chr: pos[1] + right_chr]
        extract_characters.append(user_need)
    return extract_characters

def left_texts(keyword, text, occurrence='all'):
    keyword = str(keyword).lower()
    text = text.lower()
    left_part = []
    positions = tkeypos(keyword, text)
    for i in range(len(positions)):
        left_part.append(text[:positions[i][0]])
    if occurrence == 'all':
        return left_part
    elif (occurrence <= 0) or (occurrence > len(positions)):
        return prRed("\t\t  Error: invalid occurrence")
    else:
        return left_part[occurrence - 1]

def right_texts(keyword, text, occurence='all'):
    keyword = str(keyword).lower()
    text = text.lower()
    right_part = []
    positions = tkeypos(keyword, text)
    for i in range(len(positions)):
        right_part.append(text[positions[i][1]:])
    if occurence == 'all':
        return right_part
    elif (occurence <= 0) or (occurence > len(positions)):
        return prRed("\t\t  Error: invalid occurrence")
    else:
        return right_part[occurence - 1]

def between_fixed_keyword(keyword, text):
    keyword = str(keyword).lower()
    text = text.lower()
    positions = tkeypos(keyword, text)
    texts = []
    for i in range(len(positions)):
        if i < len(positions) - 1:
            req_text = text[positions[i][1]:positions[i + 1][0]]
            texts.append(req_text)
        else:
            req_text = text[positions[i][1]:]
            texts.append(req_text)
    return texts

def between_distinct_keywords(keyword_start, keyword_end, text, keyword_start_occurence=1, keyword_end_occurence=1):
    keyword_start = str(keyword_start).lower()
    keyword_end = str(keyword_end).lower()
    text = text.lower()
    positions_ks = tkeypos(keyword_start, text)
    positions_ke = tkeypos(keyword_end, text)
    matches = []
    for i in range(len(positions_ks)):
        for j in range(len(positions_ke)):
            if positions_ks[i] < positions_ke[j]:
                match = text[positions_ks[i-1][1]:positions_ke[j-1][0]]
                matches.append((positions_ks[i-1][1],positions_ks[j-1][0],match))
    if (keyword_start_occurence > 0) and (keyword_end_occurence>0) and (keyword_start_occurence <= len(positions_ks)) and (keyword_end_occurence <= len(positions_ke)):
        req = text[positions_ks[keyword_start_occurence-1][1]:positions_ke[keyword_end_occurence-1][0]]
        return req.strip()
    else:
        return keyword_start + " keyword repeats " + str(len(positions_ks)) + " times and " + keyword_end + " keyword repeats " + str(len(positions_ke)) + " times. Change your occurence accordingly"


def text_keyword_remover(remover_list, text, replaced_by):
    textl = text.lower()
    pattern = re.compile('|'.join(map(re.escape, remover_list)))
    output = re.sub(pattern,replaced_by,textl)
    return textl

def dkeypos(keyword, dataframe):
    positions = []
    keyword = str(keyword).lower()
    for i in range(dataframe.shape[0]):
        for j in range(dataframe.shape[1]):
            if type(dataframe.iat[i, j]) == str:
                if keyword in dataframe.iat[i, j].lower():
                    positions.append((i, j))
    return positions

def dataframe_keyword_remover(remover_list, dataframe, replaced_by):
    pattern = '|'.join([r'{}'.format(w) for w in remover_list])
    output_df = dataframe.replace(pattern, replaced_by, regex=True)
    return output_df




