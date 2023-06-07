from flask import abort, jsonify
from flask_apispec import MethodResource, use_kwargs, marshal_with, doc
from flask_restful import Resource
from marshmallow import schema, fields

from app import cfg, util

class StatsResource(Resource):
    @doc(description="Returns the JSON data from the ?status game query of all servers.")
    def get(self):
        try:
            d = {}

            for server in cfg.SERVERS:
                if server["open"]:
                    try:
                        d[server["id"]] = util.fetch_server_status(server["id"])
                    except Exception as E:
                        d[server["id"]] = {"error": str(E)}

            return jsonify(d)

        except Exception as E:
            abort(500, {"error": str(E)})


class ServerStatsResource(Resource):
    @doc(description="Returns the JSON data from the ?status game query of the specified server.")
    def get(self, id):
        if not util.get_server(id):
            return abort(404, {"error": "unknown server"})

        try:
            return jsonify(util.fetch_server_status(id))
        except Exception as E:
            abort(500, {"error": str(E)})


class StatsTotalsSchema(Schema):
    total_players = fields.Integer()
    total_rounds = fields.Integer()
    total_connections = fields.Integer()

class StatsTotalsResource(Resource):
    @doc(description="Returns total unique players, total rounds, and total connections.")
    @marshal_with(StatsTotalsSchema)
    def get(self):
        return util.fetch_server_totals()
