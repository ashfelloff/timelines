import pygame
import sys
import random
import pickle
import multiprocessing
from pygame.locals import *
from pygame import mixer
from os import path


pygame.init()
mixer.init()
mixer.music.load('backgroundmusic/1.mp3')
mixer.music.play()

clock = pygame.time.Clock()
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)

fps = 60

#game window

screen_width = 750
screen_height = 750  

player = pygame.Rect((300, 250, 50, 50))

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption('Timelines')

tile_size = 37.5
game_over = 0
main_menu = True
level = 0
max_levels = 11
score = 0

white = (255, 255, 255)
blue = (12, 44, 60)

#image loader COME BACK
bg_img = pygame.image.load('img/wall.png')
restart_img = pygame.image.load('img/restart_btn.png')
start_img = pygame.image.load('img/start_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')
title_img = pygame.image.load('img/title.png')
title_img = pygame.transform.scale(title_img, (300, 100))

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# List of texts to display
texts = [
   "I jump, not to survive, but to delay the inevitable.",
    "Every rooftop feels like another fleeting lie of safety.",
    "The world crumbles beneath me as I cling to what’s left.",
    "Each leap is a gamble I no longer care to win.",
    "The sky watches indifferently as I defy its pull.",
    "I run, not to escape, but to avoid standing still.",
    "Every handhold mocks me, questioning why I bother.",
    "My body moves forward; my mind stays trapped in the past.",
    "The horizon fades faster than my hope ever could.",
    "Each step forward feels like two steps closer to nowhere.",
    "The apocalypse chases me, but I’ve been running my whole life.",
    "I vault over ruins, the same way I avoid my reflection.",
    "Every move reminds me how fragile this existence really is.",
    "The sound of my breath echoes louder than my will to live.",
    "I scale walls built by those who never saw this coming.",
    "Each fall feels more inviting than the ground I leave behind.",
    "The teleporter looms ahead, a hollow promise of salvation.",
    "I’m not running toward life; I’m running away from memories.",
    "Every obstacle feels personal, as if the world knows my sins.",
    "I survive, but survival feels like the cruelest punishment.",
    "The ground shakes, but it’s nothing compared to my own instability.",
    "My shadow keeps up, the only constant in this collapse.",
    "I push forward because stopping feels too familiar.",
    "Each ledge I grab feels colder than the void inside me.",
    "I dodge falling debris, but not the thoughts that haunt me.",
    "Every heartbeat feels borrowed, as if I don’t deserve it.",
    "I land, not with triumph, but with the weight of failure.",
    "The world burns around me, but I’ve been scorched for years.",
    "I move forward because turning back is no longer an option.",
    "Every successful jump is another reminder I’m still here.",
    "I sprint toward the future, but it feels like a dead end.",
    "The wind carries me forward, as if it knows I can’t stop.",
    "Each wall I climb feels steeper than the last, like my regrets.",
    "The stars disappear, but I’ve grown used to the darkness.",
    "Every calculated move hides the chaos in my mind.",
    "The teleporter hums ahead, indifferent to my hesitation.",
    "Every misstep feels deliberate, like my subconscious wants me to fail.",
    "I leap across the void, a metaphor I wish I didn’t understand.",
    "The closer I get to escape, the heavier my body feels.",
    "I navigate destruction, wondering if it mirrors what’s inside me."
]

# Function to display text one letter at a time
def display_text(screen, font, text, y_pos):
    displayed_text = ""
    for char in text:
        displayed_text += char
        text_surf = font.render(displayed_text, True, BLACK)
        text_rect = text_surf.get_rect(topleft=(50, y_pos))
        screen.blit(text_surf, text_rect)
        pygame.display.flip()
        time.sleep(0.1)  # Adjust the speed of the animation here

# Function to run the text display on a second display
def text_display():
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Stacking Text Display")

    # Set up game clock
    clock = pygame.time.Clock()

    # Main game loop
    running = True
    last_text_time = time.time()
    interval = random.randint(5, 6)
    font = pygame.font.Font(None, 36)
    y_pos = 50
    displayed_texts = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Check if it's time to display a new text
        current_time = time.time()
        if current_time - last_text_time >= interval:
            text = random.choice(texts)
            displayed_texts.append((text, y_pos))
            y_pos += 40  # Move the next text down
            last_text_time = current_time
            interval = random.randint(5, 6)

        # Clear the screen
        screen.fill(WHITE)

        # Display all texts
        for text, pos in displayed_texts:
            text_surf = font.render(text, True, BLACK)
            text_rect = text_surf.get_rect(topleft=(50, pos))
            screen.blit(text_surf, text_rect)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(30)

    pygame.quit()
    sys.exit()

# text_process = multiprocessing.Process(target=text_display)
# text_process.start()

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def draw_grid():
	for line in range(0, 20):
		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
		pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

def reset_level(level):
	player.reset(100, screen_height - 130)
	blob_group.empty()
	platform_group.empty()
	coin_group.empty()
	lava_group.empty()
	exit_group.empty()

	#load in level data and create world
	if path.exists(f'level{level}_data'):
		pickle_in = open(f'level{level}_data', 'rb')
		world_data = pickle.load(pickle_in)
	world = World(world_data)
	#create dummy coin for showing the score
	score_coin = Coin(tile_size // 2, tile_size // 2)
	coin_group.add(score_coin)
	return world

class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False


		#draw button
		screen.blit(self.image, self.rect)

		return action


class Player():
	def __init__(self, x, y):
		self.reset(x, y)

	def update(self, game_over):
		dx = 0
		dy = 0
		walk_cooldown = 5
		col_thresh = 20

		if game_over == 0:
			#get keypresses
			key = pygame.key.get_pressed()
			if (key[pygame.K_SPACE] or key[pygame.K_w] or key[pygame.K_UP]) and self.jumped == False and self.in_air == False:
				self.vel_y = -15
				self.jumped = True
			if (key[pygame.K_SPACE] or key[pygame.K_w] or key[pygame.K_UP]) == False:
				self.jumped = False
			if key[pygame.K_LEFT] or key[pygame.K_a]:
				dx -= 5
				self.counter += 1
				self.direction = -1
			if key[pygame.K_RIGHT] or key[pygame.K_d]:
				dx += 5
				self.counter += 1
				self.direction = 1
			if (key[pygame.K_LEFT] or key[pygame.K_a] or key[pygame.K_RIGHT] or key[pygame.K_d]) == False:
				self.counter = 0
				self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]


			#handle animation
			if self.counter > walk_cooldown:
				self.counter = 0	
				self.index += 1
				if self.index >= len(self.images_right):
					self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]


			#add gravity
			self.vel_y += 1
			if self.vel_y > 10:
				self.vel_y = 10
			dy += self.vel_y

			#check for collision
			self.in_air = True
			for tile in world.tile_list:
				#check for collision in x direction
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				#check for collision in y direction
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#check if below the ground i.e. jumping
					if self.vel_y < 0:
						dy = tile[1].bottom - self.rect.top
						self.vel_y = 0
					#check if above the ground i.e. falling
					elif self.vel_y >= 0:
						dy = tile[1].top - self.rect.bottom
						self.vel_y = 0
						self.in_air = False


			#check for collision with enemies
			if pygame.sprite.spritecollide(self, blob_group, False):
				game_over = -1

			#check for collision with lava
			if pygame.sprite.spritecollide(self, lava_group, False):
				game_over = -1

			#check for collision with exit
			if pygame.sprite.spritecollide(self, exit_group, False):
				game_over = 1


			#check for collision with platforms
			for platform in platform_group:
				#collision in the x direction
				if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				#collision in the y direction
				if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#check if below platform
					if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
						self.vel_y = 0
						dy = platform.rect.bottom - self.rect.top
					#check if above platform
					elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
						self.rect.bottom = platform.rect.top - 1
						self.in_air = False
						dy = 0
					#move sideways with the platform
					if platform.move_x != 0:
						self.rect.x += platform.move_direction


			#update player coordinates
			self.rect.x += dx
			self.rect.y += dy


		elif game_over == -1:
			self.image = self.dead_image
			if self.rect.y > 200:
				self.rect.y -= 5

		#draw player onto screen
		screen.blit(self.image, self.rect)

		return game_over


	def reset(self, x, y):
		self.images_right = []
		self.images_left = []
		self.index = 0
		self.counter = 0
		for num in range(1, 5):
			img_right = pygame.image.load(f'img/guy{num}.png')
			img_right = pygame.transform.scale(img_right, (30, 60))
			img_left = pygame.transform.flip(img_right, True, False)
			self.images_right.append(img_right)
			self.images_left.append(img_left)
		self.dead_image = pygame.image.load('img/ghost.png')
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.direction = 0
		self.in_air = True



class World():
	def __init__(self, data):
		self.tile_list = []

		#load images
		floor_img = pygame.image.load('img/floor.png')
		carpet_img = pygame.image.load('img/carpet.png')

		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(floor_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = pygame.transform.scale(carpet_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 3:
					blob = Enemy(col_count * tile_size, row_count * tile_size + 15)
					blob_group.add(blob)
				if tile == 4:
					platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
					platform_group.add(platform)
				if tile == 5:
					platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
					platform_group.add(platform)
				if tile == 6:
					lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
					lava_group.add(lava)
				if tile == 7:
					coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
					coin_group.add(coin)
				if tile == 8:
					exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
					exit_group.add(exit)
				col_count += 1
			row_count += 1


	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])



class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/blob.png')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1
		self.move_counter = 0

	def update(self):
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 50:
			self.move_direction *= -1
			self.move_counter *= -1


class Platform(pygame.sprite.Sprite):
	def __init__(self, x, y, move_x, move_y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/platform.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_counter = 0
		self.move_direction = 1
		self.move_x = move_x
		self.move_y = move_y


	def update(self):
		self.rect.x += self.move_direction * self.move_x
		self.rect.y += self.move_direction * self.move_y
		self.move_counter += 1
		if abs(self.move_counter) > 50:
			self.move_direction *= -1
			self.move_counter *= -1





class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/lava.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


class Coin(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/coin.png')
		self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)


class Exit(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/exit.png')
		self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class TextScroller:
    def __init__(self):
        self.texts = [
            "I jump, not to survive, but to delay the inevitable.",
            "Every rooftop feels like another fleeting lie of safety.",
            "The world crumbles beneath me as I cling to what's left.",
            "Each leap is a gamble I no longer care to win.",
            "The sky watches indifferently as I defy its pull.",
            "I run, not to escape, but to avoid standing still.",
            "Every handhold mocks me, questioning why I bother.",
            "My body moves forward; my mind stays trapped in the past.",
            "The horizon fades faster than my hope ever could.",
            "Each step forward feels like two steps closer to nowhere.",
            "The apocalypse chases me, but I've been running my whole life.",
            "I vault over ruins, the same way I avoid my reflection.",
            "Every move reminds me how fragile this existence really is.",
            "The sound of my breath echoes louder than my will to live.",
            "I scale walls built by those who never saw this coming.",
            "Each fall feels more inviting than the ground I leave behind.",
            "The teleporter looms ahead, a hollow promise of salvation.",
            "I'm not running toward life; I'm running away from memories.",
            "Every obstacle feels personal, as if the world knows my sins.",
            "I survive, but survival feels like the cruelest punishment.",
            "The ground shakes, but it's nothing compared to my own instability.",
            "My shadow keeps up, the only constant in this collapse.",
            "I push forward because stopping feels too familiar.",
            "Each ledge I grab feels colder than the void inside me.",
            "I dodge falling debris, but not the thoughts that haunt me.",
            "Every heartbeat feels borrowed, as if I don't deserve it.",
            "I land, not with triumph, but with the weight of failure.",
            "The world burns around me, but I've been scorched for years.",
            "I move forward because turning back is no longer an option.",
            "Every successful jump is another reminder I'm still here.",
            "I sprint toward the future, but it feels like a dead end.",
            "The wind carries me forward, as if it knows I can't stop.",
            "Each wall I climb feels steeper than the last, like my regrets.",
            "The stars disappear, but I've grown used to the darkness.",
            "Every calculated move hides the chaos in my mind.",
            "The teleporter hums ahead, indifferent to my hesitation.",
            "Every misstep feels deliberate, like my subconscious wants me to fail.",
            "I leap across the void, a metaphor I wish I didn't understand.",
            "The closer I get to escape, the heavier my body feels.",
            "I navigate destruction, wondering if it mirrors what's inside me."
        ]
        self.current_text = ""
        self.char_index = 0
        self.text_index = 0
        self.typing_speed = 1.5
        self.pause_timer = 0
        self.pause_duration = 120
        self.displayed_lines = []
        self.max_lines = 2
        self.font = pygame.font.Font(None, 20)
        self.text_color = (200, 200, 200)
        self.bar_height = 53
        
    def update(self):
        if self.pause_timer > 0:
            self.pause_timer -= 1
            if self.pause_timer <= 0:
                self.next_text()
            return

        if self.char_index < len(self.texts[self.text_index]):
            self.char_index += self.typing_speed
            self.current_text = self.texts[self.text_index][:int(self.char_index)]
        else:
            if self.pause_timer <= 0:
                self.pause_timer = self.pause_duration

    def next_text(self):
        if self.current_text:
            self.displayed_lines.append(self.current_text)
            if len(self.displayed_lines) > self.max_lines:
                self.displayed_lines.pop(0)
        self.text_index = (self.text_index + 1) % len(self.texts)
        self.char_index = 0
        self.current_text = ""

    def draw(self, screen):
        # Draw black bar at top
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, screen_width, self.bar_height))
        
        # Calculate vertical center positions
        first_line_y = self.bar_height * 0.3
        second_line_y = self.bar_height * 0.7
        
        # Draw previous line (if exists)
        if self.displayed_lines:
            text_surface = self.font.render(self.displayed_lines[-1], True, self.text_color)
            text_rect = text_surface.get_rect(center=(screen_width // 2, first_line_y))
            screen.blit(text_surface, text_rect)

        # Draw current typing text
        if self.current_text:
            text_surface = self.font.render(self.current_text, True, self.text_color)
            text_rect = text_surface.get_rect(center=(screen_width // 2, second_line_y))
            screen.blit(text_surface, text_rect)

player = Player(100, screen_height - 130)

blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()


score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)



if path.exists(f'level{level}_data'):
	pickle_in = open(f'level{level}_data', 'rb')
	world_data = pickle.load(pickle_in)
world = World(world_data)


#game loop 
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_img = pygame.image.load('img/start_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')

# Scale buttons to be smaller (adjust these values as needed)
start_img = pygame.transform.scale(start_img, (150, 50))  # Original size reduced by about 25%
exit_img = pygame.transform.scale(exit_img, (150, 50))    # Adjust these numbers as needed

start_button = Button(screen_width // 2 - start_img.get_width() // 2, 
                     screen_height // 2 - start_img.get_height(), 
                     start_img)
exit_button = Button(screen_width // 2 - exit_img.get_width() // 2, 
                    screen_height // 2 + exit_img.get_height(), 
                    exit_img)

text_scroller = TextScroller()

run = True
while run:

	clock.tick(fps)

	screen.blit(bg_img, (0, 0))

	if main_menu == True:
		screen.blit(bg_img, (0, 0))
		
		# Stack elements vertically in center
		vertical_spacing = 25  # Reduced from 50 to 25 (50% less)
		
		# Center and position title
		title_x = screen_width // 2 - title_img.get_width() // 2
		title_y = screen_height // 3
		screen.blit(title_img, (title_x, title_y))
		
		# Position start button below title
		start_y = title_y + title_img.get_height() + vertical_spacing
		start_button = Button(screen_width // 2 - start_img.get_width() // 2,
							 start_y,
							 start_img)
		
		# Position exit button below start button
		exit_y = start_y + start_img.get_height() + vertical_spacing
		exit_button = Button(screen_width // 2 - exit_img.get_width() // 2,
							exit_y,
							exit_img)
		
		# Draw buttons
		if exit_button.draw():
			run = False
		if start_button.draw():
			main_menu = False
	else:
		world.draw()

		if game_over == 0:
			blob_group.update()
			platform_group.update()
			#update score
			#check if a coin has been collected
			if pygame.sprite.spritecollide(player, coin_group, True):
				score += 1
			draw_text('X ' + str(score), font_score, white, tile_size - 10, 10)
		
		blob_group.draw(screen)
		platform_group.draw(screen)
		lava_group.draw(screen)
		coin_group.draw(screen)
		exit_group.draw(screen)

		game_over = player.update(game_over)

		#if player has died
		if game_over == -1:
			# Center the restart button
			restart_button = Button(screen_width // 2 - restart_img.get_width() // 2,
								  screen_height // 2 - restart_img.get_height() // 2,
								  restart_img)
			
			if restart_button.draw():
				world_data = []
				world = reset_level(level)
				game_over = 0
				score = 0

		#if player has completed the level
		if game_over == 1:
			#reset game and go to next level
			level += 1
			if level <= max_levels:
				#reset level
				world_data = []
				world = reset_level(level)
				game_over = 0
			else:
				# Just show restart button, no "YOU WIN!" text
				restart_button = Button(screen_width // 2 - restart_img.get_width() // 2,
									  screen_height // 2 - restart_img.get_height() // 2,
									  restart_img)
				if restart_button.draw():
					level = 1
					world_data = []
					world = reset_level(level)
					game_over = 0
					score = 0

	# Update text scroller
	text_scroller.update()
	# Draw text scroller last so it appears on top
	text_scroller.draw(screen)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()
