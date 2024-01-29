# At-cli

[![Lint Code](https://github.com/Rickyxrc/at-cli/actions/workflows/lint.yml/badge.svg)](https://github.com/Rickyxrc/at-cli/actions/workflows/lint.yml)

At-cli, a lightweight, cross-platform, fast and beautiful command line interface for https://atcoder.jp.

## Multi-language support

NOTE: This content is in Chinese, doesn't matter if you use english.

中文用户请务必看过来！这个程序是有中文支持的！

检测语言使用了 locale 库，对于 windows，由于作者目前没有一台 windows 设备，无法进行测试（或许是可以的吧）。

对于 linux，它的主要工作原理是检测环境变量 `LANG`，请设置为 `zh_CN.UTF-8` 以使用中文。

如果认为我（或其他译者）的文笔太差，或有未翻译文本，想要贡献翻译，详见 [Contribute translation](#contribute-translation) 章节。

## Installation

### Via pypi package

This package is available through [PYPI](https://pypi.org/project/atcodercli/)! Required python 3.11 or higher.

```sh
$ pip install atcodercli
```

### Via nix flakes

Add this to your flakes.nix:

```nix
    inputs = {
        ...
        atcodercli.url = "github:rickyxrc/at-cli/tags/<version>";
    };
```

And use like this:

```nix
home.packages = [ inputs.atcodercli.packages.${pkgs.system}.default ];
```

## Configuration

See config.sample.yaml for details.

WARNING: EVERY command defined here will DIRECTLY execute on your machine!

## Contribute translation

We currently use [crowdin](https://crowdin.com/project/atcodercli) and support Chinese only, if you want to contribute to other languages, let me know by issue.

## Something about code

NOTE: I'm too lazy, so this part is in Chinese.

我发现我经常搞混几个概念，所以我把几个经常出现的名词的定义写在这里，也方便各位二次开发：

- template : 模板，也就是用于生成代码的基础，不应与文件（file）混淆
- file : 文件，也就是用模板生成的文件，不应与模板（template）混淆
- problems : 题目集，也就是 problem.yaml 中的内容，存储了题目和用题目生成的模板
- config : 配置项，也就是 ~/atcli/config.yaml 中的内容，存储了模板和比较器
- contest/init : 进行比赛，其实和 contest race 是一致的，但是计划将 init 作为 文件中统一的名称，而 race 作为命令别名
- checker : 差异比较器，不应和 diff 混淆

最近正在根据定义重新修改代码中的部分内容，如果有错漏欢迎 PR。

