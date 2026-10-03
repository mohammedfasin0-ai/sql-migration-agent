import psycopg

with psycopg.connect(
    host= "127.0.0.1",
    port=5433,
    dbname= "migration_test",
    user= "postgres",
    password= "postgres",
    connect_timeout= 5,
) as conn:
    print("Connected to PostgreSQL")