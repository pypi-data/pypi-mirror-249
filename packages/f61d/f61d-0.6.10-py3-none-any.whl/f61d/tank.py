import sys
from PIL import Image as img
import numpy as np
from tqdm import tqdm

def TANK(imgA,imgB,verbose):
    global tqdm
    if not verbose:
        tqdm = lambda x:x
    siz = list(map(min,zip(imgA.size,imgB.size)))
    
    i = img.new("RGBA",siz)
    for w in tqdm(range(siz[0])):
        for h in range(siz[1]):
            try:
                pA = imgA.getpixel((w,h))
                pB = imgB.getpixel((w,h))
                
                a = 255 - (pA - pB)
                if a == 0:
                    gray = 0
                else:
                    gray = 255 * pB // a
                #print(gray)
                i.putpixel((w,h),(gray,gray,gray,a))
            except:
                pass
    return i



def make(imgOuter,imgInner,output,verbose=0,force_resize=False):
    # print(imgOuter,imgInner,output,verbose)

    # 转为灰度图像并转为np.ndarry
    imgOuter = img.open(imgOuter)
    imgOuter = imgOuter.convert('L')
    imgInner = img.open(imgInner)
    imgInner = imgInner.convert('L')

    if force_resize:
        imgInner = imgInner.resize(imgOuter.size)
    
    # 0~255 -> 128~255
    a1 = np.array(imgOuter)
    a1 = 255-(255-a1)//2
    img1 = img.fromarray(a1)

    # 0~255 -> 0~127
    a2 = np.array(imgInner)
    img2 = img.fromarray(a2//2)
    
    OutputImg = TANK(img1,img2,verbose)
    OutputImg.save(output)
    print(f'Mirage tank saved as {output}')


if __name__ == '__main__':
    # The length and width of the output image are obtained by taking the minimum value of the length and width of the input image.
    import argparse
    import os

    parser = argparse.ArgumentParser(prog='python -m f61d',
                                 description='f61d functions',
                                 allow_abbrev=True)
    
    parser.add_argument('img1', nargs=1, help='superficial image (before click / white background)')
    parser.add_argument('img2', nargs=1, help='interior image (after click / black background)')
    parser.add_argument('--verbose','-v',
                        dest='verbose',
                        action='store_true',
                        help='Show verbose (tqdm)')
    parser.add_argument('-f','--force-resize',
                        dest='force_resize',
                        action='store_true',
                        default=False,
                        help='Force resizing img2 to match the size of img1')
    parser.add_argument('-o FILE','--output FILE',
                        dest='output',
                        metavar='',
                        default='output.png',
                        nargs=1,
                        help='Output path (default output.png)')

    args = parser.parse_args()

    outerImg = args.img1[0] if os.path.isabs(args.img1[0]) else os.path.join(os.getcwd(), args.img1[0])
    innerImg = args.img2[0] if os.path.isabs(args.img2[0]) else os.path.join(os.getcwd(), args.img2[0])

    if args.output == 'output.png':
        # 没有指定output
        output = args.output
    else:
        # 指定了output
        assert isinstance(args.output, list), "Failed"
        output = args.output[0] if os.path.isabs(args.output[0]) else os.path.join(os.getcwd(), args.output[0])

    # 确保输出文件是png格式
    if not output.endswith('.png'):
        output += '.png'
        
    make(outerImg, innerImg, output, verbose=args.verbose, force_resize=args.force_resize)

'''
D:\\Pictures\\wallhaven-wqr22q.jpg D:\\Pictures\\wallhaven-2yjg26.jpg
'''
