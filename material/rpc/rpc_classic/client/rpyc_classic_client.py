import rpyc
conn = rpyc.classic.connect("rpyc_classic_server",port=18812)
print("Executando funcao diretamente no servidor")
print("usando eval para calcular 2 * pi")
conn.execute('import math')
r = conn.eval('2*math.pi')
print(r)

# Funcao 'quadrado' sendo enviado ao servidor
def quadrado(x):
    return x**2

def vezes3(x):
    return x*3

stub_quadrado = conn.teleport(quadrado)
print("4 elevado ao quadrado:")
r2 = stub_quadrado(4)
print(r2)