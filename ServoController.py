import serial
import time


if __name__ == '__main__':
    with serial.Serial('/dev/ttyS0', 115200, timeout=1) as ser:
	while True:
		text = raw_input("Enter command: ")
	
		if text == "exit":
			break

		ser.write(text)
		
		t = time.time() * 1000

		resp = ""
		while True:
			c = ser.read()
			resp += c
			if c == '>':
				break

		print "Response: {0}".format(resp)
		print "Time: {0}ms".format((time.time()*1000)-t)
		print
	
