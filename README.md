# GONGLUE

单机游戏攻略秘籍，直接点开 GONGLUE 目录查看，共计 1479 篇，所有内容都来自网络。

## 格式说明

欢迎提交攻略，目前攻略只接受纯文本的 `.txt` 文件和 Markdown 的 `.md` 文件：

纯文本格式是第一行代表标题，后面是正文，比如：

```text
《大航海4》心得

经过三天的奋斗，用三个人物通了关以后，在这想谈点体会。。。。
```

导出 HTML 时会将第一行作为标题。

而使用 Markdown 时，也会将第一行文字作为本页的标题。


## 电子书

使用 `script` 目录里的 `make_chm.py` 可以生成 chm 文件，但需要提前安装好 Html Help Workshop 并且可以在 `$PATH` 中找到 `hhc.exe` 程序。

同时需要依赖下面几个 Python 库：

- markdown
- ebooklib

不想自己编译的话，也可以到 [Release](releases) 页面里下载预先编译好的版本。

## History

- 2024/5/23：初始化提交
- 2024/5/24：完成分类
- 2024/5/25：完成 chm/epub 导出，支持 markdown，样式，内嵌图片

## TODO

- [X] 完成分类
- [X] 支持 Markdown
- [x] 支持内置图片
- [x] 支持内置样式
- [X] 导出成 chm 的脚本
- [x] 导出成 epub 的脚本
- [ ] 优化内置式样
- [ ] CI 自动生成电子书

