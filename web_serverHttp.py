import os,sys,time,socket



SERVER_ROOT ='.'
print "\n\n\n              ###  SImple HTTP Sever ###  \n\n\n"       

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(('localhost',8000))
s.listen(1)
print "Server started at Localhost:8000 or 127.0.0.1:8000 \n\n"

def reap_the_child():
	while 1:
		try:
			res = os.waitpid(-1,os.WNOHANG)
			if not res[0]:                                                  
				break
		except:	
			break


def header_(http_code, content_type):

	headr = ''
        if(http_code == 200):
		headr = 'HTTP/1.1 200 OK\n'
    	elif(http_code == 404):
		headr = 'HTTP/1.1 404 File Not Found\n'
    	date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    	headr += 'Date:' + date + '\n'
    	headr += 'Server: Python-http-server\n'
    	headr += 'Content-Type:'+ content_type + '\n'
    	headr += '\n'
    	return headr


def content_type_(file_name):
	content_types = {'html': 'text/html',
		         'txt': 'text/txt',
			 'jpg': 'image/jpeg',
	                 'png': 'image/png',
                         'pdf': 'application/pdf',
	                 'gif': 'image/gif',
		         'ico': 'icon/ico'}
	
	file_name=file_name.split('.')[-1]
	#print "getting the "+file_name+" file"    
	return content_types[file_name.split('.')[-1]]

while 1:
	#try:
	con,addr = s.accept()
	
	#except:
		#print " Some error have occured "

	reap_the_child()
	
	pid = os.fork()
	if pid:
		con.close()     
 		continue
	else:
		#s.close()
		received = con.recv(1024)
		print("Recived connection from: ",addr)
		received_data = bytes.decode(received)
		method = received_data.split(' ')[0]
		print("Requested method:",method)
		if(method == 'GET'):
	    		req_file = received_data.split(' ')[1]
	    		if(req_file == '/'):
                		req_file = '/index.html'
				print "Loading the Base HTML file"
	    		req_file = SERVER_ROOT + req_file
			print "Requested File: "+req_file + "\n"
	    	try:
	        	fp = open(req_file, 'rb')
			data = fp.read()
			fp.close()
			content_type = content_type_(req_file)
			header = header_(200, content_type)
	    	except:
			header = header_(400, 'text/html')
			data = b'<html><body><p> Error 404 File not found</p></body></html>'	
	    	response = header.encode()
	    	response += data
	    	con.send(response)
            	time.sleep(1)
            	con.close()
		sys.exit(0)	
