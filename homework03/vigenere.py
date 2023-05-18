def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    keyword = keyword.lower()
    while len(keyword) < len(plaintext):
        keyword += keyword
    ciphertext = ""

    for i in range(len(plaintext)):
        if not plaintext[i].isalpha():
            ciphertext += plaintext[i]
            continue
        wasupper = False
        if plaintext[i].isupper():
            wasupper = True
        n = ord(plaintext[i].lower())
        shift = ord(keyword[i]) - 97
        if n + shift <= 122:
            candidate = chr(n + shift)
        else: candidate = chr(n - 26 + shift)
        if wasupper:
            candidate = candidate.upper()
        ciphertext += candidate
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    keyword = keyword.lower()
    while len(keyword) < len(ciphertext):
        keyword += keyword
    plaintext = ""
    for i in range(len(ciphertext)):
        if not ciphertext[i].isalpha():
            plaintext += ciphertext[i]
            continue
        wasupper = False
        if ciphertext[i].isupper():
            wasupper = True
        n = ord(ciphertext[i].lower())
        shift = ord(keyword[i]) - 97
        if n - shift >= 97:
            candidate = chr(n - shift)
        else: candidate = chr(n + 26 - shift)
        if wasupper:
            candidate = candidate.upper()
        plaintext += candidate
    return plaintext
