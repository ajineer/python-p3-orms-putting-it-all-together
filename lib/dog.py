import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    all = []

    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed
        Dog.all.append(self)

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs(
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql).fetchall()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql).fetchall()

    def save(self):
        sql = """
        INSERT INTO dogs (name, breed) VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.breed)).fetchone()
        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]
    
    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog
    
    # creates Dog instancd from row in database
    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog
    
    # return all Dog instances created from each row in database
    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM dogs
        """   
        data = CURSOR.execute(sql).fetchall()
        cls.all = [cls.new_from_db(row) for row in data]
        return cls.all

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM dogs
            WHERE name = ?
            LIMIT 1
        """
        dog_data = CURSOR.execute(sql, (name,)).fetchone()
        dog_obj =  cls.new_from_db(dog_data)
        return dog_obj

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * 
            FROM dogs
            WHERE id = ?
            LIMIT 1
        """
        dog_data = CURSOR.execute(sql, (id, )).fetchone()
        dog_obj = cls.new_from_db(dog_data)
        return dog_obj

