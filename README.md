# file-pycrypt
~~【自用】~~借助Python加密文件/文本的demo



## 依赖

Windows系统：

```bash
pip install -i https://pypi.douban.com/simple pycryptodomex
```



## 描述

仓库内含有3个demo

- text_crypt.py
  字符串加密/解密demo
- file_crypt_cover.py
  文件加密/解密（cmd交互）
  生成的文件会覆盖原先的文件，
  文件正在被其他软件使用时候会出错且无法回滚
- file_crypt_rename.py
  文件加密/解密（cmd交互）
  生成的文件名后会加上【已加密/已解密】
  推荐使用这个，因为经常蜜汁占用（文件正在被其他软件使用）



## 示例

运行`file_crypt_rename.py`

同级目录下有一个名为 `少儿不宜.avi` 的待加密文件

加密：

```python
请输入:   秘钥（16位纯数字）    
0147258369147258
请输入:   文件名.后缀    
少儿不宜.avi
请选择:   a.加密  b.解密    
a
>>> 
```

生成文件：`少儿不宜.avi.已加密`

解密时操作相同，交互输入加密时的相同秘钥，和加密后的文件名即可解密



## 参考

属于[对称密钥加密](https://baike.baidu.com/item/%E5%AF%B9%E7%A7%B0%E5%AF%86%E9%92%A5%E5%8A%A0%E5%AF%86)算法

AES加密数据块分组长度必须为128比特，

密钥长度可以是128比特、192比特、256比特中的任意一个。