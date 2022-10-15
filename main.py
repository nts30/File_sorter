import os
from config import *
from typing import Union, Iterable


class Folder:
    """Класс для сортировки файлов по папкам"""

    def __init__(self, path: Union[Path, str]) -> None:
        self.path = path

    def _get_file_path(self):
        """Получения пути к файлу

        :return: итератор пути к файлу
        """
        return (file.path for file in os.scandir(self.path) if not file.is_dir())

    def _create_subfolder(self, subfolder_name: str) -> None:
        """Создание подпапки

        :param subfolder_name: имя подпапки
        :return:
        """
        try:
            subfolder_path = self.path / subfolder_name
            if not subfolder_path.exists():
                subfolder_path.mkdir()

        except OSError as ex:
            print(f'Не удалось создать директорию -> {repr(ex)}')

    def sort_files_by_extension(self) -> None:
        """Сортировка файлов по расширениям

        :return: None
        """
        try:
            file_count = 0
            for filepath in self._get_file_path():
                path = Path(filepath)
                extension = path.suffix.split('.')[-1]

                if extension in extensions:
                    subfolder_name = get_subfolder_name_to_extension(extension)
                    self._create_subfolder(subfolder_name)

                    new_path = Path(self.path, subfolder_name, path.name)
                    path.rename(new_path)
                    file_count += 1
            print(f'Файлов отсортировано: {file_count}')
        except Exception as ex:
            print(f'Не удалось отсортировать файлы ->{repr(ex)}')


def sorter_files() -> None:
    folder = Folder(folder_path)
    print(f'Сортировка файлов в {folder_path}')
    folder.sort_files_by_extension()


if __name__ == '__main__':
    sorter_files()
