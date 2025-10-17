import rpyc

conn = rpyc.connect("rpyc_services_server", 18811)
print("Somando 4 + 7:")
x = conn.root.soma(4,7)
print(x)

print("Dividindo 7 / 4:")
y = conn.root.divisao(7,4)
print(y)

print("Testando cliente")
conn.root.teste()
