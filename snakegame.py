import random

import pygame

# Настройки экрана
WIDTH = 640
HEIGHT = 480
CELL_SIZE = 20

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Изгиб Питона")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position, color):
        self.position = position
        self.color = color

    def draw(self, surface):
        """Рисует объект как квадрат размера CELL_SIZE."""
        rect = pygame.Rect(
            self.position[0],
            self.position[1],
            CELL_SIZE,
            CELL_SIZE,
        )
        pygame.draw.rect(surface, self.color, rect)


class Apple(GameObject):
    """Яблоко — наследник GameObject, саморазмещается случайно."""

    def __init__(self, color):
        position = self._random_position()
        super().__init__(position, color)

    def _random_position(self):
        """
        Возвращает случайную позицию на сетке.
        Координаты кратны CELL_SIZE.
        """
        max_x = (WIDTH - CELL_SIZE) // CELL_SIZE
        max_y = (HEIGHT - CELL_SIZE) // CELL_SIZE
        x = random.randint(0, max_x) * CELL_SIZE
        y = random.randint(0, max_y) * CELL_SIZE
        return x, y

    def relocate(self):
        """Перемещает яблоко в новую случайную клетку."""
        self.position = self._random_position()


class Snake:
    """Класс змейки: хранит тело, двигается и проверяет столкновения."""

    def __init__(self):
        self.body = [(CELL_SIZE * 5, CELL_SIZE * 5)]
        self.color = GREEN
        self.direction = pygame.K_RIGHT
        self.length = 1

    def head_position(self):
        """Возвращает координаты головы (первого сегмента)."""
        return self.body[0]

    def move(self):
        """
        Сдвигает змейку в направлении self.direction.
        По достижении границы телепортирует на противоположный край.
        """
        x, y = self.head_position()

        if self.direction == pygame.K_UP:
            y -= CELL_SIZE
        elif self.direction == pygame.K_DOWN:
            y += CELL_SIZE
        elif self.direction == pygame.K_LEFT:
            x -= CELL_SIZE
        elif self.direction == pygame.K_RIGHT:
            x += CELL_SIZE

        new_head = (x % WIDTH, y % HEIGHT)
        self.body.insert(0, new_head)

        if len(self.body) > self.length:
            self.body.pop()

    def draw(self, surface):
        """Рисует все сегменты змейки."""
        for segment in self.body:
            rect = pygame.Rect(
                segment[0],
                segment[1],
                CELL_SIZE,
                CELL_SIZE,
            )
            pygame.draw.rect(surface, self.color, rect)

    def change_direction(self, key):
        """
        Меняет направление, запрещая поворот на 180°.
        `key` — одна из pygame.K_… констант.
        """
        opposites = {
            pygame.K_UP: pygame.K_DOWN,
            pygame.K_DOWN: pygame.K_UP,
            pygame.K_LEFT: pygame.K_RIGHT,
            pygame.K_RIGHT: pygame.K_LEFT,
        }
        if key != opposites.get(self.direction):
            self.direction = key

    def check_collision(self):
        """Возвращает True, если голова сталкивается с телом."""
        return self.head_position() in self.body[1:]


def draw_text(surface, text, position):
    """Выводит текст `text` белым цветом в точке `position`."""
    rendered = font.render(text, True, WHITE)
    surface.blit(rendered, position)


def main():
    """Запуск главного цикла игры."""
    snake = Snake()
    apple = Apple(RED)
    score = 0
    running = True

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                snake.change_direction(event.key)

        snake.move()

        if snake.head_position() == apple.position:
            score += 1
            snake.length += 1
            apple.relocate()

        if snake.check_collision():
            running = False

        snake.draw(screen)
        apple.draw(screen)
        draw_text(screen, f"Score: {score}", (10, 10))

        pygame.display.update()
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()
