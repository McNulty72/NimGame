
from random import seed, randint, choice
from datetime import datetime
from functools import reduce

class Error(Exception):
    pass


class InputError(Error):

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class AmountError(Error):
    
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


def startGame() -> int:

   print('-' * 21)
   print('|                   |')
   print('|                   |')
   print('| BIENVENIDO A NIM  |')
   print('|                   |')
   print('|                   |')
   print('-' * 21)
   print('Intrucciones:')
   print('-'*len('instruciones:'))
   print(' El juego consiste en tres "montnones" con diferente numero de fichas.')
   print(' Los jugadores van quitando fichas por turnos.')
   print(' Cada jugador puede quitar, en cada turno tantas fichas como desee de un solo monton.')
   print(' El juego termina cuando ya no quedan fichas en ningún monton.')
   print(' Gana el jugador que ha quitado la última ficha.')
   print()
   print('Opciones:')
   print('-'*len('Opciones:'))
   print('\t1 - Jugar contra la máquina.')
   print('\t2 - Jugar contra otro jugador.')
   print('\t3 - Salir del juego.')
  
   flag=True
   while flag:
       
       try:
           opt = int(input('Elige una de las opciones: '))
           assert opt in [1, 2, 3]
           flag = False
       except AssertionError:
           print('Opción incorrecta!!!')
       except ValueError:
           print('No válido, debes introducir un número del 1 al 3!!!')

   return opt

def players(opt: int) -> tuple:

   if opt == 1:
       player1 = input('Introduce tu nombre: ')
       player2 = 'Maquina'
   elif opt == 2:
       player1 = input('Jugador 1 introduce tu nombre: ')
       player2 = input('Jugador 2 introduce tu nombre: ')
   else:
       return None
   return player1, player2

def initialBoard() -> list:

    seed(datetime.now())
    heap_1 = randint(6, 31)
    heap_2 = randint(6, 31)

    while heap_1 == heap_2:
        heap_2 = randint(6, 31)

    choices = []

    for heap in range(6, 32):

        nim_sum = heap_1 ^ heap_2 ^ heap
        if not nim_sum:
            continue
        choices.append(heap)
    
    while True:
        heap_3 = choice(choices)
        if not heap_3 in [heap_1, heap_2]:
            break

    return [heap_1, heap_2, heap_3]   

def drawBoard(board: list) -> None:

     for idx, row in enumerate(board):
         print('Monton', idx +1 , ': ', row, sep='')
         for i in range(5):
             print('| ' * row)
         print('\n')

def ramdonChoice(heaps: list) -> list:

    flag = True
    while flag:
        try:
            heap = randint(0, 2)
            amount = randint(1, heaps[heap])
            flag = False
        except:
            flag = True
    heaps[heap] -= amount
    return heaps
         
def makeAPlay(heaps: list) -> list:

    flag = True
    while flag:
        try:
            heap = int(input('¿De que montón quieres quitar, fichas? (1, 2 o 3): '))
            assert heap in [1, 2, 3]
            if not heaps[heap-1]:
                raise  InputError(heap, 'Opcion no valida')
            flag = False
        except AssertionError:
            print('Eleción no válida!!!, vuelve a elegir.')
        except ValueError:
            print('Debes introducir un número valido!!!')
        except InputError:
            print('No puedes elegir un monton vacio')
    
    flag = True
    while flag:
        try:
            amount = int(input('¿Cuantas fichas quieres quitar del mónton?: '))
            if amount <= 0:
                raise AmountError(amount, 'Opcion no valida')
            assert amount <= heaps[heap - 1]
            flag = False
        except AssertionError:
            print('No puedes quitar más fichas de las que quedan en mónton!!!')
        except ValueError:
            print('Debes introducir un número!!!')
        except AmountError:
            print('Tienes que quitar por lo menos una ficha!!')
        
    heaps[heap-1] -= amount

    drawBoard(heaps)
    
    return heaps

def checkWinner(player: str, board: list) -> bool:
    
    if sum(board) == 0:
        print(player, 'Has ganado!!!')
        return True
    return False

def machinePlay(heaps: list) -> list:

    nimsum = reduce(lambda x, y: x ^ y, heaps)
    nimZero = heaps[0] ^ nimsum
    nimOne = heaps[1] ^ nimsum
    if nimsum:
        if nimZero < heaps[0]:
            heaps[0] -= heaps[0] - nimZero
        elif nimOne < heaps[1]:
            heaps[1] -= heaps[1] - nimOne
        else:
            heaps[2] -= heaps[2] - nimTwo
    else:
        heaps = ramdonChoice(heaps)

    drawBoard(heaps)
    return heaps
                        
def main() -> None:

    opt = startGame()

    try:
        player1, player2 = players(opt)
    except TypeError:
        return
    board = initialBoard()
    drawBoard(board)
    endgame = False
    player = player1
    while not endgame:

        print(player, 'Es tu turno')
        if player == 'Maquina':
            board = machinePlay(board)
        else:
            board = makeAPlay(board)
        endgame = checkWinner(player, board)
        if player == player1:
            player = player2
        else:
            player = player1

    flag = True
    while flag:

        try:
            print('¿Quieres volver a jugar? (S/N)')
            ans = input('>')
            assert ans.upper() == 'N' or ans.upper() == 'S'
            flag = False
        except AssertionError:
            print('Opción no válida!!!')
    
    if ans.upper() == 'S':
        main()
    
if __name__ == '__main__':
    main()
