# a Database Wrapper for Redis and MySQL

## from DBService import MysqlService

### 
        mysql_server = MysqlService(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_DB)
        # query
        mysql_server.query("SELECT * FROM TABLE")
        # execute
        mysql_server.execute("UPDATE from TABLES SET a = 55 WHERE id = 1")
        # transaction
        mysql_server.query(["UPDATE from TABLES SET a = 55 WHERE id = 1","UPDATE from TABLES SET a = 545 WHERE id = 2"])

## from DBService import RedisService

        redis_server = RedisService("redis://:user@host:port/db")

## from DBService import PgsqlService

        pgsql_server = PgsqlService(PGSQL_HOST, PGSQL_USER, PGSQL_PASSWORD, PGSQL_PORT, PGSQL_DB)
        # query
        pgsql_server.query("SELECT * FROM TABLE")
        # execute
        pgsql_server.execute("UPDATE from TABLES SET a = 55 WHERE id = 1")
        # transaction
        pgsql_server.query(["UPDATE from TABLES SET a = 55 WHERE id = 1","UPDATE from TABLES SET a = 545 WHERE id = 2"])

## also support async,use them just add 'await'
        from DBService import AsyncRedisService,AsyncMysqlService,AsyncPgsqlService
        redis_server = AsyncRedisService("redis://:user@host:port/db")
        mysql_server = AsyncMysqlService(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_DB)
        pgsql_server = AsyncPgsqlService(PGSQL_HOST, PGSQL_USER, PGSQL_PASSWORD, PGSQL_PORT, PGSQL_DB)
        # or pgsql_server = AsyncPgsqlService(dsn="postgresql://username:password@localhost:5432/mydatabase")
