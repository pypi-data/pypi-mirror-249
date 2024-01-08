import sqlite3
from datetime import datetime
from src.storage_service_abstract import StorageService


class SQLiteSaveService(StorageService):
    """
    A class to implement CRUD operations with JSON.

    Attributes
    ----------
    db_name : str
        Name of your SQLite db in which will be saved information.

    Methods
    -------
     __init__:
    Create DB file, two tables "task_progress" and "email_status". Create connection and cursor.

    add_record:
    Insert current email information in your storage service.

    update_record:
    Update current email information in your storage service.

    get_record:
    Get current email information from your storage service.

    delete_record:
    Delete current email information from your storage service.
    """

    db_name = 'forager.db'

    def __init__(self):
        """
        Create DB file, two tables "task_progress" and "email_status". Create connection and cursor.

        :return: None
        """
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS task_progress (
                id INTEGER PRIMARY KEY,
                task_name TEXT NOT NULL,
                date DATETIME NOT NULL,
                status TEXT NOT NULL
                )
                """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS email_status (
                id INTEGER PRIMARY KEY,
                email TEXT NOT NULL,
                status TEXT NOT NULL
                )
                """)
            self.connection.commit()
        except sqlite3.Error as error:
            print('DB connection error', error)

    def add_record(self, data_args):
        """
        Insert email information in your storage service.

        :param data_args: dict, response from email verification command.
        :return: None
        """
        if (self.cursor.execute(
                'SELECT * FROM email_status WHERE email = ?',
                (data_args['email'],),
        ).fetchall()):
            self.update_record(data_args)
        else:
            try:
                self.cursor.execute(
                    'INSERT INTO task_progress (task_name, date, status) VALUES (?, ?, ?)',
                    ('email_verification', datetime.now(), 'add_record'),
                )
                self.cursor.execute(
                    'INSERT INTO email_status (email, status) VALUES (?, ?)',
                    (data_args['email'], data_args['status']),
                )
                self.connection.commit()
                self.cursor.close()
                return 'Values insert successfully'
            except sqlite3.Error as error:
                print('DB connection error', error)
            finally:
                if (self.connection):
                    self.connection.close()
                    print('Connection closed')

    def update_record(self, data_args):
        """
        Update current email information in your storage service.

        :param data_args: dict, response from email verification command.
        :return: None
        """
        try:
            self.cursor.execute(
                'INSERT INTO task_progress (task_name, date, status) VALUES (?, ?, ?)',
                ('email_verification', datetime.now(), 'update_record'),
            )
            self.cursor.execute(
                'UPDATE email_status SET status = ? WHERE email = ?',
                (data_args['email'], data_args['status']),
            )
            self.connection.commit()
            self.cursor.close()
            return 'Values updated successfully'
        except sqlite3.Error as error:
            print('DB connection error', error)
        finally:
            if (self.connection):
                self.connection.close()
                print('Connection closed')

    def get_record(self, email):
        """
        Get current email information from your storage service.

        :param email: str
        :return: None
        """
        try:
            self.cursor.execute('SELECT * FROM email_status WHERE email = ?', (email, ))
            emails = self.cursor.fetchall()
            for email in emails:
                return email

            self.cursor.execute(
                'INSERT INTO task_progress (task_name, date, status) VALUES (?, ?, ?)',
                ('email_verification', datetime.now(), 'get_record'),
            )
            self.connection.commit()
            self.cursor.close()
        except sqlite3.Error as error:
            print('DB connection error', error)
        finally:
            if (self.connection):
                self.connection.close()
                print('Connection closed')

    def delete_record(self, email):
        """
        Delete current email information from your storage service.

        :param email: str
        :return: None
        """
        try:
            self.cursor.execute('DELETE FROM email_status WHERE email = ?', (email,))
            self.cursor.execute(
                'INSERT INTO task_progress (task_name, date, status) VALUES (?, ?, ?)',
                ('email_verification', datetime.now(), 'delete_record'),
            )
            self.connection.commit()
            self.cursor.close()
            return f'Email - {email} deleted'
        except sqlite3.Error as error:
            print('DB connection error', error)
        finally:
            if (self.connection):
                self.connection.close()
                print('Connection closed')
