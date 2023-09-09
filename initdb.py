# import sys
# from pathlib import Path

# PACKAGE_PATH = str(Path(__file__).parent.parent)
# sys.path.insert(0, PACKAGE_PATH)

from app.config import engine
from app.main import Base  # noqa: F401


def init() -> None:
    Base.metadata.create_all(bind=engine)


def main() -> None:
    init()


if __name__ == "__main__":
    main()
