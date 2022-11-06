import pygame, numpy
import math

WIDTH = 1920 #/ 2
HEIGHT = 1080 #/ 2
BACKGROUND = (60, 110, 110)

SQUARE_ROOT_OF_TWO = math.sqrt(2)

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, startx, starty):
        super().__init__()

        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

        self.rect.center = [startx, starty]

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Player(Sprite):
    def __init__(self, startx, starty):
        super().__init__("p1_front.png", startx, starty)
        self.stand_image = self.image
        self.jump_image = pygame.image.load("p1_jump.png")

        self.walk_cycle = [pygame.image.load(f"p1_walk{i:0>2}.png") for i in range(1,12)]
        self.animation_index = 0
        self.facing_left = False

        self.speed = 8
        self.jumpspeed = 20
        self.vsp = 0
        self.gravity = 0
        self.min_jumpspeed = 4
        self.prev_key = pygame.key.get_pressed()

    def walk_animation(self):
        self.image = self.walk_cycle[self.animation_index]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

        if self.animation_index < len(self.walk_cycle)-1:
            self.animation_index += 1
        else:
            self.animation_index = 0

    def jump_animation(self):
        self.image = self.jump_image
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, boxes):
        """
        TODO Document this method.
        """
        hsp = 0
        vsp = 0
        onground = self.check_collision(0, 1, boxes)
        # check keys
        keys = pygame.key.get_pressed()

        hsp = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed
        vsp = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.speed

        # Temporarily disabled for simpler testing until we make the walking animation [1]
        
        #if hsp < 0:
            #self.facing_left = True
            #self.walk_animation()

        #else:
            #self.facing_left = False
            #self.walk_animation()
        
        # End of disable [1]


        if hsp * vsp != 0:
            hsp /= SQUARE_ROOT_OF_TWO
            vsp /= SQUARE_ROOT_OF_TWO
        if hsp == vsp == 0:
            self.image = self.stand_image

        # TODO This is a relic, should be removed if we do not use jumping.
        if self.prev_key[pygame.K_UP] and not keys[pygame.K_UP]:
            if self.vsp < -self.min_jumpspeed:
                self.vsp = -self.min_jumpspeed

        self.prev_key = keys

        # movement
        self.move(hsp, vsp, boxes)

    def move(self, x, y, boxes):
        dx = x
        dy = y

        while self.check_collision(0, dy, boxes):
            dy -= numpy.sign(dy)

        while self.check_collision(dx, dy, boxes):
            dx -= numpy.sign(dx)

        self.rect.move_ip([dx, dy])

    def check_collision(self, x, y, grounds):
        self.rect.move_ip([x, y])
        collide = pygame.sprite.spritecollideany(self, grounds)
        self.rect.move_ip([-x, -y])
        return collide


class Wall_V(Sprite):
    def __init__(self, startx, starty):
        super().__init__("TempWall_V.png", startx, starty)      #Wall Vertical

class Wall_H(Sprite):
    def __init__(self, startx, starty):
        super().__init__("TempWall_H.png", startx, starty)      #Wall Horizontal

class Wall_H_JD(Sprite):
    def __init__(self, startx, starty):
        super().__init__("TempWall_H_JD.png", startx, starty)   #Wall Horizontal Join Down

class Wall_VE_JU(Sprite):
    def __init__(self, startx, starty):
        super().__init__("TempWall_VE_JU.png", startx, starty)  #Wall Vertical End Join Up

class Barrier(Sprite):
    def __init__(self, startx, starty):
        super().__init__("Barrier.png", startx, starty)         #Barrier

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    player = Player(WIDTH / 2, HEIGHT / 2)  #Sets player to centre of screen

    boxes = pygame.sprite.Group()

    for bx in range(0, 1920, 70):          
        boxes.add(Wall_H(bx, 100))                   #Wall top horizontal row

    for by in range(170, 730, 70):          
        for bx in range(6):
            boxes.add(Wall_V(bx * 384, by))         #Wall vertical array
            boxes.add(Wall_H_JD(bx * 384, 100))     #Wall horizontal top join sections [Currently overwriting 'Wall top horizontal row'. Is this an issue?]
            boxes.add(Wall_VE_JU(bx * 384, 730))    #Wall vertical End Join Up
    
    for bx in range(0, 1920, 80):                   #Barrier bottom row
        boxes.add(Barrier(bx + 40, 1040))
            
    
    #boxes.add(Box(330, 800))                       #Individual box

    while True:
        pygame.event.pump()
        player.update(boxes)

        # Draw loop
        screen.fill(BACKGROUND)
        player.draw(screen)
        boxes.draw(screen)
        pygame.display.flip()

        clock.tick(60)
    

if __name__ == "__main__":
    main()