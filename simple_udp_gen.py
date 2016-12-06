#------------------------------------------------------------------------
# Simple UDP generator
# It generates random UDP data every 3sec to ports given in args: 
# e.g. $python UDP_gen.py 2222 3333 4444
# author: lukaszog@man.poznan.pl
# PSNC
# 12.2016
#------------------------------------------------------------------------

import sys, datetime, time, threading, random, subprocess, select, socket


UDP_DST_IP = "192.168.20.2"


print "Simple UDP generator"

def read_params():

    UDP_DST_PORTs=[]
    for arg in sys.argv[1::]:
        try: 
            port = int(arg)
            if port>0 and port<0xFFFF:
                UDP_DST_PORTs.append(int(arg))
            else:
                print "No valid UDP ports"
                break
        except ValueError:
            print "No valid UDP ports"      
            break 
    if UDP_DST_PORTs==[]:
        print "Please set UPD dst_ports"
    return UDP_DST_PORTs

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


class RandomGenerator(threading.Thread):
    def __init__(self,UDP_DST_PORTs):
        threading.Thread.__init__(self)
        self.active = True
        self.UDP_DST_PORTs = UDP_DST_PORTs
                
    def run(self):
        print "Starting random generator..."
        print "List of dst UDP ports:",self.UDP_DST_PORTs
        
        while self.active:   

            #send also random data:
            rand = random.randint(1, 10) 
            
            for port in self.UDP_DST_PORTs:
                sock.sendto(str(rand), (UDP_DST_IP, int(port)))     
                print "%s sending random UDP datagram (data: %s)"%(datetime.datetime.now(), rand)
            time.sleep(3)
                        
    def stop(self):        
        print "RandomGenerator stopping"
        self.active = False
        print "RandomGenerator stopped"

 

if __name__ == "__main__":
    
    ports = read_params()

    if len(ports)>0:
        random_g = RandomGenerator(ports)
        random_g.start()

        #may break by ctrl+c    
        try:
                        
            # Wait forever, so we can receive KeyboardInterrupt.
            while random_g.isAlive():
                         
                time.sleep(1)

        except (KeyboardInterrupt, SystemExit):
            print "FELIX : ^C received"
            
            if random_g.isAlive():
                random_g.stop()  
            

            import os, signal
            os._exit(1)        
            pid = os.getpid()
            os.kill(pid, signal.SIGTERM)
           
        # We never get here.
        raise RuntimeError, "not reached"
