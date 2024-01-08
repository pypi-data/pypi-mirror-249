import json


class cls_aide_dao_model:
	def __init__(self, new_pure_db_table_name: str, new_pure_col_name: str,
				 new_mask_name: str = None,
				 new_map_code: str = None, list_map_code: list = None,
				 new_value=None,
				 new_default_value=None,
				 is_key: bool = False, not_null: bool = False, dict0: dict = None):

		if new_pure_db_table_name.find('"') == 2:
			self.__my_pure_db_table_name = new_pure_db_table_name.replace('"', '')
		else:
			self.__my_pure_db_table_name = new_pure_db_table_name

		if new_pure_col_name.find('"') == 2:
			self.__my_pure_col_name = new_pure_col_name.replace('"', '')
		else:
			self.__my_pure_col_name = new_pure_col_name

		if new_mask_name is None:
			self.__my_mask_code = self.__my_pure_col_name
		else:
			self.__my_mask_code = new_mask_name

		if new_map_code is None:
			self.__my_map_code = self.__my_pure_col_name
		else:
			self.__my_map_code = new_map_code

		if list_map_code is None:
			pass
		else:
			list_map_code.append(new_map_code)

		if new_default_value is None:
			self.__my_default_value = None
		else:
			self.__my_default_value = self.__reform_str_value_sql(new_default_value)

		self.__my_value = self.__reform_str_value_sql(new_value)

		self.__is_key = is_key

		if self.__is_key is True:
			self.__not_null = self.__is_key
		else:
			self.__not_null = not_null

		if dict0 is None:
			pass
		else:
			dict0[self.__my_pure_col_name] = {"is_key": self.__is_key,
											  "not_null": self.__not_null,
											  "value": self.__my_value,
											  "map_code": self.__my_map_code,
											  "mask_name": self.__my_mask_code}

	@property
	def name_db_full(self):
		return str(self.__my_pure_db_table_name) + '.' + '"' + str(self.__my_pure_col_name) + '"'

	@property
	def name_db(self):
		return '"' + str(self.__my_pure_col_name) + '"'

	@property
	def name(self):
		return self.__my_pure_col_name

	@property
	def value(self):
		return self.__my_value

	def set_value(self, my_value, dict0: dict = None, is_key: bool = False):
		self.__my_value = self.__reform_str_value_sql(my_value)

		if is_key is False:
			pass
		else:
			self.__is_key = is_key

		if dict0 is None:
			pass
		else:
			dict0[self.__my_pure_col_name]["value"] = self.__my_value
			dict0[self.__my_pure_col_name]["is_key"] = self.__is_key

	@property
	def is_key(self):
		return self.__my_value

	def set_is_key(self, my_value, dict0: dict = None):
		self.__my_value = self.__reform_str_value_sql(my_value)
		if dict0 is None:
			pass
		else:
			dict0[self.__my_pure_col_name]["is_key"] = self.__my_value

	@property
	def mask_code(self):
		return self.__my_mask_code

	def set_mask_code(self, my_code):
		self.__my_mask_code = my_code

	@property
	def map_code(self):
		return self.__my_map_code

	def set_map_code(self, my_code):
		self.__my_map_code = my_code

	def default_value(self):
		return self.__my_default_value

	def set_default_value(self, new_default_value):
		self.__my_default_value = self.__reform_str_value(new_default_value)

	def set(self, my_value):
		if isinstance(my_value, type(None)) is True:
			my_value = str('NULL')
		elif isinstance(my_value, int) is True:
			pass
		elif isinstance(my_value, dict) is True:
			my_value = json.dumps(my_value)
			my_value = f"'{my_value}'"
		elif my_value[0:2] == "@#":
			my_value = my_value[2:len(my_value)]
		elif (isinstance(my_value, str) is True and my_value.isdigit() is False) or my_value == '':
			my_value = my_value.replace("'", "''")
			my_value = "'" + my_value + "'"
		else:
			my_value = str(my_value)

		col = self.name_db_full
		val = my_value
		my_dict = {col: val}
		return my_dict

	def insert(self, my_value):
		return self.set(my_value)

	def insert_sql(self, my_sql):
		return self.set(f"@#{my_sql}")

	def insert_by_mapcode(self, my_dict: dict, level_2_key: str = None):
		if my_dict.__contains__(self.map_code):
			my_value = my_dict[self.map_code]
			if isinstance(my_value, dict) and level_2_key is not None:
				if my_value.__contains__(level_2_key):
					my_value = my_value[level_2_key]
				else:
					pass
			else:
				pass
		else:
			my_value = None
		return self.set(my_value)

	###############################################################
	@staticmethod
	def __reform_str_value_sql(new_value: str):
		if new_value is None:
			return "NULL"
		else:
			if isinstance(new_value, int):
				return new_value
			else:
				if isinstance(new_value, str):
					if new_value[0:2] == "@#":
						return new_value[2:]
					elif new_value[:1] == "'" and new_value[-1:] == "'":
						return new_value
					else:
						return "'" + new_value + "'"
				else:
					return "'" + str(new_value) + "'"

	@staticmethod
	def __reform_str_value_sub(new_value, force: bool = False):
		if new_value is None:
			return "NULL"
		elif isinstance(new_value, int):
			return new_value
		elif force is True:
			return "'" + new_value + "'"
		elif new_value[:1] == "'" and new_value[-1:] == "'":
			return new_value
		else:
			return "'" + new_value + "'"

	def __reform_str_value2(self, my_value):
		if my_value.find(",") > 0:
			list_my_value = str(my_value).split(",")
			is_correct = True
			for item in list_my_value:
				if item.isalnum():
					pass
				elif item[:1] == "'" and item[-1:] == "'":
					pass
				else:
					is_correct = False

			if is_correct is True:
				pass
			else:
				my_value = self.__reform_str_value_sub(my_value)
		else:
			my_value = self.__reform_str_value_sub(my_value)
		return my_value

	@staticmethod
	def __reform_str_value(my_value):
		if isinstance(my_value, str):
			if my_value == "":
				my_value = "'" + my_value + "'"
			else:
				if my_value[0] == "'" and my_value[-1] == "'":
					max_len = len(my_value)
					max_len_1 = max_len - 1
					my_value = my_value[0] + my_value[1:max_len_1].replace("'", "''") + my_value[-1]
				else:
					my_value = my_value.replace("'", "''")
					my_value = "'" + my_value + "'"
		else:
			my_value = str(my_value)
		return my_value

	# Chr（10）：ASCII码中的换行键，相当于vbLF。
	# Chr（13）：ASCII码中的回车键，相当于vbCR。
	next_row = ' CHR(13)||CHR(10) '

	next_two_row = ' CHR(10)||CHR(13) '

	current_time = "CURRENT TIMESTAMP"

	@staticmethod
	def timestamp_gmt0():
		sql_timestamp = "TIMESTAMP (CURRENT TIMESTAMP - (CURRENT TIMEZONE * 0.36)SECONDS)"
		return sql_timestamp

	@staticmethod
	def date_gmt0():
		return "DATE(" + cls_aide_dao_model.timestamp_gmt0() + ")"

	@staticmethod
	def timestamp_gmt0_char():
		sql_timestamp = "TIMESTAMP (CURRENT TIMESTAMP - (CURRENT TIMEZONE * 0.36)SECONDS)"
		sql_timestamp = "TO_CHAR(" + sql_timestamp + ", 'yyyy-mm-dd hh24:mi:ss.nnnnnn')"
		return sql_timestamp

	@staticmethod
	def date_gmt0_char():
		return "DATE(" + cls_aide_dao_model.timestamp_gmt0_char() + ")"

	def length_BE(self, length: int, trim: bool = True, rm_string: str = "%"):
		sql = None
		if rm_string is None:
			pass
		else:
			sql = f"REPLACE({self.name_db_full},'{rm_string}','')"

		if trim is False:
			sql = f"LENGTH({sql}) >= {length}"
		else:
			sql = f"LENGTH(TRIM({sql})) >= {length}"

		return sql

	@property
	def is_null(self):
		return self.name_db_full + ' IS NULL '

	@property
	def is_not_null(self):
		return self.name_db_full + ' IS NOT NULL '

	def iss(self, my_value):
		return self.name_db_full + ' IS ' + str(my_value)

	def iss_not(self, my_value):
		return self.name_db_full + ' IS NOT ' + str(my_value)

	def append_sql(self, new_sql):
		return self.append(new_sql=new_sql)

	def append(self, new_str: str = None, split_key: str = next_row, new_sql: str = None):

		if split_key is None and new_str is None and new_sql is None:
			return self.name_db_full + ' = ' + self.name_db_full

		new_value = self.name_db_full

		if new_str is None:
			pass
		else:
			new_value = "'" + new_str + "'"

		if new_sql is None:
			pass
		else:
			new_value = new_sql

		sql = "(CASE WHEN " + self.name_db_full + ' IS NULL '
		sql = sql + " THEN " + new_value
		sql = sql + " ELSE " + self.name_db_full + "|| " + split_key + "||" + new_value
		sql = sql + " END)"
		return self.name_db_full + ' = ' + sql

	def equate_sql(self, my_value):
		return self.name_db_full + ' = ' + str(my_value)

	def not_equate_sql(self, my_value):
		return self.name_db_full + ' <> ' + str(my_value)

	def not_equate(self, my_value, match_case: bool = True):
		return self.equate(my_value, match_case=match_case, do_not=True)

	def equate(self, my_value, match_case: bool = True, do_not: bool = False):
		if my_value is None:
			if do_not is True:
				return self.name_db_full + " IS NOT NULL "
			else:
				return self.name_db_full + " IS NULL "
		else:
			if do_not is True:
				operator = " <> "
			else:
				operator = " = "

			if match_case is True:
				left = self.name_db_full
				right = self.__reform_str_value(my_value)
			else:
				left = "UCASE(" + self.name_db_full + ")"
				right = "UCASE(" + self.__reform_str_value(my_value) + ")"

			return left + operator + right

	def equate_ucase(self, my_value):
		if my_value is None:
			return self.name_db_full + " IS NULL "
		else:
			return "UCASE(" + self.name_db_full + ') = UCASE(' + self.__reform_str_value(my_value) + ')'

	@staticmethod
	def to_date_col(my_value):
		return "TO_DATE(" + my_value + " , 'yyyy-mm-dd hh24:mi:ss')"

	@staticmethod
	def to_date_str(my_value):
		return "TO_DATE('" + my_value + "' , 'yyyy-mm-dd hh24:mi:ss')"

	def compare(self, operator, my_value, is_time: bool = False):
		if is_time is True:
			return self.to_date_col(self.name_db_full) + ' ' + operator + ' ' + self.to_date_str(str(my_value))
		else:
			return self.name_db_full + ' ' + operator + ' ' + str(my_value)

	def bigger(self, my_value, is_time: bool = False):
		return self.compare(">", my_value, is_time)

	def bigger_equ(self, my_value, is_time: bool = False):
		return self.compare(">=", my_value, is_time)

	def smaller(self, my_value, is_time: bool = False):
		return self.compare("<", my_value, is_time)

	def smaller_equ(self, my_value, is_time: bool = False):
		return self.compare("<=", my_value, is_time)

	def inn(self, my_value):
		if my_value is None:
			return self.name_db_full + " IS NULL "
		else:
			return self.name_db_full + " IN " + "(" + self.__reform_str_value2(str(my_value)) + ")"

	def inn_sql(self, my_value):
		return self.name_db_full + " IN " + "(" + str(my_value) + ")"

	def not_in_sql(self, my_value):
		return self.name_db_full + " NOT IN " + "(" + str(my_value) + ")"

	def not_in(self, my_value):
		return self.name_db_full + " NOT IN " + "(" + self.__reform_str_value2(my_value) + ")"

	def set_in(self, my_value):
		return self.inn(my_value)

	def like_ucase(self, my_value, inversion: bool = False, do_not: bool = False):
		return self.like_affix(None, my_value, None, ucase=True, inversion=inversion, do_not=do_not)

	# return "UCASE(" + self.name_db_full + ') LIKE UCASE(' + self.__reform_str_value(my_value) + ')'

	def like_affix(self, prefix_key, my_value: str, suffix_key, ucase: bool = False, inversion: bool = False,
				   do_not: bool = False, is_sql: bool = False):

		if do_not is True:
			operator = " NOT LIKE "
		else:
			operator = " LIKE "

		# print("#####", "like_affix")
		if is_sql is True:
			db_value = self.name_db_full
			my_value = my_value
		else:
			if ucase is True:
				db_value = "UCASE(" + self.name_db_full + ")"
				my_value = "UCASE(" + self.__reform_str_value(my_value) + ")"
			else:
				db_value = self.name_db_full
				my_value = self.__reform_str_value(my_value)

		if prefix_key is None and suffix_key is None:
			if inversion is False:
				if my_value[0:1] != "%" and my_value[-2:-1] != "%":
					my_value = "'%'||" + my_value + "||'%'"
				else:
					pass
				return db_value + operator + my_value
			else:
				return my_value + operator + "'%'||" + db_value + "||'%'"

		else:
			if prefix_key is None:
				prefix_key = ""
			elif prefix_key[0:1] == "%":
				prefix_key = "'" + prefix_key + "'"
			else:
				prefix_key = "'" + "%" + prefix_key + "'"

			if suffix_key is None:
				suffix_key = ""
			elif suffix_key[:-1] == "%":
				suffix_key = "'" + suffix_key + "'"
			else:
				suffix_key = "'" + suffix_key + "%" + "'"

			if inversion is False:
				return prefix_key + " || " + db_value + " || " + suffix_key \
					   + operator \
					   + prefix_key + " || " + my_value + " || " + suffix_key
			else:
				return prefix_key + " || " + my_value + " || " + suffix_key \
					   + operator \
					   + prefix_key + " || " + db_value + " || " + suffix_key

	def like(self, my_value, ucase: bool = False, inversion: bool = False, do_not: bool = False):
		# print("##### inversion like")
		# print(inversion)
		# print(self.name_db_full)
		# return self.name_db_full + " LIKE " + self.__reform_str_value(my_value)
		return self.like_affix(None, my_value, None, ucase=ucase, inversion=inversion, do_not=do_not)

	def like_prefix(self, prefix_key, my_value, ucase: bool = False, inversion: bool = False, do_not: bool = False):
		# print("##### inversion like_prefix")
		# print(inversion)
		return self.like_affix(prefix_key, my_value, None, ucase=ucase, inversion=inversion, do_not=do_not)

	def like_suffix(self, my_value, suffix_key, ucase: bool = False, inversion: bool = False, do_not: bool = False):
		# print("##### inversion like_suffix")
		# print(inversion)

		return self.like_affix(None, my_value, suffix_key, ucase=ucase, inversion=inversion, do_not=do_not)

	def start_with_sql(self, my_value):
		return "LOCATE(" + my_value + "," + self.name_db_full + ")=1"

	def not_start_with_sql(self, my_value):
		return "LOCATE(" + my_value + "," + self.name_db_full + ")<>1"

	def start_with(self, my_value):
		my_value = self.__reform_str_value(my_value)
		return self.start_with_sql(my_value)

	def not_start_with(self, my_value):
		my_value = self.__reform_str_value(my_value)
		return self.not_start_with_sql(my_value)

	def end_with_sql(self, my_value):
		my_locate = "(LOCATE(" + my_value + "," + self.name_db_full + ")"
		length = my_locate + "-1 + LENGTH(" + my_value + "))=LENGTH(" + self.name_db_full + ")"
		return my_locate + ">0" + " AND " + length

	def end_with(self, my_value):
		my_value = self.__reform_str_value(my_value)
		return self.end_with_sql(my_value)

	# Base
	def contain_sql(self, my_value, do_not: bool = False, case_sensitive: bool = True, split_key: str = None):
		if case_sensitive is True:
			my_value = my_value
			db_value = self.name_db_full
		else:
			my_value = "UCASE(" + my_value + ")"
			db_value = "UCASE(" + self.name_db_full + ")"

		if split_key is not None:
			my_value = f" '{split_key}' ||{my_value} || '{split_key}'"
			db_value = f" '{split_key}' ||{db_value} || '{split_key}'"
		else:
			pass

		if do_not is True:
			return "LOCATE(" + my_value + "," + db_value + ")=0"
		else:
			return "LOCATE(" + my_value + "," + db_value + ")>0"

	def not_contain_sql(self, my_value, case_sensitive: bool = True, split_key: str = None):
		return self.contain_sql(my_value=my_value,
								do_not=True,
								case_sensitive=case_sensitive,
								split_key=split_key)

	def contain(self, my_value, do_not: bool = False, case_sensitive: bool = True, split_key: str = None):
		my_value = self.__reform_str_value(my_value)
		return self.contain_sql(my_value=my_value,
								do_not=do_not,
								case_sensitive=case_sensitive,
								split_key=split_key)

	def not_contain(self, my_value, case_sensitive: bool = True, split_key: str = None):
		return self.contain(my_value=my_value,
							do_not=True,
							case_sensitive=case_sensitive,
							split_key=split_key)

	def has(self, my_value, do_not: bool = False):
		if do_not is False:
			return "',' || " + self.name_db_full + "||','" + " LIKE " \
				   + "','||" + self.__reform_str_value_sql(my_value) + "|| ','"
		else:
			return "',' || " + self.name_db_full + "||','" + " NOT LIKE " \
				   + "','||" + self.__reform_str_value_sql(my_value) + "|| ','"
