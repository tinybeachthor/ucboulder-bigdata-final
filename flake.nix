{
  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs";
  };

  outputs = { self, flake-utils, nixpkgs }:
    flake-utils.lib.eachSystem [ "x86_64-linux" ] (system: let
      pkgs = import nixpkgs {
        inherit system;
        overlays = [ ];
      };
    in {
      devShells.default = pkgs.mkShell {
        buildInputs = with pkgs; [
          git
          gnumake

          python3
          heroku

          docker-compose
          flyway
          postgresql
          awscli

          zlib

          mdbook
          mdbook-pdf
          mdbook-toc
        ];
        LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath (with pkgs; [
          stdenv.cc.cc.lib
          zlib
        ]);
      };
    });
}
