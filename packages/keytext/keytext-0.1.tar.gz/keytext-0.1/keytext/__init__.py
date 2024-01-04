import re
import pandas as pd


def neighbourhood_words(keyword, text, left, right):
    text = text.upper()
    keyword = keyword.upper()
    text_pieces = text.split(keyword)

    if len(text_pieces) == 1:
        return None

    split_words = [piece.split() for piece in text_pieces]
    occurences = []

    for index in range(len(split_words) - 1):
        left_words = split_words[index][len(split_words[index]) - left:]
        right_words = split_words[index + 1][0: right]
        surrounded_text = " ".join(left_words + [keyword] + right_words)
        occurences.append(surrounded_text)

    return occurences


def prRed(skk): print("\033[31m{}\033[00m" .format(skk))


def left_texts(keyword, text, occurence):
    left_part = []
    positions = keyword_position(keyword, text)
    for i in range(len(positions)):
        left_part.append(text[:positions[i][0]])
    if occurence == all:
        return left_part
    elif (occurence <= 0) or (occurence > len(positions)):
        return prRed("\t\t  Error: invalid occurence")
    else:
        return left_part[occurence-1]
    

def right_texts(keyword, text, occurence):
    right_part = []
    positions = keyword_position(keyword, text)
    for i in range(len(positions)):
        right_part.append(text[positions[i][1]:])
    if occurence == all:
        return right_part
    elif (occurence <= 0) or (occurence > len(positions)):
        return prRed("\t\t  Error: invalid occurence")
    else:
        return right_part[occurence-1]


def between_fixed_keyword(keyword, text):
    text = text.upper()
    keyword = keyword.upper()
    positions = keyword_position(keyword, text)
    texts = []
    for i in range(len(positions)):
        if i < len(positions)-1:
            req_text = text[positions[i][1]:positions[i+1][0]]
            texts.append(req_text)
        else:
            req_text = text[positions[i][1]:]
            texts.append(req_text)
    return texts


def keyword_position(keyword, text):
    keyword = keyword.upper()
    text = text.upper()
    key = re.finditer(keyword, text)
    pos_start_end = [(match.start(),match.end()) for match in key]
    return pos_start_end


def neighbourhood_chr(keyword, text, left_chr, right_chr):
    keyword = keyword.upper()
    text = text.upper()
    key = re.finditer(keyword, text)
    pos_start_end = [(match.start(),match.end()) for match in key]
    need = []
    for pos in pos_start_end:
        user_need = text[pos[0]-left_chr : pos[1]+right_chr]
        need.append(user_need)
    return need


def dataframe_keyword_remover(remover_list, dataframe, replaced_by):
    pattern = '|'.join([r'{}'.format(w) for w in remover_list])
    output_df = dataframe.replace(pattern, replaced_by, regex=True)
    return output_df


def dataframe_pattern_finder(pattern, dataframe):
    all_pattern = []
    for i in range(dataframe.shape[0]):
        for j in range(dataframe.shape[1]):
            if type(dataframe.iat[i,j]) == str:
                search = re.findall(pattern, dataframe.iat[i,j])
                if len(search) > 0:
                    all_pattern.append(search)
    return all_pattern


def text_keyword_remover(remover_list, text, replaced_by):
    pattern = re.compile('|'.join(map(re.escape, remover_list)))
    output = pattern.sub(replaced_by, text)
    return output


def get_freq(text, base):

    if base == 'chr':
        frequency_dictionary = {}
        for key in text:
            if key in frequency_dictionary:
                frequency_dictionary[key] = frequency_dictionary[key] + 1
            else:
                frequency_dictionary[key] = 1
        
        output_tabular_format = pd.DataFrame.from_dict(frequency_dictionary, orient ='index')
        output_tabular_format = output_tabular_format.reset_index().rename({'index': 'charecter', 0: 'frequency'}, axis='columns')
        return output_tabular_format          
    
    elif base == 'word':
        remover_list = ['`', '~', '!', '@', '#', '$', '%', '^', '&', "*", '(', ')', '_', '-', '+', '=', '{', '}', '[', ']', '|', ':', ';', '"', '<', '>', '?', ',', '.', '/']
        text = text_keyword_remover(remover_list, text, '')
        text = text.split()
        frequency_dictionary = {}
        for key in text:
            if key in frequency_dictionary:
                frequency_dictionary[key] = frequency_dictionary[key] + 1
            else:
                frequency_dictionary[key] = 1

        output_tabular_format = pd.DataFrame.from_dict(frequency_dictionary, orient ='index')
        output_tabular_format = output_tabular_format.reset_index().rename({'index': 'word', 0: 'frequency'}, axis='columns')
        return output_tabular_format
        
    else:
        pass




