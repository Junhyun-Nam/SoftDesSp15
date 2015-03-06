import pygame
import random
import time
pygame.init()

class DrawableSurface():
    """ A class that wraps a pygame.Surface and a pygame.Rect """
    def __init__(self, surface, rect):
        """ Initialize the drawable surface """
        self.surface = surface
        self.rect = rect

    def get_surface(self):
        """ Get the surface """
        return self.surface

    def get_rect(self):
        """ Get the rect """
        return self.rect


class Balloon():
	def __init__(self):
		self.image = pygame.image.load('images/balloon.png')
		w, h = self.image.get_size()
		self.pos_x = 192 - w/2
		self.pos_y = 360 - h/2
		self.vel_x = .2 # modify this later
		self.vel_y = 0
		self.acc_y = 0.001

	def update(self):
		w, h = self.image.get_size()
		self.pos_x += self.vel_x
		self.pos_y += self.vel_y
		self.vel_y += self.acc_y
		if self.pos_x < 11 or self.pos_x > 373-w:
			self.vel_x = -self.vel_x

	def bounce(self):
		self.vel_y -= 0.8

	def get_drawables(self):
		w, h = self.image.get_size()
		return [DrawableSurface(self.image, pygame.Rect(self.pos_x, self.pos_y, w, h))]


class TopSpikes():
	def __init__(self):
		self.image = pygame.image.load('images/down.png')
		self.spikes = [1,1,1,1,1,1,1,1,1]

	def get_drawables(self):
		drawables = []
		w, h = self.image.get_size()
		for i in range(len(self.spikes)):
			if self.spikes[i] == 1:
				drawables.append(DrawableSurface(self.image, pygame.Rect(i*48-24,48,w,h)))
		return drawables

class BottomSpikes():
	def __init__(self):
		self.image = pygame.image.load('images/up.png')
		self.spikes = [1,1,1,1,1,1,1,1,1]

	def get_drawables(self):
		drawables = []
		w, h = self.image.get_size()
		for i in range(len(self.spikes)):
			if self.spikes[i] == 1:
				drawables.append(DrawableSurface(self.image, pygame.Rect(i*48-24,648,w,h)))
		return drawables

class LeftSpikes():
	def __init__(self):
		self.image = pygame.image.load('images/right.png')
		self.spikes = [0,0,0,0,0,0,0,0,0,0,0,0]

	def get_drawables(self):
		drawables = []
		w, h = self.image.get_size()
		for i in range(len(self.spikes)):
			if self.spikes[i] == 1:
				drawables.append(DrawableSurface(self.image, pygame.Rect(12,i*48+60,w,h)))
		return drawables

class RightSpikes():
	def __init__(self):
		self.image = pygame.image.load('images/left.png')
		self.spikes = [0,0,0,0,0,0,0,0,0,0,0,0]

	def get_drawables(self):
		drawables = []
		w, h = self.image.get_size()
		for i in range(len(self.spikes)):
			if self.spikes[i] == 1:
				drawables.append(DrawableSurface(self.image, pygame.Rect(348,i*48+60,w,h)))
		return drawables


class Spikes():
	def __init__(self):
		self.top = TopSpikes()
		self.bottom = BottomSpikes()
		self.left = LeftSpikes()
		self.right = RightSpikes()
		
	def get_drawables(self):
		drawables = self.top.get_drawables() + self.bottom.get_drawables() + self.left.get_drawables() + self.right.get_drawables()
		return drawables

	def update(self):
		pass

class LeftWall():
	def __init__(self):
		self.image = pygame.image.load('images/side.png')
	
	def get_drawables(self):
		w, h = self.image.get_size()
		return [DrawableSurface(self.image, pygame.Rect(0, 48, w, h))]

class RightWall():
	def __init__(self):
		self.image = pygame.image.load('images/side.png')

	def get_drawables(self):
		w, h = self.image.get_size()
		return [DrawableSurface(self.image, pygame.Rect(372, 48, w, h))]

class Walls():
	def __init__(self, balloon):
		self.left = LeftWall()
		self.right = RightWall()
		self.balloon = balloon

	def get_drawables(self):
		drawables = self.left.get_drawables() + self.right.get_drawables()
		return drawables

	def left_collide(self):
		return self.balloon.get_drawables()[0].get_rect().colliderect(self.left.get_drawables()[0])

	def right_collide(self):
		return self.balloon.get_drawables()[0].get_rect().colliderect(self.right.get_drawables()[0])


class Score():
	def __init__(self, walls):
		self.walls = walls
		self.score = 0
		self.pos_x = 200
		self.pos_y = 300
		self.scoretext = pygame.font.Font(None, 50)
		self.printable = self.scoretext.render(str(self.score), True, (0,0,0))

	def get_drawables(self):
		w, h = self.scoretext.size(str(self.score))
		return [DrawableSurface(self.printable, pygame.Rect(self.pos_x, self.pos_y, w, h))]

	def update(self):
		if self.walls.left_collide() or self.walls.right_collide():
			self.score += 1
		self.printable = self.scoretext.render(str(self.score), True, (0,0,0))

class BalloonModel():
	""" Represents the game state of our Flappy bird clone """
	def __init__(self, width, height):
		""" Initialize the flappy model """
		self.width = width
		self.height = height
		self.balloon = Balloon()
		self.spikes = Spikes()
		self.walls = Walls(self.balloon)
		self.score = Score(self.walls)


	def get_drawables(self):
		""" Return a list of DrawableSurfaces for the model """
		return self.balloon.get_drawables() + self.spikes.get_drawables() + self.walls.get_drawables() + self.score.get_drawables()
    

	#def is_dead(self):
	#	""" Return True if the player is dead (for instance) the player has collided with an obstacle, and false otherwise """
        # TODO: modify this if the player becomes more complicated
    #    player_rect = self.balloon.get_drawables()[0]
    #    return self.background.collided_with(player_rect)

	def update(self):
		""" Updates the model and its constituent parts """
		self.balloon.update()
		self.spikes.update()
		self.score.update()

class BalloonView():
	def __init__(self, model, width, height):
		self.screen = pygame.display.set_mode((width, height))
		self.model = model

	def draw(self):
		""" Redraw the full game window """
		self.screen.fill((255,255,255))
		self.drawables = self.model.get_drawables()
		for d in self.drawables:
			rect = d.get_rect()
			surf = d.get_surface()
			self.screen.blit(surf, rect)
		pygame.display.update()



class BalloonController(): # Later, add balloon.bounce when the space is pressed
    def __init__(self, model):
        self.model = model
        self.space_pressed = False
        self.running = True

    def process_events(self):
        """ process keyboard events.  This must be called periodically
            in order for the controller to have any effect on the game """
        pygame.event.pump()
        for event in pygame.event.get():
        	if event.type is pygame.QUIT:
        		self.running = False
        	elif not(pygame.key.get_pressed()[pygame.K_SPACE]):
        		self.space_pressed = False
        	elif not(self.space_pressed):
        		self.space_pressed = True
        		self.model.balloon.bounce()
            

class BalloonBurst():
    """ The main Balloon Burst class """

    def __init__(self):
        """ Initialize the balloon burst game.  Use BalloonBurst.run to
            start the game """
        self.model = BalloonModel(384, 720)
        self.view = BalloonView(self.model, 384, 720)
        self.controller = BalloonController(self.model)
        self.running = True

    def run(self):
        """ the main runloop... loop until death """
        last_update_time = time.time()
        while (self.controller.running):
            self.view.draw()
            self.controller.process_events()
            self.model.update()
            last_update_time = time.time()


if __name__ == '__main__':
	balloon = BalloonBurst()
	balloon.run()