import urllib.parse
import motor.motor_asyncio as async_motor
from sanic import Sanic, response


app = Sanic(__name__)


@app.route("/api/foo/bar")
async def test(request):
    conn = request.app.config['db']
    my_collection = 'collection_names'
    data = list(
        jsonify(doc) for doc in await conn[my_collection].find({}).sort("_id", 1).to_list(100)
    )
    return response.json({'status': 200, 'data': data}, status=200)


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


@app.listener('after_server_stop')
async def close_connection(app, loop):
    app.config['db'].close()


def jsonify(doc):
    """
    Parse asyncpg record response into JSON format
    """
    doc['id'] = str(doc['_id'])
    del doc['_id']

    return doc


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000,
            access_log=True, debug=True)