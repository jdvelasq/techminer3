# pylint: disable=too-few-public-methods
"""ChatGPT prompts"""

import textwrap

TEXTWRAP_WIDTH = 73


class PromptMixin:
    """:meta private:"""

    def format_prompt_for_dataframes(
        self,
        main_text: str,
        df_text: str,
    ):
        """:meta private:"""

        prompt = textwrap.fill(main_text, width=TEXTWRAP_WIDTH)
        prompt = prompt.replace("\n", " \\\n")
        prompt = prompt + f"\n\nTable:\n```\n{df_text}\n```\n"

        return prompt
