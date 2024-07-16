import pygame
import random
from collections import defaultdict

# Game settings
WIDTH, HEIGHT = 800, 600
STATS_WIDTH = 200
DOT_SIZE = 5
INITIAL_DOTS = {'male': 50, 'female': 50}
AGE_TO_REPRODUCE = 15
MAX_AGE = 70
DEATH_RATE = 0.00001
REPRODUCTION_INDICATOR_DURATION = 180  # in frames (3 seconds at 60 FPS)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH + STATS_WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Dot class
class Dot:
    def __init__(self, sex, age=0):
        self.sex = sex
        self.age = age
        self.color = (255, 0, 0) if sex == 'male' else (0, 255, 255)
        self.x = random.randint(0, WIDTH - DOT_SIZE)
        self.y = random.randint(0, HEIGHT - DOT_SIZE)
        self.reproduction_indicator = 0

    def move(self):
        self.x += random.randint(-5, 5)
        self.y += random.randint(-5, 5)
        self.x = max(0, min(self.x, WIDTH - DOT_SIZE))
        self.y = max(0, min(self.y, HEIGHT - DOT_SIZE))

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, DOT_SIZE, DOT_SIZE))
        if self.reproduction_indicator > 0:
            pygame.draw.circle(screen, (0, 255, 0), (self.x + DOT_SIZE // 2, self.y + DOT_SIZE // 2), DOT_SIZE * 2, 1)
            self.reproduction_indicator -= 1

    def is_colliding_with(self, other):
        return self.x == other.x and self.y == other.y and self.age >= AGE_TO_REPRODUCE and other.age >= AGE_TO_REPRODUCE

# Create initial dots
dots = [Dot(sex) for sex, count in INITIAL_DOTS.items() for _ in range(count)]
born_count = sum(INITIAL_DOTS.values())
dead_count = 0

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  # Clear screen

    total_age = 0
    oldest_male_age = oldest_female_age = 0

    # Update and draw dots
    for dot in dots:
        dot.move()
        dot.draw()
        dot.age += 1 / 60  # Increase age
        total_age += dot.age

        # Track oldest male and female
        if dot.sex == 'male' and dot.age > oldest_male_age:
            oldest_male_age = dot.age
        elif dot.sex == 'female' and dot.age > oldest_female_age:
            oldest_female_age = dot.age

    # Check for collisions and reproduction
    for i, dot in enumerate(dots):
        for other_dot in dots[i+1:]:
            if dot.is_colliding_with(other_dot) and dot.sex != other_dot.sex:
                number_of_babies = random.choices([1, 2, 3, 4], weights=[0.8, 0.1, 0.05, 0.05], k=1)[0]
                for _ in range(number_of_babies):
                    new_dot = Dot(random.choice(['male', 'female']))
                    new_dot.reproduction_indicator = REPRODUCTION_INDICATOR_DURATION
                    dots.append(new_dot)
                    born_count += 1
                break

    # Check for death
    for dot in dots[:]:
        death_chance = DEATH_RATE
        if dot.age > MAX_AGE:
            death_chance += (dot.age - MAX_AGE) * 0.05
        if random.random() < death_chance:
            dots.remove(dot)
            dead_count += 1

    # Draw statistics
    stats = {
        'Male Count': sum(1 for d in dots if d.sex == 'male'),
        'Female Count': sum(1 for d in dots if d.sex == 'female'),
        'Total Dots': len(dots),
        'Oldest Male Age': round(oldest_male_age),
        'Oldest Female Age': round(oldest_female_age),
        'Average Age': round(total_age / len(dots), 2) if dots else 0,
        'Total Born': born_count,
        'Total Died': dead_count
    }

    for i, (key, value) in enumerate(stats.items()):
        text = f'{key}: {value}'
        screen.blit(pygame.font.SysFont(None, 30).render(text, True, (0, 0, 0)), (WIDTH + 10, 30 * i))

    pygame.display.flip()  # Update the screen
    clock.tick(60)  # 60 FPS

pygame.quit()
