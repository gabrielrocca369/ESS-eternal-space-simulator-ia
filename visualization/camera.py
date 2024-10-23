import math
import pygame  # Import necessário para detectar eventos de teclado

class Camera:
    def __init__(self, position=None, look_at=None, up=None):
        """
        Inicializa a câmera com a posição, o vetor que define a direção (look_at) e o vetor 'up'.
        """
        self.position = position if position is not None else [0.0, 0.0, 0.0]
        self.look_at = look_at if look_at is not None else [0.0, 0.0, -1.0]  # Direção olhando para -Z
        self.up = up if up is not None else [0.0, 1.0, 0.0]
        self.rotation_angle = 0.0  # Ângulo de rotação no eixo Y (esquerda/direita)
        self.pitch_angle = 0.0     # Ângulo de inclinação no eixo X (cima/baixo)
        self.offset_distance = 800.0  # Distância padrão atrás do alvo

    def normalize_vector(self, vector):
        """
        Normaliza um vetor para ter magnitude 1.
        Se o vetor for nulo (magnitude zero), retorna o próprio vetor.
        """
        magnitude = math.sqrt(sum(comp ** 2 for comp in vector))
        if magnitude == 0:
            return vector  # Evita divisão por zero
        return [comp / magnitude for comp in vector]

    def update_camera_rotation(self, keys, delta_time):
        """
        Atualiza a rotação da câmera com base nas teclas pressionadas.
        """
        rotation_speed = 2.0 * delta_time  # Velocidade de rotação
        pitch_speed = 1.5 * delta_time     # Velocidade de inclinação (olhar para cima/baixo)

        # Rotaciona a câmera para esquerda e direita
        if keys[pygame.K_LEFT]:
            self.rotation_angle += rotation_speed
        if keys[pygame.K_RIGHT]:
            self.rotation_angle -= rotation_speed

        # Inclina a câmera para cima e para baixo
        if keys[pygame.K_UP]:
            self.pitch_angle = max(-math.pi / 2, self.pitch_angle - pitch_speed)  # Limita a inclinação
        if keys[pygame.K_DOWN]:
            self.pitch_angle = min(math.pi / 2, self.pitch_angle + pitch_speed)   # Limita a inclinação

    def follow_target(self, target_position, target_direction):
        """
        Alinha a câmera para seguir um alvo (por exemplo, uma nave espacial).
        A câmera posiciona-se atrás do alvo e olha para ele.
        """
        # Normaliza o vetor de direção do alvo
        direction = self.normalize_vector(target_direction)

        # Calcula a posição da câmera atrás do alvo, considerando a inclinação (pitch)
        self.position = [
            target_position[0] - direction[0] * self.offset_distance,
            target_position[1] + math.sin(self.pitch_angle) * self.offset_distance / 2,  # Inclina a câmera
            target_position[2] - direction[2] * self.offset_distance
        ]

        # Atualiza o vetor look_at para olhar para o alvo, aplicando a rotação
        self.look_at = [
            target_position[0] + math.sin(self.rotation_angle),
            target_position[1],
            target_position[2] - math.cos(self.rotation_angle)
        ]

    def get_view_matrix(self):
        """
        Retorna os parâmetros necessários para o gluLookAt.
        """
        return (
            self.position[0], self.position[1], self.position[2],
            self.look_at[0], self.look_at[1], self.look_at[2],
            self.up[0], self.up[1], self.up[2]
        )
