'''
Created on Dec 17, 2014

@author: marcel
'''

import random
import socket
from mod_operations import coin_flip,inverse,square_ZnZ

def str_to_bool(string):
    if string=='True':
        return True
    elif string=='False':
        return False
    else:
        return None

class ffs_prover:   
    #Initialize the prover's key
    #n: Agreed upon large integer
    #k: key size
    #t: number of challenges --> Should be specified by the verifier...
    def __init__(self,n,k):
        self.n=n
        self.k=k
        self.t=1
        self.s=[None]*k
        self.p=[None]*k
        for i in range(0,k):
            self.s[i]= random.randint(0,n-1)
            self.p[i]= coin_flip()*inverse(square_ZnZ(self.s[i], n),n)
            self.p[i]=self.p[i] % n
        print "Prover initialized..."
        print "\tPrivate key: "+",".join(map(str,self.s))
        print "\tPublic key: "+",".join(map(str,self.p))
    
    #open a socket to the verifier
    def register_verifier(self,ip,port):
        mysocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        mysocket.connect((ip,port))
        return mysocket.makefile()
    
    #Sends the public key to the verifier --> should use TLS?
    def advertise_key(self,mysocket):
        mysocket.write("PKA\n")
        mysocket.flush()
        response=mysocket.readline()
        if response == "OK PKA\n":
            for value in self.p:
                mysocket.write(str(value)+" ")
            mysocket.write("\n")
            mysocket.flush()
        else:
            mysocket.write("DIE\n")
            mysocket.flush()
            print "Protocol failure during key advertisment"
            exit()
    
    def start_auth(self,mysocket):
        mysocket.write("START\n")
        mysocket.flush()
        response=mysocket.readline()
        if response.split()[0:2] == ["OK","START"]:  #TODO: match pattern "OK START [0-9]+\n"
            self.t = int(response.split()[2])
            print "Verifier asked for "+str(self.t)+" challenges"             
    
    #Commit to R as described in Feige-Fiat-Shamir        
    def initiate_challenge(self,mysocket):
        mysocket.write("COMMIT\n")
        mysocket.flush()
        response=mysocket.readline()
        r=0
        b=[]
        if response == "OK COMMIT\n":
            r=random.randint(0,self.n-1)
            mysocket.write(str((coin_flip()*square_ZnZ(r, self.n)) %self.n) + " ")
            mysocket.write("\n")
            mysocket.flush()
            b=map(str_to_bool,mysocket.readline().split())
            return r,b
        else:
            mysocket.write("DIE\n")
            mysocket.flush()
            print "Protocol failure during challenge initiation"
            exit()
    
    #Computes and sends the response from the challenge    
    def challenge_response(self,r,b,mysocket):
        y=r
        for i in range(0,self.k):
            if b[i]:
                y *= self.s[i]
        mysocket.write(str(y%self.n)+"\n")
        mysocket.flush()
        
    def run(self,port):
        verifiersocket=self.register_verifier("localhost",port)
        self.advertise_key(verifiersocket)
        self.start_auth(verifiersocket)
        for i in range(0,self.t):
            r,b = self.initiate_challenge(verifiersocket)
            self.challenge_response(r, b, verifiersocket)
        verifiersocket.write("DIE\n")
        verifiersocket.flush()


class dishonest_ffs_prover:
    def __init__(self,n,k,t):   
        self.n=n
        self.k=k
        self.t=t
        
    def register_verifier(self,ip,port):
        mysocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        mysocket.connect((ip,port))
        return mysocket.makefile()
    
    def advertise_key(self,mysocket):
        mysocket.write("PKA\n")
        mysocket.flush()
        response=mysocket.readline()
        if response == "OK\n":
            for i in range(0,self.k):
                mysocket.write(str(random.randint(0,self.n-1))+" ")
            mysocket.write("\n")
            mysocket.flush()
        else:
            mysocket.write("DIE\n")
            mysocket.flush()
            print "Protocol failure during key advertisment"
            exit()
            
    def initiate_challenge(self,mysocket):
        mysocket.write("COMMIT\n")
        mysocket.flush()
        response=mysocket.readline()
        r=0
        b=[]
        if response == "OK\n":
            r=random.randint(0,self.n-1)
            mysocket.write(str((coin_flip()*square_ZnZ(r, self.n)) %self.n) + " ")
            mysocket.write("\n")
            mysocket.flush()
            b=map(str_to_bool,mysocket.readline().split())
            return r,b
        else:
            mysocket.write("DIE\n")
            mysocket.flush()
            print "Protocol failure during challenge initiation"
            exit()
            
    def challenge_response(self,r,b,mysocket):
        mysocket.write(str(random.randint(0,self.n-1))+"\n")
        mysocket.flush()
        
    def run(self,port):
        verifiersocket=self.register_verifier("localhost",port)
        self.advertise_key(verifiersocket)
        for i in range(0,self.t):
            r,b = self.initiate_challenge(verifiersocket)
            self.challenge_response(r, b, verifiersocket)
        verifiersocket.write("DIE\n")
        verifiersocket.flush()