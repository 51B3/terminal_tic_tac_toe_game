from colorama import Fore

EMPTY = Fore.RED + 'ㅤ' + Fore.RESET
CIRCLE = Fore.RED + '〇' + Fore.RESET
CROSS = Fore.RED + '✗ ' + Fore.RESET

VICTORIES = [
    [0, 1, 2],
    [0, 3, 6],
    [0, 4, 8],
    [1, 4, 7],
    [2, 4, 6],
    [2, 5, 8],
    [3, 4, 5],
    [6, 7, 8]
]
