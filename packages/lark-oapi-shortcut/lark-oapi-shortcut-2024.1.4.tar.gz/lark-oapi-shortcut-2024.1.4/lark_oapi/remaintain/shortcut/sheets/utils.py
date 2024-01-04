def column_number_to_name(n: int) -> str:
    """
    根据表格的列索引获取列名，从 0 开始
    比如 0 -> A, 1 -> B, 26 -> AA, 27 -> AB
    """
    d, m = divmod(n, 26)
    return '' if n < 0 else column_number_to_name(d - 1) + chr(m + 65)  # chr(65) = 'A'


def column_name_to_number(n: str) -> int:
    """
    根据表格的列名获取列索引，>= 1 有意义
    比如 A -> 1, B -> 2, AA -> 27, AB -> 28
    """
    if not n:
        return 0
    number = 0
    for i in range(len(n)):
        number = number * 26 + (ord(n[i]) - ord('A') + 1)
    return number
