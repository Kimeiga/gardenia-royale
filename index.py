"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/
 
From:
http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py
 
Explanation video: http://youtu.be/BCxWJgN4Nnc
 
Part of a series:
http://programarcadegames.com/python_examples/f.php?file=move_with_walls_example.py
http://programarcadegames.com/python_examples/f.php?file=maze_runner.py
http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py
http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py
http://programarcadegames.com/python_examples/f.php?file=platform_moving.py
http://programarcadegames.com/python_examples/sprite_sheets/
"""
 
import pygame
 
# Global constants
 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Physics
GRAVITY = 0.35

# Screen dimensions
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 750
 
# Character dimensions
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 40

class PhysicalObject(pygame.sprite.Sprite):
    """ This class represents any object that can interact with the world"""
 
    # -- Methods
    def __init__(self, width, height, color):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        # width = 40
        # height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
 
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of sprites we can bump against
        self.level = None
 
    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()
 
        # Move left/right
        self.rect.x += self.change_x
 
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += GRAVITY
 
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height


class Player(PhysicalObject):
    """ This class represents the bar at the bottom that the player
        controls. """
 
    # -- Methods
    def __init__(self, color):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__(PLAYER_WIDTH, PLAYER_HEIGHT, color)

        # Current item (can only hold 1 at a time)
        self.item = None
 
    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10
 
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0

class Item(PhysicalObject):
    def __init__(self, width, height, color, x, y, itemType, image, sound=None, useSound=None):
        super().__init__(width, height, color)

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.itemType = itemType
        self.loadSound(sound)

    def loadSound(self, sound):
        if sound != None:
            self.sound = pygame.mixer.Sound(sound)
        else:
            self.sound = None

    def playSound(self):
        if self.sound != None:
            self.sound.play()

    def pickUp(self):
        self.playSound()
        return self.itemType

    def use(self):
        super().use()
        self.playSound()

class Gun(Item):
    def use(self):
        #shoot

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pointingLeft):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        # self.rect = self.image.get_rect()
        # self.rect.centery = y
        # self.rect.centerx = x
        self.speed = 10 if pointingLeft else -10

    def update(self):
        # move forward
        self.rect.x += self.speed
        # kill if it moves off the top of the screen
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.kill()
        pass

 
class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
 
        self.rect = self.image.get_rect()
 
 
class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
         
        # Background image
        self.background = None
 
    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
 
    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Draw the background
        screen.fill(BLUE)
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
 
 
# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        # Array with width, height, x, and y of platform
        level = [[116, 30, 250, 210],
                 [116, 30, 934, 210],
                 [40, 20, 130, 270],
                 [40, 20, 1130, 270],
                 [30, 245, 170, 270],
                 [30, 245, 1100, 270],
                 [110, 30, 470, 240],
                 [106, 30, 720, 240],
                 [30, 105, 470, 270],
                 [30, 105, 796, 270],
                 [140, 20, 580, 355],
                 [40, 20, 130, 375],
                 [40, 20, 1130, 375],
                 [50, 20, 200, 375],
                 [50, 20, 1050, 375],
                 [40, 20, 130, 495],
                 [40, 20, 1130, 495],
                 [450, 50, 425, 438],
                 [800, 50, 250, 570],
                 [200, 50, 100, 620], 
                 [200, 50, 1000, 620]
                 ]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
 
 
def main():
    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygameactive_sprite_list.display.set_caption("Gardenia Royale")
 
    # Create the right player and left player
    rightPlayer = Player(RED)
    leftPlayer = Player(YELLOW)

    # Create all the levels
    level_list = []
    level_list.append( Level_01(rightPlayer) )
    level_list.append( Level_01(leftPlayer) )
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    rightPlayer.level = current_level
    leftPlayer.level = current_level
 
    rightPlayer.rect.x = 840
    rightPlayer.rect.y = SCREEN_HEIGHT - rightPlayer.rect.height
    active_sprite_list.add(rightPlayer)
 
    leftPlayer.rect.x = 340
    leftPlayer.rect.y = SCREEN_HEIGHT - leftPlayer.rect.height
    active_sprite_list.add(leftPlayer)

    bullet_list = pygame.sprite.Group()
 

    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
 
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    rightPlayer.go_left()
                if event.key == pygame.K_RIGHT:
                    rightPlayer.go_right()
                if event.key == pygame.K_UP:
                    rightPlayer.jump()
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and rightPlayer.change_x < 0:
                    rightPlayer.stop()
                if event.key == pygame.K_RIGHT and rightPlayer.change_x > 0:
                    rightPlayer.stop()

            # left player
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    leftPlayer.go_left()
                if event.key == pygame.K_d:
                    leftPlayer.go_right()
                if event.key == pygame.K_w:
                    leftPlayer.jump()
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and leftPlayer.change_x < 0:
                    leftPlayer.stop()
                if event.key == pygame.K_d and leftPlayer.change_x > 0:
                    leftPlayer.stop()
 
        # Update the player.
        active_sprite_list.update()
 
        # Update items in the level
        current_level.update()

        # Update bullets
        bullet_list.update()
 
        # If the player gets near the right side, shift the world left (-x)
        if rightPlayer.rect.right > SCREEN_WIDTH:
            rightPlayer.rect.right = SCREEN_WIDTH
 
        # If the player gets near the left side, shift the world right (+x)
        if rightPlayer.rect.left < 0:
            rightPlayer.rect.left = 0
 
        if leftPlayer.rect.right > SCREEN_WIDTH:
            leftPlayer.rect.right = SCREEN_WIDTH
 
        # If the player gets near the left side, shift the world right (+x)
        if leftPlayer.rect.left < 0:
            leftPlayer.rect.left = 0

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)
 
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
 
        # Limit to 60 frames per second
        clock.tick(60)
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
 
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()
 
if __name__ == "__main__":
    main()