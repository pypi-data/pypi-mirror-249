from typing import (Optional,
                    Dict,
                    List)

from pydantic import BaseModel

from .type import CrudMethods


class RequestResponseModel(BaseModel):
    requestUrlParamModel: Optional[str]
    requestRelationshipUrlParamField: Optional[List[str]]
    requestQueryModel: Optional[str]
    requestBodyModel: Optional[str]
    responseModel: Optional[str]
    jsonRequestFieldModel: Optional[str]
    jsonbRequestFieldModel: Optional[str]
    arrayRequestFieldModel: Optional[str]
    foreignListModel: Optional[List[dict]]


class CRUDModel(BaseModel):
    GET: Optional[Dict[CrudMethods, bool]]
    POST: Optional[Dict[CrudMethods, bool]]
    PUT: Optional[Dict[CrudMethods, bool]]
    PATCH: Optional[Dict[CrudMethods, bool]]
    DELETE: Optional[Dict[CrudMethods, bool]]
    PRIMARY_KEY_NAME: Optional[str]
    UNIQUE_LIST: Optional[List[str]]

    def get_available_request_method(self):
        return [i for i in self.dict(exclude_unset=True, ).keys() if i in ["GET", "POST", "PUT", "PATCH", "DELETE"]]

    def get_model_by_request_method(self, request_method):
        available_methods = self.dict()
        return available_methods[request_method]
