import cutie
import random
from colorama import Fore
from misc.config import EMPTY, CROSS, CIRCLE, VICTORIES

difficulty = None
player_side = None
bot_side = None
field = [
    EMPTY, EMPTY, EMPTY,
    EMPTY, EMPTY, EMPTY,
    EMPTY, EMPTY, EMPTY
]


def clear():
    print('\x1b[2J\x1b[H')


def choice():
    global difficulty, player_side, bot_side
    clear()
    print(Fore.LIGHTBLACK_EX + 'Выберите сложность:' + Fore.RESET)
    difficulties = ['лёгкая', 'нормальная', 'сложная']
    difficulty = difficulties[cutie.select(
        difficulties,
        deselected_prefix=Fore.LIGHTBLACK_EX + '  ' + Fore.RESET,
        selected_prefix=Fore.RED + '> ' + Fore.RESET
        )]
    clear()
    print(Fore.LIGHTBLACK_EX + 'Выберите сторону:' + Fore.RESET)
    sides = [CROSS, CIRCLE]
    player_side = sides[cutie.select(
        sides,
        deselected_prefix='  ',
        selected_prefix='> '
        )]
    bot_side = CIRCLE if player_side != CIRCLE else CROSS
    draw()


def player():
    while True:
        try:
            pos = int(input(Fore.LIGHTBLACK_EX + 'Введите номер клетки: ' + Fore.RESET))
            if pos not in range(0, 9):
                print('Допустимый диапазон значений: от 0 до 8 (включительно).')
            elif field[pos] != EMPTY:
                print('Клетка c данным номером уже занята.')
            else:
                move(pos, player_side)
                break
        except ValueError:
            print('Входные данные должны быть цифрой.')


def bot():
    empty_cells = [i for i, cell in enumerate(field) if cell == EMPTY]


    def _check(field_copy, side):
        for overlap in VICTORIES:
            if all(field_copy[i] == side for i in overlap):
                return True
            
        return False


    def easy():
        pos = random.choice(empty_cells)
        move(pos, bot_side)


    def normal():
        for pos in empty_cells:
            field_copy = field[:]
            field_copy[pos] = bot_side
            if _check(field_copy, bot_side):
                move(pos, bot_side)
                return
            
        for pos in empty_cells:
            field_copy = field[:]
            field_copy[pos] = player_side
            if _check(field_copy, player_side):
                move(pos, bot_side)
                return
                        
        """if 4 in empty_cells:
            move(4)
        else:
            easy()"""
        
        easy()

    
    def minimax(field_copy, depth, is_maximizing, alpha, beta):
        if _check(field_copy, bot_side):
            return 10 - depth
        
        if _check(field_copy, player_side):
            return depth - 10
        
        if EMPTY not in field_copy:
            return 0

        if is_maximizing:
            max_eval = -float('inf')
            for pos in [i for i, cell in enumerate(field_copy) if cell == EMPTY]:
                field_copy[pos] = bot_side
                eval = minimax(field_copy, depth + 1, False, alpha, beta)
                field_copy[pos] = EMPTY
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            return max_eval
        else:
            min_eval = float('inf')
            for pos in [i for i, cell in enumerate(field_copy) if cell == EMPTY]:
                field_copy[pos] = player_side
                eval = minimax(field_copy, depth + 1, True, alpha, beta)
                field_copy[pos] = EMPTY
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break

            return min_eval

    def hard():
        best_score = -float('inf')
        best_pos = None
        for pos in empty_cells:
            field_copy = field[:]
            field_copy[pos] = bot_side
            score = minimax(field_copy, 0, False, -float('inf'), float('inf'))
            field_copy[pos] = EMPTY
            if score > best_score:
                best_score = score
                best_pos = pos

        move(best_pos, bot_side)


    if difficulty == 'лёгкая':
        easy()

    if difficulty == 'нормальная':
        normal()

    if difficulty == 'сложная':
        hard()


def turn():
    current = CIRCLE if field.count(CIRCLE) < field.count(CROSS) else CROSS
    if current == player_side:
        player()
    else:
        bot()


def move(pos, side):
    field[pos] = side
    draw()


def check():
    for overlap in VICTORIES:
        for side in [CROSS, CIRCLE]:
            if all(field[i] == side for i in overlap):
                print(f'{side} выиграли!')
                return
            
    if EMPTY not in field:
        print(f'{CROSS}🤝 {CIRCLE} ничья!')
        return

    turn()


def draw():
    clear()
    print(
        f'⁰{field[0]}|¹{field[1]}|²{field[2]}\
        \n⎼⎼⎼ ⎼⎼⎼ ⎼⎼⎼\
        \n³{field[3]}|⁴{field[4]}|⁵{field[5]}\
        \n⎼⎼⎼ ⎼⎼⎼ ⎼⎼⎼\
        \n⁶{field[6]}|⁷{field[7]}|⁸{field[8]}\n'
    )
    check()


if __name__ == '__main__':
    choice()