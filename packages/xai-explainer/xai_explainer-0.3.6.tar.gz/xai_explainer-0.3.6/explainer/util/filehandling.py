from collections import OrderedDict
import hashlib
import json
import os
from pathlib import Path
import shutil


def ensure_dir(dirname):
    dirname = Path(dirname)
    if not dirname.is_dir():
        dirname.mkdir(parents=True, exist_ok=False)


def read_json(fname):
    fname = Path(fname)
    with fname.open("rt") as handle:
        return json.load(handle, object_hook=OrderedDict)


def write_json(content, fname):
    fname = Path(fname)
    with fname.open("wt") as handle:
        json.dump(content, handle, indent=4, sort_keys=False)


def __approx_md5__(path: Path, n_blocks=20, block_size=2**12) -> str:
    m = hashlib.md5()

    with open(path, "rb") as f:
        f.seek(0, os.SEEK_END)
        file_size = f.tell()

        # np.linspace might overflow for large files, standard python int is safer
        start_positions = [
            int(file_size * i / (n_blocks - 1)) for i in range(n_blocks)
        ]  # linearly spaced start positions
        _last_pos = -1  # for early stopping

        for start_pos in start_positions:
            end_pos = start_pos + block_size
            if end_pos > file_size:
                start_pos = max(0, file_size - block_size)
                end_pos = file_size

            if start_pos == _last_pos:
                break  # avoid reading the same block twice

            f.seek(start_pos)  # seek to start position

            _block_size = (
                end_pos - start_pos
            )  # actual block size (might be smaller than block_size)
            buf = f.read(_block_size)  # read block

            m.update(buf)  # update hash

            _last_pos = start_pos

    return m.hexdigest()


def checksum(path: Path) -> str:
    """Return unique ID for the given path. The ID is computed by
    hashing some parts of the file and appending the file-size.
    The runtime of this function is independent of the file-size and only depends on the number of blocks and the block-size.

    Note: This is not a cryptographic hash-function and should not be used as such.

    Args:
        path (Path): Location of the file.
    Returns:
        str: Hash-value computed for the specified file.
    """
    if path.is_file() and os.path.getsize(path) > 0:
        _md5 = __approx_md5__(path)
        _size = os.path.getsize(path)
        res = f"{_md5}_{_size}B"
        return res
    else:
        raise FileNotFoundError(f"File {path} does not exist or is empty.")


def clear_directory(path: Path):
    """Clear the directory.

    Args:
        path (Union[str, Path]): Path to the directory.
    """
    for f in path.glob("*"):
        if f.is_file():
            f.unlink()
        elif f.is_dir():
            shutil.rmtree(f)
