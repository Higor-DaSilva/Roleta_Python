import random

# Categorias e cartas traduzidas
naipes = ['Copas', 'Ouros', 'Paus', 'Espadas']
cartas = ['Ás', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valete', 'Dama', 'Rei']

# Função para criar baralho
def criar_baralho():
    return [(carta, naipe) for naipe in naipes for carta in cartas]

# Função para calcular valor da carta
def valor_carta(carta):
    if carta[0] in ['Valete', 'Dama', 'Rei']:
        return 10
    elif carta[0] == 'Ás':
        return 11
    else:
        return int(carta[0])

# Função para mostrar cartas
def mostrar_cartas(jogador, cartas_jogador):
    print(f"Cartas do {jogador}: {cartas_jogador}")
    print(f"Pontuação do {jogador}: {sum(valor_carta(c) for c in cartas_jogador)}\n")

# Sistema de fichas
fichas = 100

print("🎲 Bem-vindo ao Blackjack 🎲")
print(f"Você começa com {fichas} fichas.\n")

while fichas > 0:
    # Criar e embaralhar o baralho
    baralho = criar_baralho()
    random.shuffle(baralho)

    # Apostar
    while True:
        try:
            aposta = int(input(f"Quantas fichas deseja apostar? (Você tem {fichas}): "))
            if 1 <= aposta <= fichas:
                break
            else:
                print("⚠️ Valor de aposta inválido!")
        except ValueError:
            print("⚠️ Digite um número válido!")

    # Distribuir cartas
    jogador = [baralho.pop(), baralho.pop()]
    dealer = [baralho.pop(), baralho.pop()]

    # Turno do jogador
    while True:
        mostrar_cartas("Jogador", jogador)
        escolha = input('Digite "jogar" para pegar carta ou "parar" para encerrar: ').strip().lower()
        
        if escolha == "jogar":
            nova_carta = baralho.pop()
            jogador.append(nova_carta)
            if sum(valor_carta(c) for c in jogador) > 21:
                mostrar_cartas("Jogador", jogador)
                print("💥 Você estourou! Dealer vence.")
                fichas -= aposta
                break
        elif escolha == "parar":
            break
        else:
            print("⚠️ Escolha inválida!")

    # Turno do dealer (se o jogador não tiver estourado)
    if sum(valor_carta(c) for c in jogador) <= 21:
        while sum(valor_carta(c) for c in dealer) < 17:
            dealer.append(baralho.pop())

        mostrar_cartas("Dealer", dealer)
        mostrar_cartas("Jogador", jogador)

        pontuacao_jogador = sum(valor_carta(c) for c in jogador)
        pontuacao_dealer = sum(valor_carta(c) for c in dealer)

        if pontuacao_dealer > 21:
            print("🔥 Dealer estourou! Você venceu!")
            fichas += aposta
        elif pontuacao_jogador > pontuacao_dealer:
            print("🏆 Você venceu!")
            fichas += aposta
        elif pontuacao_dealer > pontuacao_jogador:
            print("💀 Dealer venceu!")
            fichas -= aposta
        else:
            print("🤝 Empate! Ninguém perde fichas.")

    print(f"💰 Fichas restantes: {fichas}\n")
    if fichas <= 0:
        print("🚫 Você ficou sem fichas! Fim de jogo.")
        break

    continuar = input("Deseja continuar jogando? (s/n): ").strip().lower()
    if continuar != 's':
        print("👋 Obrigado por jogar!")
        break
