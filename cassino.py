import random
import time

simbolos = ["🍒", "🍋", "🍉", "⭐", "🔔", "💎"]

def rodar():
    return random.choice(simbolos), random.choice(simbolos), random.choice(simbolos)

while True:
    input("Aperte Enter para jogar...")
    r1, r2, r3 = rodar()

    # Rolagem simples
    for i in range(3):
        
        print(random.choice(simbolos), end=" | ")
        time.sleep(0.3)
    print("\n")

    print(f"{r1} | {r2} | {r3}")
    if r1 == r2 == r3:
        print("3 iguais! Ganhou!")
    elif r1 == r2 or r2 == r3 or r1 == r3:
        print("2 iguais!")
    else:
        print("Nada.")
