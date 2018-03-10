# 更新時間管理など
import datetime
import time

# Ctrl+Cで終了時の処理のため
import signal
import sys

# モジュール変数の定義
import config

# OSC送信のため
import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client

# Ctrl+Cで終了時の処理
def handler(signal, frame):
        print('Exit with Ctrl+C / sys.exit(0) ')
        sys.exit(0)

# OSCのSender初期化
def init_osc_sender():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sender_ip", default="127.0.0.1", help="The ip of th OSC Sender")
    parser.add_argument("--sender_port", type=int, default=config.sender_port, help="The port the OSC sender is listening on")
    args = parser.parse_args()
    osc_client = udp_client.UDPClient(args.sender_ip, args.sender_port)

    # 設定のログ出し
    print("sender_ip:127.0.0.1, sender_port:" + str(config.sender_port) + ", address:/data")
    return osc_client

# Parameterの取得とmsgに突っ込む
def get_param(msg,arg):
    print("type {}:".format(arg))
    input_arg = input()
    msg.add_arg(int(input_arg))
    return input_arg

def task(osc_client):
  msg = osc_message_builder.OscMessageBuilder(address="/data")

  # 更新時間を送信
  update_time = str(time.asctime().split(" ")[4])
  msg.add_arg(update_time)

  get_param(msg,"X")
  get_param(msg,"Y")
  get_param(msg,"Z")
  get_param(msg,"interaction")

  msg = msg.build()
  osc_client.send(msg)

if __name__ == "__main__":

  # Ctrl+C終了時のイベント検知
  signal.signal(signal.SIGINT, handler)

  # OSC周りの初期化
  osc_client_sender = init_osc_sender()

  while True:
    task(osc_client_sender)
    time.sleep(2)

