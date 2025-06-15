# Pyru Env

`pyru_env` is a Python module for setting up a combined development environment for Python and Rust.

The generated environment includes code demonstrating how Python can call Rust using the C ABI (Application Binary Interface).

## Installation:
`pip install pyru_env`

If your Python installation is externally managed (installed with your OS), you can either use pipx or create a temporary venv that you delete after installing and running pyru_env.

## Usage:
Inside an empty directory, run either:

`python3 -m pyru_env` 

`python -m pyru_env`

The Python entry point of the generated environment is at:

`/python/src/main.py`

If running `main.py` produces no errors, the setup was successful.

## Notes:

Your main.py includes code to build and load your rust library, depending on your OS.

The rust environment is created with "cargo new arbitrary_name --lib" except Cargo.toml includes 'crate-type = ["cdylib"]' and lib.rs is overwritten with two C ABI examples.

pyru_env internally calls venv with the same python you used to call pyru_env.

## Requirements:

* Python 3.9+
* Rust (cargo, rustc) https://rustup.rs
* Tested on: Ubuntu 24, Windows 11