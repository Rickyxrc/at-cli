{
    description = "at-cli, a lightweight, cross-platform, fast and beautiful command line interface for https://atcoder.jp";

    inputs = {
        nixpkgs.url = "github:nixos/nixpkgs/nixos-23.11";
        poetry2nix.url = "github:nix-community/poetry2nix";
    };

    outputs = { nixpkgs, poetry2nix, ...}: let
        system = "x86_64-linux";
        pkgs = import nixpkgs {
            inherit system;
            overlays = [ poetry2nix.overlays.default ];
        };
        app = pkgs.poetry2nix.mkPoetryApplication {
            projectDir = pkgs.stdenv.mkDerivation {
                name = "atcli-core";
                # TODO: This is DIRTY, fix it.
                src = pkgs.nix-gitignore.gitignoreSource (pkgs.lib.cleanSource ./.) (pkgs.lib.cleanSource ./.);
                buildInputs = with pkgs; [ tree python3 python311Packages.babel ];
                buildPhase = ''
                    source $stdenv/setup
                    mkdir -p $out
                    cp . $out -r
                    python3 $out/scripts/build-mo.py
                '';
            };
        };
    in {
        devShells."${system}" = {
            default = pkgs.mkShell {
                packages = with pkgs; [ poetry ];
            };
        };

        packages."${system}".default = pkgs.writeShellApplication {
            name = "atcli";
            runtimeInputs = [ app.dependencyEnv ];
            text = ''
                python -m atcodercli "$@"
            '';
        };
    };
}
