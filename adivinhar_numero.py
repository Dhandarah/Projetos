import random

def main():
    numero_secreto = random.randint(1, 100)
    tentativas = 0
    acertou = False

    print("Bem-vindo ao jogo de Adivinhar o Número!")
    print("Estou pensando em um número entre 1 e 100.")

    while not acertou:
        tentativa = int(input("Digite sua tentativa: "))

        tentativas += 1

        if tentativa == numero_secreto:
            acertou = True
        elif tentativa < numero_secreto:
            print("O número secreto é maior!")
        else:
            print("O número secreto é menor!")

    print(f"Parabéns, você acertou o número {numero_secreto} em {tentativas} tentativas!")

if __name__ == "__main__":
    main()
