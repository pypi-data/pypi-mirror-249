# Ussy
Being human, we've all come across this familiar issue before.

*There are just so many words in the English language to ussify! How can I possibly cope with ussifying them all?*

With this pervasive problem in mind, I've created the Ussy module, a Python package dedicated to solving all of your ussification needs.

This module algorithmically ussifies words by estimating a word's phonemic sequence, and popping phonemes from the end of the word until a plosive consonant is reached. If a suitable plosive consonant is identified, "ussy" is appended to the remained grapheme sequence and returned.

# Usage

    from ussy.ussify import Ussy
    
    ussy = Ussy()
    ussified = ussy.ussify("raspberry")
    print(ussified)
    
    "raspberrussy"


## Ussy.ussify(word, plural)

`string word`: alphabetic English word string to be ussified

`boolean plural`: true if ussified word is plural, default false if singular

returns false if given string is unussifiable, or ussified string otherwise

