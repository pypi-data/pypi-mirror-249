from pyfzf.pyfzf import FzfPrompt


def select_from_list(options: list[str]) -> str | None:
    """

    :param options:
    """
    try:
        fzf = FzfPrompt()
        res = fzf.prompt(options, '--layout reverse --cycle')
        return res[0]
    except:
        return None


def select_items_from_list(options: list[str]) -> str | None:
    """
    Select several items from list
    :param options:
    """
    try:
        fzf = FzfPrompt()
        res = fzf.prompt(options, '--multi --layout reverse --cycle')
        return res
    except:
        return []


def newline(n = 1):
    """
    Prints a new line symbol N times
    :param n:
    """
    print('\n'* n)
