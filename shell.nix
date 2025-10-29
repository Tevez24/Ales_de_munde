
let
  pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/nixos-24.05.tar.gz") {};
in
pkgs.mkShell {
  buildInputs = [
    pkgs.python3
    pkgs.python3Packages.django
    pkgs.python3Packages.pip
    pkgs.python3Packages.mysqlclient
    pkgs.python3Packages.pillow
  ];
}
