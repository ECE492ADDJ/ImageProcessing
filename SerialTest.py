import serial
import time
import sys

def bit16ToString(num):
	if num > 65535 or num < 0:
		raise OverflowError
	
	c0 = chr(num & 0x00ff)
	c1 = chr((num & 0xff00) >> 8)

	return c1 + c0

def stringTo16Bit(string):
	if len(string) != 2:
		raise ValueError

	return (ord(string[0]) << 8) + ord(string[1])


def testsend(port, command, expected):
	with serial.Serial(port, 57600, timeout=1) as ser:
		t = time.time() * 1000

		ser.write(command)

		resp = ""
		while True:
			c = ser.read()
			
			if c == "":
				break
			elif c == '>':
				resp += c
				break
			else:
				resp += c

		elapsed = time.time() * 1000 - t

		print "Sent:      {0:<8}".format(command)
		print "Recieved:  {0:<8} {1:<8}".format(resp, "OK" if resp == expected else "Failure")
		print "Elapsed:   {0:2.4}ms".format(elapsed)
		print


if __name__ == '__main__':
	port = '/dev/ttyS1'

	resp = raw_input("Type \"noservo\" to confirm that servos are not connected to the DE2: ")

	if resp != "noservo":
		print "Servos connected, exiting"
		sys.exit()

	testsend(port, '<PG>', '<ACK>')

	print "65535 - 65535"
	testsend(port, '<SX%04x>' % 65535, '<ACK>')
	testsend(port, '<SY%04x>' % 65535, '<ACK>')
	testsend(port, '<GX>', '<GX%04x>' % 65535)
	testsend(port, '<GY>', '<GY%04x>' % 65535)

	print "30000 - 30000"
	testsend(port, '<SX%04x>' % 30000, '<ACK>')
	testsend(port, '<SY%04x>' % 30000, '<ACK>')
	testsend(port, '<GX>', '<GX%04x>' % 30000)
	testsend(port, '<GY>', '<GY%04x>' % 30000)

	print "1 - 1"
	testsend(port, '<SX%04x>' % 1, '<ACK>')
	testsend(port, '<SY%04x>' % 1, '<ACK>')
	testsend(port, '<GX>', '<GX%04x>' % 1)
	testsend(port, '<GY>', '<GY%04x>' % 1)

	print "65534 - 65534"
	testsend(port, '<SX%04x>' % 65534, '<ACK>')
	testsend(port, '<SY%04x>' % 65534, '<ACK>')
	testsend(port, '<GX>', '<GX%04x>' % 65534)
	testsend(port, '<GY>', '<GY%04x>' % 65534)

	print "65535 - 30000"
	testsend(port, '<SX%04x>' % 65535, '<ACK>')
	testsend(port, '<SY%04x>' % 30000, '<ACK>')
	testsend(port, '<GX>', '<GX%04x>' % 65535)
	testsend(port, '<GY>', '<GY%04x>' % 30000)

	print "30000 - 1"
	testsend(port, '<SX%04x>' % 30000, '<ACK>')
	testsend(port, '<SY%04x>' % 1, '<ACK>')
	testsend(port, '<GX>', '<GX%04x>' % 30000)
	testsend(port, '<GY>', '<GY%04x>' % 1)

	print "1 - 65534"
	testsend(port, '<SX%04x>' % 1, '<ACK>')
	testsend(port, '<SY%04x>' % 65534, '<ACK>')
	testsend(port, '<GX>', '<GX%04x>' % 1)
	testsend(port, '<GY>', '<GY%04x>' % 65534)

	testsend(port, '<nope>', '<NACK>')
	testsend(port, '<uh oh', '')
	testsend(port, 'begin>', '')
	testsend(port, 'dfjdkl', '')
	
