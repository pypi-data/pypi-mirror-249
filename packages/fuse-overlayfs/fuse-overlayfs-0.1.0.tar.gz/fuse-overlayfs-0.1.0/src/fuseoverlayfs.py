# -*- encoding: utf-8 -*-
import errno
import os
import shutil
import subprocess
from typing import Any
from typing import Callable
from typing import Iterable
from typing import Literal
from typing import overload

import attrs
import mntfinder

__all__ = ['FuseOverlayFSError', 'FuseOverlayFS']

__version__ = '0.1.0'


def _validator_factory_executable_field(basename: str | tuple[str, ...]) -> Callable[[Any, attrs.Attribute, Any], None]:
    def validator(__: Any, ___: attrs.Attribute, value: Any) -> None:
        if not os.path.exists(value):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), value)
        elif os.path.isdir(value):
            raise IsADirectoryError(errno.EISDIR, os.strerror(errno.EISDIR), value)
        elif not os.access(value, os.X_OK):
            raise PermissionError(errno.EPERM, os.strerror(errno.EPERM), value)

        actual_basename = os.path.basename(value).lower()
        if isinstance(basename, tuple):
            basenames: list[str] = [s.lower() for s in basename]
            if actual_basename not in basenames:
                raise ValueError(f'Executable name must be one of the following: {basenames!r} (got {actual_basename!r})')
        elif actual_basename != basename.lower():
            raise ValueError(f'Executable name must be {basename!r} (got {actual_basename!r}')

    return validator


def _verify_dir(raw_dir_path: str | bytes | os.PathLike, expected_permission: int) -> None:
    if not os.path.exists(raw_dir_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), raw_dir_path)
    elif not os.path.isdir(raw_dir_path):
        raise NotADirectoryError(errno.ENOTDIR, os.strerror(errno.ENOTDIR), raw_dir_path)
    elif not os.access(raw_dir_path, expected_permission):
        raise PermissionError(errno.EPERM, os.strerror(errno.EPERM), raw_dir_path)


class FuseOverlayFSError(Exception):
    pass


@attrs.define(slots=True, kw_only=True)
class FuseOverlayFS:
    executable: str = attrs.field(converter=os.fsdecode, validator=_validator_factory_executable_field('fuse-overlayfs'))

    @classmethod
    def init(cls, alter_executable: str | bytes | os.PathLike | None = None) -> 'FuseOverlayFS':
        if alter_executable is None:
            executable = shutil.which('fuse-overlayfs')
            if executable is None:
                raise FileNotFoundError('Could not find any executable named {!r} in the system $PATH'.format('fuse-overlayfs'))
        else:
            executable = alter_executable

        return cls(executable=executable)

    @staticmethod
    def isFuseOverlayFSMountPoint(target: str | bytes | os.PathLike) -> bool:
        return mntfinder.isMountPoint(target, fstype='fuse.fuse-overlayfs')

    @staticmethod
    def listAllFuseOverlayFSMountPoints() -> list[mntfinder.MountPoint]:
        return mntfinder.listAllMountPoints(fstype='fuse.fuse-overlayfs')

    @overload
    def mount(self,
              mountpoint: str | bytes | os.PathLike,
              lowerdirs: Iterable[str | bytes | os.PathLike],
              *, squash_to_root: bool = ...,
              squash_to_uid: int | None = ...,
              squash_to_gid: int | None = ...,
              static_link: bool = ...,
              noacl: bool = ...
              ) -> None:
        pass

    @overload
    def mount(self,
              mountpoint: str | bytes | os.PathLike,
              lowerdirs: Iterable[str | bytes | os.PathLike],
              *, workdir: str | bytes | os.PathLike,
              squash_to_root: bool = ...,
              squash_to_uid: int | None = ...,
              squash_to_gid: int | None = ...,
              static_link: bool = ...,
              noacl: bool = ...
              ) -> None:
        pass

    @overload
    def mount(self,
              mountpoint: str | bytes | os.PathLike,
              lowerdirs: Iterable[str | bytes | os.PathLike],
              *, upperdir: str | bytes | os.PathLike,
              workdir: str | bytes | os.PathLike,
              squash_to_root: bool = ...,
              squash_to_uid: int | None = ...,
              squash_to_gid: int | None = ...,
              static_link: bool = ...,
              noacl: bool = ...
              ) -> None:
        pass

    def mount(self, mountpoint, lowerdirs,
              *, upperdir=None, workdir=None, squash_to_root=False, squash_to_uid=None,
              squash_to_gid=None, static_link=False, noacl=False
              ) -> None:
        """
        Mounts a fuse-overlayfs filesystem.

        Note: currently not support dynamic UID/GID mapping.

        Args:
            mountpoint (str | bytes | os.PathLike):
                The path where the fuse-overlayfs filesystem will be mounted.
            lowerdirs (Iterable[str | bytes | os.PathLike]):
                The list of lower directories that will be merged together to form the overlay filesystem.
            upperdir (str | bytes | os.PathLike | None):
                The directory merged on top of all the lowerdirs where all the changes done to the file system will be written.
            workdir (str | bytes | os.PathLike | None):
                The directory used internally by fuse-overlays, must be on the same file system as the upper dir.

                If the ``upperdir`` is provided, this argument is required.
            squash_to_root (bool):
                If True, every file and directory is owned by the root user (0:0).
            squash_to_uid (int | None):
                If provided with `squash_to_gid`, every file and directory is owned by the specified uid or gid.
                Note: It has higher precedence over ``squash_to_root``.
            squash_to_gid (int | None):
                If provided with `squash_to_uid`, every file and directory is owned by the specified uid or gid.
                Note: It has higher precedence over ``squash_to_root``.
            static_link (bool):
                If True, set st_nlink to the static value 1 for all directories.

                This can be useful for higher latency file systems such as NFS, where counting the number of hard links
                for a directory with many files can be a slow operation. With this option enabled,
                the number of hard links reported when running stat for any directory is 1.
            noacl (bool):
                If True, disable ACL support in the FUSE file system.

        Raises:
            FuseOverlayFSError:
                If the mountpoint is already mounted as another filesystem or if the mount fails.
            TypeError:
                If ``upperdir`` is provided but did not provide ``workdir``,
                or ``squash_to_uid`` and ``squash_to_gid`` are not provided at the same time.

        Returns:
            None:
                The method does not return any value. It either successfully mounts the fuse-overlayfs filesystem
                or raises an exception if the mount fails.
        """
        mountpoint_canonical = os.fsdecode(os.path.realpath(mountpoint))
        if mntfinder.isMountPoint(mountpoint_canonical):
            raise FuseOverlayFSError(f'Already mounted as other filesystem: {mountpoint_canonical!r}')
        _verify_dir(mountpoint_canonical, os.R_OK | os.W_OK | os.X_OK)

        if isinstance(lowerdirs, str | bytes):
            raise TypeError('lowerdirs cannot be text or binary sequence object')
        lowerdirs_canonical = []
        for raw_lowerdir in lowerdirs:
            lowerdir = os.fsdecode(os.path.realpath(raw_lowerdir))
            _verify_dir(lowerdir, os.R_OK | os.X_OK)
            lowerdirs_canonical.append(lowerdir)

        cmdline = [
            self.executable,
            '-o', 'lowerdir={!s}'.format(':'.join(lowerdirs_canonical))
        ]
        if upperdir is not None:
            if workdir is None:
                raise TypeError('workdir must be provided with an non-empty upperdir')
            upperdir_canonical = os.fsdecode(os.path.realpath(upperdir))
            _verify_dir(upperdir_canonical, os.R_OK | os.W_OK | os.X_OK)
            cmdline.extend(['-o', f'upperdir={upperdir_canonical!s}'])
        if workdir is not None:
            workdir_canonical = os.fsdecode(os.path.realpath(workdir))
            _verify_dir(workdir_canonical, os.R_OK | os.W_OK | os.X_OK)
            cmdline.extend(['-o', f'workdir={workdir_canonical!s}'])
        if squash_to_root:
            cmdline.extend(['-o', 'squash_to_root'])
        elif squash_to_uid is not None and squash_to_gid is not None:
            if not isinstance(squash_to_uid, int):
                raise TypeError('{!r} must be an integer (got {!r})'.format('squash_to_uid', type(squash_to_uid)))
            if not isinstance(squash_to_gid, int):
                raise TypeError('{!r} must be an integer (got {!r})'.format('squash_to_gid', type(squash_to_gid)))
            cmdline.extend(['-o', f'squash_to_uid={int(squash_to_uid)!s}', '-o', f'squash_to_gid={int(squash_to_gid)!s}'])
        elif not (squash_to_uid is None and squash_to_gid is None):
            raise TypeError('{!r} must be provided with {!r}'.format('squash_to_uid', 'squash_to_gid'))
        if static_link:
            cmdline.extend(['-o', 'static_link'])
        if noacl:
            cmdline.extend(['-o', 'noacl'])
        cmdline.append(mountpoint_canonical)

        try:
            subprocess.run(args=cmdline, check=True)
        except subprocess.CalledProcessError:
            raise FuseOverlayFSError(f'Failed to mount the path {mountpoint_canonical!r} as fuse-overlayfs')

    @classmethod
    def unmount(cls, mountpoint: str | bytes | os.PathLike, *,
                method: Literal['umount', 'fusermount'] = 'fusermount',
                lazy_unmount: bool = False
                ) -> None:
        """
        Unmounts a fuse-overlayfs filesystem.

        Args:
            mountpoint (str | bytes | os.PathLike): The path of the mountpoint to be unmounted.
            method (Literal['umount', 'fusermount'], optional): The unmounting method to be used. Defaults to 'fusermount'.
            lazy_unmount (bool, optional): If True, performs a lazy unmount. Defaults to False.

        Raises:
            FuseOverlayFSError: If the unmounting method executable is not found,
                the mountpoint is not a fuse-overlayfs filesystem, or the unmount fails.
            ValueError: If the specified unmounting method is invalid.
            TypeError: If the specified unmounting method is not a string.

        Returns:
            None: The method does not return any value. It either successfully unmounts
                the fuse-overlayfs filesystem or raises an exception if the unmount fails.
        """
        if method == 'fusermount':
            fusermount_path = shutil.which('fusermount') or shutil.which('fusermount3')
            if not fusermount_path:
                raise FuseOverlayFSError(f'Cannot find fusermount or fusermount3 to unmount {mountpoint!r}')
            cmdline = [fusermount_path, '-u']
            if lazy_unmount:
                cmdline.append('-z')
        elif method == 'umount':
            cmdline = ['umount']
            if lazy_unmount:
                cmdline.append('--lazy')
        elif isinstance(method, str):
            raise ValueError(f"unmount method must be 'umount' or 'fusermount' (got {method!r})")
        else:
            raise TypeError(f"'method' must be either 'umount' or 'fusermount' (got {type(method)!r})")

        mountpoint_canonical = os.fsdecode(os.path.realpath(mountpoint))
        if not cls.isFuseOverlayFSMountPoint(mountpoint_canonical):
            raise FuseOverlayFSError(f'Not a fuse-overlayfs filesystem: {mountpoint_canonical!r}')
        if not os.path.exists(mountpoint_canonical):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), mountpoint_canonical)
        cmdline.append(mountpoint_canonical)

        try:
            subprocess.run(args=cmdline, check=True)
        except subprocess.CalledProcessError:
            raise FuseOverlayFSError(f'Failed to unmount: {mountpoint_canonical!r}')
