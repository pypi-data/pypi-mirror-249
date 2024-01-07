import os
import asyncio
import shutil
from io import BytesIO
from pathlib import Path
from random import randint
from tempfile import mkdtemp
from typing import Callable

from PIL import Image

from pydistort.image import gif_to_folder, webm_to_folder, folder_to_webm
from pydistort.utils.queue import Queue
from pydistort.utils.runners import run
from pydistort.utils.libs import json


async def distort(filename: str | Path, level: int | float, quiet=True):
    kok = (100 - level) % 100
    with Image.open(filename) as image:
        command = ['convert', f'{filename}',
                   '-liquid-rescale', f'{kok}%',
                   '-resize', f'{image.width}x{image.height}', f'{filename}']
    if os.name == 'nt':
        command = ['magick', *command]
    await run(command, quiet=quiet)
    return filename


async def distort_memory(file_io: BytesIO, ext: str, level: int | float, quiet=True) -> BytesIO:
    kok = (100 - level) % 100
    with Image.open(file_io) as image:
        command = ['convert', f'{ext}:-',
                   '-liquid-rescale', f'{kok}%',
                   '-resize', f'{image.width}x{image.height}', f'{ext}:-']
    if os.name == 'nt':
        command = ['magick', *command]
    file_io.seek(0)
    return BytesIO(await run(command, stdin=file_io.read(), quiet=quiet))


async def distort_many(
        distorts: list[list[str | Path, int | float]],
        queue: Queue = None, callback: Callable = None, quiet=True):
    """
    # callback example:
    it = 0

    async def callback(*args, **kwargs):
        nonlocal it
        it += 1
        if it % report_every:
            print(f'{it:05d}/{len(distorts):05d}')
    """
    distorts = [distort(file, level, quiet) for file, level in distorts]
    if queue:
        return await queue.add_many(distorts, callback)
    else:
        return await asyncio.gather(*distorts)


async def distort_folder(
        folder: str | Path, start=20, end=80,
        queue: Queue = None, callback: Callable = None, quiet=True):
    files = [*Path(folder).iterdir()]
    dist_step = (end-start) / (len(files) + 1)
    return await distort_many([[file, start + dist_step * i] for i, file in enumerate(files)], queue, callback, quiet)


async def distort_gif(
        filename: str | Path, start=20, end=80,
        queue: Queue = None, callback: Callable = None, quiet=True):
    folder, duration = gif_to_folder(filename, Path(mkdtemp(dir='.')))
    frames = await distort_folder(folder, start, end, queue, callback, quiet)
    first_frame, *other_frames = [Image.open(frame) for frame in frames]
    first_frame.save(filename, save_all=True, append_images=other_frames, format='gif', duration=duration, loop=0)
    [frame.close() for frame in [first_frame, *other_frames]]
    shutil.rmtree(folder)
    return filename


async def distort_webm(
        filename: str | Path, start=20, end=80,
        queue: Queue = None, callback: Callable = None, quiet=True):
    folder, framerate = await webm_to_folder(filename, Path(mkdtemp(dir='.')))
    await distort_folder(folder, start, end, queue, callback, quiet)
    await folder_to_webm(folder, filename, framerate)
    shutil.rmtree(folder)
    return filename


async def distort_flex(
        filename: str | Path, n_frames=9, start=20, end=80,
        duration=200, reverse=False, random=False,
        queue: Queue = None, callback: Callable = None, quiet=True):
    """
    reverse: n_frames=10, start=1, end=70, duration=50, reverse=True
    random: n_frames=9, start=20, end=80, duration=200, random=True
    """
    if not isinstance(filename, Path):
        filename = Path(filename)
    folder = Path(mkdtemp(dir='.'))
    frames = [shutil.copyfile(filename, folder / f'{i + 1:05d}.png') for i in range(n_frames)]
    filename.unlink()
    if random:
        frames = await distort_many([[frame, randint(start, end)] for frame in frames], queue, callback, quiet)
    else:
        frames = await distort_folder(folder, start, end, queue, callback, quiet)

    if reverse:
        first_frame, *other_frames = [Image.open(frame) for frame in frames[::-1]]
    else:
        first_frame, *other_frames = [Image.open(frame) for frame in frames]
    filename_gif = Path(filename).with_suffix('.gif')
    first_frame.save(filename_gif, save_all=True, append_images=other_frames,
                     format='gif', duration=duration, loop=0)
    [frame.close() for frame in [first_frame, *other_frames]]
    shutil.rmtree(folder)
    return filename_gif
