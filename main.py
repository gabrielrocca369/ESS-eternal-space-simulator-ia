import sys
import os
import logging
import time
import pygame
import json
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from utils.logger import GameLogger

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

# Inicializa o logger para salvar e carregar o progresso
game_logger = GameLogger()

def load_logo():
    """Carrega o logo do jogo (um .gif ou .png de uma galáxia)."""
    logo = pygame.image.load("logo_galaxy.gif").convert_alpha()  # Logo da galáxia em pixel art
    return pygame.transform.scale(logo, (300, 300))  # Ajusta o tamanho do logo

def display_menu(screen, font, logo):
    """Exibe a tela inicial com as opções de jogo, centralizando o logo e as opções."""
    screen.fill((0, 0, 0))  # Preenche a tela com preto

    # Renderiza o logo na parte superior, centralizado
    logo_rect = logo.get_rect(center=(screen.get_width() // 2, 180))
    screen.blit(logo, logo_rect)

    # Renderiza o texto centralizado na tela
    title_text = font.render("Eternal Space Simulator", True, (255, 255, 255))
    new_game_text = font.render("New Game - Press Enter to Start", True, (255, 255, 255))
    instructions_text = font.render("Press K to See Keyboard Actions", True, (255, 255, 255))

    # Calcula a posição central para o texto
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    new_game_rect = new_game_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))
    instructions_rect = instructions_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 150))

    # Desenha os textos
    screen.blit(title_text, title_rect)
    screen.blit(new_game_text, new_game_rect)
    screen.blit(instructions_text, instructions_rect)

    # Atualiza a tela
    pygame.display.flip()

def get_player_name(screen, font):
    """Exibe uma tela para o jogador digitar seu nome."""
    name = ""
    input_active = True
    instruction_text = font.render("Digite seu nome:", True, (255, 255, 255))

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Pressiona Enter para finalizar a digitação
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:  # Apaga o último caractere
                    name = name[:-1]
                else:
                    name += event.unicode  # Adiciona o caractere digitado

        # Renderiza o nome à medida que é digitado
        screen.fill((0, 0, 0))
        screen.blit(instruction_text, (screen.get_width() // 2 - 100, screen.get_height() // 2 - 50))
        name_text = font.render(name, True, (255, 255, 255))
        screen.blit(name_text, (screen.get_width() // 2 - 100, screen.get_height() // 2))
        pygame.display.flip()

    return name

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
        screen.blit(instruction_text, (screen.get_width() // 2 - 150, 100 + i * 40))  # Centraliza cada linha

    # Atualiza a tela
    pygame.display.flip()

def display_confirm_exit(screen, font):
    """Exibe a mensagem de confirmação para retornar ao menu."""
    screen.fill((0, 0, 0))  # Preenche a tela com preto
    # Renderiza a mensagem de confirmação
    message_text = font.render("Confirmar retorno ao menu? (Y/N)", True, (255, 255, 255))
    screen.blit(message_text, (screen.get_width() // 2 - 200, screen.get_height() // 2))
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
        display = (1280, 720)  # Resolução 720p
        screen = pygame.display.set_mode(display)
        pygame.display.set_caption("Eternal Space Simulator")

        # Carrega o logo
        logo = load_logo()

        # Define a fonte para exibir o texto no menu
        font = pygame.font.SysFont("Arial", 30)

        # Exibe o menu inicial
        in_menu = True
        in_instructions = False

        while in_menu:
            if in_instructions:
                display_instructions(screen, font)
            else:
                display_menu(screen, font, logo)

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

        # Carrega progresso salvo, se houver
        progress = game_logger.load_progress()
        if progress:
            player_name = progress['player_name']
        else:
            # Solicita o nome do jogador se não houver progresso salvo
            player_name = get_player_name(screen, font)

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

        # Inicializa o universo e a nave
        space = Space()
        spaceship = Spaceship(name=player_name, max_speed=80000)
        distance_traveled = 0
        play_time = 0

        if progress:
            # Carrega o progresso salvo na nave e nos objetos
            spaceship.position = progress['position']
            spaceship.velocity = progress['velocity']
            distance_traveled = progress['distance_traveled']
            play_time = progress['play_time']
            # Se você estiver salvando o estado do universo, carregue aqui
            # space.load_game_state(progress['space_state'])

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
                    game_logger.save_progress(player_name, spaceship, distance_traveled, play_time)
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_logger.save_progress(player_name, spaceship, distance_traveled, play_time)
                        confirm_exit = display_confirm_exit(screen, font)
                        if confirm_exit:
                            running = False
                            start_simulation()
                            return  # Encerra o loop atual

            # Captura os inputs do teclado
            keys = pygame.key.get_pressed()

            # Calcula o tempo decorrido
            current_time = time.time()
            delta_time = current_time - last_time
            play_time += delta_time
            last_time = current_time

            # Atualiza a física do universo e a posição da nave
            space.update(spaceship)
            spaceship.update(delta_time, keys)  # Passa delta_time e keys
            distance_traveled += sum([abs(v * delta_time) for v in spaceship.velocity])

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
