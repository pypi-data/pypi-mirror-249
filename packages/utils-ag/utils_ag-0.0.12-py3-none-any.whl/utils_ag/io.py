from pyfzf.pyfzf import FzfPrompt


def select_from_list(options: list[str]) -> str:
    """

    :param options:
    """
    fzf = FzfPrompt()
    # fzf.prompt(range(0, 10), '--multi --cycle')
    res = fzf.prompt(options, ' --layout reverse --cycle')
    return res[0]