import platform

def get_can_bus():
    system = platform.system()

    if system == "Linux":
        # GERÇEK ÇALIŞMA (vcan0)
        import can
        print("[CAN] Linux detected → using vcan0")
        return can.interface.Bus(channel="vcan0", bustype="socketcan")

    else:
        # macOS / Windows → MOCK
        print("[CAN] Non-Linux detected → using MOCK CAN bus")
        return MockBus()


class MockBus:
    def send(self, msg):
        print(f"[MOCK CAN] Sent ID={hex(msg.arbitration_id)} DATA={msg.data}")

    def recv(self, timeout=None):
        return None
