from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException,NetMikoAuthenticationException
from os import system
import re

class InvalidIPException(Exception):
    print("Raise invalid IP")

class Device_details:
    def __init__(self,ip: str):
        self.ip= ip
        self.individual_deivice_dict={"ip":self.ip,
                                        "device_type":"cisco_ios",
                                        "username":"admin",
                                        "password":"cisco"}
    def connection_tester(self) -> None:
        """
        This code will establish connection.
        :parm individual_device_list: dict.
        :raise NetMikoTimeoutException, NetMikoAuthenticationException: If connection failed
        """
        try:
            ConnectHandler(**self.individual_deivice_dict)
            print("\n\nconnection successful below details\n",self.individual_deivice_dict)
        except (NetMikoTimeoutException, NetMikoAuthenticationException):
                print("\n\nfailed to connect to below device\n",self.individual_deivice_dict)
    def check_interfaces(self):
        ssh = ConnectHandler(**self.individual_deivice_dict)
        input=ssh.send_command("sh ip int bri")
        print(input)
        split_line=input.split("\n")
        for each_item in split_line:
            starts_with_list=("gig","loop","fast","tun")
            if each_item.lower().startswith(starts_with_list):
                each_item=re.sub(r"\s+"," ",each_item.strip())
                splitted_line=each_item.split()
                for each_keyword in splitted_line:
                    if each_keyword=="down":
                        print(splitted_line[0])   
                        break
    def check_ip_address(self):
        pass
    def create_configuration(self):
        pass
    def rotes_list(self):
        pass
    def execute_configuration(self):
        pass
    
def ip_validation(ip):
    ip_validation=ip.split(".")
    try:
        for each_octate in ip_validation:
            if not 0<=int(each_octate)<=255:
                print("IP is invalid",ip)
                return False
    except InvalidIPException:
        print("invalid ip",ip)
    else:
        return True
        

def main():
    system("cls")
    print("BGP MASTER PROGRAM".center(100,"="))
    print("Below are device details and connection status")
    parser=argparse.ArgumentParser(description="Program takes file name as input")
    parser.add_argument("-f",default="device_details.csv",help="File name")
    args=parser.parse_args()
    with open(args.f,"r") as file:
        valid_ip=list(filter(ip_validation,file))
        print(*valid_ip)
    for each_ip in valid_ip:
        r=Device_details(each_ip.strip())
        r.connection_tester()
        r.check_interfaces()
            # r=Device_details(each_device.strip())
            # r.connection_tester()
            # print(Device_details.DEVICE_DETAILS_LIST)
            


if __name__=="__main__":
    main()