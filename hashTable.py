from typing import List

class AbsentKeyException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class Entry:
    def __init__(self, entryKey:any, entryValue:any):
        self.key = entryKey
        self.value = entryValue
    
    def __str__(self):
        return "(" + str(self.key) + ', ' + str(self.value) + ")"

class ChaininghashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = list([] for i in range(self.size))
        # utilizar list encadeada própria
        #   0   1   2
        # [ [], [], [] ]

    def __hash(self, key:any):
        return hash(key) % self.size
    
    def put(self, key:any, data:any ):
        slot = self.__hash(key)
        # Hash de python: pega a minha chave e converter em valor inteiro
        
        for entry in self.table[slot]:
            if key == entry.key:
                entry.value = data
                return slot
            
        self.table[slot].append(Entry(key, data))
        return slot
    
    def keys(self)->List[any]:
        result = []
        for lst in self.table:
            if lst != None:
                for entry in lst:
                    result.append(entry.key)
        return result    
    
    def displayTable(self):
        entrada = -1
        for items in self.table:
            entrada += 1
            print(f'Entrada {entrada:2d}: ', end='')
            if len(items) == 0:
                print(' None ')
                continue
            for entry in items:
                print(F'[{entry.key}, {entry.value} ]', end='')
            print()
