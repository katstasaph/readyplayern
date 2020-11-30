'''
automatically formats json entries for tracery
'''

while True:
    tracery_word = input("Enter your word: ")
    pos = input("Enter the part of speech: ")
    if (pos == "noun"):
        print(f"\"{tracery_word}_noun\": [\"{tracery_word}, #like_spackle# #{tracery_word}_similes#,\"]")
    elif (pos == "verb"):
        print(f"\"{tracery_word}_verb\": [\"{tracery_word}, #like_spackle# #{tracery_word}_similes#,\"]")
    elif (pos == "adj"):
        print(f"\"{tracery_word}_adj\": [\"{tracery_word}, #like_spackle# #{tracery_word}_similes#,\"]")
    elif (pos == "number"):
        tracery_word = int(tracery_word)
        print(f"\"{tracery_word}\": [\"#{tracery_word}_vary# (one more than the number of #{tracery_word - 1}_number#)\", \"#{tracery_word}_vary# (one more than #{tracery_word - 1}_sc#)\", \"#{tracery_word}_vary# (one less than the number of #{tracery_word + 1}_number#)\", \"#{tracery_word}_vary# (one less than #{tracery_word + 1}_sc#)\", \"#{tracery_word}_vary# (also the number of #{tracery_word}_number#)\", \"#{tracery_word}_vary# (also #{tracery_word}_sc#)\"]")
    usr_prompt = input("Input another word? y/n ")
    if (usr_prompt == "n"):
        break