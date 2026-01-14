import time
from functools import wraps


def handle_database_errors(func):
    """
    Декоратор для обработки ошибок при работе с базой данных.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            print(f'Ошибка: Обращение к несуществующему объекту - {e}')
            return None
        except ValueError as e:
            print(f'Ошибка валидации: {e}')
            return None
        except FileNotFoundError as e:
            print(f'Ошибка файла: {e}')
            return None
        except Exception as e:
            print(f'Неожиданная ошибка в функции {func.__name__}: {e}')
            return None
    return wrapper


def require_confirmation(action_description):
    """
    Декоратор для запроса подтверждения перед выполнением операции
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if kwargs.get('confirm') is False:
                return func(*args, **kwargs)

            user_input = input(
                'Вы уверены, что хотите выполнить'
                f' "{action_description}"? [y/n]: '
            ).strip().lower()
            if user_input == 'y':
                return func(*args, **kwargs)
            else:
                print('Операция отменена.')
                return None
        return wrapper
    return decorator


def measure_execution_time(func):
    """
    Декоратор для измерения времени выполнения функции.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        execution_time = end_time - start_time
        print(f'Функция {func.__name__} выполнилась '
              f'за {execution_time:.3f} секунд')
        return result
    return wrapper


def create_cache_manager():
    """Создает менеджер кэширования с поддержкой замыкания."""
    cache = {}

    def cache_result(key, value_factory):
        """
        Возвращает значение из кэша или вычисляет и кэширует его.
        """
        if key in cache:
            return cache[key]
        else:
            result = value_factory()
            cache[key] = result
            return result

    def clear_cache():
        """Полностью очищает внутренний кэш."""
        cache.clear()
        print("Кэш очищен")

    cache_result.clear = clear_cache

    return cache_result
