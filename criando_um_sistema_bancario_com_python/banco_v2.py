import time
menu = """
O que deseja fazer?
[1] Consultar extrato
[2] Saque
[3] Depósito
[4] Cadastrar novo cliente
[5] Cadastrar nova conta
[6] Listar clientes cadastrados
[7] Listar contas cadastradas
[0] Sair
=> """

saldo = 0 #Saldo atual
LIMITE_SAQUES = 3 #limite de saques por dia
LIMITE_VALOR_SAQUE = 500 #limite para cada saque
historico = '' #Histórico de operações (extrato)
num_saques = 0 #número de saques realizados no dia
clientes = {}
contas = {}

def saque(*, saldo, valor, historico, limite, num_saques, lim_valor_saque): #deve receber argumentos keyword_only (*, kwargs)
    if valor <= 0: #não se pode sacar valores negativos ou zero
        print('O valor deve ser maior que 0.')
    elif num_saques >= limite: # o limite de saques por dia deve ser respeitado
        print(f"Número diário de {limite} saques excedido. Tente novamente amanhã.")
    elif valor > lim_valor_saque: #o valor limite por saque deve ser respeitado
        print(f"Valor acima do limite por saque ({lim_valor_saque}). Operação não realizada.")
    elif valor > saldo: #não se pode sacar mais do que se tem em conta
        print("Saldo insuficiente. Operação não realizada.")
    else:
        saldo -= valor #subtrati o valor sacado do saldo
        num_saques +=1 #mantém registro do número de saques
        historico += f'{time.strftime("%d/%m/%y - %H:%M", time.localtime())} -> Saque de {valor}\n' #Registra a operação no histórico
        print(f'Saque de {valor} realizado com sucesso.')
    return num_saques, saldo, historico
    

def deposito(saldo, valor, historico, /): #deve receber argumentos position_only (args, /)
    if valor <= 0: #não se pode depositar valores negativos ou zero
        print('O valor deve ser maior que 0.')
    else:
        saldo += valor #adiciona o valor depositado ao saldo
        historico += f'{time.strftime("%d/%m/%y - %H:%M", time.localtime())} -> Depósito de {valor}\n' #Registra a operação no histórico
        print(f'Depósito de {valor} realizado com sucesso.')
    return saldo, historico

def extrato(saldo, /, *, historico): #argumentos position_only: saldo; argumentos keyword_only:extrato
    print('Extrato de operações'.center(60,'='))
    print(historico)
    print(f'Saldo atual: R$ {saldo:.2f}')
    print('='.center(60,'='))

def cadastrar_cliente(nome, nascimento, cpf, endereco):
    if cpf in clientes:
        print('O CPF inserido já possui cadastro no banco. Operação não realizada.')
    else:
        clientes[cpf] = dict(nome=nome, nascimento=nascimento, endereco=endereco)
        print(f'Usuário {nome} ({cpf}) cadastrado com sucesso')

def cadastrar_conta(cliente):
    if cliente not in clientes.keys():
        print('O CPF digitado não está cadastrado no banco. Favor cadastrar cliente ou digitar CPF cadastrado.')
    else:
        agencia = '0001'
        if contas.keys():
            num_conta = max(contas.keys())+1
        else:
            num_conta = 1
        contas[num_conta] = dict(cliente=cliente, agencia=agencia)
        print(f"Conta cadastrada para {clientes[cliente]['nome']}; Agência {agencia}, Conta {num_conta}")
        

def listar_clientes():
    print('Lista de clientes da agência 0001'.center(60, '='))
    for cpf, dados in clientes.items():
        print(cpf, dados)

def listar_contas():
    print('Lista de contas cadastradas na agência'.center(60, '='))
    for conta, cliente in contas.items():
        print(conta, cliente)

if __name__ == '__main__':
    print('Bem vindo(a) ao nosso banco.')


    while True:
        opcao = input(menu)
        if opcao == '0':
            print('Obrigado por usar nosso banco.')
            break
        elif opcao == '1':
            extrato(saldo, historico=historico)
        elif opcao == '2':
            valor = float(input("Qual valor gostaria de sacar? "))
            num_saques, saldo, historico = saque(saldo=saldo, valor=valor, historico=historico, limite=LIMITE_SAQUES, num_saques=num_saques, lim_valor_saque=LIMITE_VALOR_SAQUE)
        elif opcao == '3':
            print('Depósito'.center(60,'='))
            valor = float(input("Qual valor gostaria de depositar? "))
            saldo, historico = deposito(saldo, valor, historico)
        elif opcao == '4':
            print('Cadastro de novo cliente'.center(60,'='))
            nome = input('Digite o nome do cliente: ')
            cpf = input('Digite o CPF do cliente (apenas números): ')
            nascimento = input('Digite a data de nascimento ("DD/MM/AAAA"): ')
            endereco = input('Digite o endereço do cliente: ')
            cadastrar_cliente(nome, nascimento, cpf, endereco)
        elif opcao == '5':
            print('Cadastro de nova conta'.center(60,'='))
            cliente = input('Digite o CPF (somente números) do cliente ao qual a conta será vinculada: ')
            cadastrar_conta(cliente)
        elif opcao == '6':
            listar_clientes()
        elif opcao == '7':
            listar_contas()
        else:
            print('Opção inválida.')