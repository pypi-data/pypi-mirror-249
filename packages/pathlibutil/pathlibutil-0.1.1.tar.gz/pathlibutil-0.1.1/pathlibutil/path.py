import errno
import hashlib
import os
import pathlib
import shutil
import sys
from typing import Generator, Set


class Path(pathlib.Path):
    """Path inherites from `pathlib.Path` and adds some methods to built-in python functions"""

    default_hash = 'md5'
    """default hash algorithm for the class when no algorithm is specified for `hexdigest()` and `verify()`"""

    if sys.version_info < (3, 12):
        _flavour = pathlib._windows_flavour if os.name == 'nt' else pathlib._posix_flavour

    @property
    def algorithms_available(self) -> Set[str]:
        """
            Set of available algorithms that can be passed to `hexdigest()` and `verify()` method.
        """
        return hashlib.algorithms_available

    def hexdigest(self, algorithm: str = None, /, **kwargs) -> str:
        """
            Returns the hexdigest of the file using the named algorithm (default: `default_hash`).
        """
        try:
            args = (kwargs.pop('length'),)
        except KeyError:
            args = ()

        return hashlib.new(
            name=algorithm or self.default_hash,
            data=self.read_bytes(),
        ).hexdigest(*args)

    def verify(self, hexdigest: str, algorithm: str = None, *, strict: bool = True, **kwargs) -> bool:
        """
            Verifies the hash of the file using the named algorithm (default: `default_hash`).
        """
        _hash = self.hexdigest(algorithm, **kwargs)

        if strict:
            return _hash == hexdigest

        if len(hexdigest) < 7:
            raise ValueError('hashdigest must be at least 7 characters long')

        for a, b in zip(_hash, hexdigest):
            if a != b.lower():
                return False

        return True

    def __enter__(self) -> 'Path':
        """
            Contextmanager to changes the current working directory.
        """
        cwd = os.getcwd()

        try:
            os.chdir(self)
        except Exception as e:
            raise e
        else:
            self.__stack = cwd

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
            Restore previous working directory.
        """
        try:
            os.chdir(self.__stack)
        finally:
            del self.__stack

    def read_lines(self, **kwargs) -> Generator[str, None, None]:
        """
            Iterates over all lines of the file until EOF is reached.
        """
        with self.open(**kwargs) as f:
            yield from iter(f.readline, '')

    def size(self, **kwargs) -> int:
        """
            Returns the size in bytes of a file or directory.
        """
        if self.is_dir():
            return sum([p.size(**kwargs) for p in self.iterdir()])

        return self.stat(**kwargs).st_size

    def copy(self, dst: str, exist_ok: bool = True, **kwargs) -> 'Path':
        """
            Copies the file or directory to a destination path.
        """
        try:
            _path = shutil.copytree(
                self,
                dst,
                dirs_exist_ok=exist_ok,
                **kwargs
            )
        except NotADirectoryError:
            dst = Path(dst, self.name)

            if not exist_ok and dst.exists():
                raise FileExistsError(f'{dst} already exists')

            dst.parent.mkdir(parents=True, exist_ok=True)

            _path = shutil.copy2(
                self,
                dst,
                **kwargs
            )

        return Path(_path)

    def delete(self, *, recursive: bool = False, missing_ok: bool = False, **kwargs) -> None:
        """
            Deletes the file or directory.
        """
        try:
            self.rmdir()
        except NotADirectoryError:
            self.unlink(missing_ok)
        except FileNotFoundError as e:
            if not missing_ok:
                raise e
        except OSError as e:
            if not recursive or e.errno != errno.ENOTEMPTY:
                raise e

            shutil.rmtree(self, **kwargs)

    def move(self, dst: str) -> 'Path':
        """
            Moves the file or directory to a destination path.
        """
        src = self.resolve(strict=True)
        dst = Path(dst).resolve()
        dst.mkdir(parents=True, exist_ok=True)

        try:
            _path = shutil.move(str(src), str(dst))
        except shutil.Error as e:
            raise OSError(e)

        return Path(_path)
