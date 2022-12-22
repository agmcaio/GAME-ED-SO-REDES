from random import choice
from Words import tips
from ListaSimplesmenteEncadeada import *
from hashTable import *

class GameException(Exception):
    def __init__(self, mensagem, metodo=''):
        super().__init__(mensagem)
        self.metodo = metodo

class Game:
    def __init__(self, palavra: str, dica: str) -> None:
        self.__palavra = palavra
        self.__dica = dica
        self.__letrasAchadas = Lista() # []
        self.__letrasDigitadas = Lista() # []
        self.__hashTable = ChaininghashTable(2)
        self.__descobriuPalavra = False
        self.__gameOver = False
    
    def getPalavra() -> list:
        w = choice(list(tips.keys()))
        game = [w, tips[w]]

        return game
    
    def getDica(self):
        return self.__dica
    
    def descobriuPalavra(self):
        return self.__descobriuPalavra != False
    
    def perdeuJogo(self):
        return self.__gameOver != False
    
    def verificarLetra(self, letra: str):
        # se a letra já foi digitada ou encontrada, lança uma exceção

        if letra in self.__letrasDigitadas.lista() or letra in self.__letrasAchadas.lista():
            raise GameException("A letra já foi jogada!", "verificarLetra")
        
        # se tentar digitar mais de uma letra, lança uma exceção
        if len(letra) != 1:
            raise GameException("A letra deve ter apenas um caracter!", "verificarLetra")
        
        # se a letra não tiver na palavra
        if not letra in self.__palavra:
            self.__letrasDigitadas.inserir(1, letra)
            # self.__letrasDigitadas.append(letra) # coloca a letra na lista de letras já digitadas
            raise ValueError("A letra não existe na palavra!", "verificarLetra")
    
    # método responsavel por adicionar a letra em seu devidor lugar
    def adicionarLetra(self, letra: str):
        if not letra in self.__letrasDigitadas.lista(): # se n foi digitada ainda 
            self.__letrasDigitadas.inserir(1, letra)
            
        self.__letrasAchadas.inserir(1, letra) # se já foi achada
        
        # se a mesma palavra formada de letras achadas for igual a palavra
        if self.__letrasAchadas.tamanho() == len(self.__palavra):
            self.__descobriuPalavra = True

    def hashDisplay(self):
        self.__hashTable.put(1, f'Letras tentadas: {self.__letrasDigitadas}')
        self.__hashTable.put(2, f'Letras acertadas: {self.__letrasAchadas}')
        return self.__hashTable.displayTable()

    # interface para palavra
    def __getForcaLetras(self) -> str:
        s = '\nPalavra: '
        for i in range(len(self.__palavra)):
            if self.__palavra[i] in self.__letrasAchadas.lista():
                s += f'{self.__palavra[i]}, '
            else:
                s += f'_, '
        return s
    
    # interface para as letras digitadas
    def __getLetrasDigitadas(self) -> str:
        s = '\nLetras Jogadas: ['
        for i in range(self.__letrasDigitadas.tamanho()):
            s += f'{self.__letrasDigitadas.elemento(i+1)}, '
        s += ']\n'
            
        return s
    
    #
    def getLetrasAchadas(self) -> str:
        s = '\nLetras Acertadas: ['
        for i in range(self.__letrasAchadas.tamanho()):
            s += f'{self.__letrasAchadas.elemento(i+1)}, '
        s += ']\n'
        return s
        
    def getInformations(self) -> str:
        s = '\n=============================='
        s += self.__getLetrasDigitadas()
        s += self.getLetrasAchadas()
        s += 'Dica = ' + self.getDica()
        s += self.__getForcaLetras()
        
        return s
    
    # método que chamar o metodo adiciona a palavra a cada rodada
    def rodada(self, letra: str):
        self.adicionarLetra(letra)
        print(self.getInformations())