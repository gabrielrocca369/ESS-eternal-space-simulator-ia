import random
from simulation.physics import Physics
from utils.helpers import Helpers

class CelestialObject:
    """Classe para representar objetos celestiais como planetas, estrelas, buracos negros."""
    def __init__(self, obj_type, position, mass, size):
        self.obj_type = obj_type  # Tipo do objeto (planeta, estrela, buraco negro, etc.)
        self.position = position  # Posição 3D do objeto
        self.mass = mass          # Massa do objeto (influencia na gravidade)
        self.size = size          # Tamanho físico do objeto

    def update(self):
        pass  # Implementar comportamento específico do objeto, se necessário

    def draw(self):
        pass  # Implementar renderização do objeto

class Space:
    SECTOR_SIZE = 50000  # Aumentamos o tamanho do setor para ver uma área maior do espaço
    OBJECT_TYPES = ['planet', 'star', 'black_hole']  # Tipos de objetos celestiais
    MIN_DISTANCE_TO_GENERATE_SECTOR = 25000  # Ajustado de acordo com o novo tamanho do setor
    GRAVITY_INFLUENCE_RADIUS = 10000  # Raio de influência gravitacional dos objetos

    def __init__(self):
        self.sectors = {}  # Inicializa o dicionário de setores gerados
        self.max_active_sectors = 4  # Quantidade máxima de setores ativos no universo
        self.generate_sector(0, 0, 0)  # Gera o setor inicial onde a nave começa

    def generate_objects_in_sector(self, sector_coords):
        """Gera objetos celestiais dentro de um setor."""
        objects = []
        num_objects = random.randint(5, 20)  # Número de objetos por setor
        sector_position = (
            sector_coords[0] * self.SECTOR_SIZE,
            sector_coords[1] * self.SECTOR_SIZE,
            sector_coords[2] * self.SECTOR_SIZE
        )
        for _ in range(num_objects):
            obj_type = random.choice(self.OBJECT_TYPES)
            # Posiciona objetos mais afastados do centro do setor
            local_position = Helpers.random_position(-self.SECTOR_SIZE / 2, self.SECTOR_SIZE / 2)
            position = (
                sector_position[0] + local_position[0],
                sector_position[1] + local_position[1],
                sector_position[2] + local_position[2]
            )
            mass = random.uniform(1e15, 1e18)  # Massa dos objetos
            size = random.uniform(2000, 8000)  # Tamanho dos objetos

            obj = CelestialObject(obj_type, position, mass, size)
            objects.append(obj)

        return objects

    def generate_sector(self, x, y, z):
        """Gera um setor no universo proceduralmente, baseado nas coordenadas do setor."""
        if (x, y, z) not in self.sectors:
            sector_objects = self.generate_objects_in_sector((x, y, z))
            self.sectors[(x, y, z)] = sector_objects
            print(f"Generated sector at ({x}, {y}, {z}) with {len(sector_objects)} objects")

    def get_current_sector(self, spaceship_position):
        """Calcula em qual setor a nave está com base na sua posição."""
        sector_x = int(spaceship_position[0] // self.SECTOR_SIZE)
        sector_y = int(spaceship_position[1] // self.SECTOR_SIZE)
        sector_z = int(spaceship_position[2] // self.SECTOR_SIZE)
        return (sector_x, sector_y, sector_z)

    def update(self, spaceship):
        """Atualiza os objetos no universo e aplica gravidade na nave."""
        current_sector = self.get_current_sector(spaceship.position)

        # Gera o setor atual se ainda não foi gerado
        if current_sector not in self.sectors:
            self.generate_sector(*current_sector)

        # Limitar a quantidade de setores ativos para manter o desempenho
        if len(self.sectors) > self.max_active_sectors:
            self.remove_old_sectors(current_sector)

        # Aplica forças gravitacionais na nave somente de objetos próximos
        for sector_coords, objects in self.sectors.items():
            for obj in objects:
                distance = Physics.calculate_distance(spaceship.position, obj.position)
                if 0 < distance <= self.GRAVITY_INFLUENCE_RADIUS:
                    force_magnitude = Physics.calculate_gravitational_force(
                        spaceship.mass, obj.mass, distance
                    )
                    # Limita a força gravitacional máxima
                    max_force = 1e3  # Valor ajustável para controlar a força máxima
                    force_magnitude = min(force_magnitude, max_force)

                    # Calcula o vetor direção da força (do objeto para a nave)
                    direction_vector = [
                        obj.position[0] - spaceship.position[0],
                        obj.position[1] - spaceship.position[1],
                        obj.position[2] - spaceship.position[2]
                    ]
                    # Normaliza o vetor direção
                    direction_vector = Physics.normalize_vector(direction_vector)
                    # Calcula o vetor força
                    force_vector = [component * force_magnitude for component in direction_vector]
                    # Aplica a força na nave
                    spaceship.apply_force(force_vector)

    def remove_old_sectors(self, current_sector):
        """Remove setores antigos que estão longe da nave para manter o universo sob controle."""
        sectors_to_remove = []
        for sector_coords in list(self.sectors.keys()):
            # Calcula a distância em número de setores
            distance_sectors = (
                abs(sector_coords[0] - current_sector[0]),
                abs(sector_coords[1] - current_sector[1]),
                abs(sector_coords[2] - current_sector[2])
            )
            max_distance = 1  # Remove setores que estão a mais de 1 setor de distância
            if any(d > max_distance for d in distance_sectors):
                sectors_to_remove.append(sector_coords)

        for sector in sectors_to_remove:
            del self.sectors[sector]
            print(f"Removed sector at {sector}")
