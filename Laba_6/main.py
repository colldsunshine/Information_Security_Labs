import os
from PIL import Image

BIT_MARKER = '00000000'
L_values = [1, 2]


def text_to_bits(text):
    bits = ''.join(f'{b:08b}' for b in text.encode('utf-8'))
    return bits + BIT_MARKER


def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        if byte == BIT_MARKER:
            break
        if len(byte) == 8:
            chars.append(int(byte, 2))
    return bytes(chars).decode('utf-8', errors='ignore')


def get_l_value(bit_index):
    """
    Правило выбора следующего L = 3:
    поочередно: L(i), i-чётное / L(i), i-нечётное.
    В реализации используются значения 1 и 2.
    """
    return L_values[0] if bit_index % 2 == 0 else L_values[1]


def additive_embed(img_path, out_path, message):
    """
    Аддитивный метод.
    Вариант 19:
    - функция 1 – используем канал R
    - сканирование 1 - слева направо, сверху вниз
    - правило L = 3 - поочередно 1 и 2
    """
    img = Image.open(img_path).convert('RGB')
    pixels = img.load()
    width, height = img.size

    bits = text_to_bits(message)

    if len(bits) > width * height:
        raise ValueError("Сообщение слишком длинное для данного изображения.")

    bit_idx = 0

    for y in range(height):
        for x in range(width):
            if bit_idx >= len(bits):
                break

            r, g, b = pixels[x, y]
            current_l = get_l_value(bit_idx)

            if bits[bit_idx] == '1':
                if r <= 255 - current_l:
                    r = r + current_l
                else:
                    r = max(0, r - current_l)

            pixels[x, y] = (r, g, b)
            bit_idx += 1

        if bit_idx >= len(bits):
            break

    img.save(out_path)
    print(f"Аддитивное встраивание завершено: {out_path}")


def additive_extract(orig_path, stego_path):
    """
    Извлечение для аддитивного метода через сравнение с оригиналом.
    """
    img_orig = Image.open(orig_path).convert('RGB')
    img_stego = Image.open(stego_path).convert('RGB')

    if img_orig.size != img_stego.size:
        raise ValueError("Размеры изображений не совпадают")

    width, height = img_orig.size
    orig = img_orig.load()
    stego = img_stego.load()

    extracted_bits = ""

    for y in range(height):
        for x in range(width):
            diff = abs(stego[x, y][0] - orig[x, y][0])  # канал R
            extracted_bits += '1' if diff >= 1 else '0'

            if len(extracted_bits) % 8 == 0 and len(extracted_bits) >= 8:
                if extracted_bits[-8:] == BIT_MARKER:
                    return bits_to_text(extracted_bits[:-8])

    return bits_to_text(extracted_bits)


def lsb_embed(img_path, out_path, message):
    """
    LSB-R метод: 2 бита в каждый канал.
    """
    img = Image.open(img_path).convert('RGB')
    pixels = img.load()
    width, height = img.size

    bits = text_to_bits(message)

    max_bits = width * height * 3 * 2
    if len(bits) > max_bits:
        raise ValueError("Сообщение слишком длинное для данного изображения.")

    bit_idx = 0

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            if bit_idx < len(bits):
                chunk = bits[bit_idx:bit_idx + 2].ljust(2, '0')
                r = (r & ~0b11) | int(chunk, 2)
                bit_idx += 2

            if bit_idx < len(bits):
                chunk = bits[bit_idx:bit_idx + 2].ljust(2, '0')
                g = (g & ~0b11) | int(chunk, 2)
                bit_idx += 2

            if bit_idx < len(bits):
                chunk = bits[bit_idx:bit_idx + 2].ljust(2, '0')
                b = (b & ~0b11) | int(chunk, 2)
                bit_idx += 2

            pixels[x, y] = (r, g, b)

            if bit_idx >= len(bits):
                break

        if bit_idx >= len(bits):
            break

    img.save(out_path)
    print(f"LSB-R встраивание завершено: {out_path}")


def lsb_extract(img_path):
    img = Image.open(img_path).convert('RGB')
    pixels = img.load()
    width, height = img.size

    bits = ""

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            bits += format(r & 0b11, '02b')
            bits += format(g & 0b11, '02b')
            bits += format(b & 0b11, '02b')

            if len(bits) % 8 == 0 and len(bits) >= 8:
                if bits[-8:] == BIT_MARKER:
                    return bits_to_text(bits[:-8])

    return bits_to_text(bits)


def main():
    while True:
        print("\n" + "=" * 50)
        print("1. Аддитивный метод (встраивание)")
        print("2. Аддитивный метод (извлечение)")
        print("3. LSB-R метод (встраивание)")
        print("4. LSB-R метод (извлечение)")
        print("0. Выход")
        choice = input("Выбор: ").strip()

        if choice == '0':
            break

        elif choice == '1':
            img = input("Исходное изображение: ").strip()
            if not os.path.exists(img):
                print("Файл не найден.")
                continue

            out = input("Куда сохранить: ").strip()
            msg = input("Сообщение: ").strip()
            if not msg:
                print("Пустое сообщение.")
                continue

            try:
                additive_embed(img, out, msg)
            except Exception as e:
                print("Ошибка:", e)

        elif choice == '2':
            orig = input("Оригинал: ").strip()
            stego = input("Стего-изображение: ").strip()

            if not os.path.exists(orig) or not os.path.exists(stego):
                print("Файл не найден.")
                continue

            try:
                result = additive_extract(orig, stego)
                print("\nИзвлечено:", result)
            except Exception as e:
                print("Ошибка:", e)

        elif choice == '3':
            img = input("Исходное изображение: ").strip()
            if not os.path.exists(img):
                print("Файл не найден.")
                continue

            out = input("Куда сохранить: ").strip()
            msg = input("Сообщение: ").strip()
            if not msg:
                print("Пустое сообщение.")
                continue

            try:
                lsb_embed(img, out, msg)
            except Exception as e:
                print("Ошибка:", e)

        elif choice == '4':
            stego = input("Стего-изображение: ").strip()
            if not os.path.exists(stego):
                print("Файл не найден.")
                continue

            try:
                result = lsb_extract(stego)
                print("\nИзвлечено:", result)
            except Exception as e:
                print("Ошибка:", e)

        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    main()