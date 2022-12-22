# Nó = elemento da lista
# Um é campo dado, o outro é chamado de prox, um link para o próximo nó da lista

class ListaException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class Node:
    def __init__(self, dado):
        self.__dado = dado
        self.__prox = None
        
    @property
    def dado(self):
        return self.__dado
    
    @property
    def prox(self):
        return self.__prox
    
    @dado.setter
    def dado(self, novoDado):
        self.__dado = novoDado
    
    @prox.setter
    def prox(self, novoProx):
        self.__prox = novoProx
        
    def __str__(self):
        return str(self.__dado)
    
class Lista:
    
    def __init__(self):
        # O head começa com none pois considermos que ele não está apontando para nenhum nó
        self.__head = None
        self.__tamanho = 0
        
    def vazia(self):
        return True if self.__tamanho == 0 else False
    
    def tamanho(self):
        return self.__tamanho
    
    def busca(self, dado):
        if(self.vazia()):
            raise ListaException('A lista está vazia.')
        
        cursor = self.__head
        contador = 1
        
        while(cursor != None):
            if (cursor.dado == dado):
                return contador
            
            cursor  = cursor.prox
            contador += 1
        
        raise ListaException('O valor informado na busca não está na lista')    
        
    def elemento(self, posicao):
        try:
            # assegura que determinada condição seja válida
            
            if(self.vazia()):
                raise ListaException('Lista está vazia')
            
            # Toda vez que tivermos que percorrer uma lista encadeada precisaremos definir um cursor para percorrer os elementos e uma variável contador para ajudarmos a contar o sleemntos que vamos passando a medida que avançamos a lista
            cursor = self.__head
            contador = 1
            
            while ((cursor != None) and (contador < posicao)):
                cursor = cursor.prox
                contador += 1
            
            if (cursor != None ):
                return cursor.dado
            
            raise ListaException('A posição é inválida para a lista')
            
        except TypeError:
            raise ListaException('O argumento posicao deve ser um valor do tipo inteiro')
        
        except AssertionError:
            raise ListaException('Posicao negativa não é válida para a lista')
        
        except:
            raise
    
    def inserir(self, posicao, dado):
        try:
            assert posicao > 0
            # Condição 1: Inserção se a lista estiver vazia
            
            if(self.vazia()):
                if(posicao != 1):
                    raise ListaException('A lista está vazia. Defina o argumento posição como 1')
            
                self.__head = Node(dado)
                self.__tamanho += 1
                return
            
            # Condição 2: Inserção na primiera posição em uma lista não vazia
            if(posicao == 1):
                novo = Node(dado)
                novo.prox = self.__head
                self.__head = novo
                self.__tamanho += 1
                return
                
            # Condição 3: Inserção após a primeira posição em uma lsita não vazia
            cursor = self.__head
            contador = 1
            while((contador < posicao-1) and (cursor != None)):
                cursor = cursor.prox
                contador += 1
            
            if (cursor == None):
                raise ListaException('A posição é inválida para inserção')
            
            novo = Node(dado)
            novo.prox = cursor.prox
            cursor.prox = novo
            self.__tamanho += 1
            
        except TypeError:
            raise ListaException('O argumento posicao deve ser um valor do tipo inteiro')
        
        except AssertionError:
            raise ListaException('Posicao negativa não é válida para a lista')
        
        except:
            raise
        
    def lista(self):
        try:
            cursor = self.__head
            
            str = ''
            while( cursor != None):
                str += cursor.dado
                cursor = cursor.prox
                
                if(cursor != None):
                    continue
            return str
        except:
            raise
    
    
    def __str__(self):
        str = 'Lista: [ '
        cursor = self.__head
        while( cursor != None):
            str += f'{cursor.dado}'
            cursor = cursor.prox
            if(cursor != None):
                str += ', '
        str += ' ]'
        return str

    def imprimir(self):
        print(self.__str__())
