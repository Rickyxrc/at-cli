{
    description = "Nix develop environment for at-cli";

    inputs = {
        nixpkgs.url = "github:nixos/nixpkgs/nixos-23.11";
        poetry2nix.url = "github:nix-community/poetry2nix";
    };

    outputs = { self, nixpkgs, poetry2nix, ...}: let
        system = "x86_64-linux";
        pkgs = import nixpkgs {
            inherit system;
            overlays = [ poetry2nix.overlays.default ];
        };
    in {
        devShells."${system}".default = let
        in pkgs.mkShell {
            packages = with pkgs; [
                poetry
            ];
            shellHook = ''
                poetry shell
            '';
        };
        packages."${system}".default = pkgs.writeShellApplication {
            name = "atcli";
            runtimeInputs =
                let
                    app = pkgs.poetry2nix.mkPoetryApplication {
                        projectDir = ./.;
                    };
                in [ app.dependencyEnv ];
            text = ''
                python -m atcodercli
            '';
        };
    };
}
