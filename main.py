import logging
import os
import sys
from typing import Iterable, Union

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from config import *
from ui import Ui_MainWindow

logs_folder.mkdir() if not logs_folder.exists() else None

logging.basicConfig(filename=f"logs/file_sorter.log",
                    level=logging.DEBUG,
                    format='[%(asctime)s] %(levelname)s - %(message)s',
                    datefmt='%H:%M:%S',
                    encoding='utf-8')


class Sorter(QtWidgets.QMainWindow):
    def __init__(self):
        super(Sorter, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()

    def init_UI(self):
        """Initialize the main window

        :return:
        """
        self.setWindowTitle('File Sorter')
        self.setWindowIcon(QIcon('images/Icon.png'))

        self.ui.lineEdit.setPlaceholderText('Enter path to the folder to sort')
        self.ui.pushButton.clicked.connect(self.sort)

    def sort(self):
        """Sorter function

        :return:
        """
        input_path = self.ui.lineEdit.text()
        if input_path == '':
            self.ui.label_3.setText(f'Enter path to the folder to sort')
            self.ui.label.repaint()
            return self.sort
        start_text = f'Sorting files by extensions in {input_path}'
        self.ui.label_3.setText(f'Sorting files by extensions in {input_path}')
        folder = Folder(fr'{input_path}')
        output = folder.sort_files_by_extensions()
        self.ui.label_3.setText(f'{start_text}\n{output}')
        self.ui.label.repaint()


class Folder(Sorter):
    """A class to organize log files. """

    def __init__(self, path: Union[Path, str]) -> None:
        super(Sorter, self).__init__()
        self.path = path

    def _get_file_paths(self) -> Iterable:
        """Getting file paths

        :return: return an iterator of file paths
        """
        return (file.path for file in os.scandir(self.path) if not file.is_dir())

    def _create_subfolder(self, subfolder_name: str) -> None:
        """Creating a subfolder

        :param subfolder_name: name of the subfolder
        :return:
        """
        try:
            subfolder_path = Path(fr'{self.path}\{subfolder_name}')
            if not subfolder_path.exists():
                subfolder_path.mkdir()
        except OSError:
            logging.error(f'Failed to create subfolder')

    def sort_files_by_extensions(self) -> str:
        """Sorting files by extensions

        :return:
        """
        try:
            file_count = 0
            for filepath in self._get_file_paths():
                path = Path(filepath)
                extension = Path(filepath).suffix.split('.')[-1]

                if extension in extensions:
                    subfolder_name = get_subfolder_name_by_extension(extension)
                    self._create_subfolder(subfolder_name)

                    new_path = Path(self.path, subfolder_name, path.name)
                    logging.info(f'{path.name} ---> {"/".join(new_path.parts[-2:])}')
                    path.rename(new_path)
                    file_count += 1
            logging.info(f'Files sorted: {file_count}')
            return f'Files sorted: {file_count}'
        except Exception as ex:
            logging.error(f'Failed to sort files -> {repr(ex)}')
            return f'Failed to sort files -> {repr(ex)}'


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = Sorter()
    application.show()

    sys.exit(app.exec_())
