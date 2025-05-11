import pygame
import sys
from random import randint

# Константы
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
BOARD_BACKGROUND_COLOR = (40, 40, 40)
FPS = 20


class GameObject:
    """Базовый класс."""
    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Шаблон метода отрисовки."""
        pass


class Apple(GameObject):
    """Класс яблока. наследует от GameObject."""
    def __init__(self):
        position = self.randomize_position()
        super().__init__(position, body_color=(255, 0, 0))

    def randomize_position(self):
        """Генерирует случайную позицию по сетке."""
        x = randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        y = randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        return x, y

    def relocate(self):
        """Перемещает яблоко в новую позицию."""
        self.position = self.randomize_position()

    def draw(self, surface):
        """Рисует яблоко."""
        rect = pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Класс змейки. наследует от GameObject."""
    def __init__(self):
        center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        super().__init__(center, body_color=(0, 255, 0))
        self.positions = [center]
        self.length = 1
        self.direction = (1, 0) 
        self.next_direction = None
        self.last = None  

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Предотвращая разворот на 180 градусов."""
        if self.next_direction:
            opposite = (-self.direction[0], -self.direction[1])
            if self.next_direction != opposite:
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Смещает змейку на одну клетку в текущем направлении. Реализует телепортацию по краям экрана."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.last = self.positions[-1]
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        """Сбрасывает змейку. """
        center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.positions = [center]
        self.length = 1
        self.direction = (1, 0)
        self.next_direction = None
        self.last = None
    def draw(self, surface):
        """Рисует все сегменты змейки стирает последний сегмент цветом фона. """
        if self.last:
            rect = pygame.Rect(self.last[0], self.last[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect)
        for pos in self.positions:
            rect = pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш и устанавливает следующий вектор направления. """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = (0, -1)
            elif event.key == pygame.K_DOWN:
                snake.next_direction = (0, 1)
            elif event.key == pygame.K_LEFT:
                snake.next_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = (1, 0)


def main():
    """Инициализация Pygame и создание окна игры."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    snake = Snake()
    apple = Apple()
    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.relocate()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
