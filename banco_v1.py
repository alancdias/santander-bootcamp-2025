import time
menu = """
O que deseja fazer?
[1] Consultar extrato
[2] Saque
[3] Depósito
[0] Sair
=> """

saldo = 0 #Saldo atual
LIMITE_SAQUES = 3 #limite de saques por dia
LIMITE_VALOR_SAQUE = 500 #limite para cada saque
historico = '' #Histórico de operações (extrato)
num_saques = 0 #número de saques realizados no dia

def saque():
    global saldo, LIMITE_SAQUES, LIMITE_VALOR_SAQUE, historico, num_saques
    valor = float(input("Qual valor gostaria de sacar? "))
    if valor <= 0: #não se pode sacar valores negativos ou zero
        print('O valor deve ser maior que 0.')
    elif num_saques >= LIMITE_SAQUES: # o limite de saques por dia deve ser respeitado
        print(f"Número diário de {LIMITE_SAQUES} saques excedido. Tente novamente amanhã.")
    elif valor > LIMITE_VALOR_SAQUE: #o valor limite por saque deve ser respeitado
        print(f"Valor acima do limite por saque ({LIMITE_VALOR_SAQUE}). Operação não realizada.")
    elif valor > saldo: #não se pode sacar mais do que se tem em conta
        print("Saldo insuficiente. Operação não realizada.")
    else:
        saldo -= valor #subtrati o valor sacado do saldo
        num_saques +=1 #mantém registro do número de saques
        historico += f'{time.strftime("%d/%m/%y - %H:%M", time.localtime())} -> Saque de {valor}\n' #Registra a operação no histórico
        print(f'Saque de {valor} realizado com sucesso.')
    

def deposito():
    global saldo, historico
    valor = float(input("Qual valor gostaria de depositar? "))
    if valor <= 0: #não se pode depositar valores negativos ou zero
        print('O valor deve ser maior que 0.')
    else:
        saldo += valor #adiciona o valor depositado ao saldo
        historico += f'{time.strftime("%d/%m/%y - %H:%M", time.localtime())} -> Depósito de {valor}\n' #Registra a operação no histórico
        print(f'Depósito de {valor} realizado com sucesso.')

def extrato():
    print('Extrato de operações'.center(40, '='))
    print(historico)
    print(f'Saldo atual: R$ {saldo:.2f}')
    print('='.center(40, '='))

if __name__ == '__main__':
    print('Bem vindo(a) ao nosso banco.')


    while True:
        opcao = input(menu)
        if opcao == '0':
            print('Obrigado por usar nosso banco.')
            break
        elif opcao == '1':
            extrato()
        elif opcao == '2':
            saque()
        elif opcao == '3':
            deposito()
        else:
            print('Opção inválida.')