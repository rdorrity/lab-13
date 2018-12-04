# Lab 13
original = open('news.txt', 'r').read()  # News story from The Onion
# https://local.theonion.com/recruiter-saw-your-background-in-computer-science-and-t-1830772882
words_file = open('replacement.txt', 'r').read()
prompts_file = open('prompt.txt', 'r').read()



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


words = get_word_list(words_file)
prompts = get_word_list(prompts_file)
words_dict = dict(zip(words, prompts))
answer = mad_libs(original, words_dict)
print_nice(answer)
#print_nice(original)






