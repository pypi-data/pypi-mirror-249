import os
import shutil
import sys
from typing import Callable
from pathlib import Path
from tempfile import mkdtemp

from pydistort import Queue, gif_to_folder
from pydistort.image import seam_carving
from pydistort.image.apng_tools import gif_to_apng
from pydistort.image.seam_carving import distort_gif
from pydistort.utils.runners import run


scripts = sys.executable.split('python.exe')[0]


async def render_lottie(filename_json: str | Path, filename, quiet=True):
    command = [sys.executable, f'{scripts}lottie_convert.py', filename_json, filename, '--fps', '60']
    if not quiet:
        command.append('-p')
    await run(command, quiet=quiet)
    return filename


async def render_lottie_gif(filename_json: str | Path, quiet=True):
    filename_gif = Path(filename_json).with_suffix('.gif')
    await render_lottie(filename_json, filename_gif, quiet)
    os.remove(filename_json)
    return filename_gif


async def render_lottie_apng(filename_json: str | Path, quiet=True):
    filename_gif = await render_lottie_gif(filename_json, quiet)
    filename_png = Path(filename_json).with_suffix('.png')
    return gif_to_apng(filename_gif, filename_png)


async def distort_lottie_gif(
        filename_json: str | Path, start=20, end=80,
        queue: Queue = None, callback: Callable = None, quiet=True):
    filename = Path(filename_json).with_suffix('.gif')
    await render_lottie(filename_json, filename, quiet)
    os.remove(filename_json)
    return await distort_gif(filename, start, end, queue, callback, quiet)


async def distort_lottie_apng(
        filename_json: str | Path,
        queue: Queue = None, callback: Callable = None, quiet=True):
    from apng import APNG  # TODO
    filename_gif = Path(filename_json).with_suffix('.gif')
    filename_png = Path(filename_json).with_suffix('.png')
    await render_lottie(filename_json, filename_gif, quiet)
    os.remove(filename_json)

    folder, duration = gif_to_folder(filename_gif, Path(mkdtemp(dir='.')))
    os.remove(filename_gif)
    frames = await seam_carving.distort_folder(folder, 20, 80, queue, callback, quiet)

    with open(filename_png, 'wb'):
        APNG.from_files(frames, delay=duration).save(filename_png)
    shutil.rmtree(folder)
    return filename_png
