import sys
import argparse
from rich.console import Console

from . import __version__, MarkerApp

CONSOLE = Console()


def run() -> None:
    if len(sys.argv) == 1:
        sys.argv.append("-h")

    args = parse_cli()
    CONSOLE.print(f"[b]Args: {args}")

    # build then run
    marker = MarkerApp(
        dir_image=args["i"],
        classes=args["c"],
        classes_kpts=args["kc"],
        model=args["model"],
        use_gpu=args["gpu"],
        min_side=args["min_side"],
        summary=args["summary"],
        verbose=args["verbose"],
    )
    with CONSOLE.status("Running..."):
        marker.mainloop()


def parse_cli():
    parser = argparse.ArgumentParser(
        description="🍇🍈🍉🍊🍋🍌🍍🥭🍎🍏🍐🍑🍒🍓🫐🥝🍅🫒🥥🥑",
        epilog=f"version: {__version__} ",
    )

    parser.add_argument("-i", required=True, type=str, help="Source directory")

    parser.add_argument(
        "-c",
        default=None,
        nargs="+",
        type=str,
        help="Class names",
    )
    parser.add_argument(
        "-kc",
        default=None,
        nargs="+",
        type=str,
        help="Keypoints class names",
    )

    parser.add_argument(
        "--min-side",
        default=5,
        type=int,
        help="min bbox side",
    )

    parser.add_argument(
        "--model",
        default=None,
        type=str,
        help="Onnx model",
    )

    parser.add_argument(
        "--gpu",
        action="store_true",
        help="Use gpu",
    )

    parser.add_argument(
        "--summary",
        action="store_true",
        help="summary of labels",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Detail summary",
    )

    parser.add_argument(
        "--version",
        "-v",
        "-V",
        action="version",
        version=f"version: {__version__}",
        help="Get version",
    )

    args = vars(parser.parse_args())
    return args


if __name__ == "__main__":
    run()
