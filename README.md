# GONGLUE

单机游戏攻略秘籍，直接点开 GONGLUE 目录查看，共计 1479+ 篇，所有内容都来自网络。

## 格式说明

欢迎提交攻略，目前攻略只接受纯文本的 `.txt` 文件和 Markdown 的 `.md` 文件：

纯文本格式是第一行代表标题，后面是正文，比如：

```text
《大航海4》心得

经过三天的奋斗，用三个人物通了关以后，在这想谈点体会。。。。
```

导出 HTML 时会将第一行作为标题。

而使用 Markdown 时，也会将第一个标题（井号开头的行）作为本页的标题。


## 电子书

使用 `script` 目录里的 `make_chm.py` 和 `make_epub.py` 可以生成 chm 和 epub 电子书，但需要提前安装好 [chmcmd](https://wiki.freepascal.org/htmlhelp_compiler)，一个开源的 CHM 编译工具，并且可以在 `$PATH` 中找到 `chmcmd.exe` 程序（我自己做了一个 [精简版](https://github.com/skywind3000/support/releases/1.0.0) 下载里面的 chmcmd.zip 解压到当前目录即可）。

同时需要依赖下面几个 Python 库：

- markdown
- ebooklib
- beautifulsoup4

不想自己编译的话，也可以到 [Release](releases) 页面里下载预先编译好的版本。

## History

- 2024/5/23：初始化提交。
- 2024/5/24：完成分类。
- 2024/5/25：完成 chm/epub 导出，支持 markdown，样式，内嵌图片。
- 2024/5/26：完善 epub 在 iOS 下面的兼容性。
- 2024/5/27：改善攻略文件命名不一致问题。
- 2024/5/28：完善 CI 脚本，能够在 Release 时自动生成电子书。

## TODO

- [X] 完成分类
- [X] 支持 Markdown
- [x] 支持内置图片
- [x] 支持内置样式
- [X] 导出成 chm 的脚本
- [x] 导出成 epub 的脚本
- [x] CI 自动生成电子书
- [ ] 优化内置式样


