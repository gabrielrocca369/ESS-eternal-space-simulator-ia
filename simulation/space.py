import random
from simulation.physics import Physics
from utils.helpers import Helpers

class CelestialObject:
    """Classe para representar objetos celestiais como planetas, estrelas, buracos negros."""
    def __init__(self, obj_type, position, mass, size, has_water=False, name=None):
        self.obj_type = obj_type  # Tipo do objeto (planeta, estrela, buraco negro, etc.)
        self.position = position  # Posição 3D do objeto
        self.mass = mass          # Massa do objeto (influencia na gravidade)
        self.size = size          # Tamanho físico do objeto
        self.has_water = has_water  # Indica se o planeta tem água
        self.name = name          # Nome do corpo celeste (definido pelo jogador ou None)

    def to_dict(self):
        """Converte o objeto em um dicionário para facilitar o salvamento."""
        return {
            "obj_type": self.obj_type,
            "position": self.position,
            "mass": self.mass,
            "size": self.size,
            "has_water": self.has_water,
            "name": self.name
        }

    @classmethod
    def from_dict(cls, data):
        """Cria um objeto CelestialObject a partir de um dicionário."""
        return cls(
            obj_type=data["obj_type"],
            position=data["position"],
            mass=data["mass"],
            size=data["size"],
            has_water=data.get("has_water", False),
            name=data.get("name", None)
        )

    def update(self):
        pass  # Implementar comportamento específico do objeto, se necessário

class Space:
    SECTOR_SIZE = 70000  # Tamanho do setor
    OBJECT_TYPES = ['planet', 'star', 'black_hole']  # Tipos de objetos celestiais
    GRAVITY_INFLUENCE_RADIUS = 6000  # Raio de influência gravitacional dos objetos

    def __init__(self):
        self.sectors = {}  # Inicializa o dicionário de setores gerados
        self.max_active_sectors = 5  # Quantidade máxima de setores ativos no universo
        self.generate_sector(0, 0, 0)  # Gera o setor inicial onde a nave começa

    def generate_objects_in_sector(self, sector_coords):
        """Gera objetos celestiais dentro de um setor."""
        objects = []
        num_objects = random.randint(7, 11)  # Ajuste o número de objetos por setor
        print(f"Gerando {num_objects} objetos no setor {sector_coords}")
        sector_position = (
            sector_coords[0] * self.SECTOR_SIZE,
            sector_coords[1] * self.SECTOR_SIZE,
            sector_coords[2] * self.SECTOR_SIZE
        )
        for _ in range(num_objects):
            obj_type = random.choice(self.OBJECT_TYPES)
            # Posiciona objetos próximos ao centro do setor
            local_position = Helpers.random_position(-self.SECTOR_SIZE / 4, self.SECTOR_SIZE / 4)
            position = (
                sector_position[0] + local_position[0],
                sector_position[1] + local_position[1],
                sector_position[2] + local_position[2]
            )
            mass = random.uniform(1e15, 1e18)  # Massa dos objetos
            size = random.uniform(2000, 18000)  # Tamanho dos objetos

            # Atribuir aleatoriamente se um planeta tem água ou não
            has_water = False
            if obj_type == 'planet':
                has_water = random.choice([True, False])  # 50% de chance de ter água

            obj = CelestialObject(obj_type, position, mass, size, has_water)
            print(f"Criado objeto {obj.obj_type} na posição {obj.position}, com água: {obj.has_water}")
            objects.append(obj)

        return objects

    def generate_sector(self, x, y, z):
        """Gera um setor no universo proceduralmente, baseado nas coordenadas do setor."""
        if (x, y, z) not in self.sectors:
            sector_objects = self.generate_objects_in_sector((x, y, z))
            self.sectors[(x, y, z)] = sector_objects
            print(f"Setor gerado em ({x}, {y}, {z}) com {len(sector_objects)} objetos")

    def get_current_sector(self, spaceship_position):
        """Calcula em qual setor a nave está com base na sua posição."""
        sector_x = int(spaceship_position[0] // self.SECTOR_SIZE)
        sector_y = int(spaceship_position[1] // self.SECTOR_SIZE)
        sector_z = int(spaceship_position[2] // self.SECTOR_SIZE)
        return (sector_x, sector_y, sector_z)

    def update(self, spaceship):
        """Atualiza os objetos no universo e aplica gravidade na nave."""
        current_sector = self.get_current_sector(spaceship.position)
        print(f"Setor atual da nave: {current_sector}")

        # Gera o setor atual se ainda não foi gerado
        if current_sector not in self.sectors:
            self.generate_sector(*current_sector)

        # Limitar a quantidade de setores ativos para manter o desempenho
        if len(self.sectors) > self.max_active_sectors:
            self.remove_old_sectors(current_sector)

        # Imprime os setores ativos e quantos objetos há em cada um
        print(f"Setores ativos: {list(self.sectors.keys())}")
        for sector_coords, objects in self.sectors.items():
            print(f"Setor {sector_coords} tem {len(objects)} objetos")

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

    def save_game_state(self):
        """Salva o estado do jogo em formato JSON."""
        game_state = {
            "sectors": {
                str(sector_coords): [obj.to_dict() for obj in objects]
                for sector_coords, objects in self.sectors.items()
            }
        }
        return game_state

    def load_game_state(self, game_state):
        """Carrega o estado do jogo a partir de um arquivo JSON."""
        self.sectors = {
            eval(sector_coords): [CelestialObject.from_dict(obj_data) for obj_data in objects]
            for sector_coords, objects in game_state.get("sectors", {}).items()
        }

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
            print(f"Setor removido em {sector}")
