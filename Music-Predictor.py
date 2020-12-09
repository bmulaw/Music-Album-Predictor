import math

def clean_text(txt):
    txt = txt.lower()
    remove_parts = ['.', ',', '?', '!', ';', ':', '"','(', ')', "'", '[',']', '{', '}']
    for words in txt:
        if words in remove_parts:
            txt = txt.replace(words,'')
    lst = txt.split()
    return lst

def stem(s):
    """ This function takes in a string and removes certain characters at the tail
            end of it to return the stem of the given string. It uses a while loop
            to double check that it does not miss removing multipe tail-end terms.
        input: s, a string
    """
    count = 0
    while count <2:
        if s[-3:] == 'ing' or s[-3:] == 'dom' or s[-3:] == 'ion' or s[-3:] == 'ity' or s[-3:] == 'nal':
            s = s.replace(s[-3:], '')
        elif s[-2:] == 'er' or s[-2:] == 'ic' or s[-2:] == 'ed' or s[-2:] == 'ie' or s[-2:] == 'ly':
            s = s[:len(s)-2]
        elif s[-1] == 's' or s[-1] == 'e' or s[-1] == 'y':
            if s[-2:] == "ee":
                s = s[:len(s)-2]
            else:
                s = s[:len(s)-1]
        count += 1
    return s

def compare_dictionaries(d1,d2):
    """ This function takes in two dictionaries and returns a calculated float number
            that represents the 'simialities score' of two dictionaries
        input:  d1, a dictionary
                d2, a dictionary
    """
    score = 0
    total = sum(d1.values())
    for similar in (d2):
        if similar in d1:
            average = (d1[similar]) / total
            score += d2[similar]* math.log(average)
        else:
            average = .5 / total
            score += d2[similar] * math.log(average)     
    return score  


class TextModel:
    """ main class for the project, TextModel, which uses Naive Bayes Theorem to measure similarities between texts """

    def __init__(self,model_name):
        """ Constructor to initialize the TextModel class """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.first_person = {}

    def __repr__(self):
        """Return a string representation of the TextModel."""
        s = 'text model name: ' + self.name +'\n'
        s+= '  number of words: ' + str(len(self.words)) +'\n'
        s+= '  number of word lengths: ' + str(len(self.word_lengths))+'\n'
        s+= '  number of stems: ' + str(len(self.stems)) +'\n'
        s+= '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s+= '  number of first person words: ' + str(len(self.first_person))
        return s

    def count_spaces(self,arrayStr):
        """ This is a helper method for sentence_len(), as it takes in a list of strings
                and counts the number of words in the list by counting the spaces, and 
                returns the int of words in given sentence
            input: s, a list of strings
        """
        counter = 1
        for i in range(len(arrayStr)):
            if arrayStr[i] == " ":
                counter += 1
        return counter
    
    def sentence_len(self,s):
        """ This is a method to count the length of sentences by splitting strings with
                sentence-ending punctuations into lists that will then count how many
                words are in those sentences using count_spaces() helper function.
            input: s, a string
        """
        all_sentences = s.replace('?', '.').replace('!', '.').replace('...', '$').split('. ')
        for sentence in all_sentences:
            for elem in range(len(sentence)):
                if sentence not in self.sentence_lengths:
                    spaces = self.count_spaces(sentence)
                    self.sentence_lengths[spaces] = 1
                else:
                    spaces = self.count_spaces(sentence)
                    self.sentence_lengths[(spaces)] += 1
                
    def stem_count(self, s):
        """ This method counts the amount of times each unique stems are listed via 
                the function stems()
            input: s, a string
        """
        s = clean_text(s)
        for i in range(len(s)):
            if len(s[i]) > 3:
                a = stem(s[i])
                if a not in self.stems:
                    self.stems[a] = 1
                else:
                    self.stems[a] += 1
            else:
                if s[i] not in self.stems:
                    self.stems[s[i]] = 1
                else:
                    self.stems[s[i]] += 1
    
    def point_of_view(self,s):
        """ This method will work on my fifth dictionary that I added in which it will
                count how many times first person point-of-view terms are used and
                iteratively update the count on the first_person dictionary.
            input, s: a string        
        """
        s = clean_text(s)
        first_person_terms = ["I","i", "me", "Me", "Us", "us", "we", "We"]
        for phrases in s:
            if phrases in first_person_terms:
                if phrases not in self.first_person:
                    self.first_person[phrases] = 1
                else:
                    self.first_person[phrases] += 1    
                    
    def add_string(self,s):
        """Analyzes the string txt and adds its pieces
            to all of the dictionaries in this text model. """
        self.stem_count(s)
        self.sentence_len(s)
        self.point_of_view(s)
        word_list = clean_text(s)
        for w in word_list:
            if w not in self.words:
                self.words[w] = 1
                if len(w) not in self.word_lengths:                 
                    self.word_lengths[len(w)] = 1
                else: 
                    self.word_lengths[len(w)] += 1
            else:
                self.words[w] += 1
                if len(w) not in self.word_lengths:                 
                    self.word_lengths[len(w)] = 1
                else: 
                    self.word_lengths[len(w)] += 1

    def add_file(self, filename):
        """ This method initializes the opening of a file to add its strings 
                to the Class to be read and analyzed (i.e. word counts and word_lengths
            input: filename, a file
        """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        text = f.read()
        f.close()
        self.add_string(text)
        
    def save_model(self):
        """ This method takes in (not as a parameter however) a file and saves it
                as a dictionary """
        # file for word counts
        file_words = self.name + '_words'
        f = open(file_words, 'w')
        f.write(str(self.words))
        f.close()
        # file for word lengths
        file_length = self.name + '_word_lengths'
        l = open(file_length,'w')
        l.write(str(self.word_lengths))
        l.close()
        # file for stems
        file_stem = self.name + '_word_stems'
        s = open(file_stem,'w')
        s.write(str(self.stems))
        s.close()
        # file for sentence length
        file_sent_length = self.name + '_sentence_lengths'
        sl = open(file_sent_length,'w')
        sl.write(str(self.sentence_lengths))
        sl.close()
        # file for first person
        file_first_person = self.name + '_first_person'
        fp = open(file_first_person,'w')
        fp.write(str(self.first_person))
        fp.close()

    def read_model(self):
        """ This method takes in (not as a parameter however) a dictionary file,
                reads its contents and allows the Class to print out its analysis 
                of the contents. """
        # file to read word counts
        author_words = open(self.name+'_words', 'r')
        words_str = author_words.read()
        author_words.close()
        word_dict = dict(eval(words_str))
        self.words = word_dict
        # file to read word lengths
        author_len = open(self.name+'_word_lengths', 'r')
        len_str = author_len.read()
        author_len.close()
        len_dict = dict(eval(len_str))
        self.word_lengths = len_dict
        # file to read stems
        author_stem = open(self.name+'_word_stems', 'r')
        stem_str = author_stem.read()
        author_stem.close()
        stem_dict = dict(eval(stem_str))
        self.stems = stem_dict
        # file to read sentence lengths
        author_sent_len = open(self.name+'_sentence_lengths', 'r')
        sent_len_str = author_sent_len.read()
        author_sent_len.close()
        sent_len_dict = dict(eval(sent_len_str))
        self.sentence_lengths = sent_len_dict
        # file to read first person
        author_first_person = open(self.name+'_first_person', 'r')
        first_person_str = author_first_person.read()
        author_first_person.close()
        first_person_dict = dict(eval(first_person_str))
        self.first_person = first_person_dict


    def similarity_scores(self, other):
        """ This method compares the scores by using the compare_dictionary for
                each dictionary calculated between the two given files, and it returns
                a 2D list of all the scores for both files.
            input: other, a file containing strings
        """
        a = compare_dictionaries(other.words, self.words)
        b = compare_dictionaries(other.word_lengths, self.word_lengths)
        c = compare_dictionaries(other.stems, self.stems)
        d = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        e = compare_dictionaries(other.first_person, self.first_person)
        return [a,b,c,d,e]

    def classify(self, source1, source2):
        """ THis method takes in two files and compares the total scores of both files
                to a given text, and determines (by using most of the methods and function
                presented in this project) which of the two files are most closely
                similar to the given text.
            input:  source1, a file containing strings
                    source2, a file containing strings
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        weighted_sum1 = scores1[0] + scores1[1] + scores1[2] + scores1[3] + scores1[4] 
        weighted_sum2 = scores2[0] + scores2[1] + scores2[2] + scores2[3] + scores2[4]
        if weighted_sum1 > weighted_sum2:
            print("-> "+ str(self.name) + " is more likely to have come from " + str(source1.name))
        else:
            print("-> "+str(self.name) + " is more likely to have come from " + str(source2.name))
            
   
"""
def tests():
    source1 = TextModel("Chanel Orange")
    source1.add_file('orange.txt')

    source2 = TextModel("Blonde")
    source2.add_file('blonde.txt')
    
    new0 = TextModel("Russ's Losin' Control")
    new0.add_file('russ_losingcontrol.txt')
    new0.classify(source1, source2)    

    new1 = TextModel("Pryamid")
    new1.add_file('pyramid.txt')
    new1.classify(source1, source2)
    
    new2 = TextModel("Nigths")
    new2.add_file('nights.txt')
    new2.classify(source1, source2)

    new3 = TextModel("Sierra Leone")
    new3.add_file('sierra_leone.txt')
    new3.classify(source1, source2)
    
    new4 = TextModel("Bryson Tiller's Trap Soul")
    new4.add_file('trapsoul_tiller.txt')
    new4.classify(source1, source2)

tests() 
"""


# Feel free to download the txt files from my github and run these tests! Also, make sure to input the appropriate names of the .txt files that you would like to test.








