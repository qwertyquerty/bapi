import math

from flask import jsonify, request
from flask_apispec import MethodResource, use_kwargs, marshal_with, doc
from flask_restful import Resource
from marshmallow import schema, fields


from app import cfg, db
from app.schemas import *

class BanListResource(Resource):
    @doc(description="Get a paginated list of bans.")
    @use_kwargs(PaginationSearchQuerySchema)
    @marshal_with(PaginationResultSchema)
    def get(self, **kwargs):
        page = max(min(kwargs.get("page", type=int, default=1), 1_000_000))
        query = db.query_grouped_bans(search_query=kwargs.get("search_query"))
        length = query.count()

        displayed_bans = query.offset((page - 1) * cfg.API["items-per-page"]).limit(cfg.API["items-per-page"])

        return {
            "page": page,
            "pages": math.ceil(length / cfg.API["items-per-page"]),
            "page_length": cfg.API["items-per-page"],
            "total_length": length,
            "data": [db.Ban.to_public_dict(ban) for ban in displayed_bans]
        }
