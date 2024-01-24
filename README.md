# At-cli

At-cli, a lightweight, cross-platform, fast and beautiful command line interface for https://atcoder.jp.

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

