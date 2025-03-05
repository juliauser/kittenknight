from pygame import Rect

# Basta utilizar o comando pgzrun para aproveitar o jogo
#
# COMANDOS
# Setas para direita e esquerda para mover
# Espaço para pular
#
# Objetivo
# Coletar todas as flores


# Tamanho da janela
WIDTH = 500
HEIGHT = 300

# Variáveis de estado
game_state = "menu" # Pode ser "menu", "game", "game_over" ou "end_game"
sound_on = True  # Controla o som
button_width = 120
button_height = 40

# Botões centralizados na tela
button_start = Rect((WIDTH - button_width) // 2, 100, button_width, button_height)
button_sound = Rect((WIDTH - button_width) // 2, 150, button_width, button_height)
button_exit = Rect((WIDTH - button_width) // 2, 200, button_width, button_height)

# Música de fundo
music.play("background_music")
music.set_volume(0.1)

# Plano de fundo para o jogo
background_img = "background_img"

# Classe base para personagens (Player e Enemy)
class Character:
    def __init__(self, x, y, sprite_prefix):
        self.rect = Rect((x, y), (16, 16))
        self.speed = 1
        self.status = "idle" # Estado inicial do personagem
        self.direction = "right"  # Direção inicial do personagem
        self.gravity = 0.5
        self.velocity_y = 0
        
        # Imagens para a animação do personagem (idle e moving)
        self.idle_right = [Actor(f"{sprite_prefix}_idle1"), Actor(f"{sprite_prefix}_idle2")]
        self.moving_right = [Actor(f"{sprite_prefix}_move1"), Actor(f"{sprite_prefix}_move2")]

        self.idle_left = [Actor(f"{sprite_prefix}_idle1_left"), Actor(f"{sprite_prefix}_idle2_left")]
        self.moving_left = [Actor(f"{sprite_prefix}_move1_left"), Actor(f"{sprite_prefix}_move2_left")]
                            
        # Imagem atual e controle de animação
        self.image_index = 0
        self.current_image = self.idle_right[self.image_index]
        self.animation_timer = 0  # Timer para controlar o delay entre as trocas de imagem
        self.animation_delay = 0.2  # Tempo em segundos para trocar de imagem

    def move(self):
        # Resetar status para idle no começo de cada movimento
        self.status = "idle"
        
        # Gravidade
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

    def update_animation(self, dt):
        # Incrementa o tempo do timer pela quantidade de tempo desde o último frame
        self.animation_timer += dt
        if self.animation_timer >= self.animation_delay:
            # Atualiza a imagem de acordo com o status e direção do personagem
            if self.status == "idle":
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

            # Reinicia o timer após trocar a imagem
            self.animation_timer = 0

        # Atualiza a posição da imagem
        self.current_image.pos = self.rect.center

    def draw(self):
        # Desenha a imagem atual na tela
        self.current_image.draw()

# Classe do Player (herda de Character)
class Player(Character):
    def __init__(self, x, y):
        # Passa um prefixo específico para a animação do jogador
        super().__init__(x, y, "player")
        self.on_ground = True
        self.jump_strength = -10
        self.speed = 3

        # Adiciona animação extra do jogador
        self.idle_right.append(Actor("player_idle3"))
        
        self.idle_left.append(Actor("player_idle3_left"))


    def move(self):
        super().move()
        # Movimento para a esquerda e direita
        if keyboard.left:
            self.rect.x -= self.speed
            if self.rect.left < 0:  # Impede o personagem de ultrapassar a esquerda
                self.rect.left = 0
            self.status = "moving"
            self.direction = "left"  # Atualiza a direção para esquerda
        elif keyboard.right:
            self.rect.x += self.speed
            if self.rect.right > WIDTH:  # Impede o personagem de ultrapassar a direita
                self.rect.right = WIDTH
            self.status = "moving"
            self.direction = "right"  # Atualiza a direção para direita

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

# Classe do Enemy (herda de Character)
class Enemy(Character):
    def __init__(self, x, y, max_movement):
        super().__init__(x, y, "enemy")
        self.speed = 1  # Velocidade de movimento do inimigo
        self.count = 0
        self.max_movement = max_movement
    
    def move(self):
        super().move()
        # Mover o inimigo de um lado para o outro na plataforma
        if self.direction == "right":
            self.rect.x += self.speed
            self.count += 1
            if self.count >= self.max_movement: 
                self.direction = "left"  # Muda a direção para esquerda
                self.count -= self.count
        elif self.direction == "left":
            self.rect.x -= self.speed
            self.count += 1
            if self.count >= self.max_movement:  # Verifica se ultrapassou a borda esquerda
                self.direction = "right"  # Muda a direção para direita
                self.count -= self.count

        # Colisão com o chão ou plataformas
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity_y > 0:
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                break

        self.status = "moving"  # O inimigo está se movendo
        self.update_animation(0)  # Atualiza a animação do inimigo
    
# Classe para plataformas
class Platform:
    def __init__(self, x, y):
        self.rect = Rect(x, y, 16, 16)
        self.image = Actor("platform")  # Carrega a imagem da plataforma
        self.image.width = 16  # Ajusta a largura da imagem para o tamanho da plataforma
        self.image.height = 16  # Ajusta a altura da imagem para o tamanho da plataforma
        self.image.pos = self.rect.center  # Centraliza a imagem na plataforma

    def draw(self):
        self.image.draw()  # Desenha a plataforma


class Flower:
    def __init__(self, x, y):
        self.rect = Rect(x, y, 16, 16)
        self.image = Actor("flower")
        self.image.width = 16
        self.image.height = 16
        self.image.pos = self.rect.center
        
    def draw(self):
        self.image.draw()

# Lista de plataformas , inimigos e flores
platforms = []
enemies = []
flowers = []

# Cria o personagem
player = Player(200, 50)

# Cria o mapa, os inimigos e as flores
def create_map():
    x = 0
    while x < WIDTH:
        platforms.append(Platform(x, HEIGHT-30))
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
    flowers.append(Flower(150, 70))
    flowers.append(Flower(400, 110))
    flowers.append(Flower(450, 250))

# Função para desenhar a tela
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

# Função para desenhar o menu
def draw_menu():
    screen.draw.text("Main Menu", center=(WIDTH // 2, 50), fontsize=30)
    screen.draw.filled_rect(button_start, "blue")
    screen.draw.text("Start Game", center=button_start.center, fontsize=20, color="white")
    
    screen.draw.filled_rect(button_sound, "blue")
    sound_text = "Sound On" if sound_on else "Sound Off"
    screen.draw.text(sound_text, center=button_sound.center, fontsize=20, color="white")
    
    screen.draw.filled_rect(button_exit, "blue")
    screen.draw.text("Exit", center=button_exit.center, fontsize=20, color="white")

# Função para desenhar o jogo
def draw_game():
    screen.blit(background_img, (0, 0))
    
    for platform in platforms:
        platform.draw()
    
    player.draw()
    for flower in flowers:
        flower.draw()
    for enemy in enemies:
        enemy.draw()

# Função para desenhar tela de game over
def draw_game_over():
    screen.draw.text("Game Over!", (100, 100), fontsize=40, color="red")
    screen.draw.text("Pressione Enter para tentar novamente", (100, 150), fontsize=20, color="white")

# Função para desenhar tela de fim de jogo
def draw_end_game():
    screen.draw.text("Fim de jogo!", center=(WIDTH // 2, 50), fontsize=40, color="green")
    screen.draw.text("Obrigado por jogar!", center=(WIDTH // 2, 150), fontsize=20, color="white")

# Função para rodar o jogo
def update(dt):
    global game_state
    # Verifica se o jogo esta rodando
    if game_state == "game":
        # Move e anima o jogador
        player.move()
        player.update_animation(dt)
        # Move e anima os inimigos
        for enemy in enemies:
            enemy.move()
            enemy.update_animation(dt)
            # Verifica colisão entre jogador e inimigos para determinar derrota
            if player.rect.colliderect(enemy.rect):
                if sound_on:
                    sounds.game_over_sound.play()
                game_state = "game_over"
        # Verifica se o jogador coletou alguma flor
        for flower in flowers:
            if player.rect.colliderect(flower.rect):
                if sound_on:
                    sounds.flower_sound.play()
                flowers.remove(flower)
        # Verifica se todas as flores já foram coletadas para determinar vitória
        if len(flowers) == 0:
            game_state = "end_game"
    # Ao perder, verifica se o jogador quer tentar novamente, voltando ao menu
    elif game_state == "game_over":
        if keyboard.RETURN:
            game_state ="menu"

# Função para detectar cliques
def on_mouse_down(pos):
    global game_state, sound_on
    if sound_on:
        sounds.click_sound.play()
    if game_state == "menu":
        if button_start.collidepoint(pos):
            game_state = "game"  # Iniciar o jogo
            # Remove todos os componentes pré existentes 
            platforms.clear()
            enemies.clear()
            flowers.clear()
            # Move o jogador para posição inicial
            player.rect.x = 50
            player.rect.y = 50
            # Cria todos os componentes do jogo
            create_map()
        elif button_sound.collidepoint(pos):
            sound_on = not sound_on
            if sound_on:
                music.play("background_music")
            else:
                music.stop()
        elif button_exit.collidepoint(pos):
            exit()  # Sair do jogo
