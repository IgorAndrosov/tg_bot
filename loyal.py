def discount(sum):
    match sum:
        case 0:
            return 0
        case num if num in range(1, 499):
            return 1
        case num if num in range(500, 999):
            return 2
        case num if num in range(1000, 1499):
            return 4
        case num if num in range(1500, 2499):
            return 8
        case _:
            return 10
        
def level(sum):
    match sum:
        case 0:
            return 1
        case num if num in range(1, 499):
            return 500 - sum
        case num if num in range(500, 999):
            return 1000 - sum
        case num if num in range(1000, 1499):
            return 1500 - sum
        case num if num in range(1500, 2499):
            return 2500 - sum
        case _:
            return 'Вы достигли максимума!'