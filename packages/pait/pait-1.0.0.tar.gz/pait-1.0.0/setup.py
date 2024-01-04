# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pait',
 'pait.app',
 'pait.app.any',
 'pait.app.any.plugin',
 'pait.app.any.security',
 'pait.app.base',
 'pait.app.base.adapter',
 'pait.app.base.security',
 'pait.app.flask',
 'pait.app.flask.adapter',
 'pait.app.flask.plugin',
 'pait.app.flask.security',
 'pait.app.sanic',
 'pait.app.sanic.adapter',
 'pait.app.sanic.plugin',
 'pait.app.sanic.security',
 'pait.app.starlette',
 'pait.app.starlette.adapter',
 'pait.app.starlette.plugin',
 'pait.app.starlette.security',
 'pait.app.tornado',
 'pait.app.tornado.adapter',
 'pait.app.tornado.plugin',
 'pait.app.tornado.security',
 'pait.extra',
 'pait.field',
 'pait.model',
 'pait.openapi',
 'pait.param_handle',
 'pait.plugin',
 'pait.util']

package_data = \
{'': ['*']}

install_requires = \
['any-api==0.1.0.9']

extras_require = \
{'all': ['redis>=4.2.2,<5.0.0'], 'redis': ['redis>=4.2.2,<5.0.0']}

setup_kwargs = {
    'name': 'pait',
    'version': '1.0.0',
    'description': 'Pait is a Python api tool. Pait enables your Python web framework to have type checking, parameter type conversion, interface document generation and can display your documents through Redoc or Swagger (power by inspect, pydantic)',
    'long_description': '![](https://cdn.jsdelivr.net/gh/so1n/so1n_blog_photo@master/blog_photo/1652600629491%E6%9C%AA%E5%91%BD%E5%90%8D.jpg)\n<p align="center">\n    Pait(π tool) - <em>Python Modern API Tools, easier to use web frameworks/write API routing</em>\n</p>\n<p align="center">\n    <a href="https://codecov.io/gh/so1n/pait" target="_blank">\n        <img src="https://codecov.io/gh/so1n/pait/branch/master/graph/badge.svg?token=NEVM1VODHR" alt="Coverage">\n    </a>\n</p>\n<p align="center">\n    <a href="https://pypi.org/project/pait/" target="_blank">\n        <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/pait">\n    </a>\n    <a href="https://pypi.org/project/pait/" target="_blank">\n        <img alt="PyPI" src="https://img.shields.io/pypi/v/pait">\n    </a>\n</p>\n<p align="center">\n    <a href="https://github.com/so1n/pait/actions?query=event%3Apush+branch%3Amaster" target="_blank">\n        <img alt="GitHub Workflow Status" src="https://img.shields.io/github/actions/workflow/status/so1n/pait/python-package.yml">\n    </a>\n    <a href="https://github.com/so1n/pait/releases" target="_blank">\n        <img alt="GitHub release (release name instead of tag name)" src="https://img.shields.io/github/v/release/so1n/pait?include_prereleases">\n    </a>\n    <a href="https://github.com/so1n/pait/actions?query=event%3Apush+branch%3Amaster" target="_blank">\n        <img src="https://github.com/so1n/pait/actions/workflows/python-package.yml/badge.svg?event=push&branch=master" alt="Test">\n    </a>\n</p>\n<p align="center">\n    <a href="https://github.com/so1n/pait/tree/master/example" target="_blank">\n        <img src="https://img.shields.io/badge/Support%20framework-Flask%2CSanic%2CStarlette%2CTornado-brightgreen" alt="Support framework">\n    </a>\n</p>\n\n\n---\n**Documentation**: [https://so1n.me/pait/](https://so1n.me/pait/)\n\n**中文文档**: [https://so1n.me/pait-zh-doc/](https://so1n.me/pait-zh-doc/)\n\n---\n\n# pait\n\nPait is an api tool that can be used in any python web framework, the features provided are as follows:\n- [x] Integrate into the Type Hints ecosystem to provide a safe and efficient API interface coding method.\n - [x] Automatic verification and type conversion of request parameters (depends on `Pydantic` and `inspect`, currently supports `Pydantic` V1 and V2 versions).\n - [x] Automatically generate openapi files and support UI components such as `Swagger`,`Redoc`,`RapiDoc` and `Elements`.\n - [x] TestClient support, response result verification of test cases。\n - [x] Plugin expansion, such as parameter relationship dependency verification, Mock response, etc.。\n - [x] gRPC GateWay (After version 1.0, this feature has been migrated to [grpc-gateway](https://github.com/python-pai/grpc-gateway))\n - [ ] Automated API testing\n - [ ] WebSocket support\n - [ ] SSE support\n\n> Note:\n>\n> - mypy check 100%\n>\n> - python version >= 3.8 (support postponed annotations)\n\n\n\n# Installation\n```Bash\npip install pait\n```\n\n# Simple Example\n```python\nfrom typing import Type\nimport uvicorn  # type: ignore\nfrom starlette.applications import Starlette\nfrom starlette.responses import JSONResponse\nfrom starlette.routing import Route\n\nfrom pait.app.starlette import pait\nfrom pait.field import Body\nfrom pait.openapi.doc_route import add_doc_route\nfrom pait.model.response import JsonResponseModel\nfrom pydantic import BaseModel, Field\n\n\nclass DemoResponseModel(JsonResponseModel):\n    """demo post api response model"""\n    class ResponseModel(BaseModel):\n        uid: int = Field()\n        user_name: str = Field()\n\n    description: str = "demo response"\n    response_data: Type[BaseModel] = ResponseModel\n\n\n@pait(response_model_list=[DemoResponseModel])\nasync def demo_post(\n    uid: int = Body.i(description="user id", gt=10, lt=1000),\n    user_name: str = Body.i(description="user name", min_length=2, max_length=4)\n) -> JSONResponse:\n    return JSONResponse({\'uid\': uid, \'user_name\': user_name})\n\n\napp = Starlette(routes=[Route(\'/api\', demo_post, methods=[\'POST\'])])\nadd_doc_route(app)\nuvicorn.run(app)\n```\nSee [documentation](https://so1n.me/pait/) for more features\n\n# Support Web framework\n\n| Framework | Description            |\n|-----------|------------------------|\n| Flask     | All features supported |\n| Sanic     | All features supported |\n| Starlette | All features supported |\n| Tornado   | All features supported |\n| Django    | Coming soon            |\n\n\nIf the web framework is not supported(which you are using).\n\nCan be modified sync web framework according to [pait.app.flask](https://github.com/so1n/pait/blob/master/pait/app/flask.py)\n\nCan be modified async web framework according to [pait.app.starlette](https://github.com/so1n/pait/blob/master/pait/app/starlette.py)\n\n# Performance\nThe main operating principle of `Pait` is to convert the function signature of the route function into `Pydantic Model` through the reflection mechanism when the program is started,\nand then verify and convert the request parameters through `Pydantic Model` when the request hits the route.\n\nThese two stages are all automatically handled internally by `Pait`.\nThe first stage only slightly increases the startup time of the program, while the second stage increases the response time of the routing, but it only consumes 0.00005(s) more than manual processing.\nThe specific benchmark data and subsequent optimization are described in [#27](https://github.com/so1n/pait/issues/27).\n\n# Example\nFor more complete examples, please refer to [example](https://github.com/so1n/pait/tree/master/example)\n',
    'author': 'So1n',
    'author_email': 'so1n897046026@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/so1n/pait',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
