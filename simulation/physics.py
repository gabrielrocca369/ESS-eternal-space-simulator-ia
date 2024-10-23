import math

class Physics:
    GRAVITY_CONSTANT = 6.67430e-11  # Constante gravitacional universal

    @staticmethod
    def calculate_gravitational_force(mass1, mass2, distance):
        """
        Calcula a força gravitacional entre dois corpos.
        :param mass1: Massa do primeiro corpo
        :param mass2: Massa do segundo corpo
        :param distance: Distância entre os dois corpos
        :return: Força gravitacional escalar
        """
        if distance == 0:
            return 0.0  # Evita divisão por zero
        force = Physics.GRAVITY_CONSTANT * (mass1 * mass2) / (distance ** 2)
        return force

    @staticmethod
    def calculate_velocity(velocity, acceleration, time_step):
        """
        Atualiza a velocidade com base na aceleração e no tempo.
        :param velocity: Vetor de velocidade atual [vx, vy, vz]
        :param acceleration: Vetor de aceleração [ax, ay, az]
        :param time_step: Intervalo de tempo (delta_time)
        :return: Novo vetor de velocidade [vx, vy, vz]
        """
        return [
            velocity[0] + acceleration[0] * time_step,
            velocity[1] + acceleration[1] * time_step,
            velocity[2] + acceleration[2] * time_step
        ]

    @staticmethod
    def update_position(position, velocity, time_step):
        """
        Atualiza a posição com base na velocidade e no tempo.
        :param position: Posição atual [x, y, z]
        :param velocity: Velocidade atual [vx, vy, vz]
        :param time_step: Intervalo de tempo (delta_time)
        :return: Nova posição [x, y, z]
        """
        return [
            position[0] + velocity[0] * time_step,
            position[1] + velocity[1] * time_step,
            position[2] + velocity[2] * time_step
        ]

    @staticmethod
    def calculate_distance(pos1, pos2):
        """
        Calcula a distância entre duas posições no espaço 3D.
        :param pos1: Posição do primeiro ponto [x1, y1, z1]
        :param pos2: Posição do segundo ponto [x2, y2, z2]
        :return: Distância escalar entre os dois pontos
        """
        return math.sqrt(
            (pos1[0] - pos2[0]) ** 2 +
            (pos1[1] - pos2[1]) ** 2 +
            (pos1[2] - pos2[2]) ** 2
        )

    @staticmethod
    def normalize_vector(vector):
        """
        Normaliza um vetor para ter magnitude 1.
        :param vector: Vetor a ser normalizado [x, y, z]
        :return: Vetor normalizado [x, y, z]
        """
        magnitude = math.sqrt(sum(comp ** 2 for comp in vector))
        if magnitude == 0:
            return [0.0, 0.0, 0.0]  # Evita divisão por zero
        return [comp / magnitude for comp in vector]

    @staticmethod
    def limit_vector(vector, max_value):
        """
        Limita o comprimento de um vetor ao valor máximo especificado.
        :param vector: Vetor a ser limitado [x, y, z]
        :param max_value: Valor máximo para o comprimento do vetor
        :return: Vetor limitado [x, y, z]
        """
        magnitude = math.sqrt(sum(comp ** 2 for comp in vector))
        if magnitude > max_value and magnitude != 0:
            return [comp * max_value / magnitude for comp in vector]
        return vector
