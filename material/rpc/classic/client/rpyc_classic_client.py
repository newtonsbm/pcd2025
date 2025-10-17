import rpyc

server_host = "localhost"
server_port = 18812
conn = rpyc.classic.connect(server_host, port=server_port)


def quadrado(numero):
    return numero**2

def dobro(numero):
    return numero*2

def migracao_codigo():
    print("Exemplo Cliente RPyC Classico - migracao codigo")
    conn.execute("import math")
    resultado = conn.eval('2 * math.pi')
    print(resultado)

def migracao_funcao():
    print("Exemplo Cliente RPyC Classico - migracao funcao")
    stub_quadrado = conn.teleport(quadrado)
    print("4 elevado ao quadrado eh: ")
    resultado = stub_quadrado(4)
    print(resultado)

migracao_codigo()