import asyncio
import json
import websockets

HOST = "127.0.0.1"
PORT = 8765

clients = set()

async def handler(websocket):
    clients.add(websocket)
    print("\nBrowser connected!")

    try:
        async for message in websocket:
            data = json.loads(message)

            if data.get("type") == "robot-state":
                print(
                    f"\rRobot State: "
                    f"x={data['x']:8.3f} "
                    f"z={data['z']:8.3f} "
                    f"rotation={data['rotationY']:7.3f}",
                    end="",
                    flush=True
                )

            elif data.get("type") == "bridge-info":
                print("\n" + data.get("message", "Connected"))

    except websockets.ConnectionClosed:
        pass

    finally:
        clients.discard(websocket)
        print("\nBrowser disconnected.")

async def send_command(command):
    if not clients:
        print("\nNo browser connected.")
        return

    message = json.dumps(command)

    for client in clients:
        await client.send(message)

async def command_loop():
    loop = asyncio.get_event_loop()

    print("\nCommands:")
    print("w     = move forward")
    print("s     = move backward")
    print("a     = turn left")
    print("d     = turn right")
    print("run   = run forward")
    print("stop  = stop")
    print("quit  = exit")

    while True:
        command = await loop.run_in_executor(None, input, "\nPython > ")
        command = command.lower().strip()

        if command == "w":
            await send_command({
                "type": "robot-command",
                "forward": True,
                "back": False,
                "left": False,
                "right": False,
                "run": False
            })

        elif command == "s":
            await send_command({
                "type": "robot-command",
                "forward": False,
                "back": True,
                "left": False,
                "right": False,
                "run": False
            })

        elif command == "a":
            await send_command({
                "type": "robot-command",
                "forward": False,
                "back": False,
                "left": True,
                "right": False,
                "run": False
            })

        elif command == "d":
            await send_command({
                "type": "robot-command",
                "forward": False,
                "back": False,
                "left": False,
                "right": True,
                "run": False
            })

        elif command == "run":
            await send_command({
                "type": "robot-command",
                "forward": True,
                "back": False,
                "left": False,
                "right": False,
                "run": True
            })

        elif command == "stop":
            await send_command({
                "type": "robot-command",
                "forward": False,
                "back": False,
                "left": False,
                "right": False,
                "run": False
            })

        elif command == "quit":
            break

        else:
            print("Unknown command.")

async def main():
    async with websockets.serve(handler, HOST, PORT):
        print(f"\nPython bridge running at ws://{HOST}:{PORT}")
        await command_loop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBridge stopped.")