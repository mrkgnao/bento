with import <nixpkgs> {};

stdenv.mkDerivation rec {
  name = "bento-${version}";
  version = "0.0.1";

  src = "./";

  buildInputs = with python35Packages; [
    virtualenv
    pip
    psutil

    ipython

    gcc
  ];
}
