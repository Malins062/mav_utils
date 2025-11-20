class ScaleCalculator:
    """Калькулятор для вычисления целочисленных масштабов"""

    @staticmethod
    def calculate_best_scale(original_size: Tuple[int, int],
                             max_size: Tuple[int, int]) -> Tuple[float, Tuple[int, int]]:
        """
        Вычисляет лучший целочисленный масштаб для ВПИСЫВАНИЯ в максимальный размер
        """
        orig_width, orig_height = original_size
        max_width, max_height = max_size

        # Вычисляем необходимые масштабы для вписывания по каждой оси
        scale_x = max_width / orig_width
        scale_y = max_height / orig_height

        # Берем минимальный масштаб для полного вписывания
        required_scale = min(scale_x, scale_y)

        # Если изображение уже помещается, используем его текущий размер
        if required_scale >= 1.0:
            return 1.0, (1, 1)

        # Находим ближайший меньший целочисленный масштаб (1/n)
        # Перебираем знаменатели от 2 до 20
        best_denominator = 1
        best_scale = 1.0

        for denominator in range(2, 21):
            scale = 1.0 / denominator
            if scale <= required_scale:
                best_denominator = denominator
                best_scale = scale
            else:
                # Если нашли масштаб, который слишком мал, берем предыдущий
                if best_denominator == 1:
                    # Если даже 1:2 не помещается, берем самый маленький возможный
                    best_denominator = denominator - 1
                    best_scale = 1.0 / best_denominator
                break
        else:
            # Если дошли до конца цикла, используем самый маленький масштаб
            best_denominator = 20
            best_scale = 1.0 / best_denominator

        return best_scale, (best_denominator, 1)

