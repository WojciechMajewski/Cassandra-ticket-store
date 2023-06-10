from cassandra.cluster import Cluster, ResultSet
from cassandra.query import tuple_factory

from src.Population import Population
from src.Define_Tables import Table

Table = Table()
table_names = ['scene', 'concert', 'ticket']
Population = Population()

class CassandraConnector:

    def __init__(self, ip_address, port, keyspace, initialize):
        self.cluster = Cluster([ip_address], port)
        self.session = None
        self.create_session(keyspace, 3, 'SimpleStrategy')
        if initialize:
            self.create_tables()
            self.populate()

    def create_session(self, keyspace, replication_factor, strategy) -> None:
        self.session = self.cluster.connect()
        self.session.default_timeout = 60
        fancy_bracket_left = "{"
        fancy_bracket_right = "}"
        command = f"CREATE KEYSPACE IF NOT EXISTS {keyspace}  WITH REPLICATION = {fancy_bracket_left} 'class': '{strategy}','replication_factor': {replication_factor} {fancy_bracket_right} ;"
        self.session.execute(command)
        self.session.execute(f"USE {keyspace};")
        self.session.set_keyspace(keyspace)
        self.session.row_factory = tuple_factory
    
    def reset(self):
        for table in table_names:
            print(table)
            query = f"DROP TABLE IF EXISTS {table} ; "
            self.session.execute(query)
        print("I'VE DROPPED THEM ALL KIND SIR")

    def create_tables(self) -> None:
        self.reset()
        for table in Table.database:
            self.session.execute(table)
        print("I HAVE CREATED TABLES BE PROUD OF ME")

    def populate(self) -> None:
        for query in Population.initialize():
            self.session.execute(query)
        print("ALL INITIAL DATA INSERTED BE PROUD OF ME")

    def execute_query(self, query):
        try:
            res = self.session.execute(query)
            return res
        except Exception as error:
            # handle the exception
            print("CHECK YOUR FUCKING QUERIES DUMBASS")
            print("An exception occurred:", error) # An exception occurred: division by zero


    def reset_and_repopulate(self):
        self.reset()
        self.create_tables()
        self.populate()


def connect(initialize = True) -> CassandraConnector:
    return CassandraConnector("172.17.0.2", 9042, 'opener', initialize)