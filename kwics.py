
import re

def clean(s):
    s = re.sub(" *\n *","\n",s)
    s = re.sub("\n+"," _EOL_ ",s)
    s = re.sub(" +"," ",s)
    s = s.strip()


    return s


def get_kwic(target,doc,window = 3):

    res_ls = []

    for token in doc:
        if token.text == target:
            left = doc[max(0, token.i - window): token.i]
            right = doc[token.i + 1: token.i + 1 + window]
            s = " ".join(t.text for t in left) + " [" + token.text + "] " + " ".join(t.text for t in right)
            s = clean(s)
            res_ls.append(s)

    return "\n".join(res_ls)

# from kwics import get_kwic

# Allow import of this module
__all__ = ["get_kwic"]