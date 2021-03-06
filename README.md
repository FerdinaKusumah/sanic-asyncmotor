# Sanic Motor

Example how to use [Python Sanic](https://github.com/huge-success/sanic) and [Async MongoDB Driver](https://motor.readthedocs.io/en/stable/)  

## Prerequisites
1. Install python sanic

```shell
    $ pip install sanic
```
2. Install Motor (Asynchronous Python driver for MongoDB)
```bash
    $ pip install motor
```
3. Create conection pool
```python
import urllib.parse
import motor.motor_asyncio as async_motor

@app.listener('before_server_start')
async def register_db(app, loop):
    # Create a database connection pool
    connection_uri = "mongodb://{username}:{password}@{host}:{port}/".format(
        username="foo", password=urllib.parse.quote("bar"),
        host="localhost", port=27017
    )
    database_name = "foobar"
    app.config['db'] = async_motor.AsyncIOMotorClient(
        connection_uri,
        # in milliseconds
        maxIdleTimeMS=10000,
        # minimal pool size
        minPoolSize=10,
        # maximal pool size
        maxPoolSize=50,
        # connection timeout in miliseconds
        connectTimeoutMS=10000,
        # boolean
        retryWrites=True,
        # wait queue in miliseconds
        waitQueueTimeoutMS=10000,
        # in miliseconds
        serverSelectionTimeoutMS=10000
    )[database_name]
```

4. To see detail code you can check `main.py`
5. Happy coding :)

## Reference
1. [Sanic](https://github.com/huge-success/sanic)
2. [Async MongoDB Driver (Motor)](https://motor.readthedocs.io/en/stable/)