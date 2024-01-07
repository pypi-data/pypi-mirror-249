import asyncio
import json
import os

from flockserve.flockserver import Flockserve
from flockserve.worker_manager import Worker_manager
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse, StreamingResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from flockserve.loadbalancer import Standard_LB
import uvicorn

class Flockserve_app:
    def __init__(self, config):
        self.app = FastAPI()
        self.config = config
        self.worker_manager = Worker_manager([], self.config)
        self.server = Flockserve(self.worker_manager, config=self.config, load_balancer=Standard_LB([], self.config))

        FastAPIInstrumentor.instrument_app(self.app)
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.config.SKYPILOT_SERVIC_ACC_KEYFILE
        @self.app.on_event("startup")
        async def on_startup():
            await self.server.init_session()
            await self.worker_manager.start_skypilot_worker(worker_id=0, reinit=False)
            asyncio.create_task(self.worker_manager.periodic_load_check())
            asyncio.create_task(self.worker_manager.periodic_worker_check())

        @self.app.on_event("shutdown")
        async def on_shutdown():
            await self.server.close_session()
            for worker in self.worker_manager.worker_handlers:
                await self.worker_manager.terminate_worker(worker)

        @self.app.post("/generate", response_class=PlainTextResponse)
        async def generate_code(request: Request):
            data = await request.body()
            headers = request.headers
            stream = json.loads(data.decode('utf-8')).get('parameters', {}).get('stream', False)
            if stream:
                return StreamingResponse(self.server.handle_stream_request(data, headers), media_type="text/plain")
            else:
                try:
                    return await self.server.handle_inference_request(data, headers, "/generate")
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Error during processing: {e}")

    def run(self):
        uvicorn.run(self.app, host=self.config.HOST, port=self.config.PORT, timeout_keep_alive=5)

# Usage
if __name__ == "__main__":
    app = Flockserve_app()
    app.run()
