from os import path
from typing import Callable
from pathlib import Path
import random
from image.image_generator import SingleSourceImageGenerator
import multiprocessing


class SequenceGenerator:

    def __init__(
            self,
            sequence_length,
            image_generator_factory: Callable,
            workers: int,
            output_directory: str,
            output_prefix: str,
            extension: str,
            smoothing: bool = False
    ):
        self.sequence_length = sequence_length
        self.output_prefix = output_prefix
        self.output_directory = output_directory
        self.image_generator_factory = image_generator_factory
        self.workers = workers
        self.extension = extension
        self.smoothing = smoothing

    def run_worker(self, worker_id: int, count: int):
        image_generator: SingleSourceImageGenerator = self.image_generator_factory()
        image_generator.build()
        for i in range(1, count + 1):
            image_generator.generate_output(
                path.join(self.output_directory, f'{self.output_prefix}.{worker_id}.{i}.{self.extension}')
            )

            if self.smoothing:
                image_generator.shift_slices()
            else:
                if bool(random.getrandbits(1)):
                    image_generator.shift_slices()
                else:
                    image_generator.randomize()

    def generate(self):
        Path(self.output_directory).mkdir(parents=True, exist_ok=True)

        remainder = self.sequence_length % self.workers

        processes = []

        for i in range(0, self.workers):
            count_for_worker = self.sequence_length // self.workers
            if i == self.workers - 1:
                count_for_worker += remainder

            child_process = multiprocessing.Process(target=self.run_worker, args=(i, count_for_worker))
            child_process.start()
            processes.append(child_process)

        for process in processes:
            process.join()
