# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-08 11:07:25
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Network communication methods.
"""


from __future__ import annotations
from typing import Any, Generator, Union
from queue import Queue
from psutil import Process
from scapy.packet import Packet
from scapy.sendrecv import sniff as scapy_sniff
from reytool.rsystem import search_process
from reytool.rwrap import wrap_thread


__all__ = (
    "sniff_generator",
)


def sniff_generator(process: Union[int, str]) -> Generator[bytes, Any, None]:
    """
    Sniff process communication bytes data, return generator.

    Parameters
    ----------
    process : Process name or ID.
        - `str` : Process name.
        - `int` : Process ID.

    Returns
    -------
    Generator of process communication bytes data.
    """

    # Search process.
    if process.__class__ == int:
        processes = search_process(id_=process)
    elif process.__class__ == str:
        processes = search_process(name=process)

    # Check.
    if processes == []:
        raise ValueError("Process not found")

    # Get addr.
    process: Process = processes[0]
    addrs = [
        {
            "host": connection.laddr.ip,
            "port": connection.laddr.port
        }
        for connection in process.connections()
    ]

    # Sniff.
    filter = " || ".join(
        [
            "host %s port %s" % (
                row["host"],
                row["port"]
            )
            for row in addrs
        ]
    )
    queue: Queue[Packet] = Queue()
    fund_put_queue = lambda packet: queue.put(packet.lastlayer().original)
    wrap_thread(
        scapy_sniff,
        store=False,
        filter=filter,
        prn=fund_put_queue
    )

    # Generate.
    while True:
        packet = queue.get()
        yield packet