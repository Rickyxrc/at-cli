{
    description = "Nix develop environment for at-cli";

    inputs = {
        nixpkgs.url = "github:nixos/nixpkgs/nixos-23.11";
    };

    outputs = { self, nixpkgs, ...}: let
        system = "x86_64-linux";
    in {
        devShells."${system}".default = let
            pkgs = import nixpkgs {
                inherit system;
            };
        in pkgs.mkShell {
            packages = with pkgs; [
                poetry
            ];
            shellHook = ''
                poetry shell
            '';
        };
    };
}
