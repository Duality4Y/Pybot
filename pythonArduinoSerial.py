import serial
import socket
import time
#import sys
#ser = serial.Serial(str(raw_input("enter device for example: /dev/xx: ")), int(raw_input("and baud: ")))
ser = serial.Serial("/dev/ttyACM0",115200);
server = "irc.freenode.net"
#channel = raw_input("Enter channel: ")
channel = "#test1123"
nick = "ADuaD"
botowner = "Duality"
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircDone = False

def ping():
	ircsock.send("PONG :Pong\n")

def sendmsg(chan, msg):
	ircsock.send("PRIVMSG "+chan+" :"+msg+"\n")

def Privmsg(_nick, msg):
	ircsock.send(":"+_nick+" PRIVMSG "+botowner+" :"+msg+"\n")

def joinchan(chan):
	ircsock.send("JOIN "+chan+"\n")

def leavechan(chan):
	ircsock.send("PART "+chan+"\n");

def connectIrc():
	ircsock.connect((server, 6667))
	ircsock.send("USER "+nick+" "+nick+" "+nick+" :Arduino Irc Thingy\n")
	ircsock.send("NICK "+nick+"\n")
	joinchan(channel)

def getUserName(data):
	return data.split('~')[0][1:-1]  #extract nick

def irc():
	global channel
	ircmsg = ircsock.recv(2048)
	ircmsg = ircmsg.strip('\n\r')
	#ircmsg = str(ircmsg).lower()
	if ircmsg.find("PING :") != -1:
		ping()
		print nick+" >> "+ircmsg
	if ircmsg.find("PRIVMSG "+nick) != -1:
		if ircmsg.find(":!")!= -1:
			if ircmsg.find("join ")!= -1:
				for l in xrange(len(ircmsg)):
					if ircmsg[l] == ":":
						chan = ircmsg;
						chan = chan[l+len("join  "):len(ircmsg)]
						leavechan(channel);
						joinchan(chan);
						channel = chan.strip(' ');
		else:
			send = ircmsg.split(' :',1)[1]
			print "Pm: "+getUserName(ircmsg)+" >>",send
			Privmsg(getUserName(ircmsg),send);
	if ircmsg.find("PRIVMSG "+channel)!= -1:
		return ircmsg
	return 0;

connectIrc()

while True:
	disp = irc()
	if disp != 0:
		userNick = getUserName(disp);
		disp = disp.split(' ')
		for l in xrange(len(disp)):
			if disp[l] == "PRIVMSG":
				disp = disp[l:len(disp)][2:]
				disp = ' '.join(disp)
				disp = disp[1:]
				break
		disp = ''.join(disp);
		print ">> "+userNick+" >>: ",disp
		ser.write(str(userNick+": "+disp+"\r\n"))
		time.sleep(2)
