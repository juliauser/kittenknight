# 🍒 KittyKnight - Jogo Platformer com PgZero

Esse é um projeto super divertido de jogo platformer feito em Python usando PgZero! O objetivo? Coletar todas as cerejas enquanto desvia de inimigos travessos que patrulham o cenário! 

> Aqui o link para o vídeo no youtube:
[Kitten Knight - Gameplay 🍒](https://youtu.be/dFHdFvhP5xY)

## Requisitos

Para jogar, precisa ter o PgZero instalado, e com as variáveis de ambiente configuradas. Se ainda não tiver o PgZero, da pra instalar rapidinho com:

> **pip install pgzero**

## Bibliotecas Utilizadas

*PgZero:* Para a parte visual e lógica do jogo.

*math:* Para cálculos matemáticos essenciais.

*random:* Para adicionar aquele toque de imprevisibilidade.

*pygame.Rect:* Para cuidar das colisões no jogo.

## Como Jogar

Use as setas esquerda e direita para se movimentar.
Pressione espaço para pular. O objetivo é coletar todas as cerejas sem ser pego pelos inimigos. Se um inimigo te alcançar, aparece a mensagem de **"Game Over"**. Mas se coletar todas as cerejas, surge o tão esperado **"Parabéns! Você coletou todas as cerejas!"** 🎉

## Classes

Character: Classe base para todos os personagens.

Player: Controla o protagonista e seus pulos.

Enemy: Faz os inimigos se movimentarem de forma traiçoeira.

Platform: Representa onde o jogador pode pisar.

Cereja: São os itens fofos e coletáveis do jogo!

## Como Rodar o Jogo

Para começar a aventura, basta rodar:

> **pgzrun nome_do_arquivo.py**

Lembre-se de substituir nome_do_arquivo.py pelo nome real do seu arquivo.

## Controles

⬅️➡️ Setas: Movem o personagem.

⏹️ Espaço: Faz pular.

🔄 Enter: Reinicia o jogo depois do game over.

🎵 Recursos e Sons

Espero sempre evoluir e me divertir com as minhas criações assim como me diverti com esse projeto! :)
