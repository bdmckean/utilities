import random
import sys

def gen_password(pw_len=8):
    letters = "abcdefghijklmnopqrstuvwxyz"
    symbols = '!@'
    mypw = ""

    for i in range(pw_len):
        next_index = random.randrange(len(letters))
        mypw = mypw + letters[next_index]

    # replace 1 or 2 characters with a number
    for i in range(random.randrange(1,3)):
        replace_index = random.randrange(len(mypw)//2)
        mypw = mypw[0:replace_index] + str(random.randrange(10)) + mypw[replace_index+1:]

    # replace 1 or 2 letters with an uppercase letter
    for i in range(random.randrange(1,3)):
        replace_index = random.randrange(len(mypw)//2,len(mypw))
        mypw = mypw[0:replace_index] + mypw[replace_index].upper() + mypw[replace_index+1:]

    # replace a letter with a symbol
    replace_index = random.randrange(len(mypw)//2,len(mypw))
    symbol = symbols[random.randrange(2)]   
    mypw = mypw[0:replace_index] + symbol + mypw[replace_index+1:]  

    return(mypw)

if __name__ == '__main__':
    pw_len = 8
    if len(sys.argv) > 1:
        pw_len = int(sys.argv[1])
    pw = gen_password(pw_len)
    print (pw)
