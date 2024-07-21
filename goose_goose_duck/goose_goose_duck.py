import gdown
import os
import subprocess
from SteamPathFinder import get_steam_path, get_game_path


# список зависимостей в requirements.txt
# после установки игры следует перезагрузить компьютер,
# чтобы скрипт корректно определил путь до игры
class GameSetup:
    # атрибут с id файла для его загрузки
    download_id = '1IGENwFzLm8bBEboISadYSNEdxbnjz1fH'
    # атрибуты для поиска пути игры (id и название)
    app_id = '1568590'
    game_name = 'Goose Goose Duck'

    def __init__(self) -> None:
        # инициализация пути стима и игры
        self.find_game_path()

    def find_game_path(self):
        """Метод, находящий путь до игры и создающий путь .reg файла."""
        self.steam_path = get_steam_path()
        self.game_path = get_game_path(
            self.steam_path, self.app_id, self.game_name
        )
        # Создание полного пути к файлу
        filename = 'settings.reg'
        file_path = os.path.join(self.game_path, filename)
        self.file_path = file_path

    def download_reg_file(self):
        """Метод, загружающий файл с настройками игры."""
        # Запрос на скачивание файла
        try:
            gdown.download(id=self.download_id, output=self.file_path, quiet=False)
            print(f'Файл сохранен по адресу: {self.file_path}')

        except Exception as e:
            print(f'Ошибка при скачивании файла: {e}')

    def modify_game_settings(self):
        """Метод, вносящий значения из файла в реестр ОС."""
        # Команда для импорта .reg файла в реестр Windows
        command = f'regedit.exe "{self.file_path}"'

        # Выполнение команды
        try:
            subprocess.run(command, check=True, shell=True)
            print(f'Файл {self.file_path} успешно импортирован в реестр.')
        except subprocess.CalledProcessError as e:
            print(f'Ошибка при импорте файла {self.file_path} в реестр: {e}')

    def launch_game(self, mode):
        """Метод запускает Игру или Steam."""
        # словарь для определения пути к экзешнику стима или игры
        app = {
            'game': f'{self.game_path}\{self.game_name}.exe',
            'steam': f'{self.steam_path}\steam.exe'
        }

        # получение пути
        mode_path = app.get(mode)

        # запуск приложения
        try:
            subprocess.run(mode_path, check=True)
            print(f'Приложение {mode_path} успешно запущено.')
        except subprocess.CalledProcessError as e:
            print(f'Ошибка при запуске приложения {mode_path}: {e}')


def main():
    setup = GameSetup()
    setup.download_reg_file()
    setup.modify_game_settings()
    # указать в параметр steam или game для запуска
    # стима или игры соответсвенно
    setup.launch_game('game')


if __name__ == "__main__":
    main()
