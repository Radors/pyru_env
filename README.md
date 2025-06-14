# pyru_env

`pyru_env` is a module used to set up a combined environment for Python and Rust.

The generated environment includes code that demonstrates how Python can call Rust through C ABI.

## Install:
`pip install pyru_env`

NOTE TO SELF: expand on how to install in different scenarios

## Usage:
`python3 -m pyru_env` or `python -m pyru_env` (inside an empty directory)

main.py is located at `/python/src/main.py`. If running outputs no errors, the setup is working as intended.

## Explanation:

Your main.py includes code to build and load your rust library, depending on your OS.

The rust environment is created just as if you had ran "cargo new arbitrary_name --lib" except Cargo.toml also includes 'crate-type = ["cdylib"]' and lib.rs is overwritten with two C ABI examples.

pyru_env calls venv with the same python you used to call pyru_env.

## Requirements:

* Python 3.9+
* Rust (cargo, rustc) https://rustup.rs
* Tested on Linux and Windows (ubuntu24, windows11)