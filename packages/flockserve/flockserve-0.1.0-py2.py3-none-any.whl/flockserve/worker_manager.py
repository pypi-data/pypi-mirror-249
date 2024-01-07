"""Module for monitoring and managing worker processes."""
import asyncio
from typing import List
from flockserve.worker_handler import Worker_handler
from flockserve.config import Config
import time
import sky
import aiohttp
import multiprocessing
import logging



class Worker_manager():
    def __init__(self, worker_handlers: List[Worker_handler], config: Config):
        self.worker_handlers = worker_handlers
        self.config = config

        if hasattr(config, 'LOG_FILE'):
            logging.basicConfig(level=logging.INFO, filename=config.LOG_FILE)
        else:
            logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)


    async def start_skypilot_worker(self, worker_id, worker_type='skypilot', reinit=False):
        worker_name = self.config.WORKER_NAME_PREFIX + '-' + str(worker_id)

        if Worker_manager.is_worker_exists(worker_name):
            await self.start_skypilot_worker(worker_id + 1)
        else:
            self.launcher_sub_process = multiprocessing.Process(target=Worker_manager.launch_task_process, args=(
            worker_name, self.config.SKYPILOT_JOB_FILE, reinit))

            self.worker_handlers.append(
                Worker_handler(worker_name, worker_type, self.config.WORKER_CAPACITY, queue=0, is_initializing=True,
                               healthy=False))

            return self.launcher_sub_process.start()

    @staticmethod
    def launch_task_process(worker_name, skypilot_job_file, reinit):
        if reinit:
            sky.cancel(cluster_name=worker_name, all=True)
        try:
            task = sky.Task.from_yaml(skypilot_job_file)
            if Worker_manager.is_any_running_jobs(worker_name):
                self.logger.info("Job already running, skipping launch.")
            else:
                sky.launch(task, cluster_name=worker_name, retry_until_up=True)
        except Exception as e:
            self.logger.info("Error:", e)

    async def terminate_worker(self, worker_handler: Worker_handler):
        self.logger.info(f"Terminating worker at {worker_handler.base_url}")

        if worker_handler.worker_type == 'local' and hasattr(worker_handler, 'handle'):
            worker_handler.handle.terminate()
            worker_handler.handle.wait()
        elif worker_handler.worker_type == 'skypilot':
            sky.down(cluster_name=worker_handler.worker_name, purge=True)

    @staticmethod
    async def is_finished_initializing(worker_handler: Worker_handler):
        cluster_statuses = sky.status(cluster_names=None, refresh=False)
        cluster_status = next((x for x in cluster_statuses if x['name'] == worker_handler.worker_name), None)

        # Head IP only exists for the workers that have initialization completed.
        if cluster_status and isinstance(cluster_status.get('handle', {}).head_ip, str):
            return True
        else:
            return False

    @staticmethod
    async def is_worker_healthy(worker_handler: Worker_handler):
        if worker_handler.base_url is None:
            return False

        async with worker_handler.session.get(f"{worker_handler.base_url}/health") as response:
            if response.status != 200:
                return False

        return True

    @staticmethod
    def is_worker_exists(worker_name):
        return len(sky.status(cluster_names=worker_name, refresh=False)) != 0

    @staticmethod
    def is_worker_available(worker_name):
        return worker_name.capacity - worker_name.queue > 0 and not worker_name.is_initializing

    @staticmethod
    def is_any_running_jobs(worker_name):
        if not Worker_manager.is_worker_exists(worker_name):
            return False
        else:
            skypilot_job_queue = sky.queue(cluster_name=worker_name)
            return next((True for job in skypilot_job_queue if job.get('status').value == 'RUNNING'), False)

    @staticmethod
    async def setup_initialized_worker(worker_handler: Worker_handler, port):
        if await Worker_manager.is_finished_initializing(worker_handler):
            # Set base_url
            cluster_statuses = sky.status(cluster_names=None, refresh=False)
            cluster_status = next((x for x in cluster_statuses if x['name'] == worker_handler.worker_name), None)
            worker_handler.base_url = "http://" + cluster_status['handle'].head_ip + f":{port}"

            # Setup session
            worker_handler.session = aiohttp.ClientSession(base_url=worker_handler.base_url)

    async def periodic_load_check(self):
        while True:
            try:
                worker_load = sum([w.queue for w in self.worker_handlers])
                live_worker_count = sum([not (w.is_initializing) for w in self.worker_handlers])
                self.logger.info(
                    f"Workers: {len(self.worker_handlers)}, "
                    f"Workers Live: {live_worker_count}, "
                    f"Worker Load: {worker_load}")
            except:
                self.logger.info("Error in periodic_load_check")

            await asyncio.sleep(20)

    async def periodic_worker_check(self):
        while True:
            for worker in list(self.worker_handlers):

                if worker.is_initializing:
                    if await Worker_manager.is_finished_initializing(worker):
                        worker.is_initializing = False
                        await Worker_manager.setup_initialized_worker(worker, self.config.PORT)

                        self.logger.info(
                            f"Worker: {worker.worker_name} , initialization and setup completed: {worker.base_url}")

                else:
                    if await Worker_manager.is_worker_healthy(worker):
                        self.logger.info(f"Healthy Worker: {worker.worker_name} ")
                        worker.healthy = True
                    else:
                        self.logger.info(f"!!UNHEALTHY!! Worker: {worker.worker_name} ")
                        worker.healthy = False

                await asyncio.sleep(20)
