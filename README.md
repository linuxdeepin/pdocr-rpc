# RPC-PaddleOCR

基于 PaddleOCR 部署的 RPC 服务。

提供了一个高度封装的接口函数 `ocr`，通过不同的参数组合返回不同的值。

## 1、客户端

依赖：

```shell
sudo pip3 install pyscreenshot
```

用于截图的工具。

【使用方法】

```python
# ocr.py

def ocr(*target_strings, picture_abspath=None, similarity=0.6, return_default=False, return_first=False, lang="ch"):
    """
     通过 OCR 进行识别。
    :param target_strings: 
        目标字符,识别一个字符串或多个字符串,并返回其在图片中的坐标;
        如果不传参，返回图片中识别到的所有字符串。
    :param picture_abspath: 要识别的图片路径。
    :param similarity: 匹配度。
    :param return_default: 返回识别的原生数据。
    :param return_first: 只返回第一个,默认为 False,返回识别到的所有数据。
    :param lang: `ch`, `en`, `fr`, `german`, `korean`, `japan`
    :return: 返回的坐标是目标字符串所在行的中心坐标。
    """
```

## 2、服务端

推荐使用 `pipenv` 进行环境搭建；

安装 `pipenv` ：

```
sudo pip3 install pipenv
```

新建一个目录作为环境包 `ocr_env`：

```
cd ~
mkdir ocr_env
```

创建 `python 3.7` 环境：

```
cd ocr_env
pipenv --python 3.7
```

安装 `OCR` 依赖包：

```
pipenv install paddlepaddle -i https://mirror.baidu.com/pypi/simple
pipenv install "paddleocr>=2.0.1" -i https://mirror.baidu.com/pypi/simple
```

不出意外，这样就把依赖安装好了。

### 2.1、启动服务

将 `ocr_server.py` 文件拷贝到 `ocr_env` 目录，后台执行它就好了：

```
cd ocr_env
nohup pipenv run python ocr_server.py &
```

### 2.2、配置开机自启

你肯定不想每次机器重启之后都需要手动启动服务，因此我们需要配置开机自启。

写开机自启服务文件：

```
sudo vim /lib/systemd/system/ocr.service
```

`autoocr` 名称你可以自定义，写入以下内容：

```
[Unit]
Description=OCR Service
After=multi-user.target

[Service]
User=uos
Group=uos
Type=idle
WorkingDirectory=/home/uos/ocr_env
ExecStart=pipenv run python ocr_server.py

[Install]
WantedBy=multi-user.target
```

> 注意替换你的${USER}

修改配置文件的权限：

```
sudo chmod 644 /lib/systemd/system/ocr.service
```

自启服务生效：

```
sudo systemctl daemon-reload
sudo systemctl enable ocr.service
```

查看服务状态：

```
sudo systemctl status ocr.service
```

你可以再重启下电脑，看看服务是不是正常启动了，没报错就 OK 了。

