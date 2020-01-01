from collections import deque
from typing import Deque, List, Optional, NamedTuple

from .intcode import CodeRunner, OutputInterrupt, InputInterrupt, parse_intcode


class Packet(NamedTuple):
    x: int
    y: int


class EndPacket(StopIteration):
    def __init__(self, packet: Packet):
        super().__init__(f"Got packet: {packet}")
        self.packet = packet


class Computer(CodeRunner):
    def __init__(self, code: List[int], address: int):
        self.queue: Deque[Packet] = deque()
        super().__init__(code, name=f"NIC_{address:02}")
        self.send(address)

    def nic_step(self, computers: List["Computer"]):
        try:
            self.run()

        except OutputInterrupt:
            # Sending a packet
            recipient = next(self)
            packet = Packet(next(self), next(self))
            if recipient == 255:
                raise EndPacket(packet)
            computers[recipient].queue.append(packet)
            return True

        except InputInterrupt:
            # Polling for packets
            if not self.queue:
                self.send(-1)
            else:
                packet = self.queue.popleft()
                self.send(packet.x)
                self.send(packet.y)
            return False


def main(data: str):
    code = parse_intcode(data)
    computers = [Computer(code, addr) for addr in range(50)]
    part_1 = True
    nas_packet: Optional[Packet] = None
    nas_y_prev = None

    activity_threshold = 3
    activity = [deque([True] * activity_threshold) for _ in range(50)]

    while True:
        for i, comp in enumerate(computers):

            try:
                act = comp.nic_step(computers)

            except EndPacket as ex:
                if part_1:
                    part_1 = False
                    yield ex.packet.y
                nas_packet = ex.packet
                act = True

            if len(activity[i]) > activity_threshold:
                activity[i].popleft()
            activity[i].append(act)

        if any(any(q) for q in activity) or any(comp.queue for comp in computers):
            continue

        # NAS activity
        if nas_packet is None:
            continue
        if nas_packet.y == nas_y_prev:
            yield nas_packet.y

        computers[0].queue.append(nas_packet)
        nas_y_prev = nas_packet.y
        nas_packet = None
