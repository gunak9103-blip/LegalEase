import html
import re
import unicodedata


def sanitize_text(text: str) -> str:
    """
    Normalizes AI-generated text for predictable exports.
    """

    text = unicodedata.normalize(
        "NFKC",
        text or "",
    )

    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2022": "-",
        "\u00a0": " ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(
        r"[ \t]+\n",
        "\n",
        text,
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    )

    return text.strip()


def terms_to_list(terms: str) -> list[str]:
    """
    Converts semicolon-separated terms into a Python list.
    """

    return [
        item.strip()
        for item in terms.split(";")
        if item.strip()
    ]


def text_to_html(text: str) -> str:
    """
    Converts plain legal text to safe HTML
    for the Streamlit preview.
    """

    lines = sanitize_text(text).splitlines()

    output = []

    in_list = False

    for raw in lines:

        line = raw.strip()

        if not line:

            if in_list:
                output.append("</ul>")
                in_list = False

            output.append(
                "<div class='spacer'></div>"
            )

            continue

        escaped = html.escape(line)

        is_bullet = line.startswith(
            ("- ", "* ")
        )

        is_numbered = bool(
            re.match(
                r"^\d+[\.\)]\s+",
                line,
            )
        )

        is_heading = (
            line.isupper()
            or bool(
                re.match(
                    r"^(SECTION|ARTICLE)\s+\d+",
                    line,
                    re.I,
                )
            )
            or bool(
                re.match(
                    r"^\d+\.\s+[A-Z]",
                    line,
                )
            )
        )

        if is_bullet:

            if not in_list:
                output.append("<ul>")
                in_list = True

            output.append(
                f"<li>{html.escape(line[2:].strip())}</li>"
            )

        else:

            if in_list:
                output.append("</ul>")
                in_list = False

            if is_heading:
                output.append(
                    f"<h3>{escaped}</h3>"
                )

            elif is_numbered:
                output.append(
                    f"<p><strong>{escaped}</strong></p>"
                )

            else:
                output.append(
                    f"<p>{escaped}</p>"
                )

    if in_list:
        output.append("</ul>")

    return "\n".join(output)


def format_html_preview(text: str) -> str:

    body = text_to_html(text)

    return f"""
    <div class="legal-preview">
        {body}
    </div>
    """