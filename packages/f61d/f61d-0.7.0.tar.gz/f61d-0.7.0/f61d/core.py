import os, json, time
from requests import get

VERSION = (0,7.0)
VERSION = '.'.join(map(str, VERSION))

# print(colored(LOGO.randlogo()+' v'+VERSION+'\n\n',choice(['red','yellow','green'])))
# print(colored("Welcome to F61D. Use Help() for help.",'green'))

functions = {}
def addHelp(func):
    global functions
    funcName = getattr(func,'__name__')
    funcHelp = getattr(func,'__doc__').split('\n')
    funcHelp = [i.strip('\n ->') for i in funcHelp if '->' in i]
    functions[funcName] = '\n'.join(funcHelp)
    return func


@addHelp
def Help(page = 1,lines = 5):
    """
    -> print help page, 'Help(0)' for all functions.

    Args:
        page (int, optional): which page to print
        lines (int, optional): how many lines per page. set lines=0 for no limit.
    """
    from termcolor import colored
    yellow = lambda x: colored(x, 'yellow')
    green = lambda x: colored(x, 'green')
    cyan = lambda x: colored(x, 'cyan')
    from math import ceil

    if not isinstance(page, int) or not isinstance(lines, int):
        Help(1,10000)
        return print('Please input interger.')
    if page == 0:
        return Help(1,len(functions.keys()))

    maxPage = ceil(len(functions)/lines)
    titleWidth = max(len(i) for i in list(functions.keys())[lines * (page - 1): lines * page])
    descriptionWidth = max(len(i) for i in list(functions.values())[lines * (page - 1): lines * page])
    totalWidth = titleWidth + descriptionWidth + 14

    if (page - 1) * lines >= len(functions):
        print(f'Page Error, check the number : [1,{maxPage}]')
        return

    banner1 = yellow(f"{'<>' * (totalWidth // 4 - 2)}< ") + "H E L P" + yellow(f" >{'<>' * (totalWidth // 4 - 2)}")
    banner2 = yellow('<>' + ' ' * (totalWidth - 4 + 1) + '<>')
    print(f"{len(banner1) = }")
    print(f"{len(banner2) = }")
    if len(banner2) != len(banner1):
        banner1 = yellow('>') + banner1
        print(f"{len(banner1) = }")

    print(banner1, banner2, sep='\n')

    for i in range(min(lines,len(functions)-(page-1)*lines)):
        ind = i + lines*(page-1)
        funcName = list(functions.keys())[ind]
        description = functions[funcName]
        print(yellow('<> ') + cyan(f"{ind+1:2} ") + "<> " + cyan(funcName.ljust(titleWidth)) + f" : {green(description.ljust(descriptionWidth))} {yellow('<>')}")

    print(banner2, banner1, sep='\n')

    if page < maxPage:
        nxt_page_info = f'help({page+1}'
        nxt_page_info += '' if lines == 5 else f', {lines}'
        nxt_page_info += ') for next page'
        print(colored(nxt_page_info.center(totalWidth+5),'green'))


@addHelp
def fuckStar():
    """
    -> One click to fuck satellite
    """
    from tqdm import trange
    from random import randint

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


@addHelp
def lifeGame():
    """
    -> Play "Conway's Game of Life" in terminal
    """
    from f61d.lifeGame import game
    game()


@addHelp
def paint():
    """
    -> Draw the "Bing Dwen Dwen"
    """
    from f61d.bingdwendwen import draw
    draw()


@addHelp
def timeit(fun):
    """
    -> Take time for function excution

    Args:
        function need to take time
    """
    def wrapper(*args,**kwargs):
        t1 = time.time()
        ret = fun(*args,**kwargs)
        print(f'Function takes {time.time() - t1:.3f}s')
        return ret
    return wrapper


@addHelp
def prove(cont,process_bar=True,show_description=False):
    """
    -> Bypass PoW in ctf puzzles.
    Only the format is supported
    sha256(XXXX + {a}) = {b}

    Args:
        cont (str): Prove of Work Content.
        process_bar (bool, optional): Show process bar.
        show_description (bool, optional): Show description in process bar.

    Returns:
        pow_str (str): the 'XXXX'
        
    Example:
        >>> r = remote("127.0.0.1",6666)
        >>> PoW = r.recvuntil(">")
        >>> r.sendline(f61d.prove(PoW))
        >>> r.interactive()
    """
    if process_bar and show_description:
        print("Open tqdm bar and description may be VERY SLOW.\nDescription is not suggested.")
    from itertools import product
    import re
    from string import ascii_letters,digits
    from hashlib import sha256
    from tqdm import tqdm

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


@addHelp
def getLogo(color=True):
    """
    -> Get F61d logo
    """
    from random import choice
    try:
        import f61d.LOGO as LOGO
    except:
        import LOGO
    logo = LOGO.randlogo()
    if color:
        logo = colored(logo, choice(['cyan', 'red', 'yellow', 'green']))
    print(logo)


@addHelp
def gmgj(n, c1, c2, e1, e2):#共模攻击
    '''
    -> RSA Common-Modules Attack

    Args:
        n, c1, c2, e1, e2

    Returns:
        m (int): Plaintext
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


@addHelp
def crt(c_list,n_list):
    '''
    -> Chinese Remainder Theory

    Args:
        c_list (list[int]): Results list
        n_list (list[int]): Mudules list
        >>>
            x = c0 mod n0
            x = c1 mod n1

    Returns:
        M (int): M that satisfies the congruence equation
    '''
    from functools import reduce
    sm = 0
    prod = reduce(lambda a, b: a * b, n_list)
    for n_i, a_i in zip(n_list, c_list):
        p = prod // n_i
        sm += a_i * pow(p,-1,n_i) * p
    return int(sm % prod)


@addHelp
def mtank(outerPic, innerPic, output='output.png', verbose=False, force_resize=False):
    '''
    -> Mirage tank images maker, "python -m f61d.tank" is recommended
    PIL is required

    Args:
        outerPic (url str): Url of the outer Image.(Be shown in white background)
        innerPic (url str): Url of the inner Image.(Be shown in black background)
        output (url str, optional): Url of the output image path and filename
        verbose (bool, optional): Show progress bar
        force_resize (bool, optional): Force resizing img2 to match the size of img1

    Returns
        usage:mtank(outerIMG,innerIMG[,outputFile])
    '''
    from PIL import Image as img
    from f61d.tank import make
    import os
    if not output.endswith('.png'):
        output += '.png'
    output = output if os.path.isabs(output) else os.path.join(os.getcwd(), output)
    return make(p1, p2, output, verbose, force_resize)


@addHelp
def parse_header(s):
    '''
    -> Parse header string which is copied from Chrome.

    Args:
        s (str): Header in string format

    Returns:
        hds (dict): Header in dict format
    '''
    hds = s
    hds = hds.split('\n')
    hds = {i.split(': ',1)[0].replace(':',''):i.split(': ',1)[1] for i in hds}
    return hds


@addHelp
def download(url, to_file = None):
    """
    -> Download File with a progress bar, Only GET is supported

    Args:
        url (str): Url of file to download
        to_file (str, optional): Url of file to save. Empty to return binary content

    Returns:
        cont (bytes): Downloaded file binary content (`to_file` is unset)
    """
    import requests
    from tqdm import tqdm
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 KB
    progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

    if to_file:
        with open(to_file, 'wb') as f:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                f.write(data)
            progress_bar.close()
    else:
        file = b""
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file += data
        progress_bar.close()
        return file


@addHelp
def bc(*args, **kwargs):
    """
    -> [Blockchain] Blockchain functions. See f61d.bc for more information.
    """
    return "See f61d.bc for more information"


@addHelp
def date(*args, **kwargs):
    """
    -> Calculate date . See `python -m f61d.date` for more information.
    """
    return "See f61d.date for more information"


def getDesktop():
    try:
        import winreg
        return winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                                  r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'),
                                   "Desktop")[0]
    except:
        return os.curdir


@addHelp
def fast_setu(save=1, path=None):
    """
    -> Get a setu.

    Args:
        save (bool): Save to file
        path (url str): Path to save image (if save), default save to Desktop

    Returns:
        Image binary data
    """
    # iw233
    from random import choice
    url = ['https://iw233.cn/api.php?sort=random',
           'http://api.iw233.cn/api.php?sort=random',
           'http://ap1.iw233.cn/api.php?sort=random',
           'https://dev.iw233.cn/api.php?sort=random']

    data = download(choice(url))
    if len(data) < 1000:
        print('Visit too frequently')
        return

    if save:
        filename = randbytes(3).hex() + '.jpg'
        if path is None or not os.path.isdir(path):
            desk = getDesktop()
            ppath = os.path.join(desk, filename)
        else:
            ppath = os.path.join(path, filename)
        with open(ppath, 'wb') as f:
            f.write(data)
    return data


@addHelp
def setu(**kwargs):
    '''
    -> Get a setu by your XP, 'print(setu.__doc__)' for details

    Args:

        r18 (int, optional): 0为非 R18，1为 R18，2为混合
        num (int, optional): 一次返回的结果数量，范围为1到20
        uid (int|str, optional): 返回指定uid作者的作品
        keyword (str, optional): (Not recommend)从标题、作者、标签中按指定关键字模糊匹配的结果
        tag (str, optional): （eg.）tag='萝莉|少女&白丝|黑丝'
        size (str, optional): (eg.)size=['mini','small','thumb'] 或 size='regular',默认'original'
        proxy (str, optional): 图片地址所使用的在线反代服务（详见文档）
        dateAfter (timestamp, optional): 发布时间筛选，接受时间戳
        dateBefore (timestamp, optional): 发布时间筛选，接受时间戳
        dsc (bool, optional): 禁用对某些缩写自动转换（如 pcr => 公主连结|公主连结Re:Dive|プリンセスコネクト）
        path (url str, optional): Path to save image. Default to desktop.

        详细 API 文档请查看 https://api.lolicon.app/#/setu
    '''

    def getParam(x):
        if kwargs.get(x) is None:
            return ''
        if x == 'tag':
            return str(kwargs.get(x)).replace('&', '&tag=')
        elif x == 'size':
            if isinstance(kwargs.get(x), str):
                return args[x]
            elif isinstance(kwargs.get(x), list):
                return '&'.join(f'size={i}' for i in kwargs.get(x))[5:]
        return str(kwargs.get(x)).replace("'", '"')

    url = 'https://api.lolicon.app/setu/v2'

    params_list = ['r18', 'num', 'uid', 'keyword', 'tag', 'size', 'proxy', 'dataAfter', 'dataBefore', 'dsc', 'path']
    if uselessP := [i for i in kwargs.keys() if i not in params_list]:
        print('Invalid params:',*uselessP)

    param = {i: getParam(i) for i in params_list}
    f = lambda x: f'{x}={param[x]}' if param[x] != '' else ''
    paramUrl = '?' + '&'.join(f(i) for i in param)

    fullUrl = (url + paramUrl).strip('&')
    while '&&' in fullUrl:
        fullUrl = fullUrl.replace('&&', '&')
    print(fullUrl)

    ret = get(fullUrl).json()
    assert ret["error"] == '' ,ret['error']
    assert ret['data'] != [], "No such image"

    for ind, data in enumerate(ret["data"]):
        path = getParam('path') if getParam('path') != '' else getDesktop()

        urls = data['urls']
        for size in urls.keys():
            filename = f"{data['pid']} - {size}.{data['ext']}"
            print(f'Downloading ind: {filename}\t...', end='\n')
            filename = os.path.join(path, filename)
            download(urls[size], filename)



if __name__ == '__main__':
    Help(0)