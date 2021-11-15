import pygame, random

size=[600,600] 

NEGRO=[0,0,0]
BLANCO=[250,250,250]

class Meteor(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image=pygame.image.load("meteor.png").convert()
		self.image.set_colorkey(NEGRO)
		self.rect = self.image.get_rect()
	def update(self):
		if self.rect.y >=600:
			self.rect.y=0
			self.rect.x=random.randrange(600)
		else:
			self.rect.y+=3

class Jugador(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image=pygame.image.load("nave.png").convert()
		self.image.set_colorkey(NEGRO)
		self.rect = self.image.get_rect()
	def update(self):
		p_mouse=pygame.mouse.get_pos()
		self.rect.x=p_mouse[0]
		self.rect.y=p_mouse[1]

class Laser(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image=pygame.image.load("laser.png").convert()
		self.rect=self.image.get_rect()

	def update(self):
		self.rect.y-=3

class Game(object):
	def __init__(self):
		self.lista_meteoros=pygame.sprite.Group()
		self.lista_lasers=pygame.sprite.Group()
		self.all_sprite= pygame.sprite.Group()
		for i in range(50):
			meteor = Meteor()
			meteor.rect.x=random.randrange(600)
			meteor.rect.y=random.randrange(600)
			self.lista_meteoros.add(meteor)
			self.all_sprite.add(meteor)
		self.jugador=Jugador()
		self.all_sprite.add(self.jugador)

		self.fondo = pygame.image.load("fondo.jpg").convert()
		self.fondo = pygame.transform.scale(self.fondo,[600,600])
		self.sonido=pygame.mixer.Sound("laser.ogg")

		self.marcador=0
		self.game_over=False
	def proceso_eventos(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return False
			if self.game_over==False:
				if event.type == pygame.MOUSEBUTTONDOWN:
					laser = Laser()
					pos=pygame.mouse.get_pos()
					laser.rect.x=pos[0]+45
					laser.rect.y=pos[1]-20
					self.lista_lasers.add(laser)
					self.all_sprite.add(laser)
					self.sonido.play()
			else:
				if event.type ==pygame.KEYDOWN:
					if event.key == pygame.K_r:
						self.__init__()
					if event.key ==pygame.K_s:
						return False
		return True
	def logica(self):
		if not(self.game_over):
			self.all_sprite.update()
			for laser in self.lista_lasers:
				choques=pygame.sprite.spritecollide(laser,self.lista_meteoros,True)
				for meteor in choques:
					self.lista_lasers.remove(laser)
					self.all_sprite.remove(laser)
					self.marcador+=1
				if laser.rect.y < -5 :
					self.lista_lasers.remove(laser)
					self.all_sprite.remove(laser)
				if len(self.lista_meteoros)==0:
					self.game_over=True

	def display(self,screen):
		screen.blit(self.fondo, [0,0])
		if self.game_over ==False:
			#dibuja todo
			self.all_sprite.draw(screen)
		else:
			#pantalla de game over
			font=pygame.font.SysFont("serif",30)
			text=font.render("Game over, r para reiniciar y s para salir",True,BLANCO)
			center_x =(size[0]//2)-(text.get_width()//2)
			center_y =(size[1]//2)-(text.get_height()//2)
			screen.blit(text,[center_x,center_y])
		pygame.display.flip()
def main():
	pygame.init()
	screen=pygame.display.set_mode(size)
	clock=pygame.time.Clock()
	juego=Game()
	evolucion = True
	while evolucion :
		evolucion=juego.proceso_eventos()
		
		juego.logica()
		juego.display(screen)
		clock.tick(60)
	pygame.quit()
if __name__ == "__main__":
	main()