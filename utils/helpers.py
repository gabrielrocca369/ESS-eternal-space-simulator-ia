import random
import math

class Helpers:
    @staticmethod
    def random_position(min_value=-1000, max_value=1000):
        """
        Gera uma posição aleatória dentro de um intervalo fornecido. 
        A posição é distribuída uniformemente no espaço tridimensional.
        """
        x = random.uniform(min_value, max_value)
        y = random.uniform(min_value, max_value)
        z = random.uniform(min_value, max_value)
        print(f"Gerando posição aleatória: {x}, {y}, {z}")
        return [x, y, z]

    @staticmethod
    def limit_value(value, min_value, max_value):
        """
        Limita um valor entre um mínimo e um máximo. 
        Isso é útil para limitar coordenadas ou forças aplicadas a objetos.
        """
        limited_value = max(min(value, max_value), min_value)
        print(f"Limitando valor {value} para o intervalo [{min_value}, {max_value}]: {limited_value}")
        return limited_value

    @staticmethod
    def normalize_vector(vector):
        """
        Normaliza um vetor para ter magnitude 1. 
        Se a magnitude for zero, retorna o vetor original.
        """
        magnitude = math.sqrt(sum(comp ** 2 for comp in vector))
        if magnitude == 0:
            print(f"Vetor de magnitude zero detectado: {vector}")
            return vector
        normalized_vector = [comp / magnitude for comp in vector]
        print(f"Normalizando vetor {vector}: {normalized_vector}")
        return normalized_vector

    @staticmethod
    def round_coordinates(coordinates, precision=2):
        """
        Arredonda as coordenadas para um número de casas decimais especificado.
        Útil para evitar erros de ponto flutuante ao trabalhar com grandes coordenadas espaciais.
        """
        rounded = [round(coord, precision) for coord in coordinates]
        print(f"Coordenadas arredondadas de {coordinates} para {rounded} com precisão {precision}")
        return rounded

    @staticmethod
    def distance_between_coords(coord1, coord2):
        """
        Calcula a distância entre duas coordenadas 3D.
        Isso pode ser usado para verificar a distância entre setores ou objetos no espaço.
        """
        distance = math.sqrt(
            (coord1[0] - coord2[0]) ** 2 +
            (coord1[1] - coord2[1]) ** 2 +
            (coord1[2] - coord2[2]) ** 2
        )
        print(f"Distância entre {coord1} e {coord2}: {distance}")
        return distance

    @staticmethod
    def random_position_spherical(radius=1000):
        """
        Gera uma posição aleatória em torno de uma esfera com o raio especificado.
        Útil para distribuir objetos no espaço tridimensional de forma esférica ao redor de um ponto.
        """
        theta = random.uniform(0, 2 * math.pi)  # Ângulo no plano XY
        phi = random.uniform(0, math.pi)        # Ângulo no plano Z
        x = radius * math.sin(phi) * math.cos(theta)
        y = radius * math.sin(phi) * math.sin(theta)
        z = radius * math.cos(phi)
        print(f"Gerando posição esférica aleatória com raio {radius}: {x}, {y}, {z}")
        return [x, y, z]
