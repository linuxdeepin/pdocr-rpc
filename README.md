# pdocr-rpc

基于 `PaddleOCR` 封装的 `RPC` 服务，包含客户端和服务端。

客户端提供了一个简单易用的函数 `ocr`，通过不同的参数控制返回不同的值。

Documents：https://funny-test.github.io/pdocr-rpc

## 1、安装

```shell
pip install pdocr-rpc
```

另外还需要手动安装以下依赖：

### 1.1、客户端依赖

客户端仅需要安装**截图工具**；

- `Windows` 上安装截图工具：

  ```shell
  pip3 install pillow
  ```

- `Linux` 上安装截图工具：

```shell
pip3 install pyscreenshot
```

### 1.2、服务端依赖

安装 `PaddleOCR` 环境：

```shell
pip3 install paddlepaddle -i https://mirror.baidu.com/pypi/simple
pip3 install "paddleocr>=2.0.1" -i https://mirror.baidu.com/pypi/simple
```

## 2、使用方法

### 2.1、服务端

随意新建一个`py`文件，比如：`ocr_server.py`；

写入以下内容：

```python
# ocr_server.py
from pdocr_rpc.ocr_server import ocr_server

if __name__ == '__main__':
    ocr_server()
```

如果你想修改端口：

```python
from pdocr_rpc.ocr_server import ocr_server
from pdocr_rpc.setting import setting

setting.PORT = 8888

if __name__ == '__main__':
    ocr_server()
```

### 2.2、客户端

#### 2.1、识别当前屏幕的所有文字内容

```python
from pdocr_rpc.ocr import ocr

ocr()
```

自动识别当前整个屏幕的所有内容。

#### 2.2、指定某张图片识别的所有文字内容

```python
ocr(picture_abspath="~/Desktop/test.png")
```

返回识别图片 `test.png` 的内容。 

#### 2.3、在全屏指定查找某个字符串的坐标

```python
ocr("天天向上")
```

返回当前屏幕中，“天天向上”的坐标，如果存在多个，则返回一个字典。

#### 2.4、指定某张图片查找某个字符串的坐标

```python
ocr("天天向上"，picture_abspath="~/Desktop/test.png")
```

#### 2.5、其他参数

- 识别语言

  lang： `ch`, `en`, `fr`, `german`, `korean`, `japan`

  默认为ch，中文，如果要修改识别语言；

  ```python
  ocr(lang="ch") 
  ```

- 匹配度

  similarity: float

  默认为0.6，可以修改为从0到1的数；

  ```shell
  ocr(similarity=0.1)
  ```

- 返回原始数据

  return_default: bool

  默认为False，即默认返回识别到字符串的中心坐标，True表示返回原始数据；

  ```python
  ocr(return_default=False)
  ```

- 只返回第一个

  return_first: bool

  当传入要查找的字符串时，可能存在当前屏幕中有多个目标；

  默认情况下是会将识别到的多个目标组装成字典返回；

  return_first=True 表示返回识别到的第一个。

  ```python
  ocr(return_first=True )
  ```

  
