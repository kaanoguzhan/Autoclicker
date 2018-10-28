def string_resizer(text, length):
    len_diff = length-len(text)
    for i in range(0, len_diff):
        text = text + " "
    return text
