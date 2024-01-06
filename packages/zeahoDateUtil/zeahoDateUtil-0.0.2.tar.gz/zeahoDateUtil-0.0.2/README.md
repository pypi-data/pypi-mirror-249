# 安装上传工具
```bash
$ pip install twine
```
# 发布依赖包
#### 在当前目录下生成两个文件夹，保存了这个项目相关的所有信息
```bash
python setup.py sdist
```

#### 上传
```bash
twine upload dist/zeaho_date_util-0.0.1.tar.gz
```
#### username
```bash
__token__
```
#### api token
```bash
pypi-AgEIcHlwaS5vcmcCJDY2ZTg0ZmEwLWJhYzktNDAwYy04ZmE4LTAxMWZlZDRlYmI5NwACKlszLCIxOWE5YjM1MS0zYjU0LTRmZTctYjliNi0zOGVjNmIwMDczOGIiXQAABiAfH5Wdpr-k8dPYWqm8XKCH2EhmvgY00I5Dcy6RWqYVSQ
```
# 使用依赖
```bash
$ pip install zeahoDateUtil
$ from zeahoDateUtil.parse_datetime import parse_ymd
```