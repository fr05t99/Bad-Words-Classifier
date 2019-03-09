import re
from typing import Tuple


class TrieNode(object):
    """
    Our trie node implementation. Very basic. but does the job
    """
    
    def __init__(self, char: str):
        self.char = char
        self.children = []
        # Is it the last character of the word.`
        self.word_finished = False
        # How many times this character appeared in the addition process
        self.counter = 1
    

def add(root, word: str):
    """
    Adding a word in the trie structure
    """
    node = root
    for char in word:
        found_in_child = False
        # Search for the character in the children of the present `node`
        for child in node.children:
            if child.char == char:
                # We found it, increase the counter by 1 to keep track that another
                # word has it as well
                child.counter += 1
                # And point the node to the child that contains this char
                node = child
                found_in_child = True
                break
        # We did not find it so add a new chlid
        if not found_in_child:
            new_node = TrieNode(char)
            node.children.append(new_node)
            # And then point node to the new child
            node = new_node
    # Everything finished. Mark it as the end of a word.
    node.word_finished = True


def find_prefix(root, prefix: str) -> Tuple[bool, int]:
    """
    Check and return 
      1. If the prefix exsists in any of the words we added so far
      2. If yes then how may words actually have the prefix
    """
    node = root
    # If the root node has no children, then return False.
    # Because it means we are trying to search in an empty trie
    if not root.children:
        return False, 0
    for char in prefix:
        char_not_found = True
        # Search through all the children of the present `node`
        for child in node.children:
            if child.char == char:
                # We found the char existing in the child.
                char_not_found = False
                # Assign node as the child containing the char and break
                node = child
                break
        # Return False anyway when we did not find a char.
        if char_not_found:
            return False, 0
    # Well, we are here means we have found the prefix. Return true to indicate that
    # And also the counter of the last node. This indicates how many words have this
    # prefix
    return True, node.counter

if __name__ == "__main__":
    root = TrieNode('*')
    outputFile = open("output.txt", "w")
    #read paragraph from the file
    inputFile = open("input.txt", "r")
    text = inputFile.read()

    #read bad words from the file
    badWordfile = open("badwords.txt", "r")
    badWords = []
    for badWord in badWordfile:
        badWords.append(badWord.rstrip())

    #separate paragraph
    text = re.findall(r"[\w]+", text)
    #print(text)
    #Ensure that all words are in English
    inEnglish = True
    #Loading our dictionary
    with open("dictionary.txt") as word_file:
        english_words = set(word.strip().lower() for word in word_file)
    for i in range(len(text)):
        text[i] = text[i].lower()
    for word in text:
        if word not in english_words:
            inEnglish = False
            
    #print(badWords)     

    if inEnglish:
        #insert paragraph in trie
        for word in text:
            add(root, word)
        
        numberOfBadWords = 0
        for badWord in badWords:
            temp = find_prefix(root, badWord)
            numberOfBadWords += temp[1]

        if numberOfBadWords == 0:
            outputFile.write("No bad words")
            #print("1")
        else:
            outputFile.write("Has " + str(numberOfBadWords) + " bad words")
            #print("2")
            
    else:
        outputFile.write("Not in English")
        #print("3")
    outputFile.close()
        
