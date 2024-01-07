# roxbot



---

**Documentation**: [https://roxautomation.gitlab.io/roxbot](https://roxautomation.gitlab.io/roxbot)

**Source Code**: [https://gitlab.com/roxautomation/roxbot](https://gitlab.com/roxautomation/roxbot)


---

# Roxbot - A Pythonic KISS Robotics Framework

## Vision

`Roxbot` aspires to be a user-friendly toolkit for architecting robotic systems. Inspired by the ROS (Robot Operating System) architecture, it leverages modern and reliable open-source modules to provide a comprehensive solution. Below is an outline of the envisioned capabilities of `Roxbot`:

1. **Modular Design** - Roxbot advocates a simple, modular design where individual components synergize to create a larger system, facilitating a straightforward understanding, construction, and enhancement of robots.
    * Central to the system is the [node framework](how_it_works.md) which enables structured communication between modules.

2. **Easy Configuration** - Managing settings across software and hardware is streamlined with Roxbot, ensuring a harmonious operation.
    * Configuration definition is simplified through `dataclass` and `pydantic`, with an override mechanism using `yaml` data files.

3. **Smooth Communication Between Processes** - Roxbot ensures seamless interaction between different system segments, whether within the same process or across multiple processes.
    * `asyncio` is utilized for intra-subsystem node communication.
    * `mqtt` facilitates inter-subsystem connectivity.
    * A websocket bridge is provided for frontend integrations.

4. **Friendly Hardware Interaction** - Interacting with various hardware components is simplified, bridging software and hardware effectively. Roxbot integrates hardware through a hardware abstraction layer and CAN (Controller Area Network) interface, supporting several commonly used devices like motion controllers.
    * [odrive](https://gitlab.com/roxautomation/components/odrive-can)

5. **Kinematic Models** - Roxbot includes a variety of kinematic robot models for rapid development.
    * [trike model](trike_model.md)
    * diff-drive model
    * bicycle model

6. **Simple Diagnostic and Monitoring Tools** - Tools for assessing system health and performance are provided, ensuring smooth operation.
    * Visualization dashboards

7. **Effortless Logging and Debugging** - Roxbot simplifies issue identification and resolution through logging and debugging features.
    * Leveraging Python’s logging facilities, enhanced by libraries like `coloredlogs`.
    * Tools for data logging, replay, and `influxdb` integration.

8. **Built-in Security** - Security measures are in place to protect the system and its data from unauthorized access and other threats.
    * Containerized sub-systems
    * SSH tunnels for secure communication between systems.

9. **Community-Driven Growth** - Roxbot aims to cultivate a supportive community for collaborative learning, contribution, and development.

10. **Compatible and Portable** - Roxbot is engineered for compatibility and portability across various systems and hardware setups.
    * Smooth integration with existing ROS/ROS2 subsystems via [rosbridge](https://github.com/RobotWebTools/rosbridge_suite)
    * Extensive use of Docker for system development and deployment. Develop once - deploy anywhere.

11. **Testing and Simulation Made Easy** - Roxbot provides tools for testing and simulating robotic actions in a safe, controlled environment.
    * Adopts the "digital-twin" design principle, allowing remote development without physical hardware, enabled by simulators and mocks for each supported system component.

Harnessing established technologies like Docker, MQTT, and asyncio, and embracing Python for its ease of learning and rapid development, `Roxbot` is poised to offer a flexible and scalable framework that makes robotics development accessible and enjoyable.
