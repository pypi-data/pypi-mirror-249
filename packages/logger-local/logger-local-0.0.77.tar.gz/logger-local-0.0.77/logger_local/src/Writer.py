import os
import sys

from dotenv import load_dotenv

from ._get_connection import get_connection

load_dotenv()

# TODO: We should move this code to python-sdk/infrastructure repo.
#  We should call our_python_init() which calls get_debug() as we might want to add things in the future
os_debug = os.getenv('DEBUG', "False")
debug = os_debug.lower() == 'true' or os_debug == '1'

if debug:
    print("Writer.py debug is on debug=", debug)

global_connection = None


class Writer:
    @staticmethod
    def add_message(message, log_level):
        if debug:
            print("add_message" + message + ' ' + str(log_level), file=sys.stderr)
        connection = None
        try:
            # creating connection
            connection = get_connection()
            # connection = self._pool.get_connection()
            cursor = connection.cursor()
            query = (f"INSERT INTO logger.logger_table (message, severity_id) "
                     f"VALUES ('{message}', {log_level})")
            cursor.execute(query)
        except Exception as e:
            print("Exception Writer.py Writer.add_message caught" + str(e), file=sys.stderr)
        finally:
            if connection:
                connection.commit()

    @staticmethod
    def add_message_and_payload(message: str = None, **kwargs):
        connection = None
        try:
            connection = get_connection()
            params_to_insert = kwargs['object']
            # creating connection:
            # connection = self._pool.get_connection()
            cursor = connection.cursor()
            cursor.execute(
                f"INSERT INTO location.location_table (coordinate) "
                f"VALUES (POINT({params_to_insert.get('latitude') or 0},{params_to_insert.get('longitude') or 0}));")
            coordinate_id = cursor.lastrowid

            params_to_insert.pop('latitude', None)
            params_to_insert.pop('longitude', None)

            params_to_insert['location_id'] = coordinate_id
            listed_values = list(params_to_insert.values())
            joined_keys = ','.join(list(params_to_insert.keys()))
            if message is not None:
                listed_values.append(message)
                joined_keys += (',' if joined_keys else '') + 'message'

            placeholders = ','.join(['%s'] * len(listed_values))
            query = f"INSERT INTO logger.logger_table ({joined_keys}) VALUES ({placeholders})"
            cursor = connection.cursor()
            cursor.execute(query, listed_values)
        except Exception as e:
            print("Exception logger Writer.py add_message_and_payload " + str(e), file=sys.stderr)
        finally:
            if connection:
                connection.commit()
