# ZhousfLib

python常用工具库：coco数据集、labelme数据集、segmentation数据集、classification数据集制作和转换脚本；文件操作、表格操作、数据结构、web服务封装等工具集

### 数据集制作

* [X]  datasets/classification：数据集制作
* [X]  datasets/coco：数据集制作、格式转换、可视化、统计、数据更新/合并/提取
* [X]  datasets/labelme：数据集制作、格式转换、可视化、统计、数据更新/合并/提取
* [X]  datasets/segmentation：数据集制作

### ANN转换

* [X]  ann/torch_to_onnx：torch保存/加载onnx
* [X]  ann/torch_to_script：torch保存/加载script

### 数据库

* [X]  db/lmdb：内存映射数据库

### 装饰器

* [X]  decorator：异常捕获，AOP

### 文件下载

* [X]  download：文件批量异步下载

### 字体

* [X]  font：宋体、特殊符号字体

### 并发压测工具

* [X]  locust：demo

### 表格文件工具

* [X]  pandas：excel/csv操作、大文件读取

### pdf文件工具

* [X]  pdf：pdf导出图片、pdf文本和表格提取

### so加密工具

* [X]  so：python工程加密成so，防逆向

### web相关

* [X]  web：flask日志工具、响应体、配置

### 通用工具包

* [X]  util

* [util/cv_util]：opencv读写中文路径图片，图像相关处理
* [util/char_util]：字符相关处理，全角、半角
* [util/encrypt_util]：AES加密
* [util/iou_util]：IoU计算
* [util/json_util]：json读写
* [util/poly_util]：按照宽高对图片进行网格划分/切图
* [util/re_util]：re提取数字、字母、中文
* [util/singleton]：单例
* [util/string_util]：非空、包含、补齐
* [util/time_util]：日期、毫秒级时间戳、微秒级时间戳、日期比较
