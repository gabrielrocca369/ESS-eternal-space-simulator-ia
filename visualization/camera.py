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
        self.yaw = 0.0    # Ângulo de rotação no eixo Y (esquerda/direita)
        self.pitch = 0.0  # Ângulo de inclinação no eixo X (cima/baixo)
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
        rotation_speed = 90.0 * delta_time  # Velocidade de rotação em graus por segundo
        pitch_speed = 90.0 * delta_time     # Velocidade de inclinação em graus por segundo

        # Rotaciona a câmera para esquerda e direita
        if keys[pygame.K_LEFT]:
            self.yaw += rotation_speed
        if keys[pygame.K_RIGHT]:
            self.yaw -= rotation_speed

        # Inclina a câmera para cima e para baixo
        if keys[pygame.K_UP]:
            self.pitch += pitch_speed
        if keys[pygame.K_DOWN]:
            self.pitch -= pitch_speed

        # Limita o pitch para evitar a inversão da câmera
        max_pitch = 89.0
        if self.pitch > max_pitch:
            self.pitch = max_pitch
        if self.pitch < -max_pitch:
            self.pitch = -max_pitch

    def follow_target(self, target_position, target_direction):
        """
        Alinha a câmera para seguir um alvo (por exemplo, uma nave espacial).
        A câmera posiciona-se atrás do alvo e olha para ele.
        """
        # Converte yaw e pitch para radianos
        yaw_rad = math.radians(self.yaw)
        pitch_rad = math.radians(self.pitch)

        # Calcula a direção da câmera com base nos ângulos yaw e pitch
        direction = [
            math.cos(pitch_rad) * math.sin(yaw_rad),
            math.sin(pitch_rad),
            math.cos(pitch_rad) * math.cos(yaw_rad)
        ]
        direction = self.normalize_vector(direction)

        # Atualiza a posição da câmera com base na direção calculada
        self.position = [
            target_position[0] - direction[0] * self.offset_distance,
            target_position[1] - direction[1] * self.offset_distance,
            target_position[2] - direction[2] * self.offset_distance
        ]

        # A câmera olha para o alvo
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
