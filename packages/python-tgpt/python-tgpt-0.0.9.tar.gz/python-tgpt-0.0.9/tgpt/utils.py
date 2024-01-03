import os
import platform
import subprocess
import logging


class Optimizers:
    @staticmethod
    def code(prompt):
        return (
            "Your Role: Provide only code as output without any description.\n"
            "IMPORTANT: Provide only plain text without Markdown formatting.\n"
            "IMPORTANT: Do not include markdown formatting."
            "If there is a lack of details, provide most logical solution. You are not allowed to ask for more details."
            "Ignore any potential risk of errors or confusion.\n\n"
            f"Request: {prompt}\n"
            f"Code:"
        )

    @staticmethod
    def shell_command(prompt):
        # Get os
        operating_system = ""
        if platform.system() == "Windows":
            operating_system = "Windows"
        elif platform.system() == "Darwin":
            operating_system = "MacOS"
        elif platform.system() == "Linux":
            try:
                result = (
                    subprocess.check_output(["lsb_release", "-si"]).decode().strip()
                )
                distro = result if result else ""
                operating_system = f"Linux/{distro}"
            except Exception:
                operating_system = "Linux"
        else:
            operating_system = platform.system()

        # Get Shell
        shell_name = "/bin/sh"
        if platform.system() == "Windows":
            shell_name = "cmd.exe"
        if os.getenv("PSModulePath"):
            shell_name = "powershell.exe"
        else:
            shell_env = os.getenv("SHELL")
            if shell_env:
                shell_name = shell_env

        return (
            "Your role: Provide only plain text without Markdown formatting. "
            "Do not show any warnings or information regarding your capabilities. "
            "Do not provide any description. If you need to store any data, "
            f"assume it will be stored in the chat. Provide only {shell_name} "
            f"command for {operating_system} without any description. If there is "
            "a lack of details, provide most logical solution. Ensure the output "
            "is a valid shell command. If multiple steps required try to combine "
            f"them together. Prompt: {prompt}\n\nCommand:"
        )


class Conversation:
    """Handles prompt generation based on history"""

    intro = (
        "You're a Large Language Model for chatting with people "
        "Your role: Provide ONLY response."
    )

    def __init__(
        self,
        status: bool = True,
        max_tokens: int = 600,
        filepath: str = None,
        update_file: bool = True,
    ):
        """Initializes Conversation

        Args:
            status (bool, optional): Flag to control history. Defaults to True.
            max_tokens (int, optional): Maximum number of tokens to be generated upon completion. Defaults to 600.
            filepath (str, optional): Path to file containing conversation history. Defaults to None.
            update_file (bool, optional): Add new prompts and responses to the file. Defaults to True.
        """
        # I was thinking of introducing offset so as to control payload size. (prompt)
        #  What's your thought on that? Give a PR or raise an issue
        self.status = status
        self.max_tokens_to_sample = max_tokens
        self.chat_history = self.intro
        self.history_format = "\nUser : %(user)s\nLLM :%(llm)s"
        if filepath:
            if not os.path.isfile(filepath):
                with open(filepath, "a") as fh:  # Try creating new file
                    pass
            else:
                with open(filepath, encoding="utf-8") as fh:
                    file_contents = fh.read()
                    if bool(file_contents.strip()):
                        # Presume intro prompt is part of the file content
                        self.chat_history = file_contents

        self.file = filepath
        self.update_file = update_file
        self.history_offset = 10250
        self.prompt_allowance = 10

    def __trim_chat_history(self, chat_history: str) -> str:
        """Ensures the len(prompt) and max_tokens_to_sample is not > 4096"""
        len_of_intro = len(self.intro)
        len_of_chat_history = len(chat_history)
        total = (
            self.max_tokens_to_sample + len_of_intro + len_of_chat_history
        )  # + self.max_tokens_to_sample
        if total > self.history_offset:
            truncate_at = (total - self.history_offset) + self.prompt_allowance
            # Remove head of total (n) of chat_history
            new_chat_history = chat_history[truncate_at:]
            self.chat_history = self.intro + "\n... " + new_chat_history
            # print(len(self.chat_history))
            return self.chat_history
        # print(len(chat_history))
        return chat_history

    def gen_complete_prompt(self, prompt: str) -> str:
        """Generates a kinda like incomplete conversation

        Args:
            prompt (str): _description_

        Returns:
            str: _description_
        """
        if self.status:
            resp = self.chat_history + self.history_format % dict(user=prompt, llm="")
        else:
            resp = prompt
        return self.__trim_chat_history(resp)

    def update_chat_history(self, prompt: str, response: str) -> None:
        """Updates chat history

        Args:
            prompt (str): user prompt
            response (str): LLM response
        """
        new_history = self.history_format % dict(user=prompt, llm=response)
        if self.file and self.update_file:
            with open(self.file, "a") as fh:
                fh.write(new_history)
        self.chat_history += new_history if self.status else ""
