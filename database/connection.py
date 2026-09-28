import psycopg

def get_connection(config):
    connection = psycopg.connect(
    user=config.user,
    password=config.password,
    host=config.host,
    port=config.port,
    dbname=config.name,
    )
    return connection