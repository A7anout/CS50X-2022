from cs50 import get_string
# my variables
letters = 0
spaces = 0
words = 0
sentences = 0
# getting input (text) from the user
text = get_string("Text: ")

for i in range(len(text)):
    if text[i].isupper() or text[i].islower():  # for letters
        letters += 1
    elif text[i] == " ":  # for words
        spaces += 1
        words = spaces + 1
    elif text[i] == '.' or text[i] == '!' or text[i] == '?':
        sentences += 1

L = letters / words * 100
S = sentences / words * 100
index = 0.0588 * L - 0.296 * S - 15.8
grade = round(index)

if index < 1:
    print("Before Grade 1")
elif index > 1 and index < 16:
    print(f"Grade {grade}")
elif index > 16:
    print("Grade 16+")