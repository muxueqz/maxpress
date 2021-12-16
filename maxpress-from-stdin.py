import sys, os, re
from os.path import join as join_path
import base64
from maxpress import import_config, compile_styles, md2html

ROOT = os.path.dirname(sys.argv[0])


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
    print(result)

if __name__ == '__main__':

    # 全部转换并存档
    convert_all()

    # 只转换不存档
    # convert_all(archive=False)





