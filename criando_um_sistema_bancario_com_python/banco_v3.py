import time
from abc import ABC, abstractmethod

class Cliente:
    def __init__(self, endereco:str):
        self._endereco = endereco
        self._contas = []

    @property
    def endereco(self):
        return self._endereco

    @property
    def contas(self):
        return self._contas
    
    def adicionar_conta(self, conta):
        self._contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def cpf(self):
        return self._cpf

    @property
    def nome(self):
        return self._nome

    @property
    def data_nascimento(self):
        return self._data_nascimento

    def __str__(self):
        return f'{self._cpf} - {self._nome}'
    

class Conta:
    def __init__(self, numero, cliente, saldo, agencia):
        self._agencia = agencia
        self._numero = numero
        self._cliente = cliente
        self._historico = Historico()
        self._saldo=saldo

    @property
    def numero(self):
        return self._numero

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    @property
    def saldo(self):
        return self._saldo

    @property
    def agencia(self):
        return self._agencia

    @classmethod
    def nova_conta(cls, cliente:Cliente, numero:int):
        return cls(numero, cliente, saldo=0, agencia='0001')

    def sacar(self, valor:float):
        if valor <= 0:
            print('O valor deve ser maior que 0.')
        elif valor > self.saldo:
            print('Saldo insuficiente. Operação não realizada.')
        else:
            self._saldo -= valor
            print(f'Saque de {valor} realizado com sucesso.')
            return True
        return False

    def depositar(self, valor:float):
        if valor <= 0:
            print('O valor deve ser maior que 0.')
            return False
        else:
            self._saldo += valor
            print(f'Depósito de {valor} realizado com sucesso.')
            return True

    def __str__(self):
        return f'Agência {self.agencia} - Cc {self.numero} - {self.cliente}'


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, saldo, agencia, limite:float=500.0, limite_saques:int=3):
        super().__init__(numero, cliente, saldo, agencia)
        self._limite = limite
        self._limite_saques = limite_saques
        self.num_saques = 0

    @property
    def limite(self):
        return self._limite
    
    @property
    def limite_saques(self):
        return self._limite_saques
    
    def sacar(self, valor:float):
        if self.num_saques >= self.limite_saques:
            print(f"Número diário de {self.limite_saques} saques excedido. Tente novamente amanhã.")
        elif valor > self.limite:
            print(f"Valor acima do limite por saque ({self.limite}). Operação não realizada.")
        else:
            self.num_saques += 1
            return super().sacar(valor)
        return False
    

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            'data-hora': time.strftime("%d/%m/%y - %H:%M:%S", time.localtime()),
            'tipo': transacao.__class__.__name__,
            'valor': transacao.valor
            }
        )

    def __str__(self):
        return '\n'.join(['   -   '.join([f'{value}' for value in transacao.values()]) for transacao in self.transacoes])


class Transacao(ABC): #interface
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta:Conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta:Conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta:Conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


clientes = {}
contas = {}

def valida_cliente_conta():
    num_conta = int(input('Digite o número da conta: '))
    if num_conta not in contas.keys():
        print('Conta não encontrada. Operação não realizada.')
    else:
        cpf = input('Digite o cpf do cliente: ')
        if cpf != contas[num_conta].cliente.cpf:
            print('Cliente não associado à conta informada. Operação não realizada.')
        else:
            return True, contas[num_conta]
    return False, None

def saque(*, valor:float): #deve receber argumentos keyword_only (*, kwargs)
    success, conta = valida_cliente_conta()
    if success:
        Saque(valor).registrar(conta)
    

def deposito(valor:float, /): #deve receber argumentos position_only (args, /)
    success, conta = valida_cliente_conta()
    if success:
        Deposito(valor).registrar(conta)

def extrato(): #argumentos position_only: saldo; argumentos keyword_only:extrato
    success, conta = valida_cliente_conta()
    if success:
        print('Extrato de operações'.center(60,'='))
        print(conta, '\n')
        print(conta.historico)
        print(f'Saldo atual: R$ {conta.saldo:.2f}')
        print('='.center(60,'='))

def cadastrar_cliente(nome, nascimento, cpf, endereco):
    if cpf in clientes.keys():
        print('O CPF inserido já possui cadastro no banco. Operação não realizada.')
    else:
        clientes[cpf] = PessoaFisica(cpf, nome, nascimento, endereco)
        print(f'Cliente cadastrado: {clientes[cpf]}')

def cadastrar_conta(cliente):
    if cliente not in clientes.keys():
        print('O CPF digitado não está cadastrado no banco. Favor cadastrar cliente ou digitar CPF cadastrado.')
    else:
        num_conta = max(contas.keys()) + 1 if len(contas.keys()) else 1
        print('Número da Conta:', num_conta)
        conta = ContaCorrente(numero=num_conta, cliente=clientes[cliente], saldo=0, agencia='0001')
        clientes[cliente].adicionar_conta(conta)
        contas[num_conta] = conta
        print(f"Conta cadastrada -> {conta}")
        

def listar_clientes():
    print('Lista de clientes da agência 0001'.center(60, '='))
    for cpf, cliente in clientes.items():
        print(cliente)

def listar_contas():
    print('Lista de contas cadastradas na agência'.center(60, '='))
    for num_conta, conta in contas.items():
        print(f'{num_conta} -> {conta}')


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

if __name__ == '__main__':
    print('Bem vindo(a) ao nosso banco.')


    while True:
        opcao = input(menu)
        if opcao == '0':
            print('Obrigado por usar nosso banco.')
            break
        elif opcao == '1': #Consultar extrato
            extrato()
        elif opcao == '2': #Sacar
            valor = float(input("Qual valor gostaria de sacar? "))
            saque(valor=valor)
        elif opcao == '3': #Depositar
            print('Depósito'.center(60,'='))
            valor = float(input("Qual valor gostaria de depositar? "))
            deposito(valor)
        elif opcao == '4': #Cadastrar novo cliente
            print('Cadastro de novo cliente'.center(60,'='))
            nome = input('Digite o nome do cliente: ')
            cpf = input('Digite o CPF do cliente (apenas números): ')
            nascimento = input('Digite a data de nascimento ("DD/MM/AAAA"): ')
            endereco = input('Digite o endereço do cliente: ')
            cadastrar_cliente(nome, nascimento, cpf, endereco)
        elif opcao == '5': #Cadastrar nova conta
            print('Cadastro de nova conta'.center(60,'='))
            cliente = input('Digite o CPF (somente números) do cliente ao qual a conta será vinculada: ')
            cadastrar_conta(cliente)
        elif opcao == '6': #Listar clientes
            listar_clientes()
        elif opcao == '7': #Listar contas
            listar_contas()
        else:
            print('Opção inválida.')