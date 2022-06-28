import os
import tornado.ioloop
import tornado.web
import motor.motor_tornado
from bson import ObjectId
import json
# existing collectionsa
collections = ['goods', 'purhases', 'users_basket']

# connection string to mongo db
connection_string = 'mongodb+srv://<login>:<passwd>@cluster0.2vrmo.mongodb.net/user_shopping_list?retryWrites=true&w=majority'

# create motor client
client = motor.motor_tornado.MotorClient(connection_string)

db = client['user_shopping_list']


# for objectid overcoming
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

# handle routes
class MainHandler(tornado.web.RequestHandler):
    
    async def get(self):
        collection_list = []
        for collection in collections:
            data = await self.settings["db"][collection].find().to_list(1000)
            # json dumps for data object overcoming
            collection_list.append(JSONEncoder().encode(json.dumps(data, indent=4, sort_keys=True, default=str)))
        return self.write({"data": collection_list })

# tornado web app
app = tornado.web.Application(
    [
        (r"/", MainHandler),
    ],
    db=db,
)

if __name__ == "__main__":
    # run tornado web app   
    app.listen(8000)
    # wrapper around the asyncio event loop
    tornado.ioloop.IOLoop.current().start()
