import tgpt
import click
import cmd
import logging
import os
import sys
import clipman
import re
import rich
import getpass
from time import sleep
from threading import Thread as thr
from functools import wraps
from rich.panel import Panel
from rich.style import Style
from rich.markdown import Markdown
from rich.console import Console
from rich.live import Live
from rich.prompt import Prompt
from typing import Iterator
from tgpt.utils import Optimizers

getExc = lambda e: e.args[1] if len(e.args) > 1 else str(e)

rich_code_themes = ["monokai", "paraiso-dark", "igor", "vs", "fruity", "xcode"]

logging.basicConfig(
    format="%(asctime)s - %(levelname)s : %(message)s ",  # [%(module)s,%(lineno)s]", # for debug purposes
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

try:
    clipman.init()
except Exception as e:
    logging.debug(f"Dropping clipman in favor of pyperclip - {getExc(e)}")
    import pyperclip

    clipman.set = pyperclip.copy
    clipman.get = pyperclip.paste


def stream_output(
    iterable: Iterator,
    title: str = "",
    is_markdown: bool = True,
    style: object = Style(),
    transient: bool = False,
    title_generator: object = None,
    title_generator_params: dict = {},
    code_theme: str = "monokai",
) -> None:
    """Stdout streaming response

    Args:
        iterable (Iterator): Iterator containing contents to be stdout
        title (str, optional): Content title. Defaults to ''.
        is_markdown (bool, optional): Flag for markdown content. Defaults to True.
        style (object, optional): `rich.style` instance. Defaults to Style().
        transient (bool, optional): Flag for transient. Defaults to False.
        title_generator (object, optional): Function for generating title. Defaults to None.
        title_generator_params (dict, optional): Kwargs for `title_generator` function. Defaults to {}.
        code_theme (str, optional): Theme for styling codes. Defaults to `monokai`
    """
    render_this = ""
    with Live(render_this, transient=transient, refresh_per_second=8) as live:
        for entry in iterable:
            render_this += entry
            live.update(
                Panel(
                    Markdown(entry, code_theme=code_theme) if is_markdown else entry,
                    title=title,
                    style=style,
                )
            )
        if title_generator:
            title = title_generator(**title_generator_params)
            live.update(
                Panel(
                    Markdown(entry, code_theme=code_theme) if is_markdown else entry,
                    title=title,
                    style=style,
                )
            )


class busy_bar:
    querying = None
    __spinner = (
        ("-", "\\", "|", "/"),
        (
            "█■■■■",
            "■█■■■",
            "■■█■■",
            "■■■█■",
            "■■■■█",
        ),
        ("⣾ ", "⣽ ", "⣻ ", "⢿ ", "⡿ ", "⣟ ", "⣯ ", "⣷ "),
    )
    spin_index = 0
    sleep_time = 0.1

    @classmethod
    def __action(
        cls,
    ):
        while cls.querying:
            for spin in cls.__spinner[cls.spin_index]:
                print(" " + spin, end="\r", flush=True)
                if not cls.querying:
                    break
                sleep(cls.sleep_time)

    @classmethod
    def start_spinning(
        cls,
    ):
        try:
            cls.querying = True
            t1 = thr(
                target=cls.__action,
                args=(),
            )
            t1.start()
        except Exception as e:
            cls.querying = False
            logging.debug(getExc(e))
            t1.join()

    @classmethod
    def stop_spinning(cls):
        """Stop displaying busy-bar"""
        if cls.querying:
            cls.querying = False
            sleep(cls.sleep_time)

    @classmethod
    def run(cls, help: str = "Exception"):
        """Handle function exceptions safely why showing busy bar

        Args:
            help (str, optional): Message to be shown incase of an exception. Defaults to ''.
        """

        def decorator(func):
            @wraps(func)  # Preserves function metadata
            def main(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except KeyboardInterrupt:
                    cls.stop_spinning()
                    return
                except EOFError:
                    cls.querying = False
                    exit(logging.info("Stopping program"))
                except Exception as e:
                    cls.stop_spinning()
                    logging.error(f"{help} - {getExc(e)}")

            return main

        return decorator


class Main(cmd.Cmd):
    intro = f"Welcome to AI Chat in terminal. Type 'help' or '?' for usage info \n Submit any bug at {tgpt.__repo__}/issues/new"
    prompt = f"╭─[{getpass.getuser().capitalize()}@TGPT2](v{tgpt.__version__})\n╰─>"

    def __init__(
        self,
        max_tokens,
        temperature,
        top_k,
        top_p,
        model,
        brave_key,
        timeout,
        quiet=False,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.bot = tgpt.TGPT(
            max_tokens, temperature, top_k, top_p, model, brave_key, timeout
        )
        self.prettify = True
        self.color = "cyan"
        self.code_theme = "monokai"
        self.quiet = quiet

    @busy_bar.run("Settings saved")
    def do_settings(self, line):
        """Configre settings"""
        self.bot.max_tokens_to_sample = click.prompt(
            "Maximum tokens to sample",
            type=click.INT,
            default=self.bot.max_tokens_to_sample,
        )
        self.bot.temperature = click.prompt(
            "Temperature", type=click.FLOAT, default=self.bot.temperature
        )
        self.bot.top_k = click.prompt(
            "Chance of topic being repeated, top_k",
            type=click.FLOAT,
            default=self.bot.top_k,
        )
        self.bot.top_p = click.prompt(
            "Sampling threshold during inference time, top_p",
            type=click.FLOAT,
            default=self.bot.top_p,
        )
        self.bot.model = click.prompt(
            "Model name", type=click.STRING, default=self.bot.model
        )
        self.code_theme = Prompt.ask(
            "Enter code_theme", choices=rich_code_themes, default=self.code_theme
        )
        self.prettify = click.confirm(
            "\nPrettify markdown response", default=self.prettify
        )
        busy_bar.spin_index = click.prompt(
            "Spin bar index [0:/, 1:■█■■■, 2:⣻]",
            default=busy_bar.spin_index,
            type=click.IntRange(0, 2),
        )
        self.color = click.prompt("Response stdout font color", default=self.color)

    @busy_bar.run(help="System error")
    def do_copy_this(self, line):
        """Copy last response
        Usage:
           copy_this:
               text-copied = {whole last-response}
           copy_this code:
               text-copied = {All codes in last response}
        """
        if self.bot.last_response:
            global last_response
            last_response = self.bot.get_message(self.bot.last_response)
            if not "code" in line:
                clipman.set(last_response)
                click.secho("Last response copied successfully!", fg="cyan")
                return

            # Copies just code
            sanitized_codes = []
            code_blocks = re.findall(r"```.*?```", last_response, re.DOTALL)
            for code_block in code_blocks:
                new_code_block = re.sub(
                    "^```.*$", "", code_block.strip(), flags=re.MULTILINE
                )
                if bool(new_code_block.strip()):
                    sanitized_codes.append(new_code_block)
            if sanitized_codes:
                if len(sanitized_codes) > 1:
                    if not click.confirm("Do you wish to copy all codes"):
                        for index, code in enumerate(sanitized_codes):
                            rich.print(
                                Panel(
                                    Markdown(
                                        code_blocks[index], code_theme=self.code_theme
                                    ),
                                    title=f"Index : {index}",
                                    title_align="left",
                                )
                            )

                        clipman.set(
                            sanitized_codes[
                                click.prompt(
                                    "Enter code index",
                                    type=click.IntRange(0, len(sanitized_codes) - 1),
                                )
                            ]
                        )
                        click.secho("Code copied successfully", fg="cyan")
                    else:
                        clipman.set("\n\n".join(sanitized_codes))
                        click.secho(
                            f"All {len(sanitized_codes)} codes copied successfully!",
                            fg="cyan",
                        )
                else:
                    clipman.set(sanitized_codes[0])
                    click.secho("Code copied successfully!", fg="cyan")
            else:
                click.secho("No code found in the last response!", fg="red")
        else:
            click.secho("Chat with AI first.", fg="yellow")

    @busy_bar.run()
    def do_with_copied(self, line):
        """Attach last copied text to the prompt
        Usage:
            from_copied:
                 prompt = {text-copied}
            from_copied Debug this code:
                 prompt = Debug this code {newline} {text-copied}
        """
        issued_prompt = (
            f"{line}\n{clipman.get()}" if bool(line.strip()) else clipman.get()
        )
        click.secho(issued_prompt, fg="yellow")
        if click.confirm("Do you wish to proceed"):
            self.default(issued_prompt)

    @busy_bar.run()
    def do_code(self, line):
        """Enhance prompt for code generation
        usage :
              code <Code description>
        """
        self.default(Optimizers.code(line))

    @busy_bar.run()
    def do_shell(self, line):
        """Enhance prompt for system command (shell) generation
        Usage:
             shell <Action to be accomplished>
        """
        self.default(Optimizers.shell_command(line))
        if click.confirm("Do you wish to run the command(s) generated in your system"):
            self.do_sys(self.bot.get_message(self.bot.last_response))

    def do_clear(self, line):
        """Clear console"""
        sys.stdout.write("\u001b[2J\u001b[H")
        sys.stdout.flush()

    @busy_bar.run()
    def default(self, line):
        """Chat with ChatGPT"""
        if not bool(line):
            return
        if line.startswith("./"):
            os.system(line[2:])
        else:
            try:
                if self.quiet:
                    generated_response = self.bot.chat(line, stream=True)
                    busy_bar.stop_spinning()
                    console_ = Console()
                    with Live(console=console_, refresh_per_second=16) as live:
                        for response in generated_response:
                            live.update(
                                Markdown(response, code_theme=self.code_theme)
                                if self.prettify
                                else response
                            )
                else:
                    busy_bar.start_spinning()
                    generated_response = self.bot.chat(line, stream=True)
                    busy_bar.stop_spinning()
                    stream_output(
                        generated_response,
                        title="AI Response",
                        is_markdown=self.prettify,
                        style=Style(
                            color=self.color,
                        ),
                        code_theme=self.code_theme,
                    )
            except (KeyboardInterrupt, EOFError):
                busy_bar.stop_spinning()
                print("")
                return False  # Exit cmd

            except Exception as e:
                # logging.exception(e)
                busy_bar.stop_spinning()
                logging.error(getExc(e))

    def do_sys(self, line):
        """Execute system commands
        shortcut [./<command>]
        Usage:
            sys <System command>
                  or
             ./<System command>
        """
        os.system(line)

    def do_exit(self, line):
        """Quit this program"""
        if click.confirm("Are you sure to exit"):
            click.secho("Okay Goodbye!", fg="yellow")
            return True


@click.group()
def tgpt2_():
    pass


@tgpt2_.command()
@click.option(
    "-m", "--model", help="Model name for text-generation", default="llama-2-13b-chat"
)
@click.option(
    "-t",
    "--temperature",
    help="Charge of the generated text's randomness",
    type=click.FloatRange(0, 1),
    default=0.2,
)
@click.option(
    "-mt",
    "--max-tokens",
    help="Maximum number of tokens to be generated upon completion",
    type=click.INT,
    default=600,
)
@click.option(
    "-tp",
    "--top-p",
    help="Sampling threshold during inference time",
    type=click.FLOAT,
    default=0.999,
)
@click.option(
    "-tk",
    "--top-k",
    help="Chance of topic being repeated",
    type=click.FLOAT,
    default=-1,
)
@click.option(
    "-bk",
    "--brave-key",
    envvar="brave_key",
    help="Brave API access key",
    default="qztbjzBqJueQZLFkwTTJrieu8Vw3789u",
)
@click.option(
    "-ct",
    "--code-theme",
    help="Theme for displaying codes in response",
    type=click.Choice(rich_code_themes),
    default="monokai",
)
@click.option(
    "-bi",
    "--busy-bar-index",
    help="Index of busy bar icon : [0:/, 1:■█■■■, 2:⣻]",
    type=click.IntRange(0, 2),
    default=2,
)
@click.option("-fc", "--font-color", help="Stdout font color")
@click.option(
    "-to", "--timeout", help="Http requesting timeout", type=click.INT, default=30
)
@click.argument("prompt", required=False)
@click.option(
    "--prettify/--raw", help="Flag for prettifying markdowned response", default=True
)
@click.option(
    "-q",
    "--quiet",
    is_flag=True,
    help="Flag for controlling response-framing",
    default=False,
)
def interactive(
    model,
    temperature,
    max_tokens,
    top_p,
    top_k,
    brave_key,
    code_theme,
    busy_bar_index,
    font_color,
    timeout,
    prompt,
    prettify,
    quiet,
):
    """Chat with AI interactively"""
    bot = Main(max_tokens, temperature, top_k, top_p, model, brave_key, timeout, quiet)
    busy_bar.spin_index = busy_bar_index
    bot.code_theme = code_theme
    bot.color = font_color
    bot.prettify = prettify
    if prompt:
        bot.default(prompt)
    bot.cmdloop()


@tgpt2_.command()
@click.option(
    "-m", "--model", help="Model name for text-generation", default="llama-2-13b-chat"
)
@click.option(
    "-t",
    "--temperature",
    help="Charge of the generated text's randomness",
    type=click.FloatRange(0, 1),
    default=0.2,
)
@click.option(
    "-mt",
    "--max-tokens",
    help="Maximum number of tokens to be generated upon completion",
    type=click.INT,
    default=600,
)
@click.option(
    "-tp",
    "--top-p",
    help="Sampling threshold during inference time",
    type=click.FLOAT,
    default=0.999,
)
@click.option(
    "-tk",
    "--top-k",
    help="Chance of topic being repeated",
    type=click.FLOAT,
    default=-1,
)
@click.option(
    "-bk",
    "--brave-key",
    envvar="brave_key",
    help="Brave API access key",
    default="qztbjzBqJueQZLFkwTTJrieu8Vw3789u",
)
@click.option(
    "-ct",
    "--code-theme",
    help="Theme for displaying codes in response",
    type=click.Choice(rich_code_themes),
    default="monokai",
)
@click.option(
    "-bi",
    "--busy-bar-index",
    help="Index of busy bar icon : [0:/, 1:■█■■■, 2:⣻]",
    type=click.IntRange(0, 2),
    default=2,
)
@click.option(
    "-fc",
    "--font-color",
    help="Stdout font color",
)
@click.option(
    "-to", "--timeout", help="Http requesting timeout", type=click.INT, default=30
)
@click.argument("prompt", required=True)
@click.option(
    "--prettify/--raw", help="Flag for prettifying markdowned response", default=True
)
@click.option(
    "-q",
    "--quiet",
    is_flag=True,
    help="Flag for controlling response-framing",
    default=False,
)
@click.option(
    "-w",
    "--whole",
    is_flag=True,
    default=True,
    help="Give response back as a whole text (Default)",
)
@click.option(
    "-c",
    "--code",
    is_flag=True,
    default=False,
    help="Optimize prompt for code generation",
)
@click.option(
    "-s",
    "--shell",
    is_flag=True,
    default=False,
    help="Optimize prompt for shell command generation",
)
def generate(
    model,
    temperature,
    max_tokens,
    top_p,
    top_k,
    brave_key,
    code_theme,
    busy_bar_index,
    font_color,
    timeout,
    prompt,
    prettify,
    quiet,
    whole,
    code,
    shell,
):
    """Generate a quick response with AI (Default)"""
    bot = Main(max_tokens, temperature, top_k, top_p, model, brave_key, timeout)
    prompt = Optimizers.code(prompt) if code else prompt
    prompt = Optimizers.shell_command(prompt) if shell else prompt
    busy_bar.spin_index = busy_bar_index
    bot.quiet = quiet
    bot.code_theme = code_theme
    bot.color = font_color
    bot.prettify = prettify
    bot.default(prompt)


def main():
    args = sys.argv
    if (
        len(args) > 1
        and args[1] not in ["interactive", "generate"]
        and not "--help" in args
    ):
        sys.argv.insert(1, "generate")  # Just a hack to make 'generate' default command
    tgpt2_()


if __name__ == "__main__":
    main()
