class Celula:

    def __init__(self, valorInicial):
        self.valor = valorInicial
        self.prox = None
    
    def getValor(self):
        return self.valor

    def setValor(self, novoValor):
        self.valor = novoValor

    def getProx(self):
        return self.prox

    def setProx(self, novoProx):
        self.prox = novoProx

class ListaEncadeada:

    def __init__(self):
        self.cabeca = None

    def isEmpty(self):
        return self.cabeca == None

    def add(self, valor):
        celula = Celula(valor)
        celula.setProx(self.cabeca)
        self.cabeca = celula

    def size(self):
        count = 0
        atual = self.cabeca

        while atual != None:
            count += 1
            atual = atual.getProx()
        return count

    def busca(self, valor):
        atual = self.cabeca
        found = False

        while atual != None and not found:
            if atual.getValor() == valor:
                found = True
            else:
                atual = atual.getProx()
            
            return found

    def remove(self, valor):
        atual = self.cabeca
        anterior = None
        found = False

        while not found:
            if atual.getValor() == valor:
                found = True
            else:
                anterior = atual
                atual = atual.getProx()
            
        if anterior == None:
            self.cabeca = atual.getProx()
        else:
            anterior.setProx(atual.getProx())


