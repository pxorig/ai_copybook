# -*- coding: utf-8 -*-
# pip install pillow

import io
import base64
from PIL import Image, ImageDraw, ImageFont


class Cell:
    def __init__(self, border_size: int = 500, color: tuple = (255, 0, 0), outline_width: int = 2, dash_width: int = 3):
        self.border_size = border_size
        # 米字格设置
        self.color = color
        self.dash_width = dash_width
        self.image = Image.new('RGB', (border_size, border_size), color=(255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)
        # 绘制外框实线
        self.draw.rectangle([(0, 0), (border_size - 1, border_size - 1)], outline=color, width=outline_width)
        self._draw_dashed_line((0, 0), (border_size, border_size))
        self._draw_dashed_line((0, border_size), (border_size, 0))
        self._draw_dashed_line((0, border_size // 2), (border_size, border_size // 2))
        self._draw_dashed_line((border_size // 2, 0), (border_size // 2, border_size))

    # 绘制虚线（米字部分）
    def _draw_dashed_line(self, start, end):
        length = ((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5
        dash_length = 10
        gap_length = 10
        num_segments = int(length / (dash_length + gap_length))
        for i in range(num_segments):
            start_dash = (start[0] + (end[0] - start[0]) * i * (dash_length + gap_length) / length,
                          start[1] + (end[1] - start[1]) * i * (dash_length + gap_length) / length)
            end_dash = (start_dash[0] + (end[0] - start[0]) * dash_length / length,
                        start_dash[1] + (end[1] - start[1]) * dash_length / length)
            self.draw.line([start_dash, end_dash], fill=self.color, width=self.dash_width)

    def write(self, word: str, font: ImageFont, color: tuple = (0, 0, 0)):
        bbox = self.draw.textbbox((0, 0), word, font=font)
        char_width = bbox[2]
        char_height = bbox[3]
        x = (self.border_size - char_width) // 2
        y = (self.border_size - char_height) // 2
        self.draw.text((x, y), word, font=font, fill=color)
        return self.image


class Copybook:
    def __init__(self, words: str, font_size: int, font_path: str):
        self.font_size = font_size
        self.lines = words.split("\n")
        max_len = 0
        for line in self.lines:
            if len(line) > max_len:
                max_len = len(line)
        self.width = max_len
        self.height = len(self.lines)
        self.font = ImageFont.truetype(font_path, int(font_size * 0.75))

    def _auto_fill(self, color=(255, 255, 255)):
        image = Image.new('RGB', (self.width * self.font_size, self.height * self.font_size), color=color)
        for y in range(self.height):
            rows = self.lines[y]
            for x in range(self.width):
                cell = Cell(border_size=self.font_size)
                if x < len(rows):
                    word = rows[x]
                    if len(word) != 0:
                        cell.write(word=word, font=self.font)
                image.paste(cell.image, (x * self.font_size, y * self.font_size))
        return image

    def gen(self):
        img = self._auto_fill()
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return img_base64


if __name__ == '__main__':
    words = "  创建一个\n空白图像\n这里设置图像 大小为\n 颜色模式为\n替换为你实\n  际的字体文件路径\n   哈哈哈哈"
    c = Copybook(words=words, font_size=200, font_path='../../ttf/正楷.ttf')
    img = c.gen()
    # print(img)
