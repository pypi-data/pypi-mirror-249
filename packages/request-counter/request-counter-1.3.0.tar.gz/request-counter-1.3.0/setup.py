#!/usr/bin/env python
import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name="request-counter",
        version="1.3.0",
        packages=[
            "request_counter",
            "request_counter/management/commands",
            "request_counter/migrations",
        ],
    )
