from abc import ABC, abstractmethod

from PIL import Image

from src.print_scale_images.config import ImageConfig, ImageInfo


class ImageProcessor(ABC):
    """Абстрактный класс для обработки изображений"""

    @abstractmethod
    def process(self, image: Image.Image, config: ImageConfig) -> ImageInfo:
        pass


class A4ImageProcessor(ImageProcessor):
    """Обработчик для подготовки изображений к изменению размера на A4"""

    def __init__(self):
        # A4 в альбомной ориентации 300 DPI: 297mm x 210mm
        self.a4_size_landscape = (3508, 2480)  # высота x ширина

    def process(self, image: Image.Image, config: ImageConfig) -> ImageInfo:
        """Обрабатывает изображение для изменения размеров на A4"""

        scaled_image, scale_ratio, *_ = self._scale_image(image, config)
        a4_image = self._create_a4_page(scaled_image, config)

        return ImageInfo(
            original_path="",
            original_size=image.size,
            scaled_size=scaled_image.size,
            scale_ratio=scale_ratio,
            a4_image=a4_image,
        )

    def _scale_image(
        self, image: Image.Image, config: ImageConfig
    ) -> tuple[Image.Image, tuple[int, int], tuple[int, int, int, int]]:
        """Масштабирует изображение для вписывания в A4 с целочисленными коэффициентами"""

        # Максимальный размер с учетом отступов и места для подписи
        max_width = self.a4_size_landscape[0] - 2 * config.margin
        max_height = self.a4_size_landscape[1] - 2 * config.margin - config.text_margin

        # Вычисляем масштаб для вписывания
        width_ratio = max_width / image.width
        height_ratio = max_height / image.height
        scale = min(width_ratio, height_ratio)

        # Если изображение уже помещается, используем оригинальный размер
        if scale >= 1.0:
            scale_ratio = (1, 1)
            new_size = image.size
        else:
            # Находим ближайший меньший масштаб из допустимых: 1:1, 1:2, 1:2.5, 1:4, 1:5
            allowed_scales = [1.0, 0.5, 0.4, 0.25, 0.2]  # 1:1, 1:2, 1:2.5, 1:4, 1:5
            scale_ratio = (1, 1)

            # Ищем наибольший допустимый масштаб, который <= вычисленного
            for allowed_scale in allowed_scales:
                if allowed_scale <= scale:
                    new_scale = allowed_scale
                    break
            else:
                # Если ни один не подошел, берем самый маленький
                new_scale = allowed_scales[-1]

            # Преобразуем масштаб в ratio для подписи
            if new_scale == 1.0:
                scale_ratio = (1, 1)
            elif new_scale == 0.5:
                scale_ratio = (2, 1)
            elif new_scale == 0.4:
                scale_ratio = (5, 2)  # 1:2.5
            elif new_scale == 0.25:
                scale_ratio = (4, 1)
            elif new_scale == 0.2:
                scale_ratio = (5, 1)

            scale = new_scale
            new_size = (int(image.width * scale), int(image.height * scale))

        # Масштабируем изображение
        scaled_image = image.resize(new_size, Image.Resampling.LANCZOS)

        # Вычисляем позицию для центрирования
        x = (self.a4_size_landscape[0] - new_size[0]) // 2
        y = (self.a4_size_landscape[1] - new_size[1] - config.text_margin) // 2

        return scaled_image, scale_ratio, (x, y, new_size[0], new_size[1])

    def _create_a4_page(self, image: Image.Image, config: ImageConfig) -> Image.Image:
        """Создает страницу A4 с изображением"""

        a4_image = Image.new("RGB", self.a4_size_landscape, "white")

        # Центрируем изображение
        x = (self.a4_size_landscape[0] - image.width) // 2
        y = (self.a4_size_landscape[1] - image.height - config.text_margin) // 2

        a4_image.paste(image, (x, y))
        return a4_image
