# 服务端 linux service 配置

### 启动服务

将 `ocr_server.py` 文件拷贝到 `ocr_env` 目录，后台执行它就好了：

```
cd ocr_env
nohup pipenv run python ocr_server.py &
```

这里建议使用 pipenv 管理 Python 环境；

### 配置开机自启

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

### 缓存

在 `ocr_env/pic` 目录下保存了识别的一些缓存图片文件，您可能需要定期进行删除；

当然，你可以使用定时任务对缓存文件进行清理，例如 `crontab`、`Jenkins` 任务等。