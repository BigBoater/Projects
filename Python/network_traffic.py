import networkx as nx
from scapy.all import rdpcap, IP, TCP, UDP

net_graph = nx.MultiDiGraph()
packets = rdpcap('network_sim.pcap')
for packet in packets:
    if not packet.haslayer(IP):
        #Not a packet to analyze.
        continue
    mac_src = packet.src #Sender MAC
    mac_dst = packet.dst #Receiver MAC
    ip_src = packet[IP].src #Sender IP
    ip_dst = packet[IP].dst #Reciever IP
    w = packet[IP].len #Number of bytes in packet
    if packet.haslayer(TCP):
        sport = packet[TCP].sport #Sender port
        dport = packet[TCP].dport #Reciever port
    elif packet.haslayer(UDP):
        sport = packet[UDP].sport #Sender port
        dport = packet[UDP].dport #Reciever port
    else:
        # Not a packet to analyze
        continue
    #Define an edge in the graph
    net_graph.add_edge(
        *(str(mac_src), str(mac_dst)),
        ip_src=ip_src,
        ip_dst=ip_dst,
        sport=sport,
        dport=dport,
        weight=w
    )
print(len(net_graph.nodes))
          
