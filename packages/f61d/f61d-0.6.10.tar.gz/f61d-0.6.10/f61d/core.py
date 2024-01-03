from tqdm import tqdm,trange
from time import time as tm
import time
from random import randint,choice
# from os import *
import os
from termcolor import colored
import f61d.LOGO as LOGO
#from f61d.__version__ import *
from math import ceil
from f61d.setu import *


VERSION = (0,6.10)
VERSION = '.'.join(map(str, VERSION))

invert = lambda a,n:pow(a,-1,n)

print(colored(LOGO.randlogo()+' v'+VERSION+'\n\n',choice(['red','yellow','green'])))
print(colored("Welcome to F61D. Use Help() for help.",'green'))

help_cont = {}
help_cont[0] = 'Help     : See this help page.\n\t\t  '+colored('Help(0)','cyan')+colored(' for all functions.','green')
help_cont[1] = 'fuckStar : One Button to fuck Satellite'
help_cont[2] = 'timeit   : Take a time for your function.\n\t\t  Just add a '+colored('@timeit','cyan')+colored(' before you define the function','green')
help_cont[3] = 'paint    : Draw a Bing Dwen Dwen'
help_cont[4] = 'b64tofile: Decode base64 to a file'
help_cont[5] = 'prove    : Prove your self. Only support:\n\t\t  sha256(XXXX + abcdef) = aaabbb...'
help_cont[6] = 'Nim      : An interesting turtle game.'
help_cont[7] = 'getLogo  : Print the "F61D" LOGO.'
help_cont[8] = 'yinyang  : Draw the TaiJi.'
help_cont[9] = 'lifeGame : Play the Life Game'
help_cont[10] = 'Polynomial: from f61d.Polynomial2 import *'
help_cont[11] = 'gmgj    : Common Modulus Attack in RSA'
help_cont[12] = 'crt     : Chinese Remainder Theory'
help_cont[13] = 'mtank   : 幻影坦克 Mirage tank maker'
help_cont[14] = 'setu    : get a setu with your xp'
help_cont[15] = 'fast_setu: get a random setu'
help_cont[16] = 'parse_header: parse a header from Chrome'
help_cont[16] = 'date    : Date calculator, use \'python -m f61d.date\''
help_cont[17] = 'bc      : BlockChain functions (not finish)'

def formatNumber(x):
    if len(str(x)) == 1:
        return ' '+str(x)
    return str(x)

def Help(page=1,lines = 5):
    if type(page) != int or type(lines) != int:
        Help(1,10000)
        return print('Please input interger.')
    if page == 0:
        return Help(1,10000)
    maxPage = ceil(len(help_cont)/lines)#int((0.5+len(help_cont))/lines)+1
    if (page - 1) * lines >= len(help_cont):
        print(f'Page Error, check the number : [1,{maxPage}]')
        return
    print(colored(f"{'=-'*14}= ",'yellow')+"H E L P"+colored(f" {'=-'*14}=\n",'yellow'))
    for i in range(lines):
        try:
            n = i+lines*(page-1)
            ll = colored(help_cont[n],'green')
            print(f'   {formatNumber(n)} - '+ll)
        except:break
    print('\n'+colored(f"{'=-'*14}= ",'yellow')+f"page({page}/{maxPage})"+colored(f" {'=-'*14}=",'yellow'))
    if page < maxPage:print(colored(f'\t\t\thelp({page+1}) for next page','green'))


def fuckStar():
    '''
一键日卫星
'''
    print(' - 欢迎使用一键日卫星功能')
    print(' - 请输入要日的卫星编号(可在官网查询):',end='')
    num = input()
    while num == '':
        num = input('请重新输入：')

    bar = trange(randint(1000,2000))
    for i in bar:
        bar.set_description('Hacking:'+hex(int.from_bytes(urandom(4),'big'))[2:])
        for _ in range(66666):
            a = 1
            b = 1
            a,b = b,1
            a,b = (a+b)**2,(a-b)**2
    for i in range(3):
        print('.',end='')
        time.sleep(0.4)
    if randint(1,100) > 80 or num == 'CHY':
        for i in range(3):
            print(colored('.','green'),end='')
            time.sleep(0.4)
        print(colored('\n日卫星成功.','green'))    
    else:
        print(colored('\n日卫星失败，请重新尝试','red'))
    
def lifeGame():
    from f61d.lifeGame import game
    game()
    
def paint():
    from f61d.bingdwendwen import draw
    draw()
    
def b64tofile():
    '''
    Encode/Decode a file by Base64
    '''
    menu = '''
please choose mode (1/2):
    - 1. encode
        Base64 encode a file
    - 2. decode
        Base64 decode a file
'''
    mode = input(menu)
    f1 = input('input file name:')
    f2 = input('Output file name:')
    while mode not in ['1','2']:
        mode = input('Please choose mode (1/2):')
    f = open(f1,'rb').read()
    from base64 import b64decode,b64encode
    if mode == '1':
        df = b64decode(f)
    elif mode == '2':
        df = b64encode(f)
    with open(f2,'wb') as ff:
        ff.write(df)


def Nim():
    from f61d.nim import game
    game()


def timeit(fun):
    '''
计算你的函数运行时间
'''
    def wrapper(*args,**kwargs):
        
        t1 = tm()
        ret = fun(*args,**kwargs)
        print(f'Function takes {tm() - t1}s')

        return ret
    
    return wrapper


def prove(cont,process_bar=True,show_description=False):
    '''
    Only the format is supported
    sha256(XXXX + {a}) = {b}
    Example:

    >>> r = remote("127.0.0.1",6666)
    >>> PoW = r.recvuntil(">")
    >>> r.sendline(f61d.prove(PoW))
    >>> r.interactive()
        
    '''
    if process_bar and show_description:
        print("Open tqdm bar and description may be VERY SLOW.\nDescription is not suggested.")
    from itertools import product
    import re
    from string import ascii_letters,digits
    from hashlib import sha256

    if type(cont) == bytes:
        cont = cont.decode()
    
    cont = cont.replace(' ','')
    #print(cont)
    p = re.compile('sha256(.*?)==(.*)')
    #print(p.findall(cont)[0])
    try:
        r = p.findall(cont)[0]
    except:
        print('Failed to parse text.')
        return
    L = len(r[0].split('+')[0])-1
    a = r[0].split('+')[1][:-1]
    b = r[1]
    print(f"Proving:\n\tsha256({'X'*L} + {a}) = {b}\n")
    s = list(product(ascii_letters+digits,repeat=L))
    if process_bar:bar = tqdm(s)
    else:bar = s
    ss = lambda d:sha256(d.encode()).hexdigest()
    for i in bar:
        S = ''.join(i)
        if process_bar and show_description:bar.set_description(f"trying: {S}")
        if ss(S+a) == b:
            print('\nFind ,',S)
            return S.encode()
    else:
        print('Failed to find \'XXXX\'')
        return None

    
def getLogo():
    print(colored(LOGO.randlogo(),choice(['red','yellow','green'])))
    #print(__verion__)

def yinyang():
    import f61d.yinyang
    f61d.yinyang.main()
    
def gmgj(n, c1, c2, e1, e2):#共模攻击
    '''
        共模攻击
    '''
    def egcd(a, b):
        if b == 0:
            return a, 0
        else:
            x, y = egcd(b, a % b)
            return y, x - (a // b) * y
    
    s = egcd(e1, e2)
    s1 = s[0]
    s2 = s[1]
    if s1 < 0:
        s1 = - s1
        c1 = pow(c1,-1,n)
    elif s2 < 0:
        s2 = - s2
        c2 = pow(c2,-1,n)
    m = pow(c1, s1, n) * pow(c2, s2, n) % n
    try:
        print(bytes.fromhex(hex(m)[2:]))
    except Exception as e:
        print(str(e))
    return m

def crt(c_list,n_list):
    '''
        Chinese Remainder Theory
        x = c0 mod n0
        x = c1 mod n1
        ...
    '''
    from functools import reduce
    sm = 0
    prod = reduce(lambda a, b: a * b, n_list)
    for n_i, a_i in zip(n_list, c_list):
        p = prod // n_i
        sm += a_i * pow(p,-1,n_i) * p
    return int(sm % prod)

def mtank(outerPic,innerPic,output='tank.png'):
    '''
        Mirage tank maker
        PIL is required
        usage:mtank(outerIMG,innerIMG[,outputFile])
    '''
    from PIL import Image as img
    from f61d.tank import make
    if output.split('.')[-1] != 'png':
        print('Output file type must be PNG')
        raise ValueError
    '''
    p1 = img.open(outerPic)
    p1 = p1.convert('L')
    p2 = img.open(innerPic)
    p2 = p2.convert('L')
    '''
    make(p1,p2,getDesktop() + '\\' + output)


def parse_header(s):
    hds = s
    hds = hds.split('\n')
    hds = {i.split(': ',1)[0].replace(':',''):i.split(': ',1)[1] for i in hds}
    return hds


def SHA3(s):
    if isinstance(s,str):
        s = s.encode()
    assert isinstance(s,bytes)
    from Crypto.Hash import keccak
    h = keccak.new(digest_bits=256)
    h.update(s)
    return h.hexdigest()
