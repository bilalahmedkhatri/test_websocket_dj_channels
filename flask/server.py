import asyncio
import websockets
import numpy
import cv2
import socket


async def build_video():
    pass


def get_system_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()
    s.close()
    return ip


async def server(websocket, path):
    print(f"Client connected: {websocket.remote_address}")

    # Set the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output_video.avi', fourcc, 30.0, (640, 480))
    # ip_, port_ = websocket.remote_address
    # print(f"Client connected: {ip_}:{port_}")
    # Open the stream
    try:
        while True:
            # Continuously listen for messages from the client
            async for message in websocket:
                bytes_to_array = numpy.frombuffer(message, numpy.uint8)
                to_image = cv2.imdecode(bytes_to_array, cv2.IMREAD_COLOR)

                # testing images in video frames
                cv2.imshow("screenshot_video", to_image)
                cv2.waitKey(1)
                await websocket.send("received...")
            out.write(bytes_to_array)

    except websockets.exceptions.ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")

    finally:
        cv2.destroyAllWindows()

# Start the WebSocket server on localhost, port 8080
if __name__ == "__main__":
    start_server = websockets.serve(
        server, '', 8005, ping_interval=None)
    print("WebSocket server is running on ws://46.138.93.58:443")

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
