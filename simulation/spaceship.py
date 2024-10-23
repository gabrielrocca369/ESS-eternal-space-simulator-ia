import pygame  # Import necessário para detectar eventos de teclado
from simulation.physics import Physics

class Spaceship:
    def __init__(self, max_speed=800, mass=1000):
        self.position = [0.0, 0.0, 0.0]       # Posição inicial da nave no espaço 3D
        self.velocity = [0.0, 0.0, 0.0]       # Velocidade inicial da nave
        self.acceleration = [0.0, 0.0, 0.0]   # Aceleração inicial da nave
        self.direction = [0.0, 0.0, -1.0]     # Direção inicial da nave (eixo Z negativo)
        self.max_speed = max_speed            # Velocidade máxima permitida para a nave
        self.mass = mass                      # Massa da nave, influencia a inércia e gravidade

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

    def handle_input(self, keys):
        """Lida com a entrada do teclado para controlar a nave."""
        # Reseta a aceleração no início do método
        self.acceleration = [0.0, 0.0, 0.0]

        # Define a aceleração básica da nave em função da entrada do usuário
        acceleration_value = 50.0  # Valor ajustável para controlar a sensibilidade

        # Movimenta a nave para frente e para trás (eixo Z)
        if keys[pygame.K_w]:
            self.acceleration[2] -= acceleration_value  # Move a nave para frente
            print("Movendo para frente")
        if keys[pygame.K_s]:
            self.acceleration[2] += acceleration_value  # Move a nave para trás
            print("Movendo para trás")

        # Movimenta a nave para os lados (eixo X)
        if keys[pygame.K_a]:
            self.acceleration[0] -= acceleration_value  # Move a nave para a esquerda
            print("Movendo para a esquerda")
        if keys[pygame.K_d]:
            self.acceleration[0] += acceleration_value  # Move a nave para a direita
            print("Movendo para a direita")

        # Movimenta a nave para cima e para baixo (eixo Y)
        if keys[pygame.K_q]:
            self.acceleration[1] += acceleration_value  # Sobe a nave
            print("Movendo para cima")
        if keys[pygame.K_e]:
            self.acceleration[1] -= acceleration_value  # Desce a nave
            print("Movendo para baixo")

    def update(self, time_step, keys):
        """Atualiza a velocidade, posição e direção da nave com base na aceleração e no tempo."""
        # Lida com a entrada do teclado para alterar a aceleração da nave
        self.handle_input(keys)

        # Atualiza a velocidade com base na aceleração atual
        self.velocity = Physics.calculate_velocity(self.velocity, self.acceleration, time_step)

        # Limita a velocidade máxima da nave para evitar ultrapassar o limite
        self.velocity = Physics.limit_vector(self.velocity, self.max_speed)

        # Atualiza a posição da nave com base na velocidade atual
        self.position = Physics.update_position(self.position, self.velocity, time_step)

        # Se a nave estiver se movendo, atualiza a direção para refletir o movimento atual
        if any(self.velocity):  # Verifica se há movimento em qualquer eixo
            self.direction = Physics.normalize_vector(self.velocity)

        # Depuração: imprime a aceleração, velocidade e posição
        print(f"Aceleração: {self.acceleration}")
        print(f"Velocidade: {self.velocity}")
        print(f"Posição: {self.position}")
