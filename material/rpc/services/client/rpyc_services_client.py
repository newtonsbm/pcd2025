import rpyc

server_host = "localhost"
server_port = 18811
conn = rpyc.connect(server_host, port=server_port)

calc_services = conn.root

calc_services.teste()

resultado = calc_services.joao()
print(resultado)

print("Somando 2 + 40")
resultado = calc_services.soma(2, 40)
print(resultado)