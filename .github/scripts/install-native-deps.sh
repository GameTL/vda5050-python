#!/usr/bin/env bash
# Install native build deps for vda5050 (fmt, nlohmann_json, Paho MQTT C++).
set -euo pipefail

PAHO_CPP_TAG="${PAHO_CPP_TAG:-v1.6.0}"
FMT_TAG="${FMT_TAG:-11.2.0}"
NLOHMANN_JSON_TAG="${NLOHMANN_JSON_TAG:-v3.11.3}"
PREFIX="${CMAKE_INSTALL_PREFIX:-/usr/local}"

run_root() {
  if [[ "$(id -u)" -eq 0 ]]; then
    "$@"
  else
    sudo "$@"
  fi
}

install_fmt_json_linux() {
  if command -v apt-get >/dev/null 2>&1; then
    run_root apt-get update
    run_root apt-get install -y --no-install-recommends \
      build-essential cmake ninja-build pkg-config git \
      libssl-dev libfmt-dev nlohmann-json3-dev
  elif command -v dnf >/dev/null 2>&1; then
    run_root dnf install -y gcc-c++ cmake ninja-build pkgconfig git openssl-devel
    install_fmt_json_from_source
  elif command -v yum >/dev/null 2>&1; then
    run_root yum install -y gcc-c++ cmake ninja-build pkgconfig git openssl-devel
    install_fmt_json_from_source
  else
    echo "Unsupported Linux package manager" >&2
    exit 1
  fi
}

install_fmt_json_from_source() {
  local work
  work="$(mktemp -d)"

  git clone --depth 1 --branch "$FMT_TAG" \
    https://github.com/fmtlib/fmt.git "$work/fmt"
  cmake -S "$work/fmt" -B "$work/fmt/build" \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX="$PREFIX" \
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
    -DFMT_TEST=OFF
  cmake --build "$work/fmt/build" --parallel
  run_root cmake --install "$work/fmt/build"

  git clone --depth 1 --branch "$NLOHMANN_JSON_TAG" \
    https://github.com/nlohmann/json.git "$work/json"
  cmake -S "$work/json" -B "$work/json/build" \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX="$PREFIX" \
    -DJSON_BuildTests=OFF
  cmake --install "$work/json/build"

  rm -rf "$work"
}

install_fmt_json_macos() {
  brew install cmake ninja fmt nlohmann-json openssl@3

  PREFIX="${CMAKE_INSTALL_PREFIX:-$(brew --prefix)}"
  export CMAKE_PREFIX_PATH="$PREFIX"
  export REPAIR_LIBRARY_PATH="$PREFIX/lib:$(brew --prefix openssl@3)/lib"

  if [[ -n "${GITHUB_ENV:-}" ]]; then
    echo "CMAKE_PREFIX_PATH=$CMAKE_PREFIX_PATH" >> "$GITHUB_ENV"
    echo "REPAIR_LIBRARY_PATH=$REPAIR_LIBRARY_PATH" >> "$GITHUB_ENV"
  fi
}

install_paho() {
  local work
  work="$(mktemp -d)"
  # shellcheck disable=SC2064
  trap "rm -rf '$work'" EXIT

  git clone --depth 1 --branch "$PAHO_CPP_TAG" --recursive \
    https://github.com/eclipse/paho.mqtt.cpp.git "$work/paho.mqtt.cpp"

  cmake -S "$work/paho.mqtt.cpp" -B "$work/paho.mqtt.cpp/build" \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX="$PREFIX" \
    -DPAHO_WITH_MQTT_C=ON \
    -DPAHO_BUILD_EXAMPLES=OFF \
    -DPAHO_WITH_SSL=ON

  cmake --build "$work/paho.mqtt.cpp/build" --parallel
  run_root cmake --install "$work/paho.mqtt.cpp/build"
}

case "$(uname -s)" in
  Linux)
    install_fmt_json_linux
    install_paho
    ;;
  Darwin)
    install_fmt_json_macos
    install_paho
    ;;
  *)
    echo "Unsupported OS: $(uname -s)" >&2
    exit 1
    ;;
esac

echo "Native dependencies installed (Paho MQTT C++ $PAHO_CPP_TAG)."
