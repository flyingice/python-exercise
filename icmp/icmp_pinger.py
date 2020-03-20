#!/usr/bin/env python3
import socket
import os
import sys
import struct
import time
import select
import statistics
import signal

ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0
seq = 0
statList = []


def checksum(packet_bytes):
    csum = 0
    count_to = (len(packet_bytes) // 2) * 2
    count = 0
    while count < count_to:
        this_val = packet_bytes[count + 1] * 256 + packet_bytes[count]
        csum = csum + this_val
        csum = csum & 0xffffffff
        count = count + 2

    if count_to < len(packet_bytes):
        csum = csum + packet_bytes[len(packet_bytes) - 1]
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)

    return answer


def validateChecksum(packet):
    resType, resCode, chk, id, seq, timestamp = struct.unpack_from(
        "bbHHhd", packet, 20)
    # replace checksum field with all 0
    packet = struct.pack("bbHHhd", resType, resCode, 0, id, seq, timestamp)
    return socket.htons(checksum(packet)) & 0xffff == chk


def calculateStat(sig, frame):
    print("\r\n--- {} ping statistics ---".format(host))

    global statList
    nTotal = len(statList)
    nLost = statList.count(-1)
    print("{0} packets transmitted, {1} packets received, {2:.1f}% packet loss".format(
        nTotal, nTotal - nLost, nLost / nTotal * 100 if nTotal > 0 else 0))

    statList = list(filter(lambda x: x != -1, statList))
    try:
        print("round-trip min/avg/max/stddev = {0:.3f}/{1:.3f}/{2:.3f}/{3:.3f} ms".format(min(
            statList) * 1000, statistics.mean(statList) * 1000, max(statList) * 1000, statistics.stdev(statList) * 1000))
    except statistics.StatisticsError:
        pass

    exit(0)


def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout

    while True:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if not whatReady[0]:  # Timeout
            statList.append(-1)
            return "Request timed out."
        else:
            break

    timeReceived = time.time()
    recPacket, addr = mySocket.recvfrom(1024)

    # Fetch the ICMP header from the IP packet
    # The header of IP packet 20-byte long.
    ttl = struct.unpack_from("b", recPacket, 8)[0]
    resType, resCode, _, _, seq, timestamp = struct.unpack_from(
        "bbHHhd", recPacket, 20)
    if validateChecksum(recPacket) and resType == ICMP_ECHO_REPLY and resCode == 0:
        stat = "{0} bytes from {1}: icmp_seq={2} ttl={3} time={4:.3f} ms".format(
            len(recPacket), addr[0], seq, ttl, 1000*(timeReceived - timestamp))

    timeLeft -= howLongInSelect

    if timeLeft <= 0:
        statList.append(-1)
        return "Request timed out."
    else:
        statList.append(timeReceived - timestamp)
        return stat


def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    myChecksum = 0

    # Make a dummy header with a 0 checksum
    # struct interpret strings as packed binary data
    global seq
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, seq)
    data = struct.pack("d", time.time())

    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        # Convert 16bit integers from host to network byte order
        myChecksum = socket.htons(myChecksum) & 0xffff
    else:
        myChecksum = socket.htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, seq)
    packet = header + data
    # AF_INET address must be tuple, not str
    mySocket.sendto(packet, (destAddr, 1))

    seq += 1
    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object.


def doOnePing(destAddr, timeout):
    icmp = socket.getprotobyname("icmp")

    # SOCK_RAW is a powerful socket type. For more details: http://sockraw.org/papers/sock_raw
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    myID = os.getpid() & 0xFFFF  # Return the current process id
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()

    return delay


def ping(host, timeout=1):
    # timeout=1 means: If one second goes by without a reply from the server,
    # the client assumes that either the client's ping or the server's pong is lost

    dest = socket.gethostbyname(host)
    version = sys.version_info
    print("Pinging " + dest +
          " using Python {0}.{1}.{2}:".format(version.major, version.minor, version.micro))

    # Send ping requests to a server separated by approximately one second
    while True:
        delay = doOnePing(dest, timeout)
        print(delay)
        time.sleep(1)  # one second

    return delay


if __name__ == '__main__':
    host = "www.baidu.com"
    signal.signal(signal.SIGINT, calculateStat)
    ping(host)
