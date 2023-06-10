class Table:
    scene = """
        CREATE TABLE IF NOT EXISTS scene (
            scene_id uuid,
            name text,
            tickets list<int>,
            PRIMARY KEY (scene_id)
        );
    """

    concert = """
        CREATE TABLE IF NOT EXISTS concert (
            concert_id uuid,
            artist text,
            scene_id uuid,
            available_tickets list<int>,
            concert_date timestamp,
            PRIMARY KEY (concert_id)
        );
    """

    ticket = """
        CREATE TABLE IF NOT EXISTS ticket (
            ticket_id uuid,
            ticket_nr int,
            concert_id uuid,
            name text,
            email text,
            PRIMARY KEY (ticket_id)
        );
    """

    database = [scene, concert, ticket]

