# At-cli

At-cli, a lightweight, cross-platform, fast and beautiful command line interface for https://atcoder.jp.

## Multi-language support

NOTE: This content is in Chinese, doesn't matter if you use english.

中文用户请务必看过来！这个程序是有中文支持的！

检测使用语言的方法是环境变量 `LANG`，请将其设置为 `zh_CN.UTF-8` 以使用中文。

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
        atcodercli.url = "github:rickyxrc/at-cli/tags/v0.3.3";
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

