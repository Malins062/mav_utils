from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import math


@dataclass
class PrintConfig:
    """Конфигурация для печати"""
    dpi: int = 300
    margin: int = 100
    font_size: int = 40
    text_margin: int = 80


@dataclass
class ImageInfo:
    """Информация об обработанном изображении"""
    original_path: str
    original_size: Tuple[int, int]
    scaled_size: Tuple[int, int]
    scale_ratio: Tuple[int, int]  # (1, 2) для масштаба 1:2
    a4_image: Image.Image
