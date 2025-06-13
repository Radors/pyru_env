import shutil
import subprocess
import sys
import textwrap
from pathlib import Path


def check_directory() -> tuple[Path, Path]:
    project_root = Path.cwd()
    rust_root = Path(project_root / "rust")
    python_root = Path(project_root / "python")
    error_message = ("Subdirectory `{}` already exists. "
                     "Run pyru_env in an empty directory.")
    if rust_root.is_dir():
        raise FileExistsError(error_message.format(rust_root))
    if python_root.is_dir():
        raise FileExistsError(error_message.format(python_root))
    return rust_root, python_root


def check_cargo() -> None:
    cargo_path = shutil.which("cargo")
    if cargo_path is None:
        raise RuntimeError("`cargo` is not recognized on your machine. "
                           "Check path or get cargo with https://rustup.rs")


def setup_rust(rust_root: Path) -> None:
    subprocess.run(
        ["cargo", "new", "rust", "--lib"],
        check=True,
    )
    # overwrite lib.rs
    with open(Path(rust_root / "src" / "lib.rs"), "w",
              encoding="UTF-8") as file:
        file.write(textwrap.dedent("""\
                use std::ffi::{
                    c_int,
                };

                #[unsafe(no_mangle)]
                pub extern "C" fn example1() -> c_int {
                    1 as c_int
                }
            """))
    # append to Cargo.toml
    with open(Path(rust_root / "Cargo.toml"), "a",
              encoding="UTF-8") as file:
        file.write(textwrap.dedent("""\

                [lib]
                crate-type = ["cdylib"]
            """))


def setup_python(python_root: Path) -> None:
    python_root.mkdir()
    Path(python_root / "src").mkdir()
    Path(python_root / "tests").mkdir()
    subprocess.run(
        [sys.executable, "-m", "venv", Path(python_root / ".venv")],
        check=True,
    )
    with open(Path(python_root / "src" / "main.py"), "w",
              encoding="UTF-8") as file:
        file.write(textwrap.dedent("""\
                import ctypes
                import subprocess
                import sys
                from pathlib import Path


                def main(rust_lib):
                    pass


                def example_one(rust_lib):
                    rust_lib.example1.argtypes = []
                    rust_lib.example1.restype = ctypes.c_int
                    assert rust_lib.example1() == 1


                def example_two(rust_lib):
                    pass


                def build_and_load_rust():
                    project_root = Path(__file__).resolve().parents[2]
                    subprocess.run(
                        ["cargo", "build", "--release"],
                        cwd=Path(project_root / "rust"),
                        check=True,
                    )
                    file_prefix = ""
                    file_extension = ""
                    match sys.platform:
                        case "linux" | "linux2":
                            file_prefix = "lib"
                            file_extension = ".so"
                        case "darwin":
                            file_extension = ".dylib"
                        case "win32" | "cygwin" | "msys":
                            file_extension = ".dll"
                        case _:
                            raise OSError("unable to determine OS")
                    rust_lib = ctypes.CDLL(
                        Path(project_root / "rust" / "target" / "release" /
                             f"{file_prefix}rust{file_extension}")
                    )
                    return rust_lib


                if __name__ == "__main__":
                    rust_lib = build_and_load_rust()
                    example_one(rust_lib)
                    example_two(rust_lib)
                    main(rust_lib)
            """))


def main() -> None:
    rust_root, python_root = check_directory()
    check_cargo()
    setup_rust(rust_root)
    setup_python(python_root)


if __name__ == "__main__":
    main()
