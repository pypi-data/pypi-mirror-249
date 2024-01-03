from requests import get
from random import *
import os
from time import time

def getDesktop():
    try:
        import winreg
        return winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'),"Desktop")[0]
    except:
        return os.curdir

    
def fast_setu(save = 1,path = None):
    # iw233
    url = ['https://iw233.cn/api.php?sort=random',
           'http://api.iw233.cn/api.php?sort=random',
           'http://ap1.iw233.cn/api.php?sort=random',
           'https://dev.iw233.cn/api.php?sort=random']

    data = get(choice(url)).content
    if len(data) < 1000:
        print('Visit too frequently')
        return
    
    if not save:
        return data
    if path is None or not os.path.isdir(path):
        desk = getDesktop()
        ppath = desk + '\\' + randbytes(3).hex() + '.jpg'
    else:
        ppath = path + '\\' + randbytes(3).hex() + '.jpg'
        
    with open(ppath,'wb') as f:
        f.write(data)


def setu(**args):
    '''
print(setu.__doc__)查看说明
参数说明:
            - r18 : 0为非 R18，1为 R18，2为混合
            - num : 一次返回的结果数量，范围为1到20
            - uid : 返回指定uid作者的作品
            - keyword : (不推荐)从标题、作者、标签中按指定关键字模糊匹配的结果
            - tag : （示例）tag='萝莉|少女&白丝|黑丝'
            - size ：(示例)size=['mini','small','thumb'] 或 size='regular',默认'original'
            - proxy : 图片地址所使用的在线反代服务（详见文档）
            - dateAfter : 发布时间筛选，接受时间戳
            - dateBefore : 发布时间筛选，接受时间戳
            - dsc : 禁用对某些缩写自动转换（如 pcr => 公主连结|公主连结Re:Dive|プリンセスコネクト）

            详细 API 文档请查看 https://api.lolicon.app/#/setu
    '''

    def getParam(x):
        if x in args.keys():
            if x == 'tag':
                return str(args[x]).replace('&','&tag=')
            if x == 'size':
                if type(args[x]) == str:
                    return args[x]
                elif type(args[x]) == list:
                    return ('&'.join([f'size={i}' for i in args[x]]))[5:]
                    
            return str(args[x]).replace("'",'"')
        else:
            return ''
    
    url = 'https://api.lolicon.app/setu/v2'

    params_list = ['r18','num','uid','keyword','tag','size','proxy','dataAfter','dataBefore','dsc']
    uselessP = [i for i in args.keys() if i not in params_list]    

    if len(uselessP) >= 1:
        print('Invalid params:')
        print(*uselessP)

    param = {i:getParam(i) for i in params_list}
    f = lambda x:f'{x}={param[x]}' if param[x] != '' else ''
    paramUrl = '?' + '&'.join(f(i) for i in param)

    fullUrl = url + paramUrl
    while '&&' in fullUrl:
        fullUrl = fullUrl.replace('&&','&') 
    while fullUrl[-1] == "&":
        fullUrl = fullUrl[:-1]

    print(fullUrl)
    ret = eval(get(fullUrl).text.replace('false','False').replace('true','True'))
    if ret["error"] != '':
        print(f'Error! {ret["error"]}')
    ret = ret["data"]

    for ind,data in enumerate(ret):
        path = getParam('path')
        if path == '':path = getDesktop()

        urls = data['urls']
        for size in urls.keys():
            filename = f"{data['pid']} - {size}.{data['ext']}"
            print(f'Downloading ind: {filename}\t...',end='\t')
            
            try:
                t1 = time()
                # print(urls[size])
                pic = get(urls[size]).content
                t = time() - t1
            except:
                print('Netwrok error')
                continue
            
            with open(path + '\\' + filename,'wb') as f:
                
                print(f'speed:{str(len(pic)/1024/1024/t)[:5]} MB/s')
                # print(f'speed:{len(pic)}/{t}*1000) kB/s')
                f.write(pic)
                
