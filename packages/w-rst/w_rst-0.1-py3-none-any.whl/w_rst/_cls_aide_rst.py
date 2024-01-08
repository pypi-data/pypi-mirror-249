import datetime


class _cls_aide_rst_base:
	def __init__(self, module: str):
		self.__dict_rst = {"state": False,
						   "msg": None,
						   "data": None,
						   "dur": None,
						   'process': None,
						   'module': module}

		self.start_time = None

	@staticmethod
	def now():
		return datetime.datetime.now()

	@property
	def dur(self,
			my_time_earlier: datetime.datetime = None,
			my_time_later: datetime.datetime = None):

		if my_time_later is None:
			my_time_later = datetime.datetime.now()
		else:
			pass

		if my_time_earlier is None:
			if isinstance(self.start_time, datetime.datetime):
				my_time_earlier = self.start_time
			else:
				return None
		else:
			pass

		diff_second = (my_time_later - my_time_earlier).seconds

		return diff_second

	@staticmethod
	def __get_dict_value(my_dict_rst, my_key):
		if my_dict_rst.__contains__(my_key):
			return my_dict_rst[my_key]
		else:
			return None

	@property
	def state(self):
		return self.__get_dict_value(self.__dict_rst, "state")

	def set_state(self, new_state: bool = False):
		self.__dict_rst["state"] = new_state

	@property
	def msg(self):
		return self.__get_dict_value(self.__dict_rst, "msg")

	def set_msg(self, new_msg: object = None):
		self.__dict_rst["msg"] = new_msg

	@property
	def data(self):
		return self.__get_dict_value(self.__dict_rst, "data")

	def set_data(self, new_data: object = None):
		self.__dict_rst["data"] = new_data

	@property
	def process(self):
		return self.__get_dict_value(self.__dict_rst, "process")

	def set_process(self, new_process_name: str = None):
		self.__dict_rst["process"] = new_process_name

	@property
	def all(self):
		return self.__dict_rst

	def set(self, new_state, new_msg, new_data: object = None, new_process: str = None):
		self.set_state(new_state)
		self.set_msg(new_msg)
		self.set_data(new_data)
		if new_process is not None:
			self.set_process(new_process)
		else:
			pass

