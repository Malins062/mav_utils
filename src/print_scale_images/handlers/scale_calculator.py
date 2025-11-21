import math


class ScaleCalculator:
    """Калькулятор для вычисления целочисленных масштабов"""

    @staticmethod
    def calculate_best_scale(original_size: tuple[int, int],
                             max_size: tuple[int, int]) -> tuple[float, tuple[int, int]]:
        """
        Вычисляет лучший целочисленный масштаб для ВПИСЫВАНИЯ в максимальный размер
        """
        orig_width, orig_height = original_size
        max_width, max_height = max_size

        # Вычисляем необходимый масштаб для вписывания
        required_scale = min(max_width / orig_width, max_height / orig_height)

        # Если изображение уже помещается, используем оригинал
        if required_scale >= 1.0:
            return 1.0, (1, 1)

        # Находим наименьший целочисленный знаменатель (от 2 до 20)
        # который даст масштаб <= required_scale
        scale_denominator = min(20, max(2, math.ceil(1.0 / required_scale)))
        scale = 1.0 / scale_denominator

        return scale, (scale_denominator, 1)
