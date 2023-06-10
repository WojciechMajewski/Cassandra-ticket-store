from src.Cassandra_main import connect
from src.System import MainMenu


def main() -> None:
    client = connect()
    rs = MainMenu(client)
    rs.main()


if __name__ == '__main__':
    main()