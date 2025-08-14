import random
import time

# Naipes e cartas em português
naipes = ['♠ Espadas', '♥ Copas', '♦ Ouros', '♣ Paus']
cartas = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valete', 'Dama', 'Rei', 'Ás']

# Criar baralho
def criar_baralho():
    return [(carta, naipe) for naipe in naipes for carta in cartas]

# Função para mostrar cartas com delay dramático
def mostrar_cartas(jogador, mao):
    print(f"\n🎴 Cartas de {jogador}: ", end="")
    for carta in mao:
        time.sleep(0.5)
        print(f"{carta[0]} de {carta[1]}", end=" | ")
    print()

# Avaliação de mãos (simplificada)
def ranking_mao(mao):
    valores = [carta[0] for carta in mao]
    naipes_mao = [carta[1] for carta in mao]
    valores_ord = sorted([cartas.index(v) for v in valores], reverse=True)
    contagem = {v: valores.count(v) for v in set(valores)}
    eh_flush = len(set(naipes_mao)) == 1
    eh_straight = all(valores_ord[i] - 1 == valores_ord[i+1] for i in range(len(valores_ord)-1))

    if eh_flush and eh_straight and 'Ás' in valores:
        return (9, "Royal Flush"), valores_ord
    elif eh_flush and eh_straight:
        return (8, "Straight Flush"), valores_ord
    elif 4 in contagem.values():
        return (7, "Quadra"), valores_ord
    elif sorted(contagem.values()) == [2, 3]:
        return (6, "Full House"), valores_ord
    elif eh_flush:
        return (5, "Flush"), valores_ord
    elif eh_straight:
        return (4, "Straight"), valores_ord
    elif 3 in contagem.values():
        return (3, "Trinca"), valores_ord
    elif list(contagem.values()).count(2) == 2:
        return (2, "Dois Pares"), valores_ord
    elif 2 in contagem.values():
        return (1, "Um Par"), valores_ord
    else:
        return (0, "Carta Alta"), valores_ord

# Sistema de fichas
fichas = 200
aposta_minima = 10

print("🎰 Bem-vindo ao Texas Hold’em de Las Vegas 🎰")
print(f"Você começa com {fichas} fichas.")
print("Dealer: 'Boa sorte, campeão.'\n")

while fichas >= aposta_minima:
    baralho = criar_baralho()
    random.shuffle(baralho)

    # Aposta inicial
    pot = aposta_minima * 2
    fichas -= aposta_minima
    dealer_fichas = 200
    dealer_fichas -= aposta_minima
    print(f"💰 Pot inicial: {pot} fichas\n")

    # Cartas privadas
    mao_jogador = [baralho.pop(), baralho.pop()]
    mao_dealer = [baralho.pop(), baralho.pop()]
    mostrar_cartas("Jogador", mao_jogador)
    print("Dealer: 'Vamos ver se você tem coragem.'")

    # Mesa
    mesa = []

    # Flop
    time.sleep(1)
    mesa.extend([baralho.pop() for _ in range(3)])
    print("\n🔥 Flop na mesa:")
    mostrar_cartas("Mesa", mesa)

    # Turn
    time.sleep(1)
    mesa.append(baralho.pop())
    print("\n🔥 Turn na mesa:")
    mostrar_cartas("Mesa", mesa)

    # River
    time.sleep(1)
    mesa.append(baralho.pop())
    print("\n🔥 River na mesa:")
    mostrar_cartas("Mesa", mesa)

    # Determinar vencedor
    mao_final_jogador = mao_jogador + mesa
    mao_final_dealer = mao_dealer + mesa

    rank_jog, valores_jog = ranking_mao(mao_final_jogador)
    rank_deal, valores_deal = ranking_mao(mao_final_dealer)

    print(f"\n🃏 Sua mão final: {rank_jog[1]}")
    print(f"🃏 Mão do Dealer: {rank_deal[1]}")
    time.sleep(1)

    if rank_jog > rank_deal:
        print("🏆 Você venceu a rodada!")
        fichas += pot
    elif rank_deal > rank_jog:
        print("💀 Dealer leva tudo!")
    else:
        print("🤝 Empate! Pot dividido.")
        fichas += pot // 2

    print(f"💰 Suas fichas: {fichas}\n")
    if fichas < aposta_minima:
        print("🚫 Você não tem fichas suficientes. Fim de jogo!")
        break

    cont = input("Continuar jogando? (s/n): ").lower()
    if cont != 's':
        print("👋 Saindo da mesa de Las Vegas...")
        break
