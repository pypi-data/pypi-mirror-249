# OpenI

> PYPI package for 启智AI协作平台。

# 使用说明安装

- 启智平台提供的Python工具包，使用户能在本地上传数据集。

## 安装

*适配python3.6及以上版本*

> PYPI package for 启智 AI 协作平台。

## 安装

_适配 python3.6 及以上版本_

```bash
pip3 install -U c2net-beta
pip install c2net-beta==0.0.1 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 云脑资源初始化与上传，获取路径示例：

```
#导入包
from c2net.context import prepare, upload_output

#初始化导入数据集和预训练模型到容器内
openi_context = prepare()

#获取数据集路径，预训练模型路径，输出路径
dataset_path = openi_context.dataset_path
pretrain_model_path = openi_context.pretrain_model_path
you_must_save_here = openi_context.output_path

#回传结果到c2net
upload_output()
```
