from pick import pick
from time import sleep
import time
import uuid
from src.Cassandra_main import *
from src.QueryEngine import QueryEngine

class MainMenu:
    def __init__(self, client: CassandraConnector):
        self.client = client
        self.QE = QueryEngine()
        self.emails_used = set()
    
    def main(self):
        while(True):
            title = 'Please choose what you want to do on this beautiful day'
            options = ['List all scenes and concerts', 'Buy a ticket', 'See ticket', 'Sell ticket', 'Update ticketholder', 'quit']
            option, index = pick(options, title, indicator='=>', default_index=0)

            if index == 0:
                self.list_all()

            elif index == 1:
                self.buy_ticket()

            elif index == 2:
                self.view_ticket()

            elif index == 3:
                self.sell_ticket()

            elif index == 4:
                self.update_ticket()
            
            else:
                break

    def list_all(self):
        print("\n\n\n\nLISTING ALL SCENES")
        query = self.QE.SELECT_ALL('scene')
        query_result = self.client.execute_query(query)
        for line in query_result:
            scene_id, name, tickets = line
            print(f'Scene_name {name}, all tickets: {len(tickets)} \n')
        
        print("\n\n\n\nLISTING ALL CONCERTS")
        query = self.QE.SELECT_ALL('concert')
        query_result = self.client.execute_query(query)
        for line in query_result:
            concert_id, artist, available_tickets, concert_date, scene_id = line
            scene_name = self.get_scene_name(scene_id)
            print(f'Concert of {artist} at {scene_name}, where there are {len(available_tickets)} tickets available on {concert_date}\n')
        input("Press Enter to continue...")
    
    def get_scene_name(self, scene_id):
        query = self.QE.SELECT_WHERE('scene', 'scene_id', 'UUID', scene_id)
        scene_name = self.client.execute_query(query)[0][1]
        return scene_name
    
    def get_concert_name(self, concert_id):
        query = self.QE.SELECT_WHERE('concert', 'concert_id', 'UUID', concert_id)
        query_res = self.client.execute_query(query)[0]
        concert_name = query_res[1]
        scene_name = query_res[4]
        scene_name = self.get_scene_name(scene_name)
        return concert_name, scene_name

    def buy_ticket(self):
        concerts = dict()
        query = self.QE.SELECT_ALL('concert')
        query_result = self.client.execute_query(query)
        for line in query_result:
            concert_id, artist, available_tickets, concert_date, scene_id = line
            concerts[artist] = concert_id
        artists = list(concerts.keys())
        title = 'Please choose which concert you want to buy a ticket to'
        option, index = pick(artists, title, indicator='=>', default_index=0)
        concert_id = concerts[artists[index]]
        query = self.QE.SELECT_WHERE('concert', 'concert_id', 'UUID', concert_id)
        concert_query = self.client.execute_query(query)[0][2]
        if concert_query is not None and len(concert_query) > 0:
            title = 'Which ticket number would you like?'
            option, ticket_nr = pick(concert_query, title, indicator='=>', default_index=0)
            ticket_nr = concert_query[ticket_nr]
            concert_query.remove(ticket_nr)
            query = self.QE.UPDATE('concert', 'available_tickets', 'list', concert_query, 'concert_id', 'UUID', concert_id)
            self.client.execute_query(query)
            name = input('Please enter your name:')
            original_email = True
            while original_email:
                email = input('Please enter your email:')
                if email in self.emails_used:
                    print('Only one ticket per one email.')
                else:
                    original_email = False
                    self.emails_used.add(email)
            ticket_id = uuid.uuid4()
            values = [ticket_id, ticket_nr, concert_id, name, email]
            table_cols = ['ticket_id', 'ticket_nr', 'concert_id', 'name', 'email']
            col_types = ['UUID', 'int', 'UUID', 'text', 'text']
            query = self.QE.INSERT('ticket', table_cols, col_types, values)
            self.client.execute_query(query)
            sleep(2)
            query = self.QE.SELECT_WHERE('ticket', 'ticket_id', 'UUID', ticket_id)
            query_return = self.client.execute_query(query)
            ticket_reserved_id = query_return[0]
            query_ticket_id, query_concert_id, query_email, query_name, query_ticket_nr = ticket_reserved_id
            if query_ticket_id == ticket_id:
                print('You have successfully bought a ticket (unless someone clicked after you) :)')
            else:
                print('Sadly this ticket is already bought. Try again.')
        else:
            print("Unfortunately we've sold all our tickets")
        input("Press Enter to continue...")
    
    def update_ticket(self):
        email = input('Please enter the email you provided during buying the ticket:')
        query = self.QE.SELECT_WHERE('ticket', 'email', 'text', email)
        query_res = list(self.client.execute_query(query))
        if query_res is not None and len(query_res) > 0:
            ticket_query = query_res[0]
            ticket_id, concert_id, email, name, ticket_nr = ticket_query
            artist, scene_name = self.get_concert_name(concert_id)
            print(f'Concert of {artist} at {scene_name}, your ticket_nr is {ticket_nr} and your name is {name}\n')
            new_name = input('Provide new name of the ticket-holder:')
            query = self.QE.UPDATE('ticket', 'name', 'text', new_name, 'ticket_id', 'UUID', ticket_id)
            self.client.execute_query(query)
        else:
            print("No such email bought a ticket")
        input("Press Enter to continue...")

    def view_ticket(self):
        email = input('Please enter the email you provided during buying the ticket:')
        query = self.QE.SELECT_WHERE('ticket', 'email', 'text', email)
        query_res = list(self.client.execute_query(query))
        if query_res is not None and len(query_res) > 0:
            ticket_query = query_res[0]
            ticket_id, concert_id, email, name, ticket_nr = ticket_query
            artist, scene_name = self.get_concert_name(concert_id)
            print(f'Concert of {artist} at {scene_name}, your ticket_nr is {ticket_nr} and your name is {name}\n')
        else:
            print("No such email bought a ticket")
        input("Press Enter to continue...")

    def sell_ticket(self):
        email = input('Please enter the email you provided during buying the ticket:')
        query = self.QE.SELECT_WHERE('ticket', 'email', 'text', email)
        query_res = list(self.client.execute_query(query))
        if query_res is not None and len(query_res) > 0:
            ticket_query = query_res[0]
            ticket_id, concert_id, email, name, ticket_nr = ticket_query
            delete_query = self.QE.DELETE('ticket', 'ticket_id', 'UUID', ticket_id)
            self.client.execute_query(delete_query)
            concert_query = self.QE.SELECT_WHERE('concert', 'concert_id', 'UUID', concert_id)
            concert_query = self.client.execute_query(concert_query)[0][2]
            concert_query.append(ticket_nr)
            query = self.QE.UPDATE('concert', 'available_tickets', 'list', concert_query, 'concert_id', 'UUID', concert_id)
            self.client.execute_query(query)
            self.emails_used.remove(email)
            print("You have successfully sold a ticket")
        else:
            print("No such email bought a ticket")
