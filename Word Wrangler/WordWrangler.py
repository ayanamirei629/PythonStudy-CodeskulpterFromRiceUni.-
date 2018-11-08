"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    temp_list = list(list1)
    end = False
    num = 0
    while not end:
        if num + 2 > len(temp_list):
            end = True
        else:            
            while num + 2 <= len(temp_list) and temp_list[num] == temp_list[num + 1] :
                temp_list.pop(num + 1)
            num += 1
    new_list = temp_list    
    return new_list


def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    temp_list1 = list(list1)
    temp_list2 = list(list2)
    new_list = []
    end = False
    num = 0
    while not end:
        if num == len(temp_list1) or len(temp_list2) == 0:
            end = True
        else:
            while temp_list1[num] > temp_list2[0] and len(temp_list2) > 0:
                temp_list2.pop(0)
            if temp_list1[num] == temp_list2[0]:
                temp_list2.pop(0)
                new_list.append(temp_list1[num])
            else:
                num += 1
    return new_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """   
    temp_list1 = list(list1)
    temp_list2 = list(list2)
    new_list = []
    end = False
    #CHECK THE FIRST ELEMENT IN EACH LIST EVERYTIME THE LOOP BEGIN, IF LENGTH OF LIST GREATER THAN 1, POP THE 
    #ELEMENT, THEN WE CAN FIGURE OUT THE NEW ELEMENT ON THE LIST, IF LENGTH OF LIST EQUAL 1, LOOP FINISHED,
    #ADDING THE REMAIN PART OF OTHER LIST 
    if list1 == [] and len(list2) > 0 :
        return list2
    elif list2 == [] and len(list1) > 0:
        return list1
    elif list2 == [] and list1 == []:
        return []    
    while not end:
        while temp_list1[0] > temp_list2[0] and not end:
            new_list.append(temp_list2[0])
            if len(temp_list2) > 1:
                temp_list2.pop(0)
            else:
                new_list.extend(temp_list1)
                end = True
        while temp_list1[0] <= temp_list2[0] and not end:
            new_list.append(temp_list1[0])
            if len(temp_list1) > 1:
                temp_list1.pop(0)
            else:
                new_list.extend(temp_list2)
                end = True
    return new_list

                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if list1 == []:
        return list1
    else:
        pivot = list1[0]
        lesser = [num for num in list1 if num < pivot]
        pivots = [num for num in list1 if num == pivot]
        greater = [num for num in list1 if num > pivot]
        return merge_sort(lesser) + pivots + merge_sort(greater)
    
    

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
        return ['']
    
    first = word[0]
    rest = word[1:]
    temp = []
    rest_strings = gen_all_strings(rest)
    for string in rest_strings:
        for num in range(len(string)+1):
            temp.append(string[:num] + first + string[num:])
    return rest_strings + temp


# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    return []

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()

    
    