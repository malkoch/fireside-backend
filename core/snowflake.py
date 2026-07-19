import datetime
import threading


class SnowflakeGenerator:
    EPOCH = int(datetime.datetime(2026, 7, 18, 23, 59, 59, 999).timestamp() * 1000)

    WORKER_ID_BITS = 10
    SEQUENCE_BITS = 12

    MAX_WORKER_ID = (1 << WORKER_ID_BITS) - 1
    MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1

    WORKER_ID_SHIFT = SEQUENCE_BITS
    TIMESTAMP_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS

    def __init__(self, worker: int):
        if not (0 <= worker <= self.MAX_WORKER_ID):
            raise ValueError(f"Worker ID must be between 0 and {self.MAX_WORKER_ID}")

        self.worker = worker
        self.sequence = 0
        self.last_timestamp = -1
        self.lock = threading.Lock()

    def _current_timestamp(self):
        return int(datetime.datetime.utcnow().timestamp() * 1000)

    def _wait_next_millis(self, last_timestamp):
        timestamp = self._current_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._current_timestamp()
        return timestamp

    def generate(self):
        with self.lock:
            timestamp = self._current_timestamp()

            if timestamp < self.last_timestamp:
                raise RuntimeError("Clock moved backwards. Refusing to generate id for {} milliseconds".format(self.last_timestamp - timestamp))

            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & self.MAX_SEQUENCE

                if self.sequence == 0:
                    timestamp = self._wait_next_millis(self.last_timestamp)
            else:
                self.sequence = 0

            self.last_timestamp = timestamp

            return (
                    ((timestamp - self.EPOCH) << self.TIMESTAMP_SHIFT)
                    | (self.worker << self.WORKER_ID_SHIFT)
                    | self.sequence
            )


def generator(worker):
    gen = SnowflakeGenerator(worker)

    return lambda: gen.generate()
