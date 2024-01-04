def join(lst: list, seq: str, remove_repeat: bool = False) -> str:
    if remove_repeat:
        lst = remove_duplicates(lst)

    return seq.join(lst)


def remove_duplicates(lst: list) -> list:
    new_lst = []
    for i in lst:
        if i in new_lst:
            continue
        new_lst.append(i)
    return new_lst
