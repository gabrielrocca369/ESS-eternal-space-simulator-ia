import pygame  # Import necessário para detectar eventos de teclado
from simulation.physics import Physics
import math

class Spaceship:
    def __init__(self, name, max_speed=100000, mass=2000):
        self.name = name  # Nome do jogador, exibido sobre a nave
        self.position = [0.0, 0.0, 0.0]       # Posição inicial da nave no espaço 3D
        self.velocity = [0.0, 0.0, 0.0]       # Velocidade inicial da nave
        self.acceleration = [0.0, 0.0, 0.0]   # Aceleração inicial da nave
        self.direction = [0.0, 0.0, -1.0]     # Direção inicial da nave (eixo Z negativo)
        self.rotation_angle = 0.0             # Ângulo de rotação da nave
        self.max_speed = max_speed            # Velocidade máxima permitida para a nave
        self.mass = mass                      # Massa da nave, influencia a inércia e gravidade
        self.drag_coefficient = 0.1           # Coeficiente de arrasto

    def apply_force(self, force_vector):
        """
        Aplica uma força à nave, alterando sua aceleração com base na força aplicada.
        :param force_vector: Lista [Fx, Fy, Fz] representando o vetor de força aplicado
        """
        # Calcula a aceleração resultante da força (F = m * a => a = F / m)
        acceleration_due_to_force = [component / self.mass for component in force_vector]

        # Atualiza a aceleração atual da nave
        self.acceleration[0] += acceleration_due_to_force[0]
        self.acceleration[1] += acceleration_due_to_force[1]
        self.acceleration[2] += acceleration_due_to_force[2]

    def handle_input(self, keys, delta_time):
        """Lida com a entrada do teclado para controlar a nave."""
    
        # Reseta a aceleração no início do método
        self.acceleration = [0.0, 0.0, 0.0]

        # Define a aceleração básica da nave em função da entrada do usuário
        acceleration_value = 10000.0 * delta_time  # Valor ajustável para controlar a sensibilidade

        # Rotaciona a nave para esquerda e direita
        rotation_speed = 3.0 * delta_time  # Velocidade de rotação
        if keys[pygame.K_LEFT]:
            self.rotation_angle += rotation_speed
        if keys[pygame.K_RIGHT]:
            self.rotation_angle -= rotation_speed

        # Atualiza a direção da nave com base no ângulo de rotação
        self.direction = [
            math.sin(self.rotation_angle),  # Eixo X
            0.0,                           # Eixo Y permanece inalterado
            -math.cos(self.rotation_angle)  # Eixo Z (para frente/trás)
        ]

        # Movimenta a nave para frente e para trás com base na direção (eixo Z)
        if keys[pygame.K_w]:
            # Aplica aceleração na direção da nave
            self.acceleration[0] += self.direction[0] * acceleration_value
            self.acceleration[2] += self.direction[2] * acceleration_value
            print("Movendo para frente")
        if keys[pygame.K_s]:
            # Aplica aceleração contrária à direção da nave
            self.acceleration[0] -= self.direction[0] * acceleration_value
            self.acceleration[2] -= self.direction[2] * acceleration_value
            print("Movendo para trás")

        # Movimenta a nave para a esquerda e direita (esquerda/direita no plano XY)
        lateral_acceleration = 25.0 * delta_time  # Controla a aceleração lateral
        if keys[pygame.K_a]:
            self.acceleration[0] -= lateral_acceleration  # Move a nave para a esquerda
            print("Movendo para a esquerda")
        if keys[pygame.K_d]:
            self.acceleration[0] += lateral_acceleration  # Move a nave para a direita
            print("Movendo para a direita")

        # Movimenta a nave para cima e para baixo (eixo Y)
        if keys[pygame.K_q]:
            self.acceleration[1] += acceleration_value  # Sobe a nave
            print("Movendo para cima")
        if keys[pygame.K_e]:
            self.acceleration[1] -= acceleration_value  # Desce a nave
            print("Movendo para baixo")

        # Aplicando resistência (drag) ao movimento para evitar velocidade infinita
        self.apply_drag(delta_time)

    def update(self, time_step, keys):
        """Atualiza a velocidade, posição e direção da nave com base na aceleração e no tempo."""
    
        # Lida com a entrada do teclado para alterar a aceleração e rotação da nave
        self.handle_input(keys, time_step)

        # Atualiza a velocidade com base na aceleração atual
        self.velocity = Physics.calculate_velocity(self.velocity, self.acceleration, time_step)

        # Aplica o arrasto para desacelerar a nave (simulando resistência no espaço)
        self.apply_drag(time_step)

        # Limita a velocidade máxima da nave para evitar ultrapassar o limite
        self.velocity = Physics.limit_vector(self.velocity, self.max_speed)

        # Atualiza a posição da nave com base na velocidade atual
        self.position = Physics.update_position(self.position, self.velocity, time_step)

        # Reseta a aceleração após a atualização para evitar acumulação de força
        self.acceleration = [0.0, 0.0, 0.0]

        # Depuração: imprime a aceleração, velocidade e posição
        print(f"Aceleração: {self.acceleration}")
        print(f"Velocidade: {self.velocity}")
        print(f"Posição: {self.position}")

    def apply_drag(self, time_step):
        """Aplica uma força de arrasto (drag) para desacelerar a nave."""
        drag_force = [-v * self.drag_coefficient for v in self.velocity]
    
        # Aplica a força de arrasto à velocidade
        self.velocity = [
            self.velocity[0] + drag_force[0] * time_step,
            self.velocity[1] + drag_force[1] * time_step,
            self.velocity[2] + drag_force[2] * time_step
        ]

    def draw_name(self, renderer, camera):
        """Desenha o nome do jogador acima da nave."""
        # Defina a posição ligeiramente acima da nave para o texto
        name_position = [self.position[0], self.position[1] + 200.0, self.position[2]]
        
        # Renderiza o nome do jogador
        renderer.draw_text_3d(self.player_name, name_position, camera)