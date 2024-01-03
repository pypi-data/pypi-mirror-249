import queue, time, threading
from . import udp_session
from whatap.conf.configure import Configure as conf
q = queue.Queue(conf.max_send_queue_size)

def send_packet( packet_type, ctx, datas=[]):
    global q
    if q.full():
        return
    q.put((packet_type, ctx, datas))


def startWhatapThread():
    def __sendPackets():
        global q
        while True:
            packet_env = q.get()
            if not packet_env:
                time.sleep(0.1)
                continue
            packet_type, ctx, datas = packet_env
            udp_session.UdpSession.send_packet(packet_type, ctx, datas)
            
    t = threading.Thread(target=__sendPackets)
    t.setDaemon(True)
    t.start()

startWhatapThread()