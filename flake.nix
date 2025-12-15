{
  description = "Dev environment with Python ";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    # This function creates outputs for each system (x86_64-linux, aarch64-darwin, etc.)
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        pythonPackages = ps: with ps; [
          pandas
          requests    # HTTP library
        ];

        pythonEnv = pkgs.python3.withPackages pythonPackages;

      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            pythonEnv

            # Basic development tools
            git         # Version control
          ];

          shellHook = ''
          '';

          PROJECT_NAME = "book_analysis";
          NODE_ENV = "development";
        };
      });
}
