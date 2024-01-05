
def number_encryptor(num):
    enc_num=''
    num = str(num)
    for i in num:
        i = int(i)
        i = i+1
        i = str(i)
        enc_num+=i

    enc_num = int(enc_num)

    return f"Your Encrypted number is {enc_num}"


def number_decryptor(num):
    dec_num = ''
    num = str(num)
    for i in num:
        i = int(i)
        i = i-1
        i = str(i)
        dec_num+=i
    
    dec_num = int(dec_num)
    return f"Your Decrypted number is {dec_num}"




    


    