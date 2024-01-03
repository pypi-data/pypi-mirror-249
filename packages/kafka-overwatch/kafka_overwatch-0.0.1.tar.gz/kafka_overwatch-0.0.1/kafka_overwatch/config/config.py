#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2024 John Mille <john@ews-network.net>

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kafka_overwatch.specs.config import KafkaOverwatchInputConfiguration

from tempfile import TemporaryDirectory

from dacite import from_dict
from prometheus_client import CollectorRegistry, multiprocess

from kafka_overwatch.monitoring.prometheus import (
    set_cluster_prometheus_registry_collectors,
)
from kafka_overwatch.specs.config import Global


class OverwatchConfig:
    """
    Class to store in-memory the clusters and their configurations, derived from the input configuration
    classes.
    """

    def __init__(
        self,
        config: KafkaOverwatchInputConfiguration,
        prometheus_dir: TemporaryDirectory,
    ):
        if not config.global_:
            config.global_ = from_dict(Global, {"ClusterScanIntervalInSeconds": 30})
        self._config = config
        self._prometheus_registry_dir = prometheus_dir

        self.prometheus_registry: CollectorRegistry = CollectorRegistry(
            auto_describe=True,
        )
        self.prometheus_collectors = set_cluster_prometheus_registry_collectors(
            self.prometheus_registry
        )
        multiprocess.MultiProcessCollector(
            self.prometheus_registry, path=self._prometheus_registry_dir.name
        )

    @property
    def input_config(self):
        return self._config

    @property
    def prometheus_registry_dir(self) -> TemporaryDirectory:
        return self._prometheus_registry_dir
