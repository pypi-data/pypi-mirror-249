import os
import sqlite3
from pydantic import BaseModel

class Database(BaseModel):
    sqlpath = 'ttele.db'
    con = sqlite3.connect(sqlpath, uri=True)
    cursor = con.cursor()

    def create_tables(self):
        # subscriber != donator : 0 False 1 True
        # full_subscriber : 0 False 1 True (will join group)
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                            user_id integer primary key autoincrement,
                            username text null,
                            chat_id integer null,
                            firstname text null,
                            is_subscriber integer null,
                            is_full_subscriber integer null
                        )''')
        
        # no_tag : 0 False 1 True
        # no_keyboard : 0 False 1 True
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS settings(
                            sett_id integer primary key autoincrement,
                            no_tag integer null,
                            no_keyboard integer null,
                            id_user integer null
                        )''')
        
        # safe username of public channel
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS public_channels(
                            pchannel_id integer primary key autoincrement,
                            username text null,
                            notes text null
                        )''')
        
        # safe sticker links
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS stickers(
                            sticker_id integer primary key autoincrement,
                            link text null,
                            notes text null
                        )''')
        
        # safe messages
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS messages(
                            msg_id integer primary key autoincrement,
                            id integer null,
                            entity text null,
                            link text null,
                            type text null
                        )''')
        


        