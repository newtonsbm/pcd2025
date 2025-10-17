import rpyc

class CalculadoraService(rpyc.Service):
    def exposed_soma(self, a, b):
        return a + b
    def exposed_subtracao(self, a, b):
        return a - b
    def exposed_multiplicacao(self, a, b):
        return a * b
    def exposed_divisao(self, a, b):
        return a / b
    def exposed_teste(self):
        print("Oi! Testando...")

if __name__ == "__main__":
    print("Startinggg")
    server = rpyc.ThreadedServer(CalculadoraService, port = 18811)
    server.start()