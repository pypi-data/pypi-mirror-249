with (import <nixpkgs> {});
mkShell {
    buildInputs = [
        clang-tools
        cmake # Need this for meson to find pybind11
        meson
        ninja
        nlohmann_json
        opencv
        pkg-config
        python3Packages.build
        python3Packages.gst-python
        python3Packages.numpy
        python3Packages.pillow
        python3Packages.pybind11
        python3Packages.pylint
        python3Packages.pytest
        python3Packages.setuptools
        virtualenv
    ];
}
