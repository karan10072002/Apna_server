import os
import time
import ftplib
import threading
import pyautogui

ip="192.168.206.202"
ip2="192.168.1.100"
ip3="192.168.43.1"
port=2221

def last_files():
	path=os.path.join(os.getcwd(), "Recive")
	if "last_files.txt" in os.listdir(path):
		with open(os.path.join(path, "last_files.txt"),"r") as ff:
			last_backed_files=eval(ff.read())
			ff.close()
	else:
		last_backed_files=[]
	return last_backed_files

# os.chdir(r"F:\My_projects 27-08-19\auto image to pdf\server files")

session = ftplib.FTP()
try:
	session.connect(ip, port)
	session.login('anonymous','anonymous')
except:
	try:
		session.connect(ip2,port)
		session.login('anonymous','anonymous')
	except:
		print("\n [ERROR] The default ip adderesses are not matching up with the current one.")
		print(" Try mannually...\n")
		ip3=input("[ ] FTP Server ip address: ")
		port=int(input("[ ] Port: "))
		user=input("[ ] User: ")
		password=input("[ ] Password: ")

		session.connect(ip3, port)
		session.login(user,'password')

# session.cwd(r"/Pictures/Office Lens/") ## have the apt file location

def show_info():
	global ip, port
	print(session.getwelcome())
	print("connected to: [{0}] at port [{1}] for Pictures".format(ip,port))
	print()

def file_retrival(target_file,location):
	# session.
	# print("retrieving file from the server: ",target_file)
	with open("Recive\\"+target_file,'wb') as local:
		session.retrbinary("RETR " + location+"/"+ target_file, local.write)
	local.close()
	print(f"File downloaded: {target_file}")

def update_last_files(latest_files):
	path=os.path.join(os.getcwd(), "Recive")
	new_list=last_files()+latest_files
	with open(os.path.join(path,"last_files.txt"),"w") as gg:
		gg.write(str(new_list))
	gg.close()

show_info()

def download_file_picker(target):
	path=os.path.join(os.getcwd(), "Recive")
	# session.cwd(r"/Pictures/Office Lens/")
	all_files=session.nlst(target)
	already_exist=os.listdir(path)
	# all_pics=[x for x in all_files if (".jpg" in x) and (x not in already_exist) and (x not in last_files())]
	all_pics=[x for x in all_files if (x not in already_exist) and (x not in last_files())]
	# print("New Pics: ", all_pics)
	update_last_files(all_pics)
	return all_pics


def final_downlaod():
	office_lens=download_file_picker(r"/Pictures/Office Lens/")
	camera=download_file_picker(r"/DCIM/Camera")
	apna_mobile=download_file_picker(r"/Apna server")

	for docs in office_lens:
		file_retrival(docs,r"/Pictures/Office Lens/")
	for pics in camera:
		file_retrival(pics,r"/DCIM/Camera")
	for files in apna_mobile:
		file_retrival(files,r"/Apna server")
	# print("all files downloaded ! ")

def last_upload():
	# print("in last upload")
	path=os.path.join(os.getcwd(),"Send")
	with open(os.path.join(path,"last_upload.txt"),"r") as uu:
		a=uu.read()
		# print(a)
	uu.close()
	return a

def send_files():
	# path=os.path.join(os.getcwd(),"Send")
	path=r"C:\Users\Administrator\Pictures\Camera Roll"
	all_send_files=list(os.listdir(path))
	phone_files=list(session.nlst("/Apna server"))

	add_new_files_to_phone=[]
	for i in all_send_files:
		# print("in for loop")
		# b=last_upload()
		# print("a: ",b)

		if i not in phone_files and i not in last_upload() and i!="last_upload.txt":
			print("last upload: ")
			with open(os.path.join(path,"last_upload.txt"),"a+") as update_upload:
				with open(os.path.join(path,i),"rb") as dd:
					session.storbinary(f"STOR /Apna server/{i}", dd)
					dd.close()
				print(f"\tFile sent: {i}")
				update_upload.write(f"{i}\n")
				update_upload.close()

		add_new_files_to_phone.append(i)

	recieve_path=os.path.join(os.getcwd(), "Recive")

	new_list=last_files()+add_new_files_to_phone
	with open(os.path.join(path,"last_files.txt"),"w") as gg:
		gg.write(str(new_list))
	gg.close()

		# print("all files sent")
	# session.quit()
	# session = ftplib.FTP()
	# session.connect(ip2,port)
	# session.login('anonymous','anonymous')


status=True
def finish():
	global status
	status=input()
	if status=="stop" or status=="STOP":
		status=False
		session.quit()
		pyautogui.hotkey("alt","f4")
		# exit()
	else:
		finish()

x=threading.Thread(target=finish)
x.start()

while status==True:
	# try:
	final_downlaod()
	send_files()
	# except:
	# 	print("something went wrong")
	# 	session = ftplib.FTP()
	# 	session.connect(ip2, port)
	# 	session.login('anonymous','anonymous')
	# 	continue

		# session.quit()
		# print("\n\n\t [ ] Something went wrong please restart this application.")
		# input()

# session.quit()



"""
# all_threads=[]
for files in all_pics:
	# x = threading.Thread(target=file_retrival, args=(files,))
	# all_threads.append(x)
	# x.start()
	# time.sleep(1)
	file_retrival(files)
	pass
"""

# for th in all_threads:
# 	th.join()

# print("[ ] Captured required images !")
# input("press enter")




# input()