# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tabella']

package_data = \
{'': ['*'],
 'tabella': ['static/*',
             'templates/*',
             'templates/modals/*',
             'templates/modals/auth/*',
             'templates/monitor/*',
             'templates/schema/*',
             'templates/schema_form/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'case-switcher>=1.3.13,<2.0.0',
 'httpx>=0.26.0,<0.27.0',
 'lorem-pysum>=1.4.3,<2.0.0',
 'openrpc>=10.1.2,<11.0.0',
 'openrpcclientgenerator>=0.47.0,<0.48.0',
 'pydantic>=2.4.0,<3.0.0',
 'starlette>=0.34.0,<0.35.0',
 'uvicorn>=0.25.0,<0.26.0']

setup_kwargs = {
    'name': 'tabella',
    'version': '2.1.2',
    'description': 'Open-RPC API hosting and interactive documentation.',
    'long_description': '# Tabella\n\n![](https://img.shields.io/badge/License-ApacheV2-blue.svg)\n![](https://img.shields.io/badge/code%20style-black-000000.svg)\n![](https://img.shields.io/pypi/v/tabella.svg)\n\n## Open-RPC development framework with builtin interactive documentation.\n\n![Demo](https://gitlab.com/mburkard/tabella/-/raw/main/docs/demo.png)\n\n## Live Demo\n\nA live demo is available [here](https://tabella.burkard.cloud/).\n\n## Install\n\nTabella is on PyPI and can be installed with:\n\n```shell\npip install tabella\n```\n\nOr with [Poetry](https://python-poetry.org/)\n\n```shell\npoetry add tabella\n```\n\n## Python OpenRPC Docs\n\nThe RPC server hosted and documented by Tabella is powered\nby [Python OpenRPC](https://gitlab.com/mburkard/openrpc). Refer to the Python OpenRPC\ndocs hosted [here](https://python-openrpc.burkard.cloud/) for advanced use.\n\n## Getting Started\n\nA basic Tabella app:\n\n```python\nfrom tabella import Tabella\n\napp = Tabella()\n\n\n@app.method()\ndef echo(a: str, b: float) -> tuple[str, float]:\n    """Echo parameters back in result."""\n    return a, b\n\n\nif __name__ == "__main__":\n    app.run()\n```\n\nRun this, then open http://127.0.0.1:8000/ in your browser to use the interactive\ndocumentation.\n\nThe Open-RPC API will be hosted over HTTP on `http://127.0.0.1:8000/api` and over\nWebSockets on `ws://127.0.0.1:8000/api`.\n\n## Further Usage\n\n### Routers\n\nAn app with many modules can be organized into segments\nusing [Method Routers](https://python-openrpc.burkard.cloud/method_routers).\n\n### Security and Depends Arguments\n\nTabella passes request headers to the RPCServer process request methods. Details on\nusage can be found in the Python OpenRPC docs on\n[Depends Arguments](https://python-openrpc.burkard.cloud/security).\n\n### Set Servers\n\nSet RPC servers manually to specify transport and paths to host the RPC server on, e.g.\n\n```python\nfrom openrpc import Server\nfrom tabella import Tabella\n\napp = Tabella(\n    servers=[\n        Server(name="HTTP API", url="http://localhost:8000/my/api/path"),\n        Server(name="WebSocket API", url="ws://localhost:8000/my/api/path"),\n    ]\n)\n```\n\nThis app will host the RPCServer over HTTP and over WebSockets with the\npath `/my/api/path`.\n\n### Pydantic\n\n[Pydantic](https://docs.pydantic.dev/latest/) is used for request/response\ndeserialization/serialization as well as schema generation. Pydantic should be used for\nany models as seen here in\nthe [Python OpenRPC Docs](https://python-openrpc.burkard.cloud/basics#pydantic-for-data-models).\n\n### Starlette\n\nTabella HTTP and WebSocket server hosting uses [Starlette](https://www.starlette.io/).\n[Uvicorn](https://www.uvicorn.org/) can be used to run the starlette app.\n\n```shell\nuvicorn main:app.starlette --reload\n```\n\n## Monitor\n\nIf you are running the app with in debug mode, e.g. `app = Tabella(debug=True)`, then at\nthe path `/monitor` there is a display that will show requests and responses made to the\nRPC server as they happen.\n\n![Monitor](https://gitlab.com/mburkard/tabella/-/raw/main/docs/monitor_demo.png)\n\n## Inspired By\n\n- [OPEN-RPC Playground](https://playground.open-rpc.org/)\n- [Swagger](https://swagger.io/)\n- [Redoc](https://github.com/Redocly/redoc)\n\n## Support The Developer\n\n<a href="https://www.buymeacoffee.com/mburkard" target="_blank">\n  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png"\n       width="217"\n       height="60"\n       alt="Buy Me A Coffee">\n</a>\n',
    'author': 'Matthew Burkard',
    'author_email': 'matthewjburkard@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/mburkard/tabella',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
