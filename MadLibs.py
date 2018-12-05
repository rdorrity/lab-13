# Sara Kazemi and Ryan Dorrity
# CST 205
# Lab 13 - Madlibs
# WRITTEN AND TESTED IN PYTHON 3.7
# Modifies a short news story with user input madlibs style
# and prints the modified story to the terminal


original = open('news.txt', 'r').read()  # News story from The Onion
# https://local.theonion.com/recruiter-saw-your-background-in-computer-science-and-t-1830772882
words_file = open('replacement.txt', 'r').read()
prompts_file = open('prompt.txt', 'r').read()


# iterate through each character in a string
# if that character is a new line, we've found
# a target word/phrase, so add it to a list
# return that  list.
def get_word_list(words_to_replace):
    words = []
    psn = 0
    for char in words_to_replace:

        if char == "\n":
            found_psn = words_to_replace.find(char, psn)
            added = words_to_replace[psn:found_psn]
            words.append(added)
            psn = found_psn + 1
    return words

# given a text and a dictionary,
# look for each key within the text
# when found, prompt the user to enter input
# which is used to replace that key in the text
# a modified version of the text (with user's answers)
# is returned
def mad_libs(original, dictionary):
    temp = original
    for key in dictionary:
        if key in temp:
            new_phrase=""
            while len(new_phrase) < 1:
                new_phrase = input("Enter " + dictionary[key].lower() + "...").strip().upper()
                while (dictionary[key].lower().find("number") > 0 or dictionary[key].lower().find("year") > 0) \
                        and not new_phrase.isnumeric():
                    new_phrase = input("Enter a " + dictionary[key].lower() + "...").strip()

                temp = temp.replace(key, new_phrase)
    return temp

# At this point, everything is one LOOONG line
# Let's limit each line to about 100 characters
# to make it user readable.
def print_nice(text):
    count=0
    result=""
    for char in text:
        count+=1
        if count > 100 and char == " ":
            result=result+"\n"
            count = 0
        else:
            result=result+char
    print(result)


words = get_word_list(words_file) # make a list of all words that need to be replaced in the original story
prompts = get_word_list(prompts_file) # make a list of all the prompts for the user
words_dict = dict(zip(words, prompts)) # create a dictionary with the words to replace as keys and the prompts as values
answer = mad_libs(original, words_dict) # run the madlibs prompts and have user input answers
print_nice(answer) # print the modified story in a nice format.
#print_nice(original)






