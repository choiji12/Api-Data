# 라즈베리파이 -> 서버 소켓통신

import websockets
import asyncio

async def send_data(websocket, queue):
    while True:
        cycle = 5
        # 센서 값 로직 추가
        # sleep 부분 변수로 변경(기본 30초)
        # receive_data에서 받아온 srver_value값에서 센서이름, 변경할 시간 파싱해서 사용 (ex mq5:60 형식으로 넘어옴)
        temp_data = "test:105.2"
        await websocket.send(temp_data)

        if queue.qsize() != 0:
            temp = await queue.get()
            cycle = int(temp.split(':')[1])
            print(cycle)

        await asyncio.sleep(cycle)  # cycle만큼 대기

async def receive_data(websocket, queue):
    while True:
        # 서버로부터 메시지 수신
        server_value = await websocket.recv()
        print(f"Received data from the server: {server_value.split(':')[1]}")

        await queue.put(server_value)

async def main():
    # 로컬 테스트 시 사용
    uri = "ws://#/ws"
    # 배포환경으로 테스트 시 사용
    # uri = "wss://port-0-raspberry-pi-project-5mk12alpbcv53c.sel5.cloudtype.app/ws"

    queue = asyncio.Queue()

    async with websockets.connect(uri) as websocket:
        # send, receive 메소드를 비동기적으로 실행
        send_task = asyncio.ensure_future(send_data(websocket, queue))
        receive_task = asyncio.ensure_future(receive_data(websocket, queue))

        # 두 task 동시에 실행
        await asyncio.gather(send_task, receive_task)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())