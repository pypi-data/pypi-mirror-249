# -*- coding: utf-8 -*-
"""Prometheus metrics."""
import prometheus_client

METRICS_PORT = 8088


def setupRobotMetrics() -> None:
    """Set up Prometheus client and start metrics endpoint."""
    prometheus_client.start_http_server(METRICS_PORT)


def collectRobotMetrics() -> bytes:
    """Collect Prometheus metrics in text format."""
    return prometheus_client.generate_latest()
