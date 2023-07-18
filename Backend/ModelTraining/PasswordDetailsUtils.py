def get_first_letter_index(password: str):
    """
        Gets the index of the first letter of the password
    """
    start_index = 0
    for index, char in enumerate(password):
        if char.isalpha():
            start_index = index
            break
    return start_index

def get_base_word_start_index(password: str):
    """
        Gets the index of the first character of the base word of the provided passowrd
    """
    return get_first_letter_index(password=password)

def get_suffix_start_index(password: str):
    """
        Gets the index of the first character of the suffix of the provided passowrd
    """
    index = get_first_letter_index(password=password[::-1])
    return - index if index > 0 else len(password) + 1

def parse_password_to_3d(password: str):
    """
        Parses a password to prefix, base word, suffix as described in https://arxiv.org/abs/1912.02551
    """
    base_word_start_index = get_base_word_start_index(password=password)
    base_word_end_index = get_suffix_start_index(password=password)
    prefix = password[0 : base_word_start_index]
    base_word = password[base_word_start_index : base_word_end_index]
    suffix = password[base_word_end_index : ]
    return (prefix, base_word, suffix)

def get_shift_pattern(word: str, start_from_end: bool):
    """
        Gets the shift-pattern of the provided word
    """
    pattern = []
    no_char = True
    word = word[::-1] if start_from_end else word
    for index, letter in enumerate(word):
        if str.isalpha(letter):
            no_char = False
            if not str.islower(letter):
                pattern.append(-1 - index if start_from_end else index)
    return [] if no_char else pattern

def get_base_word_shift_pattern(base_word: str):
    """
        Gets the shift pattern (Capitalization of characters) of the base word as represented in https://arxiv.org/abs/1912.02551
    """
    mid_index = len(base_word) // 2
    left_hand_pattern = get_shift_pattern(base_word[ : mid_index], False)
    right_hand_pattern = get_shift_pattern(base_word[mid_index : ], True)[::-1]
    shift_pattern = left_hand_pattern + right_hand_pattern
    return shift_pattern

def is_leagal_password(password):
    """
        Source: isascci() here - https://github.com/lirondavid/PESrank/blob/master/PESrank/PESrank.py#L47
    """
    return all(ord(c) < 128 for c in password)
