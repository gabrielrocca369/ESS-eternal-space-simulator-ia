import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
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

        # Verifica se a câmera está posicionada corretamente
        print(f"Câmera: {camera_params}")

        # Renderiza as estrelas de fundo
        self.draw_starfield()

        # Verifica se há objetos para renderizar
        total_objects = sum(len(objects) for objects in space.sectors.values())
        print(f"Total de objetos para renderizar: {total_objects}")

        # Renderiza os objetos celestiais em todos os setores
        for sector_coords, objects in space.sectors.items():
            for obj in objects:
                self.draw_object(obj)

        # Renderiza a nave espacial
        self.draw_spaceship(spaceship, camera)

        # Renderiza o nome do jogador sobre a nave
        self.draw_text_3d(spaceship.name, spaceship.position, camera)

        # Atualiza a tela
        pygame.display.flip()

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

        if obj.obj_type == 'planet':
            # Cor do planeta depende se tem água ou não
            if obj.has_water:
                glColor3f(0.0, 0.5, 1.0)  # Azul para planetas com água
            else:
                glColor3f(0.6, 0.4, 0.2)  # Marrom/cinza para planetas sem água
        elif obj.obj_type == 'star':
            # Estrela com brilho
            glColor3f(1.0, 1.0, 0.0)  # Amarelo brilhante para estrelas
            glEnable(GL_LIGHT1)
            glLightfv(GL_LIGHT1, GL_POSITION, [0.0, 0.0, 0.0, 1.0])
            glLightfv(GL_LIGHT1, GL_DIFFUSE, [1.0, 1.0, 0.8, 1.0])
            glLightfv(GL_LIGHT1, GL_SPECULAR, [1.0, 1.0, 0.8, 1.0])
        elif obj.obj_type == 'black_hole':
            # Buraco negro: esfera negra com disco de acreção
            glColor3f(0.0, 0.0, 0.0)  # Preto para o buraco negro
            self.draw_sphere(obj.size / 100.0, 30, 30)

            # Disco de acreção em torno do buraco negro
            glColor3f(1.0, 0.5, 0.0)  # Laranja brilhante para o disco de acreção
            glBegin(GL_QUADS)
            for i in range(0, 360, 10):
                theta = math.radians(i)
                next_theta = math.radians(i + 10)
                glVertex3f(math.cos(theta) * obj.size, 0.0, math.sin(theta) * obj.size)
                glVertex3f(math.cos(next_theta) * obj.size, 0.0, math.sin(next_theta) * obj.size)
                glVertex3f(math.cos(next_theta) * (obj.size + 500), 0.0, math.sin(next_theta) * (obj.size + 500))
                glVertex3f(math.cos(theta) * (obj.size + 500), 0.0, math.sin(theta) * (obj.size + 500))
            glEnd()

        # Aumenta o tamanho dos objetos na renderização
        render_size = obj.size / 100.0  # Ajuste este valor para controlar o tamanho na tela
        self.draw_sphere(render_size, 20, 20)

        glPopMatrix()  # Restaura a matriz

    def draw_sphere(self, radius, slices, stacks):
        """Desenha uma esfera usando quadric."""
        quadric = gluNewQuadric()
        gluSphere(quadric, radius, slices, stacks)
        gluDeleteQuadric(quadric)

    def draw_spaceship(self, spaceship, camera):
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

        # Desenha uma pirâmide para representar a nave
        self.draw_pyramid(50.0)
        
        # Desenha o nome do jogador sobre a nave
        if spaceship.name:
            self.draw_text_3d(spaceship.name, spaceship.position, camera)

        glPopMatrix()

    def draw_pyramid(self, size):
        """Desenha uma pirâmide com a ponta para cima."""
        half_size = size / 2.0
        glBegin(GL_TRIANGLES)
        # Face frontal
        glVertex3f(0.0, size, 0.0)  # Ponto no topo
        glVertex3f(-half_size, 0.0, half_size)  # Base esquerda
        glVertex3f(half_size, 0.0, half_size)  # Base direita

        # Face direita
        glVertex3f(0.0, size, 0.0)
        glVertex3f(half_size, 0.0, half_size)
        glVertex3f(half_size, 0.0, -half_size)

        # Face traseira
        glVertex3f(0.0, size, 0.0)
        glVertex3f(half_size, 0.0, -half_size)
        glVertex3f(-half_size, 0.0, -half_size)

        # Face esquerda
        glVertex3f(0.0, size, 0.0)
        glVertex3f(-half_size, 0.0, -half_size)
        glVertex3f(-half_size, 0.0, half_size)
        glEnd()

        # Desenha a base
        glBegin(GL_QUADS)
        glVertex3f(-half_size, 0.0, half_size)
        glVertex3f(half_size, 0.0, half_size)
        glVertex3f(half_size, 0.0, -half_size)
        glVertex3f(-half_size, 0.0, -half_size)
        glEnd()

    def draw_text_3d(self, text, position, camera):
        """Desenha o texto como uma textura no espaço 3D."""
        # Renderiza o texto em uma superfície do Pygame
        font = pygame.font.SysFont('Arial', 32)
        text_surface = font.render(text, True, (255, 255, 255))
        text_width, text_height = text_surface.get_size()
        text_data = pygame.image.tostring(text_surface, "RGBA", True)

        # Cria uma textura OpenGL a partir da superfície
        texture_id = glGenTextures(1)
        texture_id = int(texture_id)  # Converte para inteiro padrão do Python

        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text_width, text_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

        # Ativa blending para lidar com transparências
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_TEXTURE_2D)

        # Salva a matriz atual e posiciona o texto
        glPushMatrix()
        glTranslatef(position[0], position[1] + 100, position[2])

        # Alinha o texto com a câmera
        glRotatef(-camera.yaw, 0, 1, 0)
        glRotatef(-camera.pitch, 1, 0, 0)
        glColor3f(1.0, 1.0, 1.0)

        # Ajusta o tamanho do quad de acordo com a escala desejada
        scale = 0.25  # Ajuste este valor para redimensionar o texto
        width = text_width * scale
        height = text_height * scale

        # Desenha um quad com a textura do texto
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(-width / 2, -height / 2, 0)
        glTexCoord2f(1, 0)
        glVertex3f(width / 2, -height / 2, 0)
        glTexCoord2f(1, 1)
        glVertex3f(width / 2, height / 2, 0)
        glTexCoord2f(0, 1)
        glVertex3f(-width / 2, height / 2, 0)
        glEnd()

        # Restaura a matriz e desativa texturas e blending
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)

        # Certifique-se de passar uma lista com o ID da textura
        glDeleteTextures([texture_id])
