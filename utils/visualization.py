from markupsafe import Markup
import matplotlib.colors as mcolors


def highlight_attention(tokens, scores):
    norm = mcolors.Normalize(vmin=min(scores), vmax=max(scores))
    highlighted = [
        f"<span style='background-color: rgba(255, 255, 0, {norm(score):.2f}); padding:2px'>{token.replace('##', '')}</span>"
        for token, score in zip(tokens, scores)
    ]
    return Markup(" ".join(highlighted))
