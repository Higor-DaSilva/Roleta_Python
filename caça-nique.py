# -*- coding: utf-8 -*-
import random
import time
import os
import sys
from itertools import cycle

# ==========================
# CONFIGURAÇÕES DO JOGO
# ==========================
SIMBOLOS = ["🍒", "🍋", "🍉", "⭐", "🔔", "💎"]
# Pesos (opcional): deixa 💎 e ⭐ mais raros para pagar melhor
PESOS   = [  5,    5,    5,    3,    3,    2 ]

FICHAS_INICIAIS = 100
APOSTA_MINIMA   = 5

# Pagamentos base
PAGAMENTO_TRIPLA_PADRAO = 5   # 3 iguais: aposta * 5
PAGAMENTO_DUPLA_PADRAO  = 2   # 2 iguais: aposta * 2

# Bônus por triplas especiais
BONUS_TRIPLAS = {
    "💎": 12,   # tripla de diamantes paga x12
    "⭐": 8,    # tripla de estrela paga x8
    "🔔": 6,    # tripla de sino paga x6
    # as demais usam o padrão (x5)
}

# Velocidade/tempo da animação (ajuste se quiser)
PASSOS_ANIMACAO = 16      # quantos símbolos "passam" antes de parar
PAUSA_FRAME     = 0.055   # pausa entre frames (segundos)

# ==========================
# UTILITÁRIOS DE TELA/CORES
# ==========================
CSI = "\033["  # Control Sequence Introducer

def clear():
    # limpa e posiciona o cursor no topo
    sys.stdout.write(CSI + "2J" + CSI + "H")
    sys.stdout.flush()

def color(txt, code):
    return f"\033[{code}m{txt}\033[0m"

def verde(txt): return color(txt, "92")
def vermelho(txt): return color(txt, "91")
def amarelo(txt): return color(txt, "93")
def ciano(txt): return color(txt, "96")
def bold(txt): return color(txt, "1")

# ==========================
# DESENHO DA MÁQUINA
# ==========================
def janela_simbolo(simbolo, destaque=False):
    """Retorna 3 linhas que desenham uma janelinha com o símbolo."""
    borda = "┏━━━━━┓" if destaque else "┌─────┐"
    base  = "┗━━━━━┛" if destaque else "└─────┘"
    meio  = f"│  {simbolo}  │"
    return [borda, meio, base]

def juntar_horizontal(blocos):
    """Recebe lista de blocos (cada bloco = lista de linhas) e junta lado a lado."""
    linhas = []
    altura = len(blocos[0])
    for i in range(altura):
        linha = "  ".join(b[i] for b in blocos)
        linhas.append(linha)
    return linhas

def desenhar_maquina(creditos, aposta, rolos, mensagem="", destaque=None, pot=None):
    """
    rolos: lista de 3 símbolos (ou símbolos atuais da animação)
    destaque: índice(s) para destacar janelas vencedoras (set ou list), opcional
    pot: não usado aqui, mas deixado para expansão
    """
    if destaque is None:
        destaque = set()
    janelas = []
    for idx, s in enumerate(rolos):
        janelas.append(janela_simbolo(s, destaque=(idx in destaque)))
    janelas_linhas = juntar_horizontal(janelas)

    topo = [
        "        ╔══════════════════════════════════════════╗",
        "        ║         🎰  SLOT MACHINE – VEGAS  🎰     ║",
        "        ╚══════════════════════════════════════════╝",
    ]
    visor = [
        "                 ╭────────────────────────╮",
        f"                 │  Fichas: {creditos:>4}   Aposta: {aposta:>4} │",
        "                 ╰────────────────────────╯",
    ]
    corpo = [
        "            ╭──────────────────────────────────────╮",
        "            │                                      │",
    ] + [f"            │      {linha:<36}│" for linha in janelas_linhas] + [
        "            │                                      │",
        "            ╰──────────────────────────────────────╯",
        "                    ⎺⎺⎺⎺⎺⎺⎺   ⎺⎺⎺⎺⎺⎺⎺   ⎺⎺⎺⎺⎺⎺⎺",
        "                         [  G  I  R  A  R  ]",
        "",
    ]
    if mensagem:
        corpo.append(" " * 8 + mensagem)

    return "\n".join(topo + [""] + visor + [""] + corpo)

# ==========================
# LÓGICA DO JOGO
# ==========================
def sortear_simbolo():
    # sorteio ponderado
    return random.choices(SIMBOLOS, weights=PESOS, k=1)[0]

def animar_rolos(creditos, aposta, finais):
    """
    Anima três rolos, parando um por vez.
    finais: lista com os 3 símbolos finais já sorteados.
    Retorna a sequência final (igual a 'finais'; mantido para semântica).
    """
    ciclos = [cycle(SIMBOLOS), cycle(SIMBOLOS), cycle(SIMBOLOS)]
    atuais = [next(ciclos[0]), next(ciclos[1]), next(ciclos[2])]
    passos = [PASSOS_ANIMACAO, PASSOS_ANIMACAO + 6, PASSOS_ANIMACAO + 12]

    for t in range(max(passos)):
        clear()
        # Para cada rolo, decide se ainda gira ou já travou no final
        for i in range(3):
            if t < passos[i] - 1:
                atuais[i] = next(ciclos[i])
            elif t == passos[i] - 1:
                # no último passo desse rolo, coloca o símbolo final
                atuais[i] = finais[i]

        print(desenhar_maquina(creditos, aposta, atuais))
        time.sleep(PAUSA_FRAME)

    # quadro final (garante frame limpo)
    clear()
    print(desenhar_maquina(creditos, aposta, finais))
    return finais

def calcular_premio(rolos, aposta):
    r1, r2, r3 = rolos
    # Três iguais
    if r1 == r2 == r3:
        mult = BONUS_TRIPLAS.get(r1, PAGAMENTO_TRIPLA_PADRAO)
        return aposta * mult, f"{verde('JACKPOT!')} 3 {r1} — pagamento x{mult}", {0,1,2}
    # Dupla (qualquer)
    if r1 == r2 or r2 == r3 or r1 == r3:
        # destaca a dupla
        if r1 == r2: desta = {0,1}
        elif r2 == r3: desta = {1,2}
        else: desta = {0,2}
        return aposta * PAGAMENTO_DUPLA_PADRAO, f"{amarelo('Dupla!')} pagamento x{PAGAMENTO_DUPLA_PADRAO}", desta
    # Nada
    return 0, f"{vermelho('Sem prêmio.')} Tente novamente!", set()

def pedir_aposta(creditos):
    while True:
        try:
            txt = input(f"Quantas fichas deseja apostar? (mín {APOSTA_MINIMA}, você tem {creditos}): ").strip()
            aposta = int(txt)
            if aposta < APOSTA_MINIMA:
                print(f"⚠️  A aposta mínima é {APOSTA_MINIMA}.")
            elif aposta > creditos:
                print("⚠️  Você não tem fichas suficientes.")
            else:
                return aposta
        except ValueError:
            print("⚠️  Digite um número válido.")

def main():
    random.seed()
    fichas = FICHAS_INICIAIS
    clear()
    print(bold("🎰 Bem-vindo à Slot Machine de Las Vegas!"))
    print(f"💰 Você começa com {ciano(fichas)} fichas.")
    print(f"💵 Aposta mínima: {amarelo(APOSTA_MINIMA)} fichas.")
    print("➡️  Pressione ENTER para começar.")
    input()

    while fichas >= APOSTA_MINIMA:
        aposta = pedir_aposta(fichas)
        fichas -= aposta

        # Sorteia os símbolos finais de cada rolo
        finais = [sortear_simbolo(), sortear_simbolo(), sortear_simbolo()]

        # Anima rolos e mostra máquina
        animar_rolos(fichas, aposta, finais)

        # Calcula prêmio e destaca janelas vencedoras
        ganho, msg, destaque = calcular_premio(finais, aposta)

        # Mostra mensagem de resultado com destaque
        clear()
        print(desenhar_maquina(fichas, aposta, finais, mensagem=bold(msg), destaque=destaque))
        time.sleep(0.8)

        if ganho > 0:
            fichas += ganho
            print(verde(f"\n🔔 Você ganhou {ganho} fichas!"))
        else:
            print(vermelho("\n💀 Nenhum ganho desta vez."))

        print(f"💰 Fichas atuais: {ciano(fichas)}")

        if fichas < APOSTA_MINIMA:
            print(vermelho("\n🚫 Você não tem fichas suficientes para continuar. Fim de jogo!"))
            break

        resp = input("\nDeseja continuar? (s/n): ").strip().lower()
        if resp != "s":
            print("\n👋 Obrigado por jogar! Até a próxima.")
            break

if __name__ == "__main__":
    try:
        # Ativa processamento ANSI no Windows antigo (no-op na maioria)
        os.system("")  
        main()
    except KeyboardInterrupt:
        clear()
        print("\n👋 Jogo encerrado.")

