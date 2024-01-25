# At-cli

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

