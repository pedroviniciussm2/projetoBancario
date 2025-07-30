menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
"""

menu_principal = """
[1] Criar usuário
[2] Criar conta corrente
[3] Listar contas
[4] Acessar conta existente
[5] Sair
=> """

usuarios = []
contas = []

LIMITE_SAQUES = 3
LIMITE_SAQUE_VALOR = 500

def criar_usuario():
    cpf = input("Informe o CPF (somente números): ")
    usuario_existe = any(usuario["cpf"] == cpf for usuario in usuarios)

    if usuario_existe:
        print("Já existe usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    idade = input("Informe a idade: ")
    endereco = input("Informe o endereço: ")

    usuario = {
        "cpf": cpf,
        "nome": nome,
        "idade": idade,
        "endereco": endereco
    }

    usuarios.append(usuario)
    print(f"Usuário {nome} criado com sucesso!")

def criar_conta():
    if not usuarios:
        print("Nenhum usuário cadastrado. Crie um usuário antes de criar uma conta.")
        return
    
    cpf = input("Informe o CPF do usuário para vincular a conta: ")
    usuario = next((u for u in usuarios if u["cpf"] == cpf), None)

    if not usuario:
        print("Usuário não encontrado!")
        return

    numero_conta = len(contas) + 1
    conta = {
        "numero": numero_conta,
        "usuario": usuario,
        "saldo": 0,
        "extrato": "",
        "numero_saques": 0
    }

    contas.append(conta)
    print(f"Conta número {numero_conta} criada para o usuário {usuario['nome']}.")

def listar_contas():
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    
    print("Contas cadastradas:")
    for conta in contas:
        usuario = conta["usuario"]
        print(f"Conta: {conta['numero']} | Titular: {usuario['nome']} | CPF: {usuario['cpf']}")

def acessar_conta():
    if not contas:
        print("Nenhuma conta cadastrada para acessar.")
        return None

    listar_contas()
    try:
        numero = int(input("Informe o número da conta que deseja acessar: "))
    except ValueError:
        print("Número inválido.")
        return None

    conta = next((c for c in contas if c["numero"] == numero), None)

    if not conta:
        print("Conta não encontrada.")
        return None
    
    return conta

def operacoes_conta(conta):
    while True:
        opcao = input(menu)

        if opcao == "d":
            try:
                valor = float(input("Informe o valor do depósito: "))
            except ValueError:
                print("Valor inválido.")
                continue

            if valor > 0:
                conta["saldo"] += valor
                conta["extrato"] += f"Depósito: R$ {valor:.2f}\n"
                print("Depósito realizado com sucesso!")
            else:
                print("Operação falhou! O valor informado é inválido.")

        elif opcao == "s":
            try:
                valor = float(input("Informe o valor do saque: "))
            except ValueError:
                print("Valor inválido.")
                continue

            excedeu_saldo = valor > conta["saldo"]
            excedeu_limite = valor > LIMITE_SAQUE_VALOR
            excedeu_saques = conta["numero_saques"] >= LIMITE_SAQUES

            if excedeu_saldo:
                print("Operação falhou! Você não tem saldo suficiente.")
            elif excedeu_limite:
                print(f"Operação falhou! O valor do saque excede o limite de R$ {LIMITE_SAQUE_VALOR:.2f}.")
            elif excedeu_saques:
                print("Operação falhou! Número máximo de saques excedido.")
            elif valor > 0:
                conta["saldo"] -= valor
                conta["extrato"] += f"Saque: R$ {valor:.2f}\n"
                conta["numero_saques"] += 1
                print("Saque realizado com sucesso!")
            else:
                print("Operação falhou! O valor informado é inválido.")

        elif opcao == "e":
            print("\n================ EXTRATO ================")
            print("Não foram realizadas movimentações." if not conta["extrato"] else conta["extrato"])
            print(f"\nSaldo: R$ {conta['saldo']:.2f}")
            print("==========================================")

        elif opcao == "q":
            print("Saindo da conta...")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

def main():
    while True:
        opcao = input(menu_principal)

        if opcao == "1":
            criar_usuario()

        elif opcao == "2":
            criar_conta()

        elif opcao == "3":
            listar_contas()

        elif opcao == "4":
            conta = acessar_conta()
            if conta:
                operacoes_conta(conta)

        elif opcao == "5":
            print("Encerrando o sistema.")
            break

        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()
