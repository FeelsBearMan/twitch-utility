import subprocess
import time

broadcaster_id = input("스트리머 아이디를 입력해주세요 ")

while True:
    subprocess.call(
        ["streamlink", "--output", "C:/twitch-record/{author}/{time}.mp4", f"twitch.tv/{broadcaster_id}", "best"])
    time.sleep(5)
