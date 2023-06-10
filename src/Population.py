from typing import List
import datetime
import uuid
import numpy as np
from src.QueryEngine import QueryEngine

class Population:

    def __init__(self):
        # scene basics
        self.scene_cols = ['scene_id', 'name', 'tickets']
        self.scene_col_type = ['UUID', 'text', 'list<int>']
        self.scene_names = ['Orange Main Stage', 'Tent Stage', 'Alter Stage', 'Beat Stage']
        self.scene_ticket_nr = [50, 30, 30, 20]
        self.scene_id = [uuid.uuid4() for i in range(len(self.scene_names))]
        self.scene_tickets = list(list(range(1, self.scene_ticket_nr[i] + 1)) for i in range(len(self.scene_ticket_nr)))

        # concert basics
        self.concert_cols = ['concert_id', 'artist', 'scene_id', 'available_tickets', 'concert_date']
        self.concert_col_type = ['UUID', 'text', 'UUID', 'list<int>', 'timestamp']
        self.concert_artists = ['Lil Nas X', 'Lizzo', 'OneRepublic', 'SZA', 'Machine Gun Kelly', 'Kukon', 'Nothing But Thieves', 'Brodka', 'David Kushner']
        self.concert_num = 9
        self.concert_id = [uuid.uuid4() for _ in range(self.concert_num)]
        self.concert_available_tickets = list(list(range(1, self.scene_ticket_nr[i] + 1)) for i in range(len(self.scene_ticket_nr)))

        self.QE = QueryEngine()

    def initialize(self) -> List[str]:
        inserting_scenes = 'BEGIN BATCH '
        for i in range(len(self.scene_names)):
            values = [self.scene_id[i], self.scene_names[i], self.scene_tickets[i]]
            query = self.QE.INSERT('scene', self.scene_cols, self.scene_col_type, values)
            inserting_scenes += query
        inserting_scenes += ' APPLY BATCH ;'

        inserting_concerts = 'BEGIN BATCH '
        for i in range(len(self.scene_names)):
            scene = np.random.choice(list(range(len(self.scene_id))))
            values = [self.concert_id[i], self.concert_artists[i], self.scene_id[scene], self.concert_available_tickets[i], datetime.datetime.now()]
            query = self.QE.INSERT('concert', self.concert_cols, self.concert_col_type, values)
            inserting_concerts += query
        inserting_concerts += ' APPLY BATCH ;'

        initialized = [inserting_scenes, inserting_concerts]
        return initialized