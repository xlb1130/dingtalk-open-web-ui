import json

def parse_openapi_json(base_url: str, original_json):
    if isinstance(original_json, str):
        original_json = json.loads(original_json)
    target_json_array = []

    for path, methods in original_json["paths"].items():
        for method, details in methods.items():
            operation_id = details.get("operationId")
            summary = details.get("summary")
            description = details.get("description")

            # Construct the URL based on the path
            url = f"{base_url}{path}"

            # Extract parameters from the request body schema
            parameters = {}
            if "requestBody" in details:
                schema_ref = details["requestBody"]["content"]["application/json"]["schema"].get("$ref")
                if schema_ref:
                    schema_name = schema_ref.split("/")[-1]
                    schema = original_json["components"]["schemas"].get(schema_name)
                    if schema:
                        parameters = {
                            "type": "object",
                            "properties": schema.get("properties", {})
                        }

            # Create the target JSON object
            target_json = {
                "name": operation_id,
                "url": url,
                "type": "function",
                "description": description,
                "parameters": parameters
            }

            target_json_array.append(target_json)

    return target_json_array

# Example usage
openapi_json = """
{
    "openapi": "3.1.0",
    "info": {
        "title": "mcp-server/amap-maps",
        "description": "mcp-server/amap-maps MCP Server",
        "version": "0.1.0"
    },
    "servers": [
        {
            "url": "/amap-maps"
        }
    ],
    "paths": {
        "/maps_regeocode": {
            "post": {
                "summary": "Maps Regeocode",
                "description": "将一个高德经纬度坐标转换为行政区划地址信息",
                "operationId": "tool_maps_regeocode_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/maps_regeocode_form_model"
                            }
                        }
                    },
                    "required": true
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/maps_geo": {
            "post": {
                "summary": "Maps Geo",
                "description": "将详细的结构化地址转换为经纬度坐标。支持对地标性名胜景区、建筑物名称解析为经纬度坐标",
                "operationId": "tool_maps_geo_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/maps_geo_form_model"
                            }
                        }
                    },
                    "required": true
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/maps_ip_location": {
            "post": {
                "summary": "Maps Ip Location",
                "description": "IP 定位根据用户输入的 IP 地址，定位 IP 的所在位置",
                "operationId": "tool_maps_ip_location_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/maps_ip_location_form_model"
                            }
                        }
                    },
                    "required": true
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/maps_weather": {
            "post": {
                "summary": "Maps Weather",
                "description": "根据城市名称或者标准adcode查询指定城市的天气",
                "operationId": "tool_maps_weather_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/maps_weather_form_model"
                            }
                        }
                    },
                    "required": true
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/maps_search_detail": {
            "post": {
                "summary": "Maps Search Detail",
                "description": "查询关键词搜或者周边搜获取到的POI ID的详细信息",
                "operationId": "tool_maps_search_detail_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/maps_search_detail_form_model"
                            }
                        }
                    },
                    "required": true
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/maps_bicycling": {
            "post": {
                "summary": "Maps Bicycling",
                "description": "骑行路径规划用于规划骑行通勤方案，规划时会考虑天桥、单行线、封路等情况。最大支持 500km 的骑行路线规划",
                "operationId": "tool_maps_bicycling_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/maps_bicycling_form_model"
                            }
                        }
                    },
                    "required": true
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/maps_direction_walking": {
            "post": {
                "summary": "Maps Direction Walking",
                "description": "步行路径规划 API 可以根据输入起点终点经纬度坐标规划100km 以内的步行通勤方案，并且返回通勤方案的数据",
                "operationId": "tool_maps_direction_walking_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/maps_direction_walking_form_model"
                            }
                        }
                    },
                    "required": true
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/maps_direction_driving": {
            "post": {
                "summary": "Maps Direction Driving",
                "description": "驾车路径规划 API 可以根据用户起终点经纬度坐标规划以小客车、轿车通勤出行的方案，并且返回通勤方案的数据。",
                "operationId": "tool_maps_direction_driving_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/maps_direction_driving_form_model"
                            }
                        }
                    },
                    "required": true
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/maps_direction_transit_integrated": {
            "post": {
                "summary": "Maps Direction Transit Integrated",
                "description": "公交路径规划 API 可以根据用户起终点经纬度坐标规划综合各类公共（火车、公交、地铁）交通方式的通勤方案，并且返回通勤方案的数据，跨城场景下必须传起点城市与终点城市",
                "operationId": "tool_maps_direction_transit_integrated_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/maps_direction_transit_integrated_form_model"
                            }
                        }
                    },
                    "required": true
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/maps_distance": {
            "post": {
                "summary": "Maps Distance",
                "description": "距离测量 API 可以测量两个经纬度坐标之间的距离,支持驾车、步行以及球面距离测量",
                "operationId": "tool_maps_distance_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/maps_distance_form_model"
                            }
                        }
                    },
                    "required": true
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/maps_text_search": {
            "post": {
                "summary": "Maps Text Search",
                "description": "关键词搜，根据用户传入关键词，搜索出相关的POI",
                "operationId": "tool_maps_text_search_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/maps_text_search_form_model"
                            }
                        }
                    },
                    "required": true
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/maps_around_search": {
            "post": {
                "summary": "Maps Around Search",
                "description": "周边搜，根据用户传入关键词以及坐标location，搜索出radius半径范围的POI",
                "operationId": "tool_maps_around_search_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/maps_around_search_form_model"
                            }
                        }
                    },
                    "required": true
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "HTTPValidationError": {
                "properties": {
                    "detail": {
                        "items": {
                            "$ref": "#/components/schemas/ValidationError"
                        },
                        "type": "array",
                        "title": "Detail"
                    }
                },
                "type": "object",
                "title": "HTTPValidationError"
            },
            "ValidationError": {
                "properties": {
                    "loc": {
                        "items": {
                            "anyOf": [
                                {
                                    "type": "string"
                                },
                                {
                                    "type": "integer"
                                }
                            ]
                        },
                        "type": "array",
                        "title": "Location"
                    },
                    "msg": {
                        "type": "string",
                        "title": "Message"
                    },
                    "type": {
                        "type": "string",
                        "title": "Error Type"
                    }
                },
                "type": "object",
                "required": [
                    "loc",
                    "msg",
                    "type"
                ],
                "title": "ValidationError"
            },
            "maps_around_search_form_model": {
                "properties": {
                    "keywords": {
                        "type": "string",
                        "title": "Keywords",
                        "description": "搜索关键词"
                    },
                    "location": {
                        "type": "string",
                        "title": "Location",
                        "description": "中心点经度纬度"
                    },
                    "radius": {
                        "type": "string",
                        "title": "Radius",
                        "description": "搜索半径"
                    }
                },
                "type": "object",
                "required": [
                    "location"
                ],
                "title": "maps_around_search_form_model"
            },
            "maps_bicycling_form_model": {
                "properties": {
                    "origin": {
                        "type": "string",
                        "title": "Origin",
                        "description": "出发点经纬度，坐标格式为：经度，纬度"
                    },
                    "destination": {
                        "type": "string",
                        "title": "Destination",
                        "description": "目的地经纬度，坐标格式为：经度，纬度"
                    }
                },
                "type": "object",
                "required": [
                    "origin",
                    "destination"
                ],
                "title": "maps_bicycling_form_model"
            },
            "maps_direction_driving_form_model": {
                "properties": {
                    "origin": {
                        "type": "string",
                        "title": "Origin",
                        "description": "出发点经度，纬度，坐标格式为：经度，纬度"
                    },
                    "destination": {
                        "type": "string",
                        "title": "Destination",
                        "description": "目的地经度，纬度，坐标格式为：经度，纬度"
                    }
                },
                "type": "object",
                "required": [
                    "origin",
                    "destination"
                ],
                "title": "maps_direction_driving_form_model"
            },
            "maps_direction_transit_integrated_form_model": {
                "properties": {
                    "origin": {
                        "type": "string",
                        "title": "Origin",
                        "description": "出发点经度，纬度，坐标格式为：经度，纬度"
                    },
                    "destination": {
                        "type": "string",
                        "title": "Destination",
                        "description": "目的地经度，纬度，坐标格式为：经度，纬度"
                    },
                    "city": {
                        "type": "string",
                        "title": "City",
                        "description": "公共交通规划起点城市"
                    },
                    "cityd": {
                        "type": "string",
                        "title": "Cityd",
                        "description": "公共交通规划终点城市"
                    }
                },
                "type": "object",
                "required": [
                    "origin",
                    "destination",
                    "city",
                    "cityd"
                ],
                "title": "maps_direction_transit_integrated_form_model"
            },
            "maps_direction_walking_form_model": {
                "properties": {
                    "origin": {
                        "type": "string",
                        "title": "Origin",
                        "description": "出发点经度，纬度，坐标格式为：经度，纬度"
                    },
                    "destination": {
                        "type": "string",
                        "title": "Destination",
                        "description": "目的地经度，纬度，坐标格式为：经度，纬度"
                    }
                },
                "type": "object",
                "required": [
                    "origin",
                    "destination"
                ],
                "title": "maps_direction_walking_form_model"
            },
            "maps_distance_form_model": {
                "properties": {
                    "origins": {
                        "type": "string",
                        "title": "Origins",
                        "description": "起点经度，纬度，可以传多个坐标，使用竖线隔离，比如120,30|120,31，坐标格式为：经度，纬度"
                    },
                    "destination": {
                        "type": "string",
                        "title": "Destination",
                        "description": "终点经度，纬度，坐标格式为：经度，纬度"
                    },
                    "type": {
                        "type": "string",
                        "title": "Type",
                        "description": "距离测量类型,1代表驾车距离测量，0代表直线距离测量，3步行距离测量"
                    }
                },
                "type": "object",
                "required": [
                    "origins",
                    "destination"
                ],
                "title": "maps_distance_form_model"
            },
            "maps_geo_form_model": {
                "properties": {
                    "address": {
                        "type": "string",
                        "title": "Address",
                        "description": "待解析的结构化地址信息"
                    },
                    "city": {
                        "type": "string",
                        "title": "City",
                        "description": "指定查询的城市"
                    }
                },
                "type": "object",
                "required": [
                    "address"
                ],
                "title": "maps_geo_form_model"
            },
            "maps_ip_location_form_model": {
                "properties": {
                    "ip": {
                        "type": "string",
                        "title": "Ip",
                        "description": "IP地址"
                    }
                },
                "type": "object",
                "required": [
                    "ip"
                ],
                "title": "maps_ip_location_form_model"
            },
            "maps_regeocode_form_model": {
                "properties": {
                    "location": {
                        "type": "string",
                        "title": "Location",
                        "description": "经纬度"
                    }
                },
                "type": "object",
                "required": [
                    "location"
                ],
                "title": "maps_regeocode_form_model"
            },
            "maps_search_detail_form_model": {
                "properties": {
                    "id": {
                        "type": "string",
                        "title": "Id",
                        "description": "关键词搜或者周边搜获取到的POI ID"
                    }
                },
                "type": "object",
                "required": [
                    "id"
                ],
                "title": "maps_search_detail_form_model"
            },
            "maps_text_search_form_model": {
                "properties": {
                    "keywords": {
                        "type": "string",
                        "title": "Keywords",
                        "description": "搜索关键词"
                    },
                    "city": {
                        "type": "string",
                        "title": "City",
                        "description": "查询城市"
                    },
                    "types": {
                        "type": "string",
                        "title": "Types",
                        "description": "POI类型，比如加油站"
                    }
                },
                "type": "object",
                "required": [
                    "keywords"
                ],
                "title": "maps_text_search_form_model"
            },
            "maps_weather_form_model": {
                "properties": {
                    "city": {
                        "type": "string",
                        "title": "City",
                        "description": "城市名称或者adcode"
                    }
                },
                "type": "object",
                "required": [
                    "city"
                ],
                "title": "maps_weather_form_model"
            }
        }
    }
}
"""

if __name__ == "__main__":
    functions = parse_openapi_json(openapi_json)
    for func in functions:
        print(func)