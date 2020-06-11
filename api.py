import io
import json
import mimetypes
import os
import pickle
import uuid

import falcon

import msgpack
import nasdaqAPI

api = application = falcon.API()


class GetData(object):

    # The resource object must now be initialized with a path used during POST
    def __init__(self):
        self.dataScrapper = nasdaqAPI.NasdaqDataStreamer({"SYM":"tsla"})

    def on_post(self, req, resp):

        settings = req.stream.read(req.content_length or 0).decode("utf-8")

        self.dataScrapper.update(json.loads(settings))
        data = self.dataScrapper.run()

        resp.body = json.dumps(data)
        resp.status = falcon.HTTP_201


get_data = GetData()

api.add_route('/get_data', get_data)

