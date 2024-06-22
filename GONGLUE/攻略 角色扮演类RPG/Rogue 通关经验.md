# Rogue 通关经验

官方攻略见同目录下：《Rogue 官方手册》文档。

## 通关经验

- 没路可走时，不是游戏出错，而是有隐藏门和隐藏通路，在怀疑有隐藏门和路的周围一格多按几次 `s` 进行搜索可以发现（每按一次大概有 25% 的概率发现，所以重点点地方每走一步多按几下）。
- 注意食物规划，太过饥饿会晕倒，持续晕倒会死亡。
- 在使用 `e`，`q`, `t`, `r` 等命令后面需要输入物品编号时，可以输入 `*` 查看当前可以使用的对应物品，不用每次用之前按 `i` 看半天。
- 碰到怪多的地方先逃跑到狭长通道，边走边恢复血，不停的喝药和远程攻击，或者用传送卷轴传送走。
- 厉害的不会动的盖屋可用 `t` 命令远程投掷伤害，或者 `z` 命令魔杖远程攻击。
- 注意冰冻怪 `I` ，如果不动的话，先别主动招惹，清空周围的怪再量力而行。
- 拿到耶多尔附身符后，碰到楼梯 `%` 可以用 `<` 命令返回上层，这时你可以用 `<` 和 `>` 在多层间来回探索不着急去一层离开。
- `rogue-clone` 有巫师模式，按 `Ctrl+w` 并输入 `bathtub` 可以开启，开启后 `Ctrl+s` 可以查看全地图，很管用，但开启巫师模式后分数不记录到排行榜。

## 伤害计算

总体伤害的公式为：

    总体伤害 = 武器伤害 + 力量加成 + 等级加成 + 戒指加成

其中武器伤害：

| What | Damage |
|-|-|
| BOW/DART | 1d1 |
| ARROW | 1d2 |
| DAGGER | 1d3 |
| SHURIKEN | 1d4 | 
| MACE | 2d3 |
| LONG_SWORD | 3d4 |
| TWO_HANDED_SWORD | 4d5 |

武器伤害计算：

武器伤害一般描述为类似：`1d2`，`3d4` 之类的用字母 `d` 分割的两个数字，前面一个叫做 `n` 后一个叫做 `d`，伤害计算为：

    武器基础伤害 = sum([random(1, d) for x in n])

就是重复 n 轮，每轮取一个 [1, d] 的随机数，再把他们加起来。

而力量（strength）对应的伤害加成为：

| finsl_strength | 伤害加成 |
|-|-|
| <= 6 | final_strength - 5 |
| <= 14| 1|
| <= 17| 3|
| <= 18| 4|
| <= 20| 5|
| <= 21| 6|
| <= 30| 7|
| > 30 | 8|

其中：final_strength = strength + ring_strength_add

等级加成和戒指加成：

    等级戒指伤害加成 = (角色等级 + 戒指等级 - 戒指数量 + 1) / 2

最终：武器伤害，力量伤害加成，等级和戒指加成，三者合起来组成了最终的伤害值。



## 游戏获取

对于 Linux （debian/ubuntu）而言，默认包管理器中已经包含 rogue，用下面命令安装：

```bash
sudo apt-get install bsdgames-nonfree
```

然后输入 `rogue` 即可进入游戏；同时 Windows 用户有多个选择:

- [https://github.com/skywind3000/rogue-clone/releases](https://github.com/skywind3000/rogue-clone/releases)
- [https://rogueclone.sourceforge.net](https://rogueclone.sourceforge.net)
- [https://oryxdesignlab.itch.io/classic-rogue](https://oryxdesignlab.itch.io/classic-rogue)
- [https://github.com/mikeyk730/Rogue-Collection/releases](https://github.com/mikeyk730/Rogue-Collection/releases)

注意：下载第二个的话，中文系统下要设置环境变量：

```
set ROGUEOPTS=noPCgraphics
```

禁用扩展字符，避免乱码；使用第一个 `rogue-clone` 进入巫师模式后，用 CTRL+g 可以恢复血量和体力。

对于 GBA 用户，可以下载 AGB_Rogue：

- [https://www.gamebrew.org/wiki/AGB_Rogue_GBA](https://www.gamebrew.org/wiki/AGB_Rogue_GBA)

