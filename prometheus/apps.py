import logging
import os
import typing as t
from contextlib import contextmanager

from django.apps import AppConfig
from django.conf import settings
from prometheus_client import Counter, push_to_gateway
from prometheus_client.registry import REGISTRY

logger = logging.getLogger(__name__)


class PrometheusConfig(AppConfig):
    name = "prometheus"


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class PrometheusManager(metaclass=Singleton):
    def __init__(self) -> None:
        self.metric_types = self._get_metric_types()

    def membership_request_fail(self, sender: t.Union[object, str], **kwargs) -> None:
        """
        :param sender: instance of a class, or a string description of who the sender is
        """
        counter = self.metric_types["counters"]["membership_request_fail"]
        self._increment_counter(counter=counter, increment_by=1, labels={})

    def membership_request_success(self, sender: t.Union[object, str], **kwargs) -> None:
        """
        :param sender: instance of a class, or a string description of who the sender is
        """
        counter = self.metric_types["counters"]["membership_request_success"]
        self._increment_counter(counter=counter, increment_by=1, labels={})

    def transaction_fail(self, sender: t.Union[object, str], **kwargs) -> None:
        """
        :param sender: instance of a class, or a string description of who the sender is
        """
        counter = self.metric_types["counters"]["transaction_fail"]
        self._increment_counter(counter=counter, increment_by=1, labels={})

    def transaction_success(self, sender: t.Union[object, str], **kwargs) -> None:
        """
        :param sender: instance of a class, or a string description of who the sender is
        """
        counter = self.metric_types["counters"]["transaction_success"]
        self._increment_counter(counter=counter, increment_by=1, labels={})

    def _increment_counter(self, counter: Counter, increment_by: t.Union[int, float], labels: t.Dict):
        with self._prometheus_push_manager(
            prometheus_push_gateway=settings.PROMETHEUS_PUSH_GATEWAY,
            prometheus_job=settings.PROMETHEUS_JOB,
        ):
            counter.inc(increment_by)
            if labels:
                counter.labels(**labels)

    @staticmethod
    def _get_metric_types() -> t.Dict:
        """
        Define metric types here (see https://prometheus.io/docs/concepts/metric_types/),
        with the name, description and a list of the labels they expect.
        """
        metric_types = {
            "counters": {
                "membership_request_fail": Counter(
                    name="membership_request_fail",
                    documentation="Incremental count of failed membership request saves",
                ),
                "membership_request_success": Counter(
                    name="membership_request_success",
                    documentation="Incremental count of successful membership request saves",
                ),
                "transaction_fail": Counter(
                    name="transaction_fail",
                    documentation="Incremental count of failed merchant transaction saves",
                ),
                "transaction_success": Counter(
                    name="transaction_success",
                    documentation="Incremental count of successful merchant transaction saves",
                ),
            },
        }

        return metric_types

    @staticmethod
    @contextmanager
    def _prometheus_push_manager(prometheus_push_gateway: str, prometheus_job: str):
        push_timeout = 3  # PushGateway should be running in the same pod
        grouping_key = {"pid": str(os.getpid())}

        try:
            yield
        finally:
            if settings.PUSH_PROMETHEUS_METRICS:
                logger.debug("Prometheus push manager started")
                try:
                    push_to_gateway(
                        gateway=prometheus_push_gateway,
                        job=prometheus_job,
                        registry=REGISTRY,
                        grouping_key=grouping_key,
                        timeout=push_timeout,
                    )
                except Exception as e:
                    logger.exception(str(e))
