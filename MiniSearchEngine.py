import os
import re


# This class for read from file. For each word with file name
class listnode:

    def __init__(self, word, filename):
        self.word = word
        self.filename = filename


# This is trie node class.
class Node:

    def __init__(self, char):
        # Each node has a character
        self.char = char
        self.parent = None
        # 36 alphanum character
        # 36 means that 26 alphabetic and 10 numeric character
        self.children = [None] * 36
        self.isEndOfWord = False
        # includingFiles includes file names that has this word.
        # For example a -> r -> a -> b -> a , and "araba" is word of Filex then...
        # last a's includingfiles.append("File_name").
        self.includingfiles = list()
        # patternfiles ->> a -> r -> a -> b -> a, for each character patternfiles.append("File_name")
        # for a, ar ,ara, arab, araba
        self.patternfiles = list()
        # positions of desired word, for each file
        self.occurencewords = {}


class Trie:
    # Constructor with root node without character
    def __init__(self, root):
        self.root = root

    # char a=0th index
    # char z=25th index
    # char 0=26th index
    # char 9=35th index
    def charToIndex(self, char):
        if str.isalpha(char):
            return ord(char) - ord('a')
        if str.isdigit(char):
            return ord(char) - 22

    # insert each word to trie
    def insert(self, word, filename, position):
        temp = self.root
        # word read from file
        for char in word:
            #             O -root       each node has maximum 36 children because there is 36 alphanum character
            #           / | \           for example ara - ars - hi - mo these are words
            #          /  |  \          If we think for root, it has 3 children. Rest of 33 index set to None.
            #         a   h   m
            #        /    |    \
            #        r    i     o
            #       / \
            #      a   s

            childIndex = self.charToIndex(char)
            # it means that we have to create this node
            if temp.children[childIndex] is None:
                temp.children[childIndex] = Node(char)  # create new trie node
                temp.children[childIndex].parent = temp  # indicate parent reference
            # this pattern exists in this file
            self.onlyifnotinthelist(temp.children[childIndex].patternfiles, filename[0])

            # if dict has no key named as filename, then create new key with list value
            # after, we will add this key to positions of desired word
            try:
                if temp.children[childIndex].occurencewords[filename[0]] is None:
                    print()
            except:
                temp.children[childIndex].occurencewords[filename[0]] = list()

            # append new position to value of filename's key
            # for example, { "file1",[0, 12 ,48] } 0, 12 and 48 are positions of desired word
            temp.children[childIndex].occurencewords[filename[0]].append(position + 1)
            # move on trie
            temp = temp.children[childIndex]
        # if this word exists in this file than add this filename to this node's includingfiles
        self.onlyifnotinthelist(temp.includingfiles, filename[0])

        temp.isEndOfWord = True

    # if the word exists in trie then return true
    def search(self, word):
        # to lower character
        word = word.lower()
        temp = self.root
        for char in word:
            childIndex = self.charToIndex(char)
            # for example, we search "araba"
            # root -> a -> r -> --- but node r has no child that is a
            # then we understand that this word does not exists in the trie
            if temp.children[childIndex] is None:
                return False
            else:
                temp = temp.children[childIndex]
        # we search "ara". "ara" is part of "araba" bu if it is not end of word then return false
        return temp.isEndOfWord

    # if this pattern exists in trie return true with positions
    def startingwith(self, pattern):
        pattern = pattern.lower()

        temp = self.root
        for char in pattern:

            childIndex = self.charToIndex(char)
            if temp.children[childIndex] is None:
                print("There is no such a word in these files!")
                return False
            else:
                temp = temp.children[childIndex]

        self.printstartingwordswithposition(temp.occurencewords)

        # print(temp.patternfiles)
        return True

    # it prints files that has words that starting with given pattern and its positions
    def printstartingwordswithposition(self, occurencewords):
        positions = ""
        for i in occurencewords.keys():
            print(i)
            for b in occurencewords[i]:
                positions += str(b)+" "
            print(positions)
            positions=""

    # this method finds common words in given files
    def commonwords(self, itr, files, toparent):

        if itr is None:
            return
        # it traverse all 36 children of node except None ones.
        for i in range(36):
            # move on trie
            self.commonwords(itr.children[i], files, toparent)
            # a -> r -> a -> b -> a
            # itr = r , root = second a
            if itr.children[i] is not None:
                root = itr.children[i]
                # if second a is end of word and this node's includingfiles list includes all files given in parameter
                # assume that second a is end of word, and "ara" exists in file1, file5, file8, file9 and file10
                # if we search common words in file1 and file5
                # file1 and file5 exists in "ara" 's including filer, so that we can say that this word is common for...
                # given files.
                # all(elem in root.includingfiles for elem in files) function return true if and only if...
                # all elements in files exists in includingfiles list.
                if root.isEndOfWord == True and all(elem in root.includingfiles for elem in files):
                    # we reverse traversal on trie for capturing word.
                    # then we will reverse this words
                    temp = root
                    while temp.char != "":
                        toparent.append(temp.char)
                        temp = temp.parent
                    toparent.append("-")
                    # for example a b a r a - n o y m a k - r ı t
                    # words are tır, kamyon, araba
                    # we will traverse in list for capturing these.

    # we do not want to add same item to the list again
    def onlyifnotinthelist(self, list, element):
        if element not in list:
            list.append(element)


#
def read_file(wordlist):
    for root, dirs, files in os.walk('sampleTextFiles'):
        for file in files:
            # add words with filename
            # we want only alphanumeric characters
            # AGA BURADA ALPHANUMERIC METHODU GIBI BI SEY YAPMAK DAHA IYI
            # YAPABILIRSEN BAKARSIN
            wordlist.append(listnode(
                list(open(root + "/" + file, 'r').read().replace(',', '').replace('.', "").replace("'", "")
                     .replace('-', "").replace(';', "").lower().split()), file.split()))


if __name__ == '__main__':
    # input for common words, we want common words these exists in these file
    files = ["file1.txt", "file2.txt", "file3.txt", "file4.txt", "file5.txt"]
    wordlist = list()
    toparent = list()

    read_file(wordlist)

    root = Node("")
    trie = Trie(root)

    # We use enumerate function because of this function counts all words it traversed
    for obje in wordlist:
        for i, j in enumerate(obje.word):
            # we send word, its filename and positon of word to the insert method
            trie.insert(j, obje.filename, i)

    # return true if har exists in any files.
    # print(trie.search("har"))

    # it finds words starting with input.
    trie.startingwith("har")
    # it finds common words.
    # to parent is list for words. Then we will re-traverse on this list
    print()
    filenames = ""
    for i in files:
        filenames += str(i) + " "
    print("Common words in ", filenames, "are:")
    trie.commonwords(root, files, toparent)

    # for common words. re-traverse on list as described above
    toparent.reverse()
    common = ""
    for i in toparent:
        if i == '-':
            common += "\n"
        else:
            common += i

    print(common)
