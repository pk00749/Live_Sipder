import urllib.request
import re
import os
# 全局变量用来记录图片的编号
gl_z = 0


def down_img(url1):
    """下载图片"""
    # 处理图片链接,拼接http:
    url = "https:" + re.sub(r"\?", "", url1)
    global gl_z
    print(url)
    # 请求链接
    response = urllib.request.urlopen(url)
    # 读取内容
    data = response.read()
    # 切片取出图片名称
    file_name = url[url.rfind('/') + 1:]
    # 生成列表
    a = [x for x in range(10000)]
    # 打开文件用以写入
    dirPath = r'F:\img'
    file = open(os.path.join(dirPath, "img" + file_name + str(a[gl_z]) + ".jpg"), "wb")
    file.write(data)
    # 关闭文件
    file.close()
    # 编号加1
    gl_z += 1


if __name__ == '__main__':
    # 要抓去信息的网址
    home = """http://www.huya.com/g/xingxiu"""
    # 模拟请求头
    headers = {
        "Host": "www.huya.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
    }
    # 构造好请求对象 将请求提交到服务器 获取的响应就是到首页的html代码
    request = urllib.request.Request(url=home, headers=headers)
    response = urllib.request.urlopen(request)
    # 读取抓到的内容并解码
    html_data = response.read().decode()
    """huyaimg.msstatic.com/avatar/1054/db/6590aa9bcf98e12e5d809d371e46cc_180_135.jpg
    """
    # 使用正则 从首页中 提取出所有的图片链接
    img_list = re.findall(r"//huyaimg\.msstatic\.com.+\.jpg\?", html_data)
    print(img_list)
    # 取出每张图片进行下载
    for img_url in img_list:
        print(img_url)
        down_img(img_url)