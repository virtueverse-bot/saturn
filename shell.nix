{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python
    pkgs.imagemagick
  ];

  shellHook = ''
    export PATH="$PATH:$PWD"
  '';
}
