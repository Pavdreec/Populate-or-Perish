import json
import requests
import re
from word_segmentation import segment

search_term ='migration'  # mandatory element
newspaper_id ='809' # 809 for The Age
year ='1936'        #
number ='10'       # arbitrary value
next_start = '*'    # '*' required in the program

def remove_spans(article):
    article = article.replace('<span> ','')
    article = article.replace('</span> ','')
    article = article.replace('<span>','')
    article = article.replace('</span>','')
    article = article.replace('<p> ','')
    article = article.replace('</p> ','')
    article = article.replace('<p>','')
    article = article.replace('</p>','')
    return article

def find_punctuation (word):
    punctuation_list = ['.', ',', '!', '?']
    punctuation_index = max([word.find(punctuation) for punctuation in punctuation_list])
    str = ' '
    if punctuation_index == -1:
        return str.join(segment(word[0: len(word)]))
    return find_punctuation(word[0:punctuation_index]) + word[punctuation_index] + ' ' + str.join(segment(word[punctuation_index + 1: len(word)]))


def correct_segmentation (article):
    corrected_article = ''
    for word in article.split():
        apostroph_index = word.find('\'')
        if apostroph_index != -1:
            corrected_article = corrected_article + find_punctuation(word[0 : apostroph_index]) + '\'' + find_punctuation(word[apostroph_index + 1: len(word)]) + ' '
        else:
            corrected_article = corrected_article + find_punctuation(word) + ' '

    return corrected_article

while next_start:
    url = 'https://api.trove.nla.gov.au/v2/result?key=cu6itqnfsrluofve&zone=newspaper&q='+ search_term + '&l-title=' + newspaper_id + '&l-year=' + year + '&l-category=Article&n=' + number + '&include=articletext&encoding=json&s=' + next_start
    resp = requests.get(url)
    json_data = resp.json()

    #print(json_data['response']['zone'][0]['records'])

    if 'nextStart' in json_data['response']['zone'][0]['records']:
        next_start = json_data['response']['zone'][0]['records']['nextStart']
    else:
        next_start = ''

    print(next_start)
    for counter in range(int(json_data['response']['zone'][0]['records']['n'])):
        identifier = json_data['response']['zone'][0]['records']['article'][counter]['id'] + ".txt"
        date = json_data['response']['zone'][0]['records']['article'][counter]['date']
        article = json_data['response']['zone'][0]['records']['article'][counter]['articleText']
        file1 = open('/Users/pavdreec/Documents/MASTERproef/Articles/' + date + '_' + identifier,"w")
        article = remove_spans(article)
        article = correct_segmentation(article)
        file1.write(article)
        file1.close()



