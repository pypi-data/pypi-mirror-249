# pip install psycopg2
import psycopg2

import datetime


class __cls_aide_rst_base:
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


class __cls_aide_sql_pgs:
	# noinspection PyMissingConstructor
	def __init__(self):
		pass

	@staticmethod
	def Chk(s: str):
		if s[0] != '"' and s[-1] != '"':
			return f'"{s}"'
		elif s[0] == '"' and s[-1] != '"':
			return f'{s}"'
		elif s[0] != '"' and s[-1] == '"':
			return f'"{s}'
		else:
			return s

	@property
	def _system_schemas(self):
		return "'pg_toast','pg_catalog','information_schema'"

	@property
	def _sql_list_activity_count(self):
		return "SELECT " \
			   + " count(*) FROM pg_stat_activity"

	def _sql_list_schemas(self, no_system_schemas: bool = True):
		sql = 'SELECT nspname AS schema_name ' + ' FROM pg_catalog.pg_namespace'

		if no_system_schemas is True:
			sql = f" {sql} WHERE nspname NOT IN ({self._system_schemas})"
		else:
			pass

		return sql

	def _sql_list_tables(self, schema_name: str):

		sql = 'SELECT nspname AS ' + self.Chk(schema_name) + ' FROM pg_catalog.pg_namespace;'

		return sql

	def _sql_list_all_tables(self, split_schema_table: bool = False, no_system_schemas: bool = True):
		if split_schema_table is True:
			sql = "SELECT " \
				  + " '\"' || table_schema || '\"' as table_schema ,'\"' || table_name || '\"'  as table_name " \
				  + " FROM information_schema.tables"
		else:
			sql = "SELECT " \
				  + " '\"' || table_schema || '\".\"'  || table_name || '\"'  as table_name " \
				  + " FROM information_schema.tables"

		if no_system_schemas is True:
			sql = f" {sql} WHERE table_schema NOT IN ({self._system_schemas})"
		else:
			pass

		return sql

	@staticmethod
	def _sql_list_table_structure(table_name: str):
		table_name = table_name.replace('"', '')

		if table_name.find("."):
			arr_table_name = table_name.split(".")
			table_schema = arr_table_name[0]
			table_name = arr_table_name[1]
		else:
			table_schema = None
			table_name = table_name

		sql = "SELECT *" \
			  + " FROM information_schema.columns " \
			  + f" WHERE table_name = '{table_name}'"

		if table_schema is None:
			pass
		else:
			sql = sql + f" AND table_schema = '{table_schema}'"

		return sql


class cls_pgs_conn(__cls_aide_rst_base, __cls_aide_sql_pgs):
	# noinspection PyMissingConstructor
	def __init__(self, host=None, port=None, database=None, user=None, password=None):
		self.rst = self._cls_aide_rst_base("pgs")

		self.__dirt_connection_info = {"host": None,
									   "port": None,
									   "database": None,
									   "user": None,
									   "password": None,
									   "connected": None,
									   "connected_time": None,
									   "SQL": None}

		self.conn = None

		if database is None:
			pass
		else:
			self.set_host(host)
			self.set_port(port)
			self.set_database(database)
			self.set_user(user)
			self.set_password(password)

			self.connect()

	@property
	def connection_info(self):
		return self.__dirt_connection_info

	@property
	def host(self):
		return self.__dirt_connection_info["host"]

	def set_host(self, new_value):
		self.__dirt_connection_info["host"] = new_value

	@property
	def port(self):
		return self.__dirt_connection_info["port"]

	def set_port(self, new_value):
		self.__dirt_connection_info["port"] = new_value

	@property
	def database(self):
		return self.__dirt_connection_info["database"]

	def set_database(self, new_value):
		self.__dirt_connection_info["database"] = new_value

	@property
	def user(self):
		return self.__dirt_connection_info["user"]

	def set_user(self, new_value):
		self.__dirt_connection_info["user"] = new_value

	@property
	def password(self):
		return self.__dirt_connection_info["password"]

	def set_password(self, new_value):
		self.__dirt_connection_info["password"] = new_value

	@property
	def connected(self):
		return self.__dirt_connection_info["connected"]

	def set_connected(self, new_value):
		if new_value is None:
			new_value = False
		else:
			pass

		self.__dirt_connection_info["connected"] = new_value

	@property
	def connected_time(self):
		return self.__dirt_connection_info["connected_time"]

	def set_connected_time(self, new_value):
		self.__dirt_connection_info["connected_time"] = new_value

	@property
	def SQL(self):
		return self.__dirt_connection_info["SQL"]

	def set_SQL(self, new_value):
		self.__dirt_connection_info["SQL"] = new_value

	def connect(self):
		self.rst.set_process("connect")
		try:
			self.set_connected(False)
			self.conn = psycopg2.connect(host=self.host, database=self.database, port=self.port, user=self.user,
										 password=self.password)

			self.set_connected(True)

			self.rst.set(self.connected,
						 f'Connected! Cost:{self.rst.dur}',
						 self.host)
		except Exception as e:

			if e:
				self.rst.set(False,
							 f'Exception:Connection failed! Cost:{self.rst.dur}',
							 e.__str__())
			else:
				self.rst.set(False,
							 f'DB ERROR:Connection failed! Cost:{self.rst.dur}',
							 f'DB error_log:######################')

	def disconnect(self):
		if self.connected is True:
			if self.connected is True:
				self.conn.close()
				self.set_connected(False)

	def __execute_sql_base__(self, sql, sql_type):
		self.rst.set_process(sql_type + "." + self.rst.process)

		self.set_SQL(sql)

		if self.connected is True:
			pass
		else:
			self.connect()
			if self.rst.state is False:
				return None

		self.rst.set(False, None, None)

		try:
			cur = self.conn.cursor()
			cur.execute(self.SQL)
			data = cur.fetchall()

			if sql_type == "SELECT":
				pass
				data_desc = cur.description
				data_header = [desc[0] for desc in data_desc]
				data_with_header = {i: dict(zip(data_header, row)) for i, row in enumerate(data)}
				data = data_with_header
			else:
				pass

			cur.close()

			self.rst.set(True,
						 f'{sql_type} successful!Cost:{self.rst.dur}',
						 data)
		except Exception as e:
			if e:
				self.rst.set(False,
							 'Exception:' + e.__str__().replace("'", "") + f',Cost:{self.rst.dur}',
							 sql)
			else:
				self.rst.set(False,
							 'DB ERROR:' + self.conn.stmt_errormsg() + f',Cost:{self.rst.dur}',
							 sql)
		return self.rst.state

	def __execute_sql(self, sql, sql_type):
		sql = sql.strip()
		if sql[0:6].upper() == sql_type.upper():
			self.__execute_sql_base__(sql, sql_type)
		else:
			self.rst.set(False, f'Only {sql_type} SQL can be execute!,Cost:{self.rst.dur}', sql)

	def select(self, sql):
		self.__execute_sql(sql, sql_type='SELECT')

	def insert(self, sql):
		self.__execute_sql(sql, sql_type="INSERT")

	def update(self, sql):
		self.__execute_sql(sql, sql_type='UPDATE')

	def delete(self, sql):
		self.__execute_sql(sql, sql_type='DELETE')

	def creat(self, sql):
		self.__execute_sql(sql, sql_type="CREATE")

	def load_activity_count(self):
		self.rst.set_process("load_activity_count")

		sql = self._sql_list_activity_count

		self.select(sql)

	def load_schemas(self, no_system_schemas: bool = True):
		self.rst.set_process("load_schemas")

		sql = self._sql_list_schemas(no_system_schemas=no_system_schemas)

		self.select(sql)

	def load_tables(self, schema_name):
		self.rst.set_process("load_tables")

		sql = self._sql_list_tables(schema_name=schema_name)

		self.select(sql)

	def load_all_tables(self, split_schema_table: bool = False, no_system_schemas: bool = True):
		self.rst.set_process("load_all_tables")

		sql = self._sql_list_all_tables(split_schema_table=split_schema_table, no_system_schemas=no_system_schemas)

		self.select(sql)

	def load_table_structure(self, table_name):
		self.rst.set_process("load_table_structure")

		sql = self._sql_list_table_structure(table_name=table_name)

		self.select(sql)
