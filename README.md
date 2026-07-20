# vda5050-python

## Notice 

This repo is still pre-release

based on 

- `sauk2:feat/experimental-adapter` `fe13fe60ec38ef61c41fdfcf091d8b674ba19b57` 
- `feat/master/order-lifecycle-and-actions` `c50ec598c361de77a0c5e8bb3bbdd9c80e770544`

## Quick Run

Run the current mqtt_pair set: a Mosquitto broker, `/master`, and `/adapter`
(same identity: `ACME` / `AGV-001`).

### Docker images with Mosquitto

```bash
# Terminal 1 — MQTT broker
mosquitto -v -p 1883

# Terminal 2 — master only
docker run --platform linux/amd64 \
  -e MQTT_BROKER=tcp://host.docker.internal:1883 \
  ghcr.io/gametl/vda5050-python/master:main

# Terminal 3 — adapter (pairs with /master)
docker run --platform linux/amd64 \
  -e MQTT_BROKER=tcp://host.docker.internal:1883 \
  ghcr.io/gametl/vda5050-python/adapter:main
```

On Linux, use `tcp://172.17.0.1:1883` (or your host IP) instead of
`host.docker.internal` if that hostname is unavailable.

### Compose (broker + master + adapter)

```bash
cd examples/docker
docker compose up --build
```

### Pull images

```bash
docker pull --platform linux/amd64 ghcr.io/gametl/vda5050-python/master:main
docker pull --platform linux/amd64 ghcr.io/gametl/vda5050-python/adapter:main
```

### Install as Python Package 
```bash
# Placeholder for PyPI pip install
# See examples/docker/master_app/pyproject.toml for example of adding the whl to your project

```
## Manual Installation()

- Clone this repository
- `pip install ./vda5050-python`

Local Install 

### Prequiste

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
uv venv --python /opt/homebrew/bin/python3.12 # use your system python as base. A `libfmt.12.2.0.dylib` will error an arm64 & x86 mismatch MacOS
cd vda5050-python; 
export CMAKE_PREFIX_PATH="/opt/homebrew${CMAKE_PREFIX_PATH:+:$CMAKE_PREFIX_PATH}"
```



## Usage
###  Start Simple Master and Adapter
See [examples/mqtt_pair/README.md](examples/mqtt_pair/README.md) for more usage examples and details.

## Bindings
This repo python packaging is based in scikit_build_example

## License

pybind11 is provided under a BSD-style license that can be found in the LICENSE
file. By using, distributing, or contributing to this project, you agree to the
terms and conditions of this license.
