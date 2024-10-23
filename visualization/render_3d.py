import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import math  # Import necessário para cálculos matemáticos
import random  # Import necessário para gerar o starfield

class Renderer:
    def __init__(self):
        """Inicializa parâmetros do renderizador."""
        # Configura a cor de limpeza (fundo preto)
        glClearColor(0.1, 0.1, 0.1, 1.0)
        # Ativa o teste de profundidade
        glEnable(GL_DEPTH_TEST)
        self.starfield = self.generate_starfield(500)  # Gera 500 estrelas de fundo

        # Configura a iluminação
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 0, 1))  # Luz na posição da câmera
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.7, 0.7, 0.7, 1.0))
        glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

        print("Renderizador inicializado com sucesso.")

    def generate_starfield(self, num_stars):
        """Gera uma lista de posições para as estrelas de fundo."""
        stars = []
        for _ in range(num_stars):
            x = random.uniform(-50000, 50000)
            y = random.uniform(-50000, 50000)
            z = random.uniform(-50000, 50000)
            stars.append((x, y, z))
        return stars

    def render(self, space, spaceship, camera):
        """Renderiza os objetos do espaço e a nave."""
        # Limpa a tela e o buffer de profundidade
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Carrega a matriz de identidade
        glLoadIdentity()

        # Posiciona a câmera usando os parâmetros retornados por get_view_matrix
        camera_params = camera.get_view_matrix()
        gluLookAt(*camera_params)

        # Renderiza as estrelas de fundo
        self.draw_starfield()

        # Renderiza os objetos celestiais em todos os setores
        for sector_coords, objects in space.sectors.items():
            for obj in objects:
                self.draw_object(obj)

        # Renderiza a nave espacial
        self.draw_spaceship(spaceship)

    def draw_starfield(self):
        """Desenha as estrelas de fundo."""
        glDisable(GL_LIGHTING)
        glPointSize(1.0)
        glBegin(GL_POINTS)
        glColor3f(1.0, 1.0, 1.0)  # Cor branca para as estrelas
        for star in self.starfield:
            glVertex3f(*star)
        glEnd()
        glEnable(GL_LIGHTING)

    def draw_object(self, obj):
        """Desenha um objeto celestial como planeta, estrela ou buraco negro."""
        glPushMatrix()  # Salva a matriz atual para restaurá-la mais tarde
        # Posiciona o objeto no espaço
        glTranslatef(float(obj.position[0]), float(obj.position[1]), float(obj.position[2]))

        # Define a cor do objeto baseado no tipo
        if obj.obj_type == 'planet':
            glColor3f(0.0, 0.5, 1.0)  # Azul para planetas
        elif obj.obj_type == 'star':
            glColor3f(1.0, 1.0, 0.0)  # Amarelo para estrelas
        elif obj.obj_type == 'black_hole':
            glColor3f(0.5, 0.0, 0.5)  # Roxo para buracos negros

        # Aumenta o tamanho dos objetos na renderização
        render_size = obj.size / 500.0  # Ajuste este valor para controlar o tamanho na tela
        self.draw_sphere(render_size, 20, 20)

        glPopMatrix()  # Restaura a matriz

    def draw_sphere(self, radius, slices, stacks):
        """Desenha uma esfera usando quadric."""
        quadric = gluNewQuadric()
        gluSphere(quadric, radius, slices, stacks)
        gluDeleteQuadric(quadric)

    def draw_spaceship(self, spaceship):
        """Desenha a nave espacial."""
        glPushMatrix()
        # Posiciona a nave no espaço
        glTranslatef(float(spaceship.position[0]), float(spaceship.position[1]), float(spaceship.position[2]))

        # Calcula a velocidade atual da nave
        speed = math.sqrt(sum(v ** 2 for v in spaceship.velocity))

        # Define um limiar para considerar a nave parada
        speed_threshold = 0.1  # Ajuste conforme necessário

        # Verifica se a nave está em movimento
        if speed > speed_threshold:
            glColor3f(0.5, 1.0, 0.5)  # Verde claro quando em movimento
        else:
            glColor3f(0.0, 0.5, 1.0)  # Azul quando parada

        # Desenha um cubo para representar a nave
        self.draw_cube(40.0)
        glPopMatrix()

    def draw_cube(self, size):
        """Desenha um cubo com o tamanho especificado."""
        half_size = size / 2.0
        glBegin(GL_QUADS)
        # Face frontal
        glVertex3f(-half_size, -half_size, half_size)
        glVertex3f(half_size, -half_size, half_size)
        glVertex3f(half_size, half_size, half_size)
        glVertex3f(-half_size, half_size, half_size)
        # Face traseira
        glVertex3f(-half_size, -half_size, -half_size)
        glVertex3f(-half_size, half_size, -half_size)
        glVertex3f(half_size, half_size, -half_size)
        glVertex3f(half_size, -half_size, -half_size)
        # Face esquerda
        glVertex3f(-half_size, -half_size, -half_size)
        glVertex3f(-half_size, -half_size, half_size)
        glVertex3f(-half_size, half_size, half_size)
        glVertex3f(-half_size, half_size, -half_size)
        # Face direita
        glVertex3f(half_size, -half_size, -half_size)
        glVertex3f(half_size, half_size, -half_size)
        glVertex3f(half_size, half_size, half_size)
        glVertex3f(half_size, -half_size, half_size)
        # Face superior
        glVertex3f(-half_size, half_size, -half_size)
        glVertex3f(-half_size, half_size, half_size)
        glVertex3f(half_size, half_size, half_size)
        glVertex3f(half_size, half_size, -half_size)
        # Face inferior
        glVertex3f(-half_size, -half_size, -half_size)
        glVertex3f(half_size, -half_size, -half_size)
        glVertex3f(half_size, -half_size, half_size)
        glVertex3f(-half_size, -half_size, half_size)
        glEnd()
