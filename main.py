import sys
import os
import logging
import time
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Configura o logging para registrar erros no arquivo errorlog.txt
logging.basicConfig(filename='errorlog.txt', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_exception(exc_type, exc_value, exc_traceback):
    """Função para capturar exceções não tratadas e registrar no log."""
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

# Captura exceções não tratadas no programa
sys.excepthook = log_exception

# Adiciona o diretório raiz ao sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Importações dos módulos
from simulation.space import Space
from simulation.spaceship import Spaceship
from visualization.render_3d import Renderer
from visualization.camera import Camera

def display_menu(screen, font):
    """Exibe a tela inicial com as opções de jogo."""
    screen.fill((0, 0, 0))  # Preenche a tela com preto

    # Renderiza o texto na tela
    title_text = font.render("Eternal Space Simulator", True, (255, 255, 255))
    new_game_text = font.render("New Game - Press Enter to Start", True, (255, 255, 255))
    instructions_text = font.render("Press K to See Keyboard Actions", True, (255, 255, 255))

    # Posiciona o texto no centro da tela
    screen.blit(title_text, (100, 100))
    screen.blit(new_game_text, (100, 200))
    screen.blit(instructions_text, (100, 300))

    # Atualiza a tela
    pygame.display.flip()

def display_instructions(screen, font):
    """Exibe as instruções de controle do teclado."""
    screen.fill((0, 0, 0))  # Preenche a tela com preto

    # Renderiza o texto das instruções
    instructions = [
        "W - Move Forward",
        "S - Move Backward",
        "A - Move Left",
        "D - Move Right",
        "Q - Move Up",
        "E - Move Down",
        "Press Esc to Go Back to Menu"
    ]

    for i, line in enumerate(instructions):
        instruction_text = font.render(line, True, (255, 255, 255))
        screen.blit(instruction_text, (100, 100 + i * 40))  # Posiciona cada linha de instrução

    # Atualiza a tela
    pygame.display.flip()

def display_confirm_exit(screen, font):
    """Exibe a mensagem de confirmação para retornar ao menu."""
    screen.fill((0, 0, 0))  # Preenche a tela com preto
    # Renderiza a mensagem de confirmação
    message_text = font.render("Confirmar retorno ao menu? (Y/N)", True, (255, 255, 255))
    screen.blit(message_text, (100, 100))
    pygame.display.flip()

    # Espera pelo input do jogador
    confirming = True
    while confirming:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True  # Jogador confirmou
                elif event.key == pygame.K_n:
                    return False  # Jogador cancelou
    return False  # Caso padrão

def start_simulation():
    try:
        # Inicializa o pygame
        pygame.init()
        display = (1280, 720)  # Alterado para resolução 720p
        screen = pygame.display.set_mode(display)
        pygame.display.set_caption("Eternal Space Simulator")

        # Define a fonte para exibir o texto no menu
        font = pygame.font.SysFont("Arial", 30)

        # Exibe o menu inicial
        in_menu = True
        in_instructions = False

        while in_menu:
            if in_instructions:
                display_instructions(screen, font)
            else:
                display_menu(screen, font)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Pressiona Enter para iniciar o jogo
                        in_menu = False
                        in_instructions = False
                    elif event.key == pygame.K_k:  # Pressiona K para ver as instruções
                        in_instructions = True
                    elif event.key == pygame.K_ESCAPE and in_instructions:
                        in_instructions = False  # Volta ao menu se estiver nas instruções

        # Reinicializa a janela para o modo OpenGL
        pygame.display.quit()
        pygame.display.init()
        screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Eternal Space Simulator")

        # Configura a projeção e o modelo OpenGL
        glViewport(0, 0, display[0], display[1])
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(75, (display[0] / display[1]), 0.1, 400000.0)  # Campo de visão ajustado para 75
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glEnable(GL_DEPTH_TEST)

        # Força a janela a receber foco
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        pygame.event.clear()
        pygame.display.flip()

        # Define a fonte novamente após mudar para o modo OpenGL
        font = pygame.font.SysFont("Arial", 30)

        # Inicializa o universo e a nave
        space = Space()
        spaceship = Spaceship(max_speed=50000)

        # Inicializa o motor de renderização e a câmera
        renderer = Renderer()
        camera = Camera()

        # Definir o tempo entre atualizações (time_step) para física e renderização
        time_step = 0.016  # Aproximadamente 60 FPS (1/60)
        last_time = time.time()

        # Loop principal da simulação
        running = True
        while running:
            # Processa os eventos do Pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Chama a função para confirmar se o jogador quer voltar ao menu
                        confirm_exit = display_confirm_exit(screen, font)
                        if confirm_exit:
                            # Retorna ao menu inicial
                            running = False
                            start_simulation()
                            return  # Encerra o loop atual

            # Captura os inputs do teclado
            keys = pygame.key.get_pressed()

            # Calcula o tempo decorrido
            current_time = time.time()
            delta_time = current_time - last_time
            last_time = current_time

            # Atualiza a física do universo e a posição da nave
            space.update(spaceship)
            spaceship.update(delta_time, keys)  # Passa delta_time e keys

            # Atualiza a rotação da câmera
            camera.update_camera_rotation(keys, delta_time)

            # A câmera segue a nave com suavidade
            camera.follow_target(spaceship.position, spaceship.direction)

            # Renderiza o estado atual do universo, da nave e da câmera
            renderer.render(space, spaceship, camera)

            # Atualiza a tela
            pygame.display.flip()

            # Pausa para manter o tempo constante entre atualizações (time_step)
            time.sleep(max(0, time_step - delta_time))

        pygame.quit()

    except Exception as e:
        logging.error("Error in start_simulation", exc_info=True)
        print(f"Ocorreu um erro durante a execução da simulação. Confira 'errorlog.txt' para mais detalhes.")

if __name__ == "__main__":
    start_simulation()
