import re
from typing import Callable, Dict, Optional


def make_tex_escape(extra_strings: Optional[Dict[str, str]] = None) -> Callable[[str], str]:
    def tex_escape(value: str) -> str:
        substitute_strings = {
            "&": "\\&",
            "#": "\\#",
            "%": "\\%",
            "LaTeX": "\\LaTeX\\ ",
            "1st": "1\\textsuperscript{st}",
            "2nd": "2\\textsuperscript{nd}",
            "3rd": "3\\textsuperscript{rd}",
            **{f"{i}th": "".join([str(i), "\\textsuperscript{th}"]) for i in range(4, 10)},
            **(extra_strings or {}),
        }
        substitute_re = {re.escape(k): v for k, v in substitute_strings.items()}
        pattern = re.compile("|".join(substitute_re.keys()))
        return pattern.sub(lambda m: substitute_re[re.escape(m.group(0))], value)

    return tex_escape
