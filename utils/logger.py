import json
import os

class GameLogger:
    def __init__(self, save_file="game_progress.json"):
        self.save_file = save_file

    def save_progress(self, player_name, spaceship, distance_traveled, play_time):
        """
        Salva o progresso do jogo em um arquivo JSON.
        :param player_name: Nome do jogador
        :param spaceship: Objeto da nave contendo posição, velocidade, etc.
        :param distance_traveled: Distância total percorrida
        :param play_time: Tempo total de jogo
        """
        data = {
            "player_name": player_name,
            "spaceship": {
                "position": spaceship.position,
                "velocity": spaceship.velocity,
                "acceleration": spaceship.acceleration,
                "rotation_angle": spaceship.rotation_angle,
            },
            "distance_traveled": distance_traveled,
            "play_time": play_time
        }

        # Escreve o progresso no arquivo JSON
        with open(self.save_file, "w") as f:
            json.dump(data, f, indent=4)

    def load_progress(self):
        """
        Carrega o progresso do jogo de um arquivo JSON.
        :return: Dicionário contendo o progresso do jogo, ou None se o arquivo não existir.
        """
        if os.path.exists(self.save_file):
            with open(self.save_file, "r") as f:
                return json.load(f)
        return None
