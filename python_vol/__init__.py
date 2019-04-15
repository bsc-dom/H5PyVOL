from .abstract import H5Object, H5Dataset, H5Group, H5File, H5VOL

class Object(H5Object):
	def __init__(self, name: str):
		self.name: str = name
		self.open: bool = True

	def H5VL_python_object_close(self, dxpl_id, req):
		self.open = False

class Dataset(H5Dataset, Object):
	def __init__(self, name: str, array: list):
		Object.__init__(self, name)
		self.array: list = array

	def H5VL_python_dataset_read(self, mem_type_id, mem_space_id, file_space_id, xfer_plist_id, req):
		print('Reading dataset ' + self.name + ' = ' + str(self.array))
		return self.array

	def H5VL_python_dataset_write(self, mem_type_id, mem_space_id, file_space_id, xfer_plist_id, buf, req):
		print('Writing dataset ' + self.name + ' = ' + str(buf))
		self.array = buf

class Group(H5Group, Object):
	def __init__(self, name: str):
		Object.__init__(self, name)
		self.groups: dict = {}
		self.datasets: dict = {}

	def H5VL_python_dataset_create(self, loc_params, name: str, dcpl_id, dapl_id, dxpl_id, req) -> Dataset:
		print('Creating dataset ' + name)
		dataset = Dataset(name, None)
		self.datasets[name] = dataset
		return dataset

class File(H5File, Object):
	def __init__(self, name: str):
		Object.__init__(self, name)
		self.groups: dict = {'/': Group('/')}

	def H5VL_python_group_create(self, loc_params, name: str, gcpl_id, gapl_id, dxpl_id, req) -> Group:
		print('Creating group ' + name)
		group = Group(name)
		self.groups[name] = group
		return group

	def H5VL_python_group_open(self, name: str, flags, fapl_id, dxpl_id, req) -> Group:
		print('Opening group ' + name)
		return self.groups[name]

class VOL(H5VOL):
	def __init__(self):
		self.files: dict = {}

	def H5VL_python_file_create(self, name: str, flags, fcpl_id, fapl_id, dxpl_id, req) -> File:
		print('Creating file ' + name)
		new_file = File(name)
		self.files[name] = new_file
		return new_file
