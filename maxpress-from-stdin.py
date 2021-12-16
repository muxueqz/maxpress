from urllib.request import urlopen, Request
import sys, os, re
from os.path import join as join_path
import base64
from maxpress import import_config, compile_styles, md2html

ROOT = os.path.dirname(sys.argv[0])

def img2base64(html):    # 修复有时微信服务器获取不到图片的问题
    imgs = re.findall('img src="([^"]*)', html)

    headers = { 'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36' }
    new_imgs = {}

    for i in imgs:
        req = Request(i, headers=headers)
        image_data = urlopen(req).read()
        encoded = base64.b64encode(image_data) # Creates a bytes object
        img_path = 'data:image/png;base64,{}'.format(encoded.decode('utf8'))
        html = html.replace(i, img_path)

    return html

# 转换temp下的所有md文档
# @report_error
def convert_all(src=join_path(ROOT, 'temp'),
                dst=join_path(ROOT, 'result', 'html'),
                archive=None, styles=None):  # 通过styles参数传入css文件名列表时，默认样式将失效

    config = import_config()
    if archive is None: archive = config['auto_archive']

    if not styles:
        compile_styles()
    elif isinstance(styles, str): styles = [styles]

    text = sys.stdin.read()
    result = md2html(text, styles,
                     poster=config['poster_url'],
                     banner=config['banner_url'],
                     convert_list=config['convert_list'],
                     ul_style=config['ul_style'])
    print(img2base64(result))

if __name__ == '__main__':

    # 全部转换并存档
    convert_all()

    # 只转换不存档
    # convert_all(archive=False)





