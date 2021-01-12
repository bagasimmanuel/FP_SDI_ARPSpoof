import os,sys, subprocess
from time import sleep, time
from twilio.rest import Client

account_sid = "ACd2aad69d68f473467ef52261ba018d23" #SID Token dari Twilio
auth_token = "693b2ec7658e4377ae42837f6561a901" #Auth Token dari Twilio

client = Client(account_sid,auth_token)


threshold = 12
mac_dict = {}
time_dict = {}

#Checking for root privilleges
try:
    if os.getuid() != 0:
        print "ERROR: ARPSHIELD requires root privillege to run"
        os._exit(1)
except:
    # Its a windows system
    print "ERROR: ARPSHIELD Cannot run on Windows"
    sleep(1.5)
    os._exit(1)

# Check if the dependancy requirements are met.
try:
    from scapy.all import sniff
    import netifaces
except:
    print "Ada bberapa modul yang belum lengkap, tolong install Scapy dan Netifaces terlebih dahulu"
    print "Exit.."
    sleep(0.7)
    sys.exit()

# start main import statements

from scapy.all import *
import netifaces

# Selection on Interface (USER)
available_interface = netifaces.interfaces()
print("")
interface = raw_input("Please select the interface you wish to use. {}\n".format(str(available_interface)))
if interface not in available_interface:
    print "Interface" ,interface ,"not Available"
    exit()


# Get IP and MAC of Gateway
def getGateway(txt):
    if txt == "ip":
        try:
            getGateway = sr1(IP(dst="1.1.1.1", ttl=0) / ICMP() / "XXXXXXXXXXX", verbose=False, timeout=2)
            print "Gateway IP: " , getGateway.src 
            return getGateway.src

        except:
            print("shit happened")
            return ("192.168.38.2")
    elif txt =="ip_of_selected_interface":
        getGateway = sr1(IP(dst="1.1.1.1", ttl=0) / ICMP() / "XXXXXXXXXXX", verbose=False, timeout=2)
        print "Your IP: " , getGateway[IP].dst 
        return getGateway[IP].dst
    else:
        try:
            query = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=txt)
            ans, _ = srp(query, timeout=2, verbose=0)
            for _, rcv in ans:
                return(rcv[Ether].src)
                break
        except:
            print("Initialization Failed!")


mac_of_selected_interface = get_if_hwaddr(interface)
gatewayip = getGateway("ip")
gatewaymac = getGateway(gatewayip)
ip_of_selected_interface = getGateway("ip_of_selected_interface")

def check_for_spoof_attack(source, dest, s_mac, gatewaymac, gatewayip, d_mac):
    if source == gatewayip and s_mac != gatewaymac:
        print("ARP Attack Detected.") 
        #Twilio
        message = client.messages.create(
                            body="ARP POISONING, SEGERA DISCONNECT JARINGAN INTERNET",
                            from_="whatsapp:+14155238886",
                            to="whatsapp:+6281217113313"
        )
        sleep(10)



def process_packets(packet):
    source = packet.psrc
    dest = packet.pdst
    operation = packet.op
    s_mac = packet.hwsrc
    d_mac = packet.hwdst
    #print(source,dest,s_mac,operation)

    check_for_spoof_attack(source, dest, s_mac, gatewaymac, gatewayip, d_mac)


print 'Your MAC: ' , mac_of_selected_interface
print "Menu: \n \t1. Start ARP SHIELD \n\t2. Exit"
choice = input("Enter your choice : ")

if choice == '1':
    os.system("clear")
    print "ARPSHIELD Started. Any output will be redirected to log file."
    sniff(filter="arp",prn=process_packets, store=0 )
elif choice =='2':
    print "Exiting ARPSHIELD."
    sleep(1.5)
    print "Bye!"
    sleep(1.6)
    exit(101)
else:
    print "Invalid Choice"
    exit(101)
