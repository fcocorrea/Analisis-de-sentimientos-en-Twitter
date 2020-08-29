# Funciones para el modelamiento de texto

from collections import Counter
import spell
import re

acronyms = open("acronyms.txt", "r")
acronyms = [line.strip() for line in acronyms.readlines()]


def remove_symbols(sentence):
    """Función que elimina los simbolos de 
    una frase.
    
    input: cadena de texto (str)
    output: cadena de texto sin simbolos (str)
    """    
    new_text = re.sub(r'[^\w]', " ", sentence)
    return new_text

def remove_numers_out(sentence):
    """Eliminamos todos los números de una frase
    excepto aquellos que están dentro de un texto. 
    Esto es para evitar eliminar numeros de abreviaciones
    tales como J4F (just for fun) o J4U (just for you)
    
    input: cadena de texto (str)
    output: cadena de texto sin urls (str)
    """    
    word_replace = re.compile(r'([\d+](\w*)[\d+])|([\s](\d+)[\s])')
    new_text = re.sub(word_replace, " ", sentence)
    return new_text


def remove_url(sentence):
    """Elimina todas las páginas web de
    una string o sentencia de texto.
    
    input: cadena de texto (str)
    output: cadena de texto sin urls (str)
    """    
    try:
        word_replace = re.compile(r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*')
    except:
        pass
    new_text = re.sub(word_replace, " ", sentence)
    return new_text


def remove_short_words(sentence):
    """Elimina todas aquellas palabras que su
    contenido sea menor o igual a 2.
    
    input: cadena de texto (str)
    output: cadena de texto sin palabras pequeñas (str)    
    """
    new_text = ' '.join(word for word in sentence.split() if len(word)>2)
    return new_text


def replace_users(sentence):
    """Reemplaza a todos los usuarios de twitter, es decir, 
    que empiecen con @. Además elimina aquellas palabras que
    comienzan con el signo &, como &amp y &quot"""
    
    word_replace = re.compile(r'[@&#][A-Za-z0-9_]+')
    new_text = re.sub(word_replace, " ", sentence)
    return new_text.lower()

def remove_extra_vowels(sentence):
    """Reemplaza las palabras donde tengan más de tres vocales
    como por ejemplo loooove --> loove, sooooo --> soo
    Se realiza con dos y no con una, porque hay palabras como 
    sweet que tienen dos vocales. Luego la función autocorrect_words
    tomara estas palabras y las corregira, dado que no puede corregir
    palabras que tengan demasiadas sílavas, dejándolas igual.

    input: cadena de texto (str)
    output: cadena de texto sin muchas vocales (str)
    """

    word_replace = re.compile(r'[aeiou]{3,}')
    word_list = re.findall(word_replace, sentence)
    word_list.sort(key=lambda word_list:len(word_list),
        reverse=True)
    
    for i in word_list:
        sentence = sentence.replace(i, i[:2])
    return sentence

def replace_laugh(sentence):
    """Convierte todas las risas como hahaha, lololol en solo
    haha

    input: cadena de texto (str)
    output: cadena de texto dejando todas las risas como "haha"
    """

    word_replace = re.compile(r'\b(?:a*(?:ha)+h?|(?:l+o+)+l+)\b')
    new_text = re.sub(word_replace, "haha", sentence) # probar con hahah
    return new_text

def autocorrect_words(sentence):
    """Cambiar las palabras que están con errores ortograficos
    a través de la función spell. 

    input: cadena de texto (str)
    output: cadena de texto con errores ortográficos corregidos.
    """

    for word in sentence.split():
        if word not in acronyms and spell.P(word) == 0.0:
            sentence = sentence.replace(word, spell.correction(word))
    return sentence

def delete_unique_words(sentence, words):
    """Elimina las palabras que no se repiten a lo largo de todos 
    los tweets.
    
    input: cadena de texto (str) y las palabras únicas a eliminar.
    output: cadena de texto sin palabras únicas.
    dentro de todos los tweets
    """

    new_text = re.sub(words, " ", sentence)
    return new_text  


