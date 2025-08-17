import pygame
import random
import sys

# Inicialização
pygame.init()
pygame.display.set_caption("Jogo Snake Python")

# Tela
largura, altura = 1200, 800
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

# Cores
preta = (0, 0, 0)
branca = (255, 255, 255)
vermelha = (255, 0, 0)
verde = (0, 255, 0)

# Parâmetros
tamanho_quadrado = 20
velocidade_jogo = 15

# Funções
def gerar_comida():
    comida_x = round(random.randrange(0, largura - tamanho_quadrado) / tamanho_quadrado) * tamanho_quadrado
    comida_y = round(random.randrange(0, altura - tamanho_quadrado) / tamanho_quadrado) * tamanho_quadrado
    return comida_x, comida_y

def desenhar_comida(tamanho, comida_x, comida_y):
    pygame.draw.rect(tela, verde, [comida_x, comida_y, tamanho, tamanho])

def desenhar_cobra(tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, branca, [pixel[0], pixel[1], tamanho, tamanho])

def desenhar_pontuacao(pontuacao):
    fonte = pygame.font.SysFont("Helvetica", 35)
    texto = fonte.render(f"Pontos: {pontuacao}", True, vermelha)
    tela.blit(texto, [10, 10])

def mostrar_game_over(pontuacao):
    tela.fill(preta)
    fonte = pygame.font.SysFont("Helvetica", 60)
    texto = fonte.render("GAME OVER", True, vermelha)
    tela.blit(texto, [largura // 2 - 150, altura // 2 - 80])

    texto2 = pygame.font.SysFont("Helvetica", 35).render(f"Pontuação: {pontuacao}", True, branca)
    tela.blit(texto2, [largura // 2 - 90, altura // 2])

    texto3 = pygame.font.SysFont("Helvetica", 25).render("Pressione R para Reiniciar ou ESC para sair", True, branca)
    tela.blit(texto3, [largura // 2 - 180, altura // 2 + 50])
    pygame.display.update()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    esperando = False
                    rodar_jogo()
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def selecionar_direcao(tecla, vx, vy):
    if tecla == pygame.K_UP and vy == 0:
        return 0, -tamanho_quadrado
    elif tecla == pygame.K_DOWN and vy == 0:
        return 0, tamanho_quadrado
    elif tecla == pygame.K_LEFT and vx == 0:
        return -tamanho_quadrado, 0
    elif tecla == pygame.K_RIGHT and vx == 0:
        return tamanho_quadrado, 0
    return vx, vy

def rodar_jogo():
    x = largura // 2
    y = altura // 2

    velocidade_x = 0
    velocidade_y = 0

    tamanho_cobra = 1
    pixels = []

    comida_x, comida_y = gerar_comida()
    fim_jogo = False

    while not fim_jogo:
        tela.fill(preta)
        desenhar_pontuacao(tamanho_cobra - 1)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                velocidade_x, velocidade_y = selecionar_direcao(evento.key, velocidade_x, velocidade_y)

        x += velocidade_x
        y += velocidade_y

        #   Se bater com a parede
        if x < 0 or x >= largura or y < 0 or y >= altura:
            fim_jogo = True
            break

        # Comer comida
        if x == comida_x and y == comida_y:
            tamanho_cobra += 1
            comida_x, comida_y = gerar_comida()

        # Atualizar corpo da cobra
        novo_cabeca = [x, y]
        pixels.append(novo_cabeca)
        if len(pixels) > tamanho_cobra:
            del pixels[0]

        # Se bater com o próprio corpo
        for bloco in pixels[:-1]:
            if bloco == novo_cabeca:
                fim_jogo = True
                break

        desenhar_comida(tamanho_quadrado, comida_x, comida_y)
        desenhar_cobra(tamanho_quadrado, pixels)

        pygame.display.update()
        relogio.tick(velocidade_jogo)

    mostrar_game_over(tamanho_cobra - 1)

# Inicia o jogo
rodar_jogo()
