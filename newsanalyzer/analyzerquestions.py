class q1():
    num_words = TextAnalyzer('https://www.webucator.com/how-to/william-henry-harrisons-inaugural-address.cfm', "url")
    print ("The number of words in Harrison's speech is: ", num_words.word_count)

class q2():
    least_common_letter = TextAnalyzer('pride-and-prejudice.txt', "path")
    letter = least_common_letter.char_distribution()
    print ("The least common letter in Pride and Prejudice is: ", least_common_letter._cchars[-1][0])

class q3():
    cwords = TextAnalyzer('pride-and-prejudice.txt', "path")
    common_words = cwords.common_words(minlen=11, maxlen=11)
    print("The most common word of 11 letters in P&P is: ", common_words[0][0])