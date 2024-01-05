"""Messing Function"""
from pathlib import Path
from typing import List, Union

from discord import Embed, File, Member, Message, NotFound
from discord.ext.commands import Context


async def send_message(
    ctx: Union[Context, Member],
    content: str = None,
    embed: Embed = None,
    files: str = None,
    reply: bool = False,
    markup=None,
    delete: float = None,
) -> Message | None:
    """

    @param ctx:
    @param content:
    @param embed:
    @param files:
    @param reply:
    @param markup:
    @param delete:
    @return:
    """
    payload = {
        "content": content,
        "embed": embed,
        "files": fileio(files),
        "delete_after": delete,
        "reference": ctx.message if reply else None,
        "view": markup,
    }
    try:
        return await ctx.send(**payload)
    except NotFound:
        return None


async def edit_message(
    message: Message,
    content: str = None,
    embed: Embed = None,
    files: str = None,
    delete: float = None,
    markup=None,
) -> Message | None:
    """

    @param message:
    @param content:
    @param embed:
    @param files:
    @param delete:
    @param markup:
    @return:
    """
    payload = {
        "content": content,
        "embed": embed,
        "attachments": fileio(files),
        "delete_after": delete,
        "view": markup,
    }
    try:
        return await message.edit(**payload)
    except NotFound:
        return None


async def delete_message(message: Message, delay: float = None) -> None:
    """

    @param message:
    @param delay:
    @return:
    """
    try:
        return await message.delete(delay=delay)
    except NotFound:
        return None


async def send_files(
    ctx: Context,
    content: str = None,
    files: str = None,
    reply: bool = False,
    delete: float = None,
) -> Message | None:
    """

    @param ctx:
    @param content:
    @param files:
    @param reply:
    @param delete:
    @return:
    """
    payload = {
        "content": content,
        "files": fileio(files),
        "delete_after": delete,
        "reference": ctx.message if reply else None,
    }
    try:
        return await ctx.send(**payload)
    except NotFound:
        return None


def fileio(files: Union[str, Path, List[Union[str, Path]]]) -> List[File]:
    """

    @param files:
    @return:
    """
    if not files:
        return []
    if isinstance(files, (str, Path)):
        files = [files]  # Convert single file input to a list
    elif not isinstance(files, list):
        raise ValueError("files must be a string, pathlib.Path, or a list of files")
    else:
        files = []
    # Filter out file that don't exist and convert the remaining paths to File objects
    return [
        File(file)
        for file in files
        if isinstance(file, (str, Path)) and Path(file).exists()
    ]
