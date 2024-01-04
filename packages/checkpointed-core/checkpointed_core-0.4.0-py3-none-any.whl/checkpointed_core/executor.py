import asyncio
import logging

from .handle import PipelineStepHandle
from .instructions import Instruction, Start, Sync
from .store import ResultStore


class TaskExecutor:

    def __init__(self, instructions: list[Instruction], *, loop=None):
        self._loop = loop if loop is not None else asyncio.get_event_loop()
        self._pending: list[Start] = []
        self._blocked: list[Sync] = []
        for instruction in instructions:
            if isinstance(instruction, Start):
                self._pending.append(instruction)
            elif isinstance(instruction, Sync):
                self._blocked.append(instruction)
            else:
                raise NotImplementedError(f"Instruction {instruction} is not supported")
        self._active = set()
        self._done = set()

    def run(self,
            result_store: ResultStore,
            config_by_step: dict[PipelineStepHandle, dict],
            logger: logging.Logger) -> None:
        self._loop.run_until_complete(self._run(result_store, config_by_step, logger))

    async def _run(self,
                   result_store: ResultStore,
                   config_by_step: dict[PipelineStepHandle, dict],
                   logger: logging.Logger):
        while self._pending or self._blocked or self._active:
            self._unblock_tasks(logger)
            self._start_pending_tasks(result_store, config_by_step, logger)
            done, self._active = await asyncio.wait(self._active, return_when=asyncio.FIRST_COMPLETED)
            for data in done:
                result, handle, factory = data.result()
                logger.info(f'Task {handle} finished')
                self._done.add(handle)

    def _unblock_tasks(self, logger: logging.Logger):
        for task in self._blocked.copy():
            if task.steps <= self._done:
                logger.info(f"Unblocking {len(task.then)} tasks")
                self._blocked.remove(task)
                self._pending.extend(task.then)

    def _start_pending_tasks(self,
                             result_store: ResultStore,
                             config_by_step: dict[PipelineStepHandle, dict],
                             logger: logging.Logger):
        while self._pending:
            task = self._pending.pop()
            logger.info(f"Starting pending task {task.step}")
            args = {}
            for handle, factory, name in task.inputs:
                logger.info(f'Loading input {name} ({handle}, type {factory.__name__}) for task {task.step}')
                args[name] = result_store.retrieve(handle, factory)
            instance = task.factory(config_by_step[task.step])

            async def wrapper(_handle=task.step,
                              _factory=task.factory,
                              _instance=instance,
                              _inputs=tuple(args.items())):
                logger.info(f'[{_handle}] Running task')
                if result_store.have_checkpoint_for(_handle):
                    logger.info(f'[{_handle}] Loading result from checkpoint')
                    result = result_store.retrieve(_handle, _factory)
                else:
                    logger.info(f'[{_handle}] Executing step')
                    result = await _instance.execute(**dict(_inputs))
                    logger.info(f'[{_handle}] Storing result')
                    result_store.store(_handle,
                                       _factory,
                                       result,
                                       _instance.get_checkpoint_metadata())
                logger.info(f'[{_handle}] Finished task')
                return result, _handle, _factory

            self._active.add(asyncio.Task(wrapper(), loop=self._loop))
