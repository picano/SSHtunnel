from sshtunnel import SSHTunnelForwarder
import argparse
from time import sleep

'''
Python SSH Tunnel Utility - E. Bullen Feb 2016
Wrapper around **sshtunnel** - see https://github.com/pahaz/sshtunnel/

sshtunnel has dependancies on
    paramiko
    ecdsa
    pycrypto
    
General useage:
    pytunnel -s <remote server host-name/IP-addr> -l <localport>  -r <remoteport> [ -k <sshkey> ] [ -u <ssh user> ] [-p <ssh port>] 
    
    sshkey defaults to ./key.priv if not specified
    user defaults to ORACLE
    
Example - tunnel port 1521 from local host to 1521 at 129.152.150.7 over SSH with oracle user:

$> python pytunnel.py -s 129.152.150.7 -l 1521 -r 1521 -k D:\Oracle\Cloud\testkey\rsa.priv
>  Server Bound to Local Port: 1521
>  Control-C to stop local-host tunnel on port 1521 to 129.152.150.7:1521
      
Windows command-line example for calling the sshtunnel module directly >> Without using this wrapper <<
python -m sshtunnel -U oracle -K D:/Oracle/Cloud/testkey/rsa.priv -L :1521 -R 127.0.0.1:1521 -p 22 129.152.150.7

'''


def fileexists(fname):
    #ToDo
    pass

def defaultconfig():
    global SSHPORT
    SSHPORT = 22
    global SSHUSER
    SSHUSER = "oracle"
    global SSHKEY
    SSHKEY = "./key.priv"
    global CNAME
    CNAME = "./pytunnel.conf"

def configfile(cname):
    # Todo
    #return exist, config
    pass

def parseargs():
    parser = argparse.ArgumentParser(description='SSH tunnel utility')
    parser.add_argument('-s', '--server', help='remote Server host-name or IP address', required=True)
    parser.add_argument('-l', '--localport', help='local TCP port', required=True)
    parser.add_argument('-r', '--remoteport', help='remote TCP port', required=True)
    parser.add_argument('-k', '--sshkey', help='path to private key file - default='+ SSHKEY, required=False)
    parser.add_argument('-u', '--sshuser', help='SSH user - default=' + SSHUSER, required=False)
    parser.add_argument('-p', '--sshport', help='SSH port - default='+ str(SSHPORT), required=False)
        
    args = parser.parse_args()

    # Set vars:
    if args.sshuser:
        sshuser = args.sshuser  #or use default
    else:
        sshuser = SSHUSER
    localport = int(args.localport)
    remotehost = args.server
    remoteport = int(args.remoteport)
    if args.sshkey:
        privatekey = args.sshkey #(or use default)
    else:
        privatekey = SSHKEY
    if args.sshuser:
        sshuser = args.sshuser
    else:
        sshuser = SSHUSER
    if args.sshport:
        sshport = args.sshport
    else:    
        sshport = SSHPORT
    
    return sshuser, localport, remotehost, remoteport, privatekey, sshuser, sshport

if __name__ == '__main__':
    
    defaultconfig()
    sshuser, localport, remotehost, remoteport, privatekey, sshuser, sshport = parseargs()
     
    #fileexists(privatekey)    
    
    try:
        server = SSHTunnelForwarder(
            (remotehost, sshport), 
    		    ssh_username = sshuser,
    			#ssh_password="",
    			ssh_private_key = privatekey,
    	        local_bind_address=('127.0.0.1', localport),
    			remote_bind_address=('127.0.0.1', remoteport))
        
        server.start()
        print("Server Bound to Local Port:", server.local_bind_port)
        print("Control-C to stop local-host tunnel on port {0} to {1}:{2}".format(localport,remotehost,remoteport))
        while True:
            # press Ctrl-C for stopping
            sleep(1)
    		
        #server.stop()
    
    except KeyboardInterrupt:
        pass
    	
    except Exception as err:	
        print("General Exception " , err )
    finally:
        server.close()
        print('Tunnel Session Closed')
