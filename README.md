## 介绍

![image-20241214002950974](image.png)

正如软件的标题名 功能就是批量修改PDF文件的背景颜色

## 实现原理

利用 `PyMuPDF` 库的能力来读取 PDF 文件的页面内容，并在新创建的页面上绘制背景颜色，然后将原始页面内容显示在新背景上，从而实现了 PDF 背景颜色的修改
