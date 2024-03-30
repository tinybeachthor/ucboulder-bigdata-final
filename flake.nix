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

          docker-compose
          flyway
          postgresql
        ];
        LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";
      };
    });
}
