from pyfzf.pyfzf import FzfPrompt


def select_from_list(options: list[str]) -> str | None:
    """

    :param options:
    """
    try:
        fzf = FzfPrompt()
        res = fzf.prompt(options, ' --layout reverse --cycle')
        return res[0]
    except:
        return None
