from pygame import Rect
# Bem-vindo(a) ao mundo de Kitten Knight

# Tamanho da janela
WIDTH = 500
HEIGHT = 300

# Variáveis de estado
game_state = "menu"     # Pode ser "menu", "game", "game_over" ou "end_game"
sound_on = True         # Controla o som
button_width = 120
button_height = 40

# Botões do menu
button_start = Rect((WIDTH - button_width) // 2, 100, button_width, button_height)
button_sound = Rect((WIDTH - button_width) // 2, 150, button_width, button_height)
button_exit = Rect((WIDTH - button_width) // 2, 200, button_width, button_height)

# Música
music.play("background_music")
music.set_volume(0.2)

# Background do jogo
background_img = "background_img"

# Classe base para os personagens (Player e Enemy)
class Character:
    def __init__(self, x, y, sprite_prefix):
        self.rect = Rect((x, y), (16, 32))
        self.speed = 1
        self.status = "idle"        # Estado inicial do personagem
        self.direction = "right"    # Direção inicial do personagem
        self.gravity = 0.5
        self.velocity_y = 0
        
        # Imagens para a animação do personagem (idle e moving) e controle de animação
        self.idle_right = [Actor(f"{sprite_prefix}_idle1"), Actor(f"{sprite_prefix}_idle2")]
        self.moving_right = [Actor(f"{sprite_prefix}_move1"), Actor(f"{sprite_prefix}_move2")]

        self.idle_left = [Actor(f"{sprite_prefix}_idle1_left"), Actor(f"{sprite_prefix}_idle2_left")]
        self.moving_left = [Actor(f"{sprite_prefix}_move1_left"), Actor(f"{sprite_prefix}_move2_left")]
                            
        self.image_index = 0
        self.current_image = self.idle_right[self.image_index]
        self.animation_timer = 0
        self.animation_delay = 0.2

    # Reset do status idle e Gravidade
    def move(self):
        self.status = "idle"
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

    def update_animation(self, dt):
        self.animation_timer += dt      # Incrementa o tempo pela quantidade de tempo desde o último frame
        if self.animation_timer >= self.animation_delay:
            if self.status == "idle":   # Atualiza a imagem de acordo com o status e direção do personagem
                if self.direction == "right":
                    self.current_image = self.idle_right[self.image_index]
                else:
                    self.current_image = self.idle_left[self.image_index]
                self.image_index = (self.image_index + 1) % len(self.idle_right)
            elif self.status == "moving":
                if self.direction == "right":
                    self.current_image = self.moving_right[self.image_index % len(self.moving_right)]
                else:
                    self.current_image = self.moving_left[self.image_index % len(self.moving_left)]
                self.image_index = (self.image_index + 1) % len(self.moving_right)
            self.animation_timer = 0                # Reinicia o timer após trocar a imagem
        self.current_image.pos = self.rect.center   # Atualiza a posição da imagem

    def draw(self):
        self.current_image.draw()   # Desenha a imagem atual na tela

# Classe do PLAYER (herda de Character). Prefixos e Animações
class Player(Character):
    def __init__(self, x, y):
        super().__init__(x, y, "player")
        self.on_ground = True
        self.jump_strength = -10
        self.speed = 3
        self.idle_right.append(Actor("player_idle3"))
        self.idle_left.append(Actor("player_idle3_left"))

    # Movimentação (esquerda e direita) e limitadores
    def move(self):
        super().move()
        if keyboard.left:
            self.rect.x -= self.speed
            if self.rect.left < 0:
                self.rect.left = 0
            self.status = "moving"
            self.direction = "left"
        elif keyboard.right:
            self.rect.x += self.speed
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            self.status = "moving"
            self.direction = "right"

        # Pulo
        if keyboard.space and self.on_ground:
            self.velocity_y = self.jump_strength
            if sound_on:
                sounds.jump_sound.play()
            self.on_ground = False
            
        # Colisão com o chão ou plataformas
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity_y > 0:
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.on_ground = True
                break

# Classe do INIMIGO (herda de Character)
class Enemy(Character):
    def __init__(self, x, y, max_movement):
        super().__init__(x, y, "enemy")
        self.speed = 1  # Velocidade de movimento do inimigo
        self.count = 0
        self.max_movement = max_movement
        
    # Movimentação e colisão
    def move(self):
        super().move()
        if self.direction == "right":
            self.rect.x += self.speed
            self.count += 1
            if self.count >= self.max_movement: 
                self.direction = "left"
                self.count -= self.count
        elif self.direction == "left":
            self.rect.x -= self.speed
            self.count += 1
            if self.count >= self.max_movement:
                self.direction = "right"
                self.count -= self.count
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity_y > 0:
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                break
        self.status = "moving"
        self.update_animation(0)
    
class Platform:
    def __init__(self, x, y):
        self.rect = Rect(x, y, 16, 16)
        self.image = Actor("platform")
        self.image.width = 16
        self.image.height = 16
        self.image.pos = self.rect.center
    def draw(self):
        self.image.draw()

class Cherry:
    def __init__(self, x, y):
        self.rect = Rect(x, y, 16, 16)
        self.image = Actor("cherry")
        self.image.width = 16
        self.image.height = 16
        self.image.pos = self.rect.center
        
    def draw(self):
        self.image.draw()

# Lista de plataformas, inimigos e cerejas
platforms = []
enemies = []
cherrys = []

player = Player(100, 50)    # Cria o personagem

# Cria o mapa, os inimigos e as cerejas
def create_map():
    x = 0
    while x < WIDTH:
        platforms.append(Platform(x, HEIGHT-16))
        x += 16
    x = 100
    while x < 200:
        platforms.append(Platform(x, 180))
        x +=16
    x = 300
    while x < 400:
        platforms.append(Platform(x, 130))
        x +=16
    
    x = 150
    while x < 250:
        platforms.append(Platform(x, 90))
        x +=16
    enemies.append(Enemy(152, 60, 90))
    enemies.append(Enemy(302, 50, 90))
    enemies.append(Enemy(150, 200, 200))
    cherrys.append(Cherry(150, 70))
    cherrys.append(Cherry(400, 110))
    cherrys.append(Cherry(450, 250))

# Função para desenhar a TELA
def draw():
    global game_state
    screen.clear()
    if game_state == "menu":
        draw_menu()
    elif game_state == "game":
        draw_game()
    elif game_state == "game_over":
        draw_game_over()
    elif game_state == "end_game":
        draw_end_game()

# Função para desenhar o MENU
def draw_menu():
    screen.fill((164,161,208))
    screen.draw.text("Menu Principal", center=(WIDTH // 2, 50), fontsize=30, color="black")
    screen.draw.filled_rect(button_start, "pink")
    screen.draw.text("Iniciar Jogo", center=button_start.center, fontsize=20, color="black")
    screen.draw.text("Feito com muito carinho <3 por Julia Nogueira Figueiredo", (15, 275), fontsize=15, color="black")
    
    screen.draw.filled_rect(button_sound, "pink")
    sound_text = "Musica: ON" if sound_on else "Musica: OFF"
    screen.draw.text(sound_text, center=button_sound.center, fontsize=20, color="black")
    
    screen.draw.filled_rect(button_exit, "pink")
    screen.draw.text("Sair", center=button_exit.center, fontsize=20, color="black")

# Função para desenhar o JOGO
def draw_game():
    screen.blit(background_img, (0, 0))
    for platform in platforms:
        platform.draw()
        player.draw()
    for cherry in cherrys:
        cherry.draw()
    for enemy in enemies:
        enemy.draw()

# Função para desenhar tela de GAME OVER
def draw_game_over():
    screen.fill((164,161,208))
    screen.draw.text("Fim de Jogo!", (100, 100), fontsize=40, color="red")
    screen.draw.text("Aperte 'Enter' para tentar novamente", (100, 150), fontsize=20, color="black")

# Função para desenhar tela FINAL
def draw_end_game():
    screen.fill((164,161,208))
    screen.draw.text("Parabens!", (100, 100), fontsize=40, color="black")
    screen.draw.text("Obrigada por jogar!", (100, 150), fontsize=20, color="black")
    screen.draw.text("Aperte 'Enter' para retornar ao Menu", (100, 200), fontsize=20, color="black")

# Função para rodar o jogo
def update(dt):
    global game_state
    if game_state == "game":
        player.move()
        player.update_animation(dt)
        for enemy in enemies:
            enemy.move()
            enemy.update_animation(dt)
            if player.rect.colliderect(enemy.rect):
                if sound_on:
                    sounds.game_over_sound.play()
                game_state = "game_over"
        for cherry in cherrys:
            if player.rect.colliderect(cherry.rect):
                if sound_on:
                    sounds.cherry_sound.play()
                cherrys.remove(cherry)
        if len(cherrys) == 0:
            game_state = "end_game"
    elif game_state == "game_over":
        if keyboard.RETURN:
            game_state ="menu"
    elif game_state == "end_game":
        if keyboard.RETURN:
            game_state ="menu"

# Função para detectar cliques
def on_mouse_down(pos):
    global game_state, sound_on
    if sound_on:
        sounds.click_sound.play()
    if game_state == "menu":
        if button_start.collidepoint(pos):
            game_state = "game" # Iniciar o jogo
            platforms.clear()
            enemies.clear()
            cherrys.clear()
            player.rect.x = 50
            player.rect.y = 50
            create_map()
        elif button_sound.collidepoint(pos):
            sound_on = not sound_on
            if sound_on:
                music.play("background_music")
            else:
                music.stop()
        elif button_exit.collidepoint(pos):
            exit()  # Sair do jogo