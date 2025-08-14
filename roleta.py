import random
import time

# Símbolos da slot
simbolos = ["🍒", "🍋", "🍉", "⭐", "🔔", "💎"]

# Função para girar os rolos
def rodar():
    return random.choice(simbolos), random.choice(simbolos), random.choice(simbolos)

# Função para exibir giro com suspense
def animar_giro():
    for _ in range(3):
        print(random.choice(simbolos), end=" | ")
        time.sleep(0.3)
    print()

# Sistema de fichas
fichas = 100
aposta_minima = 5

print("🎰 Bem-vindo à Slot Machine de Las Vegas 🎰")
print(f"💰 Você começa com {fichas} fichas.")
print(f"💵 Aposta mínima: {aposta_minima} fichas.\n")

while fichas >= aposta_minima:
    # Escolher aposta
    while True:
        try:
            aposta = int(input(f"Quantas fichas deseja apostar? (Você tem {fichas}): "))
            if aposta_minima <= aposta <= fichas:
                break
            else:
                print(f"⚠️ A aposta deve ser entre {aposta_minima} e {fichas}.")
        except ValueError:
            print("⚠️ Digite um número válido.")

    fichas -= aposta

    input("\n🎯 Aperte Enter para girar...")
    print("\n🎡 Girando...\n")
    animar_giro()

    r1, r2, r3 = rodar()
    print(f"🎯 Resultado: {r1} | {r2} | {r3}")

    # Verifica combinações
    if r1 == r2 == r3:
        ganho = aposta * 5
        fichas += ganho
        print(f"💎 JACKPOT! 3 iguais! Você ganhou {ganho} fichas!")
    elif r1 == r2 or r2 == r3 or r1 == r3:
        ganho = aposta * 2
        fichas += ganho
        print(f"⭐ Dupla! Você ganhou {ganho} fichas!")
    else:
        print("💀 Nada dessa vez...")

    print(f"💰 Fichas restantes: {fichas}\n")

    if fichas < aposta_minima:
        print("🚫 Você não tem fichas suficientes. Fim de jogo!")
        break

    continuar = input("Deseja continuar jogando? (s/n): ").strip().lower()
    if continuar != 's':
        print("👋 Saindo da Slot Machine... Até a próxima!")
        break
