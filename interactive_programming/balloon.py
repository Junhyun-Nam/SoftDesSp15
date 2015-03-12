import pygame
import random
import time
pygame.init()

class DrawableSurface(pygame.sprite.Sprite):
    """ A class that wraps a pygame.Surface and a pygame.Rect """
    def __init__(self, surface, rect):
        """ Initialize the drawable surface """
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.rect = rect
        self.mask = pygame.mask.from_surface(self.surface)

    def get_surface(self):
        """ Get the surface """
        return self.surface

    def get_rect(self):
        """ Get the rect """
        return self.rect

    def get_mask(self):
    	""" Get the mask """
    	return self.mask


class Balloon():
	def __init__(self):
		self.image = pygame.image.load('images_/balloon.png')
		w, h = self.image.get_size()
		self.pos_x = 192 - w/2
		self.pos_y = 360 - h/2
		self.vel_x = .45
		self.vel_y = 0
		self.acc_y = 0.005
		self.burst = False
		self.burst_x = 0
		self.burst_y = 0
		self.bird = False

	def update(self, state):
		if state == 'run':
			w, h = self.image.get_size()
			self.pos_x += self.vel_x
			self.pos_y += self.vel_y
			self.vel_y += self.acc_y
			if self.pos_x < 12 or self.pos_x > 373-w:
				self.vel_x = -self.vel_x
			self.burst_x = self.pos_x
			self.burst_y = self.pos_y
		elif state == 'end':
			if not self.burst:
				self.image = pygame.image.load('images_/burst72.png')
				self.pos_x = self.burst_x - 24
				self.pos_y = self.burst_y - 24
				self.burst = True
			else:
				if not self.bird:
					self.pos_x = self.burst_x
					self.pos_y = self.burst_y
					self.bird = True
					if self.burst_x < 192:
						self.image = pygame.image.load('images_/twitter_black.png')
						self.vel_x = 9
						self.vel_y = 0
						self.acc_y = -3
					else:
						self.image = pygame.image.load('images_/twitter_black_rev.png')
						self.vel_x = -9
						self.vel_y = 0
						self.acc_y = -3
				self.pos_x += self.vel_x
				self.pos_y += self.vel_y
				self.vel_y += self.acc_y


	def bounce(self):
		self.vel_y = -.95

	def get_drawables(self):
		w, h = self.image.get_size()
		return [DrawableSurface(self.image, pygame.Rect(self.pos_x, self.pos_y, w, h))]

class Wall():
	def __init__(self, pos_x, pos_y, is_side):
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.is_side = is_side
		if self.is_side:
			self.image = pygame.image.load('images_/side.png')
		else:
			self.image = pygame.image.load('images_/topbottom.png')

	def get_drawables(self):
		w, h = self.image.get_size()
		return [DrawableSurface(self.image, pygame.Rect(self.pos_x, self.pos_y, w, h))]

class Walls():
	def __init__(self, balloon):
		self.left = Wall(0, 48, True)
		self.right = Wall(372, 48, True)
		self.top = Wall(0, 0, False)
		self.bottom = Wall(0, 672, False)
		self.balloon = balloon

	def get_drawables(self):
		drawables = self.left.get_drawables() + self.right.get_drawables() + self.top.get_drawables() + self.bottom.get_drawables()
		return drawables

	def left_collide(self):
		return self.balloon.get_drawables()[0].get_rect().colliderect(self.left.get_drawables()[0])

	def right_collide(self):
		return self.balloon.get_drawables()[0].get_rect().colliderect(self.right.get_drawables()[0])



class Score():
	def __init__(self, walls):
		self.walls = walls
		self.score = 0

	def update(self):
		if self.walls.left_collide() or self.walls.right_collide():
			self.score += 1

	def get_score(self):
		return self.score


class Spike():
	def __init__(self, place, score = 0):
		self.place = place
		self.score = score
		self.x_coords = dict()
		self.y_coords = dict()
		if self.place == 'top':
			self.image = pygame.image.load('images_/down.png')
			self.spikes = [1,1,1,1,1,1,1,1,1]
			for i in range(len(self.spikes)):
				self.x_coords[i] = i*48 - 24
				self.y_coords[i] = 48
		elif self.place == 'bottom':
			self.image = pygame.image.load('images_/up.png')
			self.spikes = [1,1,1,1,1,1,1,1,1]
			for i in range(len(self.spikes)):
				self.x_coords[i] = i*48 - 24
				self.y_coords[i] = 648
		elif self.place == 'left':
			self.image = pygame.image.load('images_/right.png')
			self.spikes =  [0,0,0,0,0,0,0,0,0,0,0,0]
			for i in range(len(self.spikes)):
				self.x_coords[i] = 12
				self.y_coords[i] = i*48 + 60
		elif self.place == 'right':
			self.image = pygame.image.load('images_/left.png')
			self.spikes =  [0,0,0,0,0,0,0,0,0,0,0,0]
			for i in range(len(self.spikes)):
				self.x_coords[i] = 348
				self.y_coords[i] = i*48 + 60

	def get_drawables(self):
		drawables = []
		w, h = self.image.get_size()
		for i in range(len(self.spikes)):
			if self.spikes[i] == 1:
				drawables.append(DrawableSurface(self.image, pygame.Rect(self.x_coords[i],self.y_coords[i],w,h)))
		return drawables

	def update(self, state):
		if state == 'run':
			cur_score = self.score.get_score()
			if cur_score < 10:
				binary = [0,0,0,0,0,0,0,1,1,1]
			elif cur_score < 20:
				binary = [0,1]
			else:
				binary = [0,0,1,1,1]
			for i in range(len(self.spikes)):
				self.spikes[i] = random.choice(binary)

class Spikes():
	def __init__(self, balloon, score):
		self.top = Spike('top')
		self.bottom = Spike('bottom')
		self.left = Spike('left', score)
		self.right = Spike('right', score)
		self.balloon = balloon
		
	def get_drawables(self):
		drawables = self.top.get_drawables() + self.bottom.get_drawables() + self.left.get_drawables() + self.right.get_drawables()
		return drawables

	def is_collided(self):
		for drawable in self.get_drawables():
			if pygame.sprite.collide_mask(self.balloon.get_drawables()[0], drawable) != None:
				return True
		return False


class Texts():
	def __init__(self, score, state):
		self.score = score
		self.state = state
		self.score_value = self.score.get_score()

	def drawable_text(self, size, input_string, pos_x, pos_y):
		text = pygame.font.SysFont("purisa", size)
		w, h = text.size(input_string)
		return DrawableSurface(text.render(input_string, True, (0,0,0)), pygame.Rect(pos_x - w/2, pos_y - h/2, w, h))

	def get_drawables(self):
		global hiscore
		if self.state == 'start':
			drawables = [self.drawable_text(40, "Balloon Burst", 192, 180), 
						 self.drawable_text(30, "High score  " + str(hiscore), 192, 250),
						 self.drawable_text(30, "Press spacebar", 192, 500),
						 self.drawable_text(30, "to start", 192, 545)]
		elif self.state == 'run':
			drawables = [self.drawable_text(100, str(self.score_value), 192, 360)]
		elif self.state == 'end':
			drawables = [self.drawable_text(40, "Game over", 192, 180),
						 self.drawable_text(30, "High score  " + str(hiscore), 192, 250),
						 self.drawable_text(100, str(self.score_value), 192, 360),
						 self.drawable_text(30, "Press spacebar", 192, 500),
						 self.drawable_text(30, "to restart", 192, 545)]
		return drawables

	def update(self, state):
		self.score_value = self.score.get_score()
		self.state = state



class BalloonModel():
	""" Represents the game state of our Balloon Burst clone """
	def __init__(self, width, height):
		""" Initialize the flappy model """
		self.width = width
		self.height = height
		self.balloon = Balloon()
		self.walls = Walls(self.balloon)
		self.score = Score(self.walls)
		self.spikes = Spikes(self.balloon, self.score)
		self.status = {0:'start', 1:'run', 2:'end', 3:'quit'}
		self.state = 0
		self.texts = Texts(self.score, self.get_state())

	def get_drawables(self):
		""" Return a list of DrawableSurfaces for the model """
		return self.balloon.get_drawables() + self.spikes.get_drawables() + self.walls.get_drawables() + self.texts.get_drawables()
    
	def is_dead(self):
		""" Return True if the player is dead (for instance) the player has collided with an obstacle, and false otherwise """
		return self.spikes.is_collided()

	def get_state(self):
		return self.status[self.state]

	def change_state(self):
		self.state += 1
		self.state = self.state%3

	def quit_game(self):
		self.state = 3

	def update(self):
		""" Updates the model and its constituent parts """
		self.balloon.update(self.get_state())
		self.score.update()
		self.texts.update(self.get_state())
		if self.walls.left_collide():
			self.spikes.right.update(self.get_state())
		elif self.walls.right_collide():
			self.spikes.left.update(self.get_state())



class BalloonView():
	def __init__(self, model, width, height):
		self.screen = pygame.display.set_mode((width, height))
		self.model = model

	def draw(self):
		""" Redraw the full game window """
		background_color = [(255,255,0), (178,255,102), (51,255,255), (102,102,255), (255,51,153), (255,128,0)]
		if self.model.score.get_score() > 50:
			cur_color = (255,128,0)
		else:
			cur_color = background_color[self.model.score.get_score()/10]
		if self.model.get_state() == 'end':
			cur_color = (255,0,0)
		self.screen.fill(cur_color)
		self.drawables = self.model.get_drawables()
		for d in self.drawables:
			rect = d.get_rect()
			surf = d.get_surface()
			self.screen.blit(surf, rect)
		pygame.display.update()



class BalloonController():
    def __init__(self, model):
        self.model = model
        self.space_pressed = False

    def process_events(self):
        """ process keyboard events.  This must be called periodically
            in order for the controller to have any effect on the game """
        pygame.event.pump()
        for event in pygame.event.get():
        	if event.type is pygame.QUIT:
        		self.model.quit_game()
        	elif self.model.get_state() in ['start', 'end']:
        		if not(pygame.key.get_pressed()[pygame.K_SPACE]):
        			self.space_pressed = False
        		elif not(self.space_pressed):
        			self.space_pressed = True
        			self.model.change_state()
        	elif self.model.get_state() == 'run':
        		if not(pygame.key.get_pressed()[pygame.K_SPACE]):
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
	

    def run(self):
        """ the main runloop... loop until death """
        global hiscore
        while (self.model.get_state() is not 'quit'):
        	if self.model.get_state() == 'start':
        		self.model = BalloonModel(384, 720)
        		self.view = BalloonView(self.model, 384, 720)
        		self.controller = BalloonController(self.model)
        	else:
        		self.model.update()
        		if self.model.get_state() == 'run':
        			if self.model.is_dead():
        				self.model.change_state()
        				hiscore = max(hiscore, self.model.score.get_score())
        	self.view.draw()
        	self.controller.process_events()
        	if self.model.get_state() == 'end':
        		time.sleep(0.1)


if __name__ == '__main__':
	hiscore = 0
	balloon = BalloonBurst()
	balloon.run()
