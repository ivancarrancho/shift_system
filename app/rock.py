def take_shift(choice):
    choices = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    if choice in choices:
        return f'el turno fué seleccionado {choice}'

    return f'Opción inválida'
