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
          jsonpickle
          opencv4
          pip
          pandas
          pypdf
          pypandoc
          pyyaml
          requests    # HTTP library
          virtualenv
        ];

        pythonEnv = pkgs.python312.withPackages pythonPackages;

      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            pythonEnv
            python312

            git         # Version control
            javaPackages.compiler.openjdk25
            libGL
            pkg-config
            poppler-utils
            tesseract
            stdenv.cc.cc.lib
          ];

          shellHook = ''
            export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH
            if [ ! -d .venv ]; then
              python -m venv .venv
              source .venv/bin/activate
              pip3.12 install --upgrade pip
              pip3.12 install pi-heif wisup_e2m konlpy marker-pdf
              pip install numpy==1.26.2
              pip install pdfplumber==0.11.4
              pip install numpy==1.26.2
              pip install pdfplumber==0.11.4
              pip install pdfminer-six=20231228
              pip install pdfminer-six==20231228
              pip install unstructured-inference==0.7.36
            else
              source .venv/bin/activate
            fi
          '';

#numpy==1.26.2 pdfplumber==0.11.4 pdfminer-six==20231228  unstructured-inference==0.7.36
          PROJECT_NAME = "book_analysis";
          NODE_ENV = "development";
        };
      });
}
