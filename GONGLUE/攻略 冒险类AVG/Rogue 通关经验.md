# Rogue（肉鸽）

官方攻略见同目录下：《Rogue 官方手册》文档。

## 通关经验

- 没路可走时，不是游戏出错，而是有隐藏门和隐藏通路，在怀疑有隐藏门和路的周围一格多按几次 `s` 进行搜索可以发现（每按一次大概有 25% 的概率发现，所以重点点地方每走一步多按几下）。
- 注意食物规划，太过饥饿会晕倒，持续晕倒会死亡。
- 碰到怪多的地方先逃跑到狭长通道，边走边恢复血，不停的喝药和远程攻击。
- 厉害的不会动的盖屋可用 `t` 命令远程投掷伤害，或者 `z` 命令魔杖远程攻击。
- 注意冰冻怪 `I` ，如果不动的话，先别主动招惹，清空周围的怪再量力而行。
- 拿到耶多尔附身符后，碰到楼梯 `%` 可以用 `<` 命令返回上层，这时你可以用 `<` 和 `>` 在多层间来回探索不着急去一层离开。
- `rogue-clone` 有巫师模式，按 `Ctrl+w` 并输入 `bathtub` 可以开启，开启后 `Ctrl+s` 可以查看全地图，很管用，但开启巫师模式后分数不记录到排行榜。


## 游戏获取

对于 Linux （debian/ubuntu）而言，默认包管理器中已经包含 rogue，用下面命令安装：

```bash
sudo apt-get install bsdgames-nonfree
```

然后输入 `rogue` 即可进入游戏；同时 Windows 用户可以二选一:

- [https://rogueclone.sourceforge.net](https://rogueclone.sourceforge.net)
- [https://github.com/skywind3000/rogue-clone/releases](https://github.com/skywind3000/rogue-clone/releases)

注意：下载第一个的话，中文系统下要设置环境变量：

```
set ROGUEOPTS=noPCgraphics
```

禁用扩展字符，避免乱码。

