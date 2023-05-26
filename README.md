# pdocr-rpc

基于 PaddleOCR 封装的 RPC 服务，包含客户端和服务端。

客户端提供了一个简单易用的函数 `ocr`，通过不同的参数控制返回不同的值。

## 安装

```shell
pip install pdocr-rpc
```

另外还需要手动安装以下依赖：

### 客户端依赖

客户端仅需要安装**截图工具**；

- `Windows` 上安装截图工具：

```shell
pip3 install pillow
```

- `Linux` 上安装截图工具：

`Linux` 上推荐安装 `pyscreenshot`；

```shell
pip3 install pyscreenshot
```

### 服务端依赖

安装 `PaddleOCR` 环境

```shell
pip3 install paddlepaddle -i https://mirror.baidu.com/pypi/simple
pip3 install "paddleocr>=2.0.1" -i https://mirror.baidu.com/pypi/simple
```



## 1、使用方法

### 1.1、导入

```python
from pdocr_rpc import ocr
```

### 1.2、使用场景

#### 1.1.1、识别当前屏幕的所有文字内容

```python
ocr()
```

自动识别当前整个屏幕的所有内容。

#### 1.1.2、指定某张图片识别的所有文字内容

```python
ocr(picture_abspath="~/Desktop/test.png")
```

返回识别图片 `test.png` 的内容。 

#### 1.1.3、在全屏指定查找某个字符串的坐标

```python
ocr("天天向上")
```

返回当前屏幕中，“天天向上”的坐标，如果存在多个，则返回一个字典。

#### 1.1.4、指定某张图片查找某个字符串的坐标

```python
ocr("天天向上"，picture_abspath="~/Desktop/test.png")
```

### 1.3、其他参数

```shell
similarity: 匹配度。
return_default: 返回识别的原生数据。
return_first: 只返回第一个,默认为 False,返回识别到的所有数据。
lang: `ch`, `en`, `fr`, `german`, `korean`, `japan`
```

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

### 2.3、缓存

在 `ocr_env/pic` 目录下保存了识别的一些缓存图片文件，您可能需要定期进行删除；

当然，你可以使用定时任务对缓存文件进行清理，例如 `crontab`、`Jenkins` 任务等。
