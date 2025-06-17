{
  description = "Nix flakes";

  inputs = {
    nixpkgs.url = "nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix.url = "github:nix-community/poetry2nix";
    poetry2nix.inputs.nixpkgs.follows = "nixpkgs";
    poetry2nix.inputs.flake-utils.follows = "flake-utils";
    poetry2nix.inputs.systems.follows = "flake-utils/systems";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
      poetry2nix,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        p2n = poetry2nix.lib.mkPoetry2Nix { inherit pkgs; };
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            rmapi
          ];
        };
        packages.default = p2n.mkPoetryApplication {
          projectDir = ./.;
          preferWheels = true;
          overrides = p2n.overrides.withDefaults (
            final: prev: {
              remarks = prev.remarks.overridePythonAttrs (old: {
                buildInputs = (old.buildInputs or [ ]) ++ [ prev.poetry-core ];
              });
              rmc = prev.rmc.overridePythonAttrs (old: {
                buildInputs = (old.buildInputs or [ ]) ++ [ prev.poetry-core ];
              });
            }
          );
        };
      }
    );
}
