"""
2023.06.26 01:40:00
"""
import shlex
import asyncio
from pathlib import Path

from pydistort.utils.libs import json


async def run(
        command: list,
        *,
        stdin=None, quiet=True,
        log_stdout=False, ret_stderr=False,
        unsafe_command: str = None,
        env: dict = None,
) -> bytes:
    parsed_command = unsafe_command or shlex.join([str(_) for _ in command])
    proc = await asyncio.create_subprocess_shell(
        parsed_command,
        stdin=asyncio.subprocess.PIPE if stdin else None,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        **({'env': env} if env else {}))

    stdout, stderr = await proc.communicate(stdin)

    if not quiet:
        print(f'[{parsed_command!r} exited with {proc.returncode}]')
        if stderr:
            print(f'[stderr]\n{stderr.decode(errors="ignore")}')
        if stdout and log_stdout:
            print(f'[stdout]\n{stdout.decode(errors="ignore")}')
    return stderr if ret_stderr else stdout


async def probe(filename: str | Path, stdin=None) -> dict:
    return json.loads(
        (await run(['ffprobe', '-show_format', '-show_streams', '-of', 'json', filename], stdin=stdin)).decode()
         )
