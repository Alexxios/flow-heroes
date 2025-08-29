import os
from pathlib import Path
import json

from pygame import Surface
import pygame.image

from constants import PROJECT_ROOT



class ResourceManager:
    def __init__(self, base_path="assets"):
        self.base_path = Path(PROJECT_ROOT) / base_path

    def get_path(self, *relative_path):
        """Возвращает абсолютный путь к ресурсу"""
        return str(self.base_path.joinpath(*relative_path))

    def load_image(self, *relative_path) -> Surface:
        return pygame.image.load(self.base_path.joinpath(*relative_path))

    def load_font(self, *relative_path, size=20):
        return pygame.font.Font(self.base_path.joinpath(*relative_path), size)

    # def read_text(self, *relative_path, encoding="utf-8"):
    #     """Читает текстовый файл"""
    #     path = self.base_path.joinpath(*relative_path)
    #     with open(path, "r", encoding=encoding) as f:
    #         return f.read()
    #
    # def read_json(self, *relative_path, encoding="utf-8"):
    #     """Читает JSON файл"""
    #     return json.loads(self.read_text(*relative_path, encoding=encoding))
    #
    # def read_binary(self, *relative_path):
    #     """Читает бинарный файл"""
    #     path = self.base_path.joinpath(*relative_path)
    #     with open(path, "rb") as f:
    #         return f.read()


    # Можно добавить другие методы по необходимости
    # (для изображений, звуков и т.д.)
