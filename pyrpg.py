import pygame
from pygame_tools import *
from pygame.locals import *

class World:

    def __init__(self, board_path: str, tile_dict: dict, cell_size: Point):
        self.board_path = board_path
        self.tile_dict = tile_dict
        self.cell_size = cell_size
        with open(board_path, 'r') as f:
            self.board = [[int(cell) for cell in row if cell != '\n'] for row in f]
        self.collision_list = []
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if self.tile_dict[cell] == None:
                    self.collision_list.append(Rect((j * self.cell_size.x, i * self.cell_size.y), cell_size))

    def draw(self, screen: pygame.Surface, offset: Point):
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if self.tile_dict[cell] != None:
                    screen.blit(self.tile_dict[cell], (j * self.cell_size.x + offset.x, i * self.cell_size.y + offset.y))

class Player(pygame.sprite.Sprite):

    def __init__(self, pos: Point):
        self.image = pygame.image.load('assets/player.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = Rect(pos, (5, 4)) # hitbox not size of image
        self.height = self.image.get_height()
        self.velocity = Point(0, 0)
        self.visual_offset_in_image = Point(1, 0)
        self.facing_right = True

    def update(self, collision_list: [Rect]):
        if self.velocity.x > 0:
            self.facing_right = True
        elif self.velocity.x < 0:
            self.facing_right = False
        self.rect.x += self.velocity.x
        for i in self.rect.collidelistall(collision_list):
            if self.facing_right:
                self.rect.right = collision_list[i].left
            else:
                self.rect.left = collision_list[i].right
        self.rect.y += self.velocity.y
        for i in self.rect.collidelistall(collision_list):
            if self.velocity.y < 0: # moving down
                self.rect.top = collision_list[i].bottom
            else:
                self.rect.bottom = collision_list[i].top
        self.velocity = Point(0, 0)

    def draw(self, screen: pygame.Surface, offset: Point):
        screen.blit(self.image if self.facing_right else pygame.transform.flip(self.image, True, False), (self.rect.x + offset.x - self.visual_offset_in_image.x, self.rect.bottom + offset.y - self.height - self.visual_offset_in_image.y))
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 1) # hitbox

class RPG(GameScreen):

    def __init__(self):
        pygame.init()
        real_size = Point(900, 600)
        super().__init__(pygame.display.set_mode(real_size), real_size, (real_size.x // 4, real_size. y // 4))
        self.cell_size = Point(16, 4)
        self.world = World(
                'assets/map.txt',
                {
                    0: None,
                    1: pygame.image.load('assets/grass.png')
                },
                self.cell_size
            )
        self.camera_scroll = Point(0, 0)
        self.player = Player(Point(32, 8))

    def update(self):
        self.screen.fill('skyblue')
        self.world.draw(self.screen, self.camera_scroll)
        self.player.update(self.world.collision_list)
        self.player.draw(self.screen, self.camera_scroll)
        self.keyboard_input()

    def keyboard_input(self):
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            # move up
            self.player.velocity.y -= 3
        if keys[K_a]:
            # move left
            self.player.velocity.x -= 3
        if keys[K_s]:
            # move down
            self.player.velocity.y += 3
        if keys[K_d]:
            # move right
            self.player.velocity.x += 3

if __name__ == '__main__':
    RPG().run()
