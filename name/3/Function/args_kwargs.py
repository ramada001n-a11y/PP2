# Использование *args (кортеж позиционных аргументов) и **kwargs (словарь именованных)
def print_info(*args, **kwargs):
    print("Позиционные аргументы (args):", args)
    print("Именованные аргументы (kwargs):", kwargs)

print_info(1, 2, 3, name="Алексей", role="Разработчик")