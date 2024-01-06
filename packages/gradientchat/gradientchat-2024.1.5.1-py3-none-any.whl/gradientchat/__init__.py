__version__ = "2024.01.05.01"

class Bot:
	cli = __import__("socketio").Client()
	isConn = False
	cmds = []
	def __init__(self, usern, pref=None):
		if type(usern) != type(""):
			raise TypeError("Bot name must be a string")
		if type(pref) != type(""): pref = f"{usern[0].lower()}!"
		def setupCli():
			me = None
			@self.cli.on("connect")
			def onConn():
				self.cli.emit("auth", {"usern": usern})
			@self.cli.on("auth")
			def authHandle(aObj):
				nonlocal me
				if aObj["status"] != 0:
					raise Exception(f"Connection error, code {aObj['status']} message: {aObj['err']}") from None
				print("Connected!")
				me = aObj["me"]
				print(me)
			@self.cli.on("message")
			def onMsg(msg):
				print(locals())
				import html
				if msg["author"]["id"] == me["id"]: return
				msg["txt"] = html.unescape(msg["txt"])
				if not msg["txt"].startswith(pref): return
				msg["txt"] = msg["txt"][len(pref):].split(" ")
				for obj in self.cmds:
					if obj["name"] == msg["txt"][0]:
						break
					if id(obj) == id(self.cmds[-1]):
						if msg["txt"][0] == "help":
							res = ["Available commands:", ""]
							for c in self.cmds:
								res += f"\u00a0\u00a0\u00a0\u00a0- {c['name']}"
								if not c["func"].__doc__ is None: res[-1] += f" - {c['func'].__doc__}"
							return
						return self.sendMsg(f"Command \"{msg['txt'][0]}\" does not exist")
				try:
					sendMsg(obj["func"]())
				except:
					self.sendMsg(f"Error while executing \"{obj['name']}\":\n\n" + __import__("traceback").format_exc())
		setupCli()
	def cmd(self, arg=None):
		if self.isConn:
			raise TypeError("Cannot add commands when bot is connected")
		def decor(func):
			def wrapper(*args, **kwargs):
				result = func(*args, **kwargs)
				return result
			return wrapper
		if callable(arg):
			func = arg
			arg = func.__name__
			self.cmds.append({"name": arg, "func": func})
			return decor(func)
		self.cmds.append({"name": arg, "func": func})
		return decor
	def connect(self, servUrl=None):
		if self.isConn:
			raise Exception("Already connected")
		self.isConn = True
		try:
			self.cli.connect("https://gradientchat.glitch.me/" if type(servUrl) != type("") else servUrl)
		except BaseException as err:
			raise err from None
		self.cli.wait()
	def sendMsg(self, *msg):
		if not self.isConn:
			raise TypeError("Cannot send messages when bot isn't connected")
		self.cli.emit("message", " ".join(msg))