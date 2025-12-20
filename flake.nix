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
          pip
          pandas
          requests    # HTTP library
          virtualenv
          pypdf
          pypandoc
          pyyaml
        ];

        pythonEnv = pkgs.python312.withPackages pythonPackages;

      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            pythonEnv

            python312
            git         # Version control
          ];

          shellHook = ''
            if [ ! -d .venv ]; then
              python -m venv .venv
              source .venv/bin/activate
              pip3.12 install --upgrade pip
              pip3.12 install wisup_e2m konlpy
            else
              source .venv/bin/activate
            fi
          '';

          PROJECT_NAME = "book_analysis";
          NODE_ENV = "development";
        };
      });
}
