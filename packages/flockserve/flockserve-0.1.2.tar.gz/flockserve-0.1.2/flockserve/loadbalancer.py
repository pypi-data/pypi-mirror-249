"""Module for load balancing logics"""
import asyncio
from flockserve.worker_manager import Worker_manager
from flockserve.worker_handler import Worker_handler


class Load_balancer():
    """
    Base class for load balancer
    """
    def __init__(self, worker_manager:Worker_manager, config):
        self.worker_manager = worker_manager
        self.config = config

    async def select_worker(self) -> Worker_handler:
        raise NotImplementedError


class Standard_LB(Load_balancer):
    """
    Selects the worker with the least queue length
    """
    def __init__(self, worker_manager, config):
        super().__init__(worker_manager, config)

    async def select_worker(self) -> Worker_handler:
        while True:
            available_workers = [worker for worker in self.worker_manager.worker_handlers if Worker_manager.is_worker_available(worker)]
            if available_workers:
                selected_worker = min(available_workers, key=lambda w: w.queue)
                break
            await asyncio.sleep(1)
        return selected_worker
