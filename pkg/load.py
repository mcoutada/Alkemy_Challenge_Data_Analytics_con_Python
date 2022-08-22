import os

import decouple as d
import sqlalchemy as s

import pkg.logger as logger


def exists_in_db(t, e):
    """
    It checks if a table exists in the database.

    :param t: the table name
    :return: A boolean value.
    """
    return s.inspect(e).has_table(table_name=t, schema=POSTGRES_SCHEMA)


# Set the logger for this file
log = logger.set_logger(logger_name=logger.get_rel_path(__file__))

POSTGRES_USER = d.config("POSTGRES_USER")
POSTGRES_PASSWORD = d.config("POSTGRES_PASSWORD")
POSTGRES_DB = d.config("POSTGRES_DB")
POSTGRES_PORT = d.config("POSTGRES_PORT")
POSTGRES_HOST = d.config("POSTGRES_HOST")
POSTGRES_SCHEMA = d.config("POSTGRES_SCHEMA")


def load(dfs_dic):
    url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    engine = s.create_engine(url)

    # Apply prefix to category names as they will be used as table names in
    # the database
    dfs_dic = {f"alk_{cat}": df for cat, df in dfs_dic.items()}

    # Apply exists_in_db to all elements in a list
    exist_in_db = [exists_in_db(tb, engine) for tb in dfs_dic.keys()]

    # Check if all tables exist in the database
    if not all(exist_in_db):
        # If none of them exist, create them
        if not any(exist_in_db):
            with open(os.path.join(os.getcwd(), "pkg", "db_create_tables.sql")) as file:
                engine.execute(s.text(file.read()))
                log.info("Tables created")

        else:
            log.critical(
                "Some tables exist in the database but not all of them. Please check the database."
            )
            exit()

    # Load the dataframes into the database
    for cat, df in dfs_dic.items():
        df.to_sql(
            name=cat,
            con=engine,
            if_exists="replace",
            index=False,
            schema=POSTGRES_SCHEMA,
        )


if __name__ == "__main__":
    load()
