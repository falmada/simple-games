import pygame
import random
import datetime

# Inicializar pygame
pygame.init()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

# Configuración de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Juego de Multiplicación")

# Fuentes
font = pygame.font.SysFont(None, 55)
input_font = pygame.font.SysFont(None, 35)

# Función para mostrar texto en la pantalla
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Clase para representar el número cayendo
class FallingNumber:
    def __init__(self, speed):
        self.value = self.generate_valid_number()
        self.x = random.randint(0, screen_width - 50)
        self.y = -50
        self.speed = speed
        self.color = BLACK
        self.attempts = 0
        self.partial_prompt = self.generate_partial_prompt()

    def generate_valid_number(self):
        factor1 = random.randint(2, 10)
        factor2 = random.randint(2, 10)
        return factor1 * factor2

    def generate_partial_prompt(self):
        factors = [(i, self.value // i) for i in range(2, 11) if self.value % i == 0]
        factor1, factor2 = random.choice(factors)
        return f"{factor1} x "

    def fall(self):
        self.y += self.speed

    def draw(self, surface):
        draw_text(str(self.value), font, self.color, surface, self.x, self.y)

# Función para leer el puntaje más alto desde el archivo
def read_high_score():
    try:
        with open("high_score.txt", "r") as file:
            line = file.readline()
            if line:
                score, date = line.split(",")
                return int(score), date.strip()
    except FileNotFoundError:
        return 0, ""
    return 0, ""

# Función para escribir el puntaje más alto en el archivo
def write_high_score(score, date):
    with open("high_score.txt", "w") as file:
        file.write(f"{score},{date}")

# Inicialización del juego
def start_game(speed):
    clock = pygame.time.Clock()
    falling_number = FallingNumber(speed)
    lives = 3
    score = 0
    input_text = falling_number.partial_prompt
    failed_numbers = []

    high_score, high_score_date = read_high_score()

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if len(input_text) > len(falling_number.partial_prompt):
                        input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    try:
                        partial_factor1 = int(falling_number.partial_prompt.split('x')[0])
                        factor2 = int(input_text.split('x')[1].strip())
                        product = partial_factor1 * factor2
                        if falling_number.value == product:
                            score += 1
                            falling_number = FallingNumber(speed)
                            input_text = falling_number.partial_prompt
                        else:
                            score -= 1
                            falling_number.attempts += 1
                            if falling_number.attempts == 1:
                                falling_number.color = ORANGE
                                input_text = falling_number.partial_prompt
                            elif falling_number.attempts == 2:
                                lives -= 1
                                failed_numbers.append(falling_number.value)
                                falling_number = FallingNumber(speed)
                                input_text = falling_number.partial_prompt
                                if lives == 0:
                                    running = False
                    except ValueError:
                        input_text = falling_number.partial_prompt
                elif event.unicode.isdigit():
                    input_text += event.unicode

        falling_number.fall()
        falling_number.draw(screen)
        if falling_number.y > screen_height:
            lives -= 1
            failed_numbers.append(falling_number.value)
            falling_number = FallingNumber(speed)
            input_text = falling_number.partial_prompt
            if lives == 0:
                running = False

        draw_text(f"Vidas: {lives}", font, RED, screen, 10, 10)
        draw_text(f"Puntaje: {score}", font, RED, screen, screen_width - 200, 10)
        draw_text(f"Respuesta: {input_text}", input_font, BLACK, screen, 10, screen_height - 50)
        pygame.display.flip()
        clock.tick(30)

    # Actualizar puntaje más alto si es necesario
    if score > high_score:
        high_score = score
        high_score_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        write_high_score(high_score, high_score_date)

    # Mostrar puntaje final y detalles de errores
    screen.fill(WHITE)
    draw_text(f"Puntaje Final: {score}", font, RED, screen, screen_width // 2 - 100, screen_height // 2 - 150)
    y_offset = screen_height // 2 - 100
    for number in failed_numbers:
        factor1 = random.randint(2, 10)
        factor2 = number // factor1
        draw_text(f"{number} -> {factor1}x{factor2}", input_font, BLACK, screen, screen_width // 2 - 100, y_offset)
        y_offset += 40
    draw_text(f"Puntaje Más Alto: {high_score} ({high_score_date})", input_font, BLACK, screen, screen_width // 2 - 150, y_offset)
    draw_text("Presiona 'R' para volver a jugar o 'ESC' para salir", input_font, BLACK, screen, screen_width // 2 - 200, screen_height - 100)
    pygame.display.flip()

    # Esperar entrada del usuario para reiniciar o salir
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    start_game(speed)
                if event.key == pygame.K_ESCAPE:
                    waiting = False
                    pygame.quit()
                    return

# Configuración de velocidad ajustable
start_game(speed=2)
