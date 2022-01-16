import math


# Настройки монитора
WIDTH = 1200
HEIGHT = 800

# Основные настройки
FPS = 60

# цвета
colors = \
    {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "gray": (125, 125, 125),
    "light-gray": (200, 200, 200),
    "light-blue": (0, 160, 255),
    "yellow": (220, 220, 0)
    }

# Прочее
TILE_WIDTH = 100
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2

# Ray-casting технология
len_of_rays = 1000  # Длина луча
FOV = math.pi / 3  # Угол обзора
HALF_FOV = FOV / 2

NUM_OF_RAYS = 300  # Количество лучей испускаемых камерой
dt_ANGLE = FOV / NUM_OF_RAYS  # Угол между лучами

DIST = NUM_OF_RAYS / (2 * math.tan(HALF_FOV))  # Расстояние до объекта
PROJECTION_C = 3 * DIST * TILE_WIDTH  # Коэфициент отображения
SCALE = WIDTH // NUM_OF_RAYS  # Коэфициент масштабирования объекта на экране
PENTA_HEIGHT = 5 * HEIGHT
DOUBLE_HEIGHT = 2 * HEIGHT

# Мини-карта
MINIMAP_SCALE = 5
MINIMAP_RESOLUTION = (260, 180)
MAP_SCALE = 2 * MINIMAP_SCALE
MAP_TILE = TILE_WIDTH // MAP_SCALE
MAP_POS = (0, 620)

# Текстуры
T_WIDTH, T_HEIGHT = 1200, 1200
T_Scale = T_WIDTH // TILE_WIDTH
HALF_TEX_HEIGHT = T_HEIGHT // 2

# Спрайты
DOUBLE_PI = math.pi * 2
Center_RAY = NUM_OF_RAYS // 2 - 1
NONE_VISIABLE_RAYS = 100
FAKE_RAYS_RANGE = NUM_OF_RAYS - 1 + 2 * NONE_VISIABLE_RAYS
