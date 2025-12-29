#!/usr/bin/env python3
"""Basit XORShift tabanlı rastgele sayı üreteci."""

from __future__ import annotations

import argparse
import time


class XORShift32:
    """Deterministik ve hafif bir 32-bit XORShift RNG."""

    def __init__(self, seed: int | None = None):
        seed = seed if seed is not None else time.time_ns()
        self.state = seed & 0xFFFFFFFF
        if self.state == 0:
            self.state = 0xA5A5A5A5  # XORShift sıfır durumunda kilitlenir; kaçın.

    def next_u32(self) -> int:
        x = self.state
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= x >> 17
        x ^= (x << 5) & 0xFFFFFFFF
        self.state = x & 0xFFFFFFFF
        return self.state

    def random(self) -> float:
        return self.next_u32() / 0xFFFFFFFF


def generate(count: int, seed: int | None = None) -> list[int]:
    rng = XORShift32(seed)
    return [rng.next_u32() for _ in range(count)]


def main():
    parser = argparse.ArgumentParser(description="XORShift RNG ile rastgele sayı üretir.")
    parser.add_argument("-n", "--count", type=int, default=10, help="Üretilecek sayı adedi.")
    parser.add_argument("-s", "--seed", type=int, help="İsteğe bağlı tohum.")
    args = parser.parse_args()

    numbers = generate(args.count, args.seed)
    for i, value in enumerate(numbers, 1):
        print(f"{i:02d}: {value}")


if __name__ == "__main__":
    main()
