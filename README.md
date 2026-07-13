# vda5050-python

## Installation

- Clone this repository
- `pip install ./vda5050-python`

Local Install 

## Prequiste

```bash
# MacOS
# compile and install paho mqtt 
git clone https://github.com/eclipse/paho.mqtt.cpp
cd paho.mqtt.cpp
git co v1.6.0
git submodule update --init
cmake -Bbuild -H. -DPAHO_WITH_MQTT_C=ON -DPAHO_BUILD_EXAMPLES=ON
sudo cmake --build build/ --target install
 
brew install fmt nlohmann-json
```

```bash
uv venv --python /opt/homebrew/bin/python3.13 # use your system python as base. A `libfmt.12.2.0.dylib` will error an arm64 & x86 mismatch MacOS
cd vda5050-python; 
export CMAKE_PREFIX_PATH="/opt/homebrew${CMAKE_PREFIX_PATH:+:$CMAKE_PREFIX_PATH}"
```



## Start Simple Master and Adapter

See [examples/mqtt_pair/README.md](examples/mqtt_pair/README.md) for more usage examples and details.

# Bindings

- since the template `scikit_build_example`: add vda5050_core as submodules in CMakeList.txt
- Have the **init**.py import `._core.cpp` binding , register submodules from core. 
- Occupy **init**.pyi for intelisense autocomplete + pylance + description + How-To use function, class, vars,

# Notes

Around fmt 11, pulling fmt::format through core.h was deprecated.
in `logger.hpp` and `protocol_adapter.hpp` change from `#include <fmt/core.h>` to `#include <fmt/format.h>`

# Uninstall

Only if you need to delete and are sure no other software depends on this. 

```bash
sudo rm -rf /opt/homebrew/include/mqtt \
  /opt/homebrew/lib/cmake/PahoMqttCpp \
  /opt/homebrew/lib/libpaho-mqttpp3*
brew uninstall libpaho-mqtt
```

# Run this package

2 Option: 

- uv venv and install and run `example_master_webserver.py` [TODO]
- Run the option above in a docker compose. see `example/docker/README.md` [TODO]



## Files

This example has several files that are a good idea, but aren't strictly
necessary. The necessary files are:

- `pyproject.toml`: The Python project file
- `CMakeLists.txt`: The CMake configuration file
- `src/main.cpp`: The source file for the C++ build
- `src/vda5050-python/__init__.py`: The Python portion of the module. The root of the module needs to be `<package_name>`, `src/<package_name>`, or `python/<package_name>` to be auto-discovered.

These files are also expected and highly recommended:

- `.gitignore`: Git's ignore list, also used by `scikit-build-core` to select files for the SDist
- `README.md`: The source for the PyPI description
- `LICENSE`: The license file

There are also several completely optional directories:

- `.github`: configuration for [Dependabot](https://docs.github.com/en/code-security/dependabot) and [GitHub Actions](https://docs.github.com/en/actions)
- `conda.recipe`: Example recipe. Normally you should submit projects to conda-forge instead of building them yourself, but this is useful for testing the example.
- `docs/`: Documentation
- `tests/`: Tests go here

And some optional files:

- `.pre-commit-config.yaml`: Configuration for the fantastic static-check runner [pre-commit](https://pre-commit.com).
- `noxfile.py`: Configuration for the [nox](https://nox.thea.codes) task runner, which helps make setup easier for contributors.

This is a simplified version of the recommendations in the [Scientific-Python
Development Guide](https://learn.scientific-python.org/development), which is a *highly* recommended read for anyone
interested in Python package development (Scientific or not). The guide also
has a cookiecutter that includes scikit-build-core and pybind11 as a backend
choice.

### CI Examples

There are examples for CI in `.github/workflows`. A simple way to produces
binary "wheels" for all platforms is illustrated in the "wheels.yml" file,
using [cibuildwheel](https://cibuildwheel.readthedocs.io).

## License

pybind11 is provided under a BSD-style license that can be found in the LICENSE
file. By using, distributing, or contributing to this project, you agree to the
terms and conditions of this license.
