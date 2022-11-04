# Copyright 2022 Mike Shoup
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
import time
from datetime import datetime

import prometheus_client
import pyemvue


def main():
    loglevel = os.getenv("EMVUE_EXPORTER_LOG_LEVEL", "INFO")
    logging.basicConfig(
        format="%(asctime)s %(message)s", level=getattr(logging, loglevel.upper())
    )

    vue = pyemvue.PyEmVue()
    vue.login(
        os.getenv("EMVUE_EXPORTER_USERNAME"),
        os.getenv("EMVUE_EXPORTER_PASSWORD"),
    )

    port = os.getenv("EMVUE_EXPORTER_PORT", 10110)
    prometheus_client.start_http_server(port)

    collectors = register_prometheus_collectors()

    while True:
        set_prometheus_values(collectors, vue)
        time.sleep(os.getenv("EMVUE_EXPORTER_POLL_DELAY", 60))


def register_prometheus_collectors():
    collectors = {}

    collectors["device_energy_kwh"] = prometheus_client.Gauge(
        "emvue_device_energy_kwh",
        "Energy Usage for device",
        ["device_name", "channel_name"],
    )

    return collectors


def set_prometheus_values(collectors, vue_client):
    data = get_data(vue_client)

    logging.info(data)

    for device, channels in data.items():
        for channel, usage in channels.items():
            collectors["device_energy_kwh"].labels(
                device_name=device, channel_name=channel
            ).set(usage)


def get_data(vue_client):
    result = {}

    for device in vue_client.get_devices():
        if device.device_name == "":
            continue

        result[device.device_name] = {}

        usage = vue_client.get_device_list_usage(
            deviceGids=[device.device_gid],
            instant=datetime.utcnow(),
            scale=pyemvue.enums.Scale.MINUTE.value,
            unit=pyemvue.enums.Unit.KWH.value,
        )[device.device_gid]

        for item in usage.channels.items():
            channel = item[1]
            if channel.usage is not None:
                result[device.device_name][channel.name] = channel.usage

    return result
