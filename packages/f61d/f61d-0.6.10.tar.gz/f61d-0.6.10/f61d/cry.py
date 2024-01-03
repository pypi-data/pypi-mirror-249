def decfence(s,n):
    '''
    Decrypts a string that has been encoded using the Rail Fence Cipher.

    Args:
        s (str): The encoded string to be decrypted.
        n (int): The number of rails or lines used in the Rail Fence Cipher.

    Returns:
        str: The decrypted original string.

    Example:
        >>> decfence('HlWleoodl_r',3)
        'Hello_World'
    '''
    from math import ceil
    row = ceil(len(s)/n)
    n_of_c = (len(s)-1)%n + 1
    T = [[0]*n for i in range(row)]
    r = ''
    ind = 0
    for i in range(n):
        if i >= n_of_c:
            for j in range(row-1):
                # print(j,i,s[ind])
                T[j][i] = s[ind]
                ind += 1
        else:
            for j in range(row):
                # print(j,i,s[ind])
                T[j][i] = s[ind]
                ind += 1
    # print('\n'.join([''.join([j for j in i if j != 0]) for i in T]))
    r = ''.join([''.join([j for j in i if j != 0]) for i in T])
    return r

def encfence(s,n):
    '''
    Encrypts a string using the Rail Fence Cipher.

    Args:
        s (str): The string to be encrypted.
        n (int): The number of rails or lines to be used in the Rail Fence Cipher.

    Returns:
        str: The encrypted string.

    Example:
        >>> encfence('Hello_World',3)
        Hel
        lo_
        Wor
        ld
        'HlWleoodl_r'
    '''
    l = [s[i*n:i*n+n] for i in range(len(s)//n)]
    if ''.join(l) != s:
        l.append(s[-(len(s) - n*len(l)):])
    r = ''
    print('\n'.join(l))
    for i in range(n):
        for j in l:
            try:
                r += j[i]
            except:
                pass
    return r
