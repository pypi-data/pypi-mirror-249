def count_in_list(lst: list, s: str) -> int:
    """
    lst에서 s가 나타나는 횟수를 반환하는 함수.
    """
    count = 0
    for i in lst:
        if i == s:
            count += 1
    return count
