from aiohttp import web
from aiohttp.web import Request, Response


routes = web.RouteTableDef()


@routes.post('/analyze')
async def analyze(request: Request) -> Response:
    data = await request.post()
    print(data)
    return web.json_response({'data': 'james is dum'})

app = web.Application()
app.add_routes(routes)
web.run_app(app)
