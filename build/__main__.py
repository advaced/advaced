# Modules for project-building
from cmd import build as build_cmd
from lib import build as build_lib


def build_project() -> int:
    # Build the command(s)
    success_cmd = build_cmd()

    # Build the library
    success_lib = build_lib()

    if not success_cmd or not success_lib:
        # Logging for development
        print('build failed')

        return False

    return True


if __name__ == '__main__':
    build_project()
