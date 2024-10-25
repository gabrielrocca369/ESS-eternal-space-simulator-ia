import json
from pathlib import Path
import logging

class GameLogger:
    def __init__(self, save_file="game_progress.json"):
        self.save_file = Path(save_file)
        logging.basicConfig(
            filename='game_logger.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def save_progress(self, player_name, spaceship, distance_traveled, play_time, save_name=None):
        """
        Salva o progresso do jogo em um arquivo JSON.
        :param player_name: Nome do jogador
        :param spaceship: Objeto da nave contendo posição, velocidade, etc.
        :param distance_traveled: Distância total percorrida
        :param play_time: Tempo total de jogo
        :param save_name: Nome do arquivo de salvamento (opcional)
        """
        if save_name is None:
            save_path = self.save_file
        else:
            save_path = Path(f"{save_name}.json")

        data = {
            "player_name": player_name,
            "spaceship": spaceship.to_dict(),
            "distance_traveled": distance_traveled,
            "play_time": play_time
        }

        try:
            with save_path.open("w") as f:
                json.dump(data, f, indent=4)
            logging.info(f"Progresso do jogo salvo com sucesso em {save_path}.")
        except Exception as e:
            logging.error(f"Falha ao salvar o progresso do jogo em {save_path}: {e}")

    def load_progress(self, save_name=None):
        """
        Carrega o progresso do jogo de um arquivo JSON.
        :param save_name: Nome do arquivo de salvamento (opcional)
        :return: Dicionário contendo o progresso do jogo, ou None se o arquivo não existir.
        """
        if save_name is None:
            save_path = self.save_file
        else:
            save_path = Path(f"{save_name}.json")

        if save_path.exists():
            try:
                with save_path.open("r") as f:
                    data = json.load(f)
                logging.info(f"Progresso do jogo carregado com sucesso de {save_path}.")
                return data
            except Exception as e:
                logging.error(f"Falha ao carregar o progresso do jogo de {save_path}: {e}")
        else:
            logging.warning(f"Arquivo de progresso {save_path} não encontrado.")
        return None

    def reset_progress(self, save_name=None):
        """
        Reseta o progresso do jogo apagando o arquivo de salvamento.
        :param save_name: Nome do arquivo de salvamento (opcional)
        """
        if save_name is None:
            save_path = self.save_file
        else:
            save_path = Path(f"{save_name}.json")

        try:
            if save_path.exists():
                save_path.unlink()  # Remove o arquivo
                logging.info(f"Progresso do jogo resetado com sucesso em {save_path}.")
            else:
                logging.info(f"Nenhum arquivo de progresso encontrado para resetar em {save_path}.")
        except Exception as e:
            logging.error(f"Falha ao resetar o progresso do jogo em {save_path}: {e}")
