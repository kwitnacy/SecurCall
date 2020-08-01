import socket
import pyaudio
import time
import threading
import audioop
import random
import secrets
from pylibsrtp import Policy, Session


class Client:
    def __init__(self):
        self.CHUNK = 512
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.frames1 = []
        self.frames2 = []
        self.p = pyaudio.PyAudio()
        self.UDP_CONNECTION = None
        self.SEQUENCE_NUM = 0
        self.TIMESTAMP = 0
        self.SSRC = 0
        self.SRTPkey = secrets.token_bytes(30)
        self.rx_session = None
        self.tx_session = None

    def test(self):
        self.init_UDP_connection()
        self.init_session()
        t_udp_controller = threading.Thread(target=self.udp_controller)
        t_udp_controller.start()
        return True

    def init_session(self):
        self.SEQUENCE_NUM = random.randint(1, 9999)
        self.TIMESTAMP = random.randint(1, 9999)
        self.SSRC = random.randint(1, 9999)
        tx_policy = Policy(key=self.SRTPkey, ssrc_type=Policy.SSRC_ANY_OUTBOUND)
        self.tx_session = Session(policy=tx_policy)
        rx_policy = Policy(key=self.SRTPkey, ssrc_type=Policy.SSRC_ANY_INBOUND)
        self.rx_session = Session(policy=rx_policy)

    def udp_controller(self):
        inp = self.init_audio_input()
        output = self.init_audio_output()

        inp.start_stream()
        output.start_stream()
        while True:  # inp.is_active() and out.is_active():
            print("ON AIR")
            time.sleep(0.1)
        inp.stop_stream()
        inp.close()
        output.stop_stream()
        output.close()

    def init_audio_input(self):
        def callback(in_data, frame_count, time_info, status):
            try:
                in_data = audioop.lin2alaw(in_data, 2)
                in_data = b'\x80\x08' + self.SEQUENCE_NUM.to_bytes(2, byteorder='big') + \
                          self.TIMESTAMP.to_bytes(4, byteorder='big') + self.SSRC.to_bytes(4, byteorder='big') + in_data
                in_data = self.tx_session.protect(in_data)
                self.UDP_CONNECTION.sendto(in_data, ("127.0.0.1", 12344))
            except Exception as e:
                print("UDP sending error:", e)
                return in_data, pyaudio.paComplete

            if self.SEQUENCE_NUM > 65530:
                self.SEQUENCE_NUM = random.randint(1, 9999)
            else:
                self.SEQUENCE_NUM += 1
            self.TIMESTAMP += 1
            return in_data, pyaudio.paContinue

        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK,
                        stream_callback=callback)
        return stream

    def init_audio_output(self):
        def callback(in_data, frame_count, time_info, status):
            while True:
                try:
                    self.UDP_CONNECTION.settimeout(1)
                    in_data, _ = self.UDP_CONNECTION.recvfrom(self.CHUNK * 2)
                    in_data = self.rx_session.unprotect(in_data)
                    # print('first: ', len(in_data))
                    in_data = audioop.alaw2lin(in_data[12:], 2)
                    # print('second', len(in_data))
                    self.UDP_CONNECTION.settimeout(None)
                    break
                except socket.timeout as e:
                    print("Odtwarzanie błąd 1:", e)
                    continue
                except:
                    return in_data, pyaudio.paComplete
            return in_data, pyaudio.paContinue

        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        output=True,
                        frames_per_buffer=self.CHUNK,
                        stream_callback=callback)
        return stream

    def init_UDP_connection(self):
        tmp = 55555
        self.UDP_CONNECTION = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.UDP_CONNECTION.bind(("127.0.0.1", 12344))
        except Exception as e:
            pass
            # print("UDP init error:", str(e))
        self.UDP_MY_PORT = tmp


if __name__ == "__main__":
    print('GO')

    p = pyaudio.PyAudio()

    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i))

    c = Client()
    c.test()

