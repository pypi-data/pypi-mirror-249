def encsimple(word, shift=5):
    '''
    Simple encryter. 
    Adds specified shift t ascii value of characters.
    Default shift is 5.
    '''
    encword = ''
    for x in word:
        encword += chr(ord(x) + shift)
    return encword

def enccomplex(word, key=0):
    '''
    This function encrypts a sentence using a key. 
    Default key is 0. The key can be any string or number.
    Recommended keys: 0, mother, father, brother, sister, child, God, animal, whitespace. Key cannot be an empty string.
    '''
    encword = ''
    shift = 12 
    keyhere = [x for x in str(key)]
    for i, x in enumerate(word):
        encword += chr(ord(x) - shift + (len(word)%(i+1)) + ord(keyhere[i%(len(keyhere))])%2 )
    return encword

def decsimple(word, shift=5):
    '''
    Simple decrypter. 
    Shift must be the same as the encryption shift. 
    Default shift is 5.
    '''
    encword = ''
    return encword.join(list(chr(ord(x) - shift) for x in word))

def deccomplex(word, key=0):
    '''
    This function dencrypts a sentence using a key. 
    The key must be identical to the encrypting key.
    '''
    shift = 12 
    keyhere = [x for x in str(key)]
    return ''.join(list(chr(ord(x) + shift - (len(word)%(i+1)) - ord(keyhere[i%(len(keyhere))])%2) for i, x in enumerate(word))) 
    