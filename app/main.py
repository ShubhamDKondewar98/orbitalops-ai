
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
import asyncio
from app.telemetry.background_task import run_telemetry_loop
from app.api import health_routes, telemetry_routes, alerts_routes, approval_routes, reports_routes


app = FastAPI(title="OrbitalOps AI")

app.include_router(health_routes.router)
app.include_router(telemetry_routes.router)
app.include_router(alerts_routes.router)
app.include_router(approval_routes.router)
app.include_router(reports_routes.router)

background_task_handle: asyncio.Task | None = None


@app.post("/simulation/start")
async def start_simulation():
    global background_task_handle

    if background_task_handle is not None and not background_task_handle.done():
        return {"status": "already_running"}

    background_task_handle = asyncio.create_task(run_telemetry_loop())
    return {"status": "started"}


@app.post("/simulation/stop")
async def stop_simulation():
    global background_task_handle

    if background_task_handle is None or background_task_handle.done():
        return {"status": "not_running"}

    background_task_handle.cancel()
    return {"status": "stopped"}




