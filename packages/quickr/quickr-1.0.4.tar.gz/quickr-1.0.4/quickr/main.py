from os import getcwd, listdir
from os.path import join, abspath, dirname, isdir
import argparse
from shutil import copytree
import colorama
import questionary


def get_templates(template_dir):
    template_names = [
        folder
        for folder in listdir(template_dir)
        if isdir(join(template_dir, folder)) and not folder.startswith("__")
    ]
    return template_names


def main():
    parser = argparse.ArgumentParser(
        prog="quick",
        description="Creates a project template in the specified directory.",
    )
    parser.add_argument("project_name", help="Target project name", default="project")
    parser.add_argument("-t", "--template", help="Project template")
    args = parser.parse_args()

    template_dir = join(dirname(abspath(__file__)), "templates")

    if args.template is None:
        template_names = get_templates(template_dir)
        args.template = questionary.select(
            "Which template to use?", template_names
        ).ask()

    src_dir = join(template_dir, args.template)
    dest_dir = join(getcwd(), args.project_name)

    try:
        copytree(src_dir, dest_dir)
    except Exception as e:
        print(colorama.Fore.RED, f"Copy error: {e}", colorama.Fore.RESET)
    else:
        print(
            colorama.Fore.GREEN,
            f'The project "{args.project_name}" has been successfully created!',
            colorama.Fore.RESET,
        )
