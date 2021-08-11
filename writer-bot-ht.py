'''File Name: writer-bot-ht.py
   Author: Longxin Li
   Purpose: this program will print out the random lyrics
            that follow the Markov chain analysis, and
            each line has ten words.
   CS120'''
import random  # import the random.
SEED = 8
NONWORD = '@'
random.seed(SEED)  # set the random seed.

class Hashtable:
    def __init__(self, size):
        '''Initializes the object with information
        extracted from line.
        Parameters: size is the size of the hashtable.
        Returns: None.
        Pre-condition: size is an integer.
        Post-condition: None.'''
        self._size = size
        self._pair = [None] * size

    def _hash(self, key):
        '''The method to calc the index of the key.
        Parameters: key is a the pair of the words.
        Returns: The index of the key.
        Pre-condition: key is a string.
        Post-condition: index is an integer.'''
        p = 0
        for c in key:
            p = 31 * p + ord(c)
        return p % self._size

    def put(self, key, value):
        '''To put the key and value into the hashtable.
        Parameters: key is a the pair of the words, value is
                    the next words behind key.
        Returns: None.
        Pre-condition: key is a string, value is a list.
        Post-condition: None.'''
        hash_value = self._hash(key)
        flag = True
        if self._pair[hash_value] is None:
            self._pair[hash_value] = [key, [value]]
        else:
            while self._pair[hash_value] is not None:
                if self._pair[hash_value][0] == key:
                    self._pair[hash_value][1].append(value)
                    flag = False
                    break
                hash_value -= 1
            if flag:
                self._pair[hash_value] = [key, [value]]

    def get(self, key):
        '''To find if the key is available in the hashtable.
        Parameters: key is a the pair of the words.
        Returns: The value of the key or None.
        Pre-condition: key is a string.
        Post-condition: string or None.'''
        index1 = self._hash(key)
        for i in range(self._size):
            if self._pair[index1] is None:
                return None
            elif self._pair[index1][0] ==key:
                return self._pair[index1][1]
            index1-=1
            if index1==-1:
                index1=self._size-1
        return None

    def __contains__(self, key):
        '''To find if the key is in the hashtable.
        Parameters: key is a the pair of the words.
        Returns: True or False.
        Pre-condition: key is a string.
        Post-condition: True or None.'''
        return self.get(key) is None

    def __str__(self):
        '''This function is to just return the
        attributes of the each class.
        Parameters: None.
        Returns: The attributes of the each class.
        Pre-condition: None.
        Post-condition: String.'''
        return str(self._pair)


def enter():
    '''Ask user to input the name of the lyrics, the
        size for prefix in Markov chain analysis, and how
        many words user wants to print out.
    Parameters: None.
    Returns: source_txt is the txt name for the lyrics.
             prefix_size is the size for prefix in Markov chain
             analysis, random_size is number of the words user
             wants to print out.
    Pre-condition: None.
    Post-condition: source_txt is a string, prefix_size
                    and random_size are all int'''
    source_txt = input()
    table_size = int(input())
    prefix_size = int(input())
    if prefix_size < 1:
        print('ERROR: specified prefix size is less than one')
        exit()
    random_size = int(input())
    if random_size < 1:
        print('ERROR: specified size of the generated text is less than one')
        exit()
    return source_txt, prefix_size, random_size, table_size


def readfile(source_txt, prefix_size):
    '''Go through the lyrics and stored it in to a list.
    Parameters: source_txt is the txt name for the lyrics. prefix_size
                is the size for prefix in Markov chain analysis.
    Returns: list1 is a list that sotred the lyrics word by
             word, stored is a tuple that stored NONWORD as
             first word's prefix.
    Pre-condition: source_txt is a string, prefix_size is int.
    Post-condition: list1 is a list, stored is a tuple.'''
    list1 = []

    for i in range(prefix_size):
        list1.append(NONWORD)  # create the empty for first word's prefix.
    key=' '.join(list1)
    open_file = open(source_txt)  # open the file.
    for line in open_file:
        line = line.strip('/n').strip(' ').split()  # split every word by space.
        for word in line:
            list1.append(word)  # store the words orderly.
    return list1,key


def store(list1, prefix_size, hash):
    '''Store the data from the lyrics into a dictionary, prefix is key
       and values will be the word behind key. The text generation
       continues until the last suffix is reached, or until a sufficient
       amount of text has been generated.
    Parameters: list1 is a list that sotred the lyrics word by
             word, prefix_size is the size for prefix in Markov chain
             analysis.
    Returns: dict1 is a dictionary that stord the lyrics data.
    Pre-condition: list1 is a list, prefix_size is int.
    Post-condition: dict1 is a dictionary'''
    key1 = tuple(list1)  # make list1 hasable, and will save as tuple.
    for i in range(len(list1) - prefix_size):
        key = ' '.join(key1[i:prefix_size + i])
        value = list1[i + prefix_size]
        hash.put(key, value)

def output(hash, random_size, key):
    '''Find all the words that should print out folllow the Markov chain
       analysis and store that word by word into a list.
    Parameters: dict1 is a dictionary that stord the lyrics data,
                random_size is number of the words user wants to print out.
                stored is a tuple that stored NONWORD as first word's prefix.
    Returns: output_list is a list that with all the words should print out.
    Pre-condition: dict1 is a dictionary, random_size is int, stored is a
                   tuple.
    Post-condition: output_list is a list'''
    output_list = []
    while len(output_list) < random_size: #length need same with random_size.

        values = hash.get(key)
        if values is None:
            break
        if len(values) > 1: #ckeck if there has more than one values.
            loca = random.randint(0,len(values)-1)
            value = values[loca] #get 'random' value folllow the seed.
        else:
            value = values[0]
        output_list.append(value)
        key = key.split(' ')+[value] #change key to next one.
        key=' '.join(key[1:])
    return output_list

def printout(output_list):
    '''Check the nomber of words each line, make sure every line at most has
       ten words, then print out those words every line with ten words.
    Parameters: output_list is a list that with all the words should print
                out.
    Returns: The random lyrics folllow the Markov chain analysis.
    Pre-condition: output_list is a list.
    Post-condition: The output are many strings'''
    out_list = []
    number1 = 0
    number2 = 10  # max words for each line is 10.
    for times in range(len(output_list)):
        data = []
        data.append(output_list[number1:number2])  # find words in each line.
        out_list.append(data[0])
        number1 += 10
        number2 += 10  # move to next ten words.
        if output_list[number1:number2] == []:
            break  # if run over all the words, stop.
    for i in out_list:
        print(' '.join(i))  # put all word togeter, space between two words.

def main():
    source_txt, prefix_size, random_size, table_size = enter()
    list1,key= readfile(source_txt, prefix_size)
    hash = Hashtable(table_size)
    store(list1, prefix_size, hash)
    result=output(hash, random_size, key)
    printout(result)

main()


