import inspect
import logging
from typing import Callable, Type, Dict, Any, List, Optional

from pydantic import BaseModel


logger = logging.getLogger(__name__)


class BaseResponse(BaseModel):
    success: bool = True
    error: Optional[str] = None


def function(name: str,
             description: str,
             request_model: Type[BaseModel],
             response_model: Type[BaseModel],
             is_consequential: bool = False):
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            logger.info(f"Run function [{name}] with arguments [{args}]")
            return func(*args, **kwargs)

        wrapper.function_metadata = {
            "name": name,
            "description": description,
            "request_model": request_model,
            "response_model": response_model,
            "is_consequential": is_consequential
        }

        return wrapper

    return decorator


def tool(name: str):
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.function_metadata = {
            "name": name
        }

        return wrapper

    return decorator


class Tool:

    def __init__(self, schema_format: str = "openai_function"):
        self._function_by_name = {}
        self._function_schemas = []

        for name, func in inspect.getmembers(self, predicate=inspect.ismethod):
            if hasattr(func, "function_metadata"):
                metadata = getattr(func, "function_metadata")
                self._function_by_name[metadata["name"]] = func

                if schema_format == "api":
                    schema = {
                        f"/api/{metadata['name']}": {
                            "post": {
                                "summary": metadata['description'],
                                "operationId": metadata["name"],
                                "requestBody": {
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "type": "object",
                                                "properties": metadata["request_model"].schema()["properties"]
                                            }
                                        }
                                    },
                                    "required": True
                                },
                                "responses": {
                                    "200": {
                                        "description": "Successful Response",
                                        "content": {
                                            "application/json": {
                                                "schema": {
                                                    "type": "object"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                else:
                    schema = {
                        "type": "function",
                        "function": {
                            "name": metadata["name"],
                            "description": metadata["description"],
                            "parameters": metadata["request_model"].schema(),
                        }
                }
                self._function_schemas.append(schema)

    def run(self, function_name: str, arguments: dict) -> BaseResponse:
        logger.info(f"Find and run function [{function_name}]")

        func = self._function_by_name.get(function_name, None)
        if func:
            return func(self._parse_request_obj(func, arguments))
        else:
            return BaseResponse(success=False, error=f"Unknown function: {function_name}")

    @property
    def function_names(self):
        return self._function_by_name.keys()

    @property
    def schema(self) -> List[Dict[str, Any]]:
        return self._function_schemas

    def _parse_request_obj(self, func, arguments: dict):
        metadata = getattr(func, "function_metadata")
        request_model = metadata["request_model"]
        return request_model.parse_obj(arguments)
