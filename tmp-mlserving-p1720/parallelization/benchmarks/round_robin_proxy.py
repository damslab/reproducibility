import asyncio
import itertools

import aiohttp
from aiohttp import web


class RoundRobinProxy:

    def __init__(self, target_ports):
        self.target_ports = target_ports
        self.port_cycle = itertools.cycle(self.target_ports)

    async def handle_request(self, request):
        target_port = next(self.port_cycle)
        target_url = f"http://localhost:{target_port}{request.path_qs}"

        async with aiohttp.ClientSession() as session:
            try:
                # Forward the request
                async with session.request(
                        method=request.method,
                        url=target_url,
                        headers=request.headers,
                        data=request.content,
                ) as response:
                    # Start sending the response
                    resp = web.StreamResponse(status=response.status,
                                              headers=response.headers)
                    await resp.prepare(request)

                    # Stream the response content
                    async for chunk in response.content.iter_any():
                        await resp.write(chunk)

                    await resp.write_eof()
                    return resp

            except Exception as e:
                return web.Response(text=f"Error: {str(e)}", status=500)


async def main(args):
    server_ports = []
    for i in range(args.num_servers):
        port = 8100 + i * 100
        server_ports.append(port)
    print(f"Starting {args.num_servers} servers on ports {server_ports}")
    proxy = RoundRobinProxy(server_ports)
    app = web.Application()
    app.router.add_route('*', '/{path:.*}', proxy.handle_request)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8000)
    await site.start()

    print("Proxy server started on http://localhost:8000")

    # Keep the server running
    await asyncio.Event().wait()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_servers', type=int, default=2,
                       help='Number of backend servers to load balance between')
    args = parser.parse_args()
    asyncio.run(main(args))

