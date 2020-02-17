from random import uniform

from aiohttp import web
from aiohttp.web import Request, Response
import aiohttp_cors

from object_generation import get_object
from utils import parse_from_bytes


routes = web.RouteTableDef()


@routes.post('/analyze')
async def analyze(request: Request) -> Response:
    data = await request.post()
    result = await get_object(data['text'])
    return web.json_response({
        'filename': result[0], 'points': result[1]})


@routes.post('/analyze-file')
async def analyze_file(request: Request) -> Response:
    data = await request.post()
    f = data['file'].file
    try:
        text = parse_from_bytes(f.read())
        result = await get_object(text)
        return web.json_response({
            'filename': result[0], 'points': result[1], 'text': text}, status=200)
    except ValueError as e:
        return web.json_response({'message': str(e)}, status=400)


@routes.get('/example')
async def example(request: Request) -> Response:
    gen = (round(uniform(0, 100), 1) for _ in range(3))
    return web.json_response(
        {'valence': next(gen), 'arousal': next(gen), 'dominance': next(gen)})


app = web.Application()
app.add_routes(routes)


# Configure default CORS settings.
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )
})

# Configure CORS on all routes.
for route in list(app.router.routes()):
    cors.add(route)

web.run_app(app, host='0.0.0.0', port=3999)
