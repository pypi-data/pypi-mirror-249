#!/usr/bin/env python3
"""
ROS Bridge Prototype

This script provides a prototype for interfacing with ROS through rosbridge using websockets.

protocol specification:
https://github.com/RobotWebTools/rosbridge_suite/blob/ros2/ROSBRIDGE_PROTOCOL.md

Author: Jev Kuznetsov
Copyright (c) 2024 ROX Automation
"""

from __future__ import annotations

import json
import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Optional

import websockets

logger = logging.getLogger(__name__)


class Subscriber:
    """
    Represents a subscriber in ROS bridge communication.

    Attributes:
        websocket (websockets.WebSocketClientProtocol): The WebSocket connection to ROS bridge.
        topic (str): The ROS topic to subscribe to.
    """

    def __init__(self, websocket: websockets.WebSocketClientProtocol, topic: str):
        self.websocket = websocket
        self.topic = topic

    def __aiter__(self) -> Subscriber:
        """Returns itself as an asynchronous iterator."""
        return self

    async def __anext__(self) -> Any:
        """Asynchronously gets the next message from the subscribed topic."""
        msg = await self.websocket.recv()
        return json.loads(msg)


class Publisher:
    """
    Represents a publisher in ROS bridge communication.

    Attributes:
        websocket (websockets.WebSocketClientProtocol): The WebSocket connection to ROS bridge.
        topic (str): The ROS topic to publish to.
    """

    def __init__(self, websocket: websockets.WebSocketClientProtocol, topic: str):
        self.websocket = websocket
        self.topic = topic

    async def publish(self, msg: Any) -> None:
        """Publishes a message to the ROS topic."""
        message = json.dumps({"op": "publish", "topic": self.topic, "msg": msg})
        await self.websocket.send(message)


class ROS_Bridge:
    """
    Manages communication with ROS through rosbridge using websockets.

    Attributes:
        uri (str): URI for connecting to ROS bridge.
        websocket (Optional[websockets.WebSocketClientProtocol]): WebSocket connection.
    """

    def __init__(self, uri: str):
        self.uri = uri
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None

    async def connect(self) -> None:
        """Establishes the WebSocket connection to the ROS bridge."""
        try:
            if self.websocket is None:
                logger.info(f"Connecting to ROS bridge at {self.uri}")
                self.websocket = await websockets.connect(self.uri)
            else:
                logger.info("WebSocket connection already established")
        except Exception as e:
            logger.error(f"Failed to connect to ROS bridge: {e}")
            raise

    async def disconnect(self) -> None:
        """Closes the WebSocket connection."""
        try:
            if self.websocket:
                logger.info("Disconnecting from ROS bridge")
                await self.websocket.close()
                self.websocket = None
            else:
                logger.info("WebSocket connection already closed")

        except Exception as e:  # pylint: disable=broad-except
            logger.error(f"Failed to disconnect from ROS bridge: {e}")

    async def __aenter__(self) -> ROS_Bridge:
        """Asynchronously establish the connection when entering the context."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Asynchronously close the connection when exiting the context."""
        await self.disconnect()

    @asynccontextmanager
    async def publisher(
        self, topic: str, msg_type: str
    ) -> AsyncGenerator[Publisher, None]:
        """Context manager for ROS publisher."""
        if self.websocket is None:
            raise ConnectionError("WebSocket connection is not established")

        await self.websocket.send(
            json.dumps({"op": "advertise", "topic": topic, "type": msg_type})
        )
        try:
            yield Publisher(self.websocket, topic)
        finally:
            if self.websocket:
                # Unadvertise the topic when done
                logger.info(f"Unadvertising topic {topic}")
                await self.websocket.send(
                    json.dumps({"op": "unadvertise", "topic": topic})
                )

    @asynccontextmanager
    async def subscriber(self, topic: str) -> AsyncGenerator[Subscriber, None]:
        """Context manager for ROS subscriber."""
        if self.websocket is None:
            raise ConnectionError("WebSocket connection is not established")

        await self.websocket.send(json.dumps({"op": "subscribe", "topic": topic}))

        try:
            yield Subscriber(self.websocket, topic)
        finally:
            if self.websocket:
                # Unsubscribe from the topic when done
                logger.info(f"Unsubscribing from topic {topic}")
                await self.websocket.send(
                    json.dumps({"op": "unsubscribe", "topic": topic})
                )
