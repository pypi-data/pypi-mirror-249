import json
from typing import Optional
from logging import getLogger

import time



class TokenFileOrganizer:
    def __init__(self, filename: str, load_on_init: bool = True) -> None:
        self.TIMESTAMP_STR = "_added_date"
        self.TOKEN_VALID_DURATION_EPOCH = 60 * 60 * 24 * 30

        self.filename = filename
        self.logger = getLogger(__name__)

        self.tokens: list[dict[str, str]] = []
        if load_on_init:
            self.load()

    def load(self) -> None:
        try:
            with open(self.filename) as f:
                self.tokens = json.load(f)
        except FileNotFoundError:
            pass
        self.logger.info(f"Token file loaded: {self.filename}, length {len(self.tokens)}")

    def write(self) -> None:
        with open(self.filename, "w") as outfile:
            outfile.write(json.dumps(self.tokens))
        self.logger.info(f"Token file write succeed: {self.filename}")

    def add(self, token: dict[str, str]) -> None:
        token[self.TIMESTAMP_STR] = str(time.time())
        self.tokens.append(token)
        self.logger.info(f"Token added: ", token.__str__())

    def elimination(self) -> None:
        current_time = time.time()
        eliminate_before_time = current_time - self.TOKEN_VALID_DURATION_EPOCH
        self.logger.info(f"Token elimination started: length before elimination {len(self.tokens)}, eliminate before time {eliminate_before_time}")
        self.tokens = [t for t in self.tokens if float(t[self.TIMESTAMP_STR]) >= eliminate_before_time]
        self.logger.info(f"Token elimination finished: length after elimination {len(self.tokens)}")
