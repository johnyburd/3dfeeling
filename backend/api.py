from random import uniform

from aiohttp import web
from aiohttp.web import Request, Response


routes = web.RouteTableDef()


@routes.post('/analyze')
async def analyze(request: Request) -> Response:
    data = await request.post()
    print(data)
    return web.json_response({'data': 'james is dum'})


@routes.get('/example')
async def example(request: Request) -> Response:
    gen = (round(uniform(0, 100), 1) for _ in range(3))
    return web.json_response(
        {'valence': next(gen), 'arousal': next(gen), 'dominance': next(gen)})


app = web.Application()
app.add_routes(routes)
web.run_app(app, host='0.0.0.0', port=3999)
