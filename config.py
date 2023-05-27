from itertools import chain
from pathlib import Path

folder_path = Path(r'X:\test')

subfolder_name_to_extensions = {
    'video': ('mp4', 'mov', 'avi', 'mkv', 'wmv', 'mpg', 'mpeg', 'm4v', 'h264'),
    'audio': ('mp3', 'wav', 'ogg', 'flac', 'aif', 'mid', 'midi', 'wma'),
    'image': ('jpg', 'png', 'bmp', 'jpeg', 'svg', 'tif', 'tiff'),
    'archive': ('zip', 'rar', '7z', 'z', 'gz', 'pkg', 'deb'),
    'text': ('pdf', 'txt', 'doc', 'docx', 'rtf', 'odt'),
    'spreadsheet': ('xlsx', 'xls', 'xlsm'),
    'presentation': ('pptx', 'ppt'),
    'book': ('fb2', 'epub', 'mobi'),
    'gif': ('gif',),
    'torrent': ('torrent',),
    'exe': ('exe',)
}

subfolder_names = tuple(subfolder_name_to_extensions.keys())

extensions = tuple(chain.from_iterable(
    (subfolder_name_to_extensions.values())))

logs_folder = Path('logs')


def get_subfolder_name_by_extension(extension: str) -> str:
    """
    Returns the subfolder name for the given extension.

    :param extension: extension name
    :return: subfolder name
    """
    for subfolder_name, tuple_of_extensions in subfolder_name_to_extensions.items():
        if extension in tuple_of_extensions:
            return subfolder_name

