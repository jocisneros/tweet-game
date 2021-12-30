# file_handling.py

from os import remove
from pathlib import Path
import re
import unicodedata


def slugify(value: str, allow_unicode=False) -> str:
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def write_bytes_to_cache(file_name: str, content: bytes) -> str:
    """Write bytes to a file in the cache directory."""
    src_dir = Path(__file__).parent.absolute();

    file_path = f"{src_dir}\\cache\\{slugify(file_name, allow_unicode=True)}.jpeg";

    with open(file_path, "w+b") as file:
        file.write(content)

    return file_path

def delete_file(file_path: str) -> None:
    """Delete a file at a given path."""
    if Path(file_path).exists:
        remove(file_path);
    return

