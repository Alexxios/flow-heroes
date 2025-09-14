import os
import zipfile

from constants import PROJECT_ROOT
from core.game import Game

def extract_nested_zips(start_zip, target_dir):
    with zipfile.ZipFile(start_zip, 'r') as zip_ref:
        zip_ref.extractall(target_dir)
        for file in zip_ref.namelist():
            if file.endswith('.zip'):
                nested_zip_path = os.path.join(target_dir, file)
                extract_nested_zips(nested_zip_path, target_dir)
                os.remove(nested_zip_path)  # Удаляем распакованный архив


if __name__ == "__main__":
    gamekit_dir = os.path.join(PROJECT_ROOT, "assets", "gamekit")
    if not os.path.exists(gamekit_dir):
        os.makedirs(gamekit_dir)
        extract_nested_zips("../assets/craftpix-891169-platformer-game-kit-pixel-art.zip", gamekit_dir)
        extract_nested_zips("../assets/craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks.zip", gamekit_dir)
        extract_nested_zips("../assets/craftpix-net-440623-free-pixel-magic-sprite-effects-pack.zip", gamekit_dir)
        extract_nested_zips("../assets/craftpix-net-661050-free-tiny-pixel-hero-sprites-with-bow-attacks.zip", gamekit_dir)

    game = Game("Game", 576 * 2, 324 * 2)
    game.run()
