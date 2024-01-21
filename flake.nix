{
    description = "Nix develop environment for at-cli";

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
            projectDir = ./.;
        };
    in {
        devShells."${system}" = {
            default = pkgs.mkShell {
                packages = with pkgs; [ poetry app.dependencyEnv ];
                shellHook = ''
                    alias atcli-dev="poetry run python3 -m atcodercli"
                '';
            };
        };
        packages."${system}".default = pkgs.writeShellApplication {
            name = "atcli";
            runtimeInputs =
                [ app.dependencyEnv ];
            text = ''
                python -m atcodercli "$@"
            '';
        };
    };
}
