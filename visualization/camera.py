import math

class Camera:
    def __init__(self, position=None, look_at=None, up=None):
        """
        Inicializa a câmera com a posição, o vetor que define a direção (look_at) e o vetor 'up'.
        """
        self.position = position if position is not None else [0.0, 0.0, 0.0]
        self.look_at = look_at if look_at is not None else [0.0, 0.0, -1.0]  # Direção olhando para -Z
        self.up = up if up is not None else [0.0, 1.0, 0.0]

    def normalize_vector(self, vector):
        """
        Normaliza um vetor para ter magnitude 1.
        Se o vetor for nulo (magnitude zero), retorna o próprio vetor.
        """
        magnitude = math.sqrt(sum(comp ** 2 for comp in vector))
        if magnitude == 0:
            return vector  # Evita divisão por zero
        return [comp / magnitude for comp in vector]

    def follow_target(self, target_position, target_direction):
        """
        Alinha a câmera para seguir um alvo (por exemplo, uma nave espacial).
        A câmera posiciona-se atrás do alvo e olha para ele.
        """
        # Define uma distância fixa atrás do alvo
        offset_distance = 400.0  # Ajuste conforme necessário

        # Normaliza o vetor de direção do alvo
        direction = self.normalize_vector(target_direction)

        # Calcula a posição da câmera atrás do alvo
        self.position = [
            target_position[0] - direction[0] * offset_distance,
            target_position[1] + 30.0,  # Eleva a câmera um pouco acima da nave
            target_position[2] - direction[2] * offset_distance
        ]

        # Atualiza o vetor look_at para olhar para o alvo
        self.look_at = target_position.copy()

    def get_view_matrix(self):
        """
        Retorna os parâmetros necessários para o gluLookAt.
        """
        return (
            self.position[0], self.position[1], self.position[2],
            self.look_at[0], self.look_at[1], self.look_at[2],
            self.up[0], self.up[1], self.up[2]
        )
