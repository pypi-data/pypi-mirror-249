# Python wrapper of `fuse-overlayfs`

`fuse-overlayfs` is an implementation of overlay+shiftfs in FUSE for rootless containers, and the command name. [See this project's homepage.](https://github.com/containers/fuse-overlayfs)

## Install

Just run the command: `pip install fuse-overlayfs`.

Or you can download and install the wheel file from release page manually.

## Usage

A simple mount:

```pycon
>>> from fuseoverlayfs import FuseOverlayFS
>>> fuse_overlayfs = FuseOverlayFS.init()
>>> mnt = '/path/to/mountpoint'
>>> lowerdirs = ['/path/to/lowerdir1', '/path/to/lowerdir2']
>>> upperdir = '/path/to/upperdir'
>>> workdir = '/path/to/workdir'
>>> fuse_overlayfs.mount(mnt, lowerdirs, upperdir=upperdir, workdir=workdir)
>>>
```

A read-only mount, just remove argument `upperdir` and `workdir`:

```pycon
>>> from fuseoverlayfs import FuseOverlayFS
>>> fuse_overlayfs = FuseOverlayFS.init()
>>> mnt = '/path/to/another/mountpoint'
>>> lowerdirs = ['/path/to/lowerdir3', '/path/to/lowerdir4']
>>> fuse_overlayfs.mount(mnt, lowerdirs)
>>>
```

For more helpful information, see docstrings:

```pycon
>>> from fuseoverlayfs import FuseOverlayFS
>>> help(FuseOverlayFS.mount)
>>> help(FuseOverlayFS.unmount)
>>>
```
