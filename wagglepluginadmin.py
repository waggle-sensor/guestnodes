#!/usr/bin/env python3

import sys
import subprocess
import argparse
from tabulate import tabulate

def waggle_help():
	print("Usage: wagglepluginadmin COMMAND [OPTIONS]")
	print("COMMANDS")
	print("    list: list of the waggle plugins")
	print("   start: start waggle plugin(s)")
	print("          options")
	print("              all: start all the plugins detected by systemd")
	print("        # or name: start the plugin in the list")
	print("   stop: stop waggle plugin(s)")
	print("          options")
	print("              all: stop all the plugins detected by systemd")
	print("        # or name: stop the plugin in the list")
	print("   help: print help page")
	print("   exit: terminate the program")

def do_command_output(cmd):
	try:
		ret, output = subprocess.getstatusoutput(cmd)
		if ret != 0:
			return []
		return output.split('\n')
	except AttributeError:
		print("The system does not support the command %s" % cmd)
	return []

def do_command(cmd):
	try:
		ret = subprocess.run(cmd.split())
		return ret.returncode
	except AttributeError:
		print("The system does not support the command %s" % cmd)
	return -1

def get_all_plugins():
	CMD = 'systemctl list-unit-files waggle-plugin-* | grep waggle-plugin-'
	result = do_command_output(CMD)
	plugins = {}
	for unit in result:
		sp = unit.strip().split()
		plugins[sp[0]] = [sp[1]]
	return plugins

def get_all_plugin_status():
	CMD = 'systemctl --all list-units waggle-plugin-* | grep waggle-plugin-'
	result = do_command_output(CMD)
	plugins = {}
	for unit in result:
		sp = unit.strip().split()
		sp[4] = ' '.join(sp[4:])
		sp = sp[:5]
		plugins[sp[0]] = sp[1:]
	return plugins

class PluginManager(object):
	def __init__(self):
		self.plugins = {}
		self.commands = {
			'list' : self.print_list,
			'start' : self.start_plugin,
			'stop' : self.stop_plugin,
			'enable' : self.enable_plugin,
			'disable' : self.disable_plugin,
			'help' : self.print_help
		}

	def print_base(self):
		ret, msg = self.print_list([])

	def print_list(self, arg):
		p1 = get_all_plugins()
		p2 = get_all_plugin_status()
		for plugin_name in p1:
			info_list = p1[plugin_name]
			if plugin_name in p2:
				info_list.extend(p2[plugin_name])
			else:
				info_list.extend(['-', '-', '-', '-'])
			p1[plugin_name] = info_list
		
		items = []
		self.plugins.clear()
		for plugin_name in p1:
			idx = len(self.plugins)
			value = p1[plugin_name]
			value.insert(0, plugin_name)
			self.plugins[idx] = value
			value.insert(0, idx)
			items.append(value) 
		headers = ['INDEX', 'PLUGIN', 'STATE', 'LOAD', 'ACTIVE', 'SUB', 'DESCRIPTION']
		print(tabulate(items, headers, tablefmt="psql"))
		return True, ''

	def get_plugin_name(self, arg):
		list = []
		if arg[0] == 'all' or arg[0] == 'All':
			arg = range(0, len(self.plugins))

		for plugin in arg:
			if isinstance(plugin, int):
				plugin = self.plugins[plugin][1]
			elif plugin.isdigit():
				plugin = self.plugins[int(plugin)][1]
			list.append(plugin)
		return list

	def start_plugin(self, arg):
		if arg == []:
			return False, 'invalid argument'
		plugin_list = self.get_plugin_name(arg)
		CMD = 'systemctl start %s' % ' '.join(plugin_list)
		ret = do_command(CMD)
		if ret != 0:
			print('Coult not start the plugin %s' % plugin)
		return True, ''


	def stop_plugin(self, arg):
		if arg == []:
			return False, 'invalid argument'
		plugin_list = self.get_plugin_name(arg)
		CMD = 'systemctl stop %s' % ' '.join(plugin_list)
		ret = do_command(CMD)
		if ret != 0:
			print('Could not stop the plugin %s' % plugin)
		return True, ''

	def enable_plugin(self, arg):
		if arg == []:
			return False, 'invalid argument'
		plugin_list = self.get_plugin_name(arg)
		CMD = 'systemctl enable %s' % ' '.join(plugin_list)
		ret = do_command(CMD)
		if ret != 0:
			print('Could not enable the plugin %s' % plugin)
		return True, ''

	def disable_plugin(self, arg):
		if arg == []:
			return False, 'invalid argument'
		plugin_list = self.get_plugin_name(arg)
		CMD = 'systemctl disable %s' % ' '.join(plugin_list)
		ret = do_command(CMD)
		if ret != 0:
			print('Could not disable the plugin %s' % plugin)
		return True, ''

	def print_help(self, arg):
		waggle_help()
		return True, ''

	def execute_command(self, cmd, args):
		try:
			func = self.commands[cmd]
			ret, msg = func(args)
			if not ret:
				print(msg)
		except Exception as e:
			print("command execution error %s" % str(e))


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('commands',nargs='*')
	args = parser.parse_args()

	pm = PluginManager()

	if args.commands:
		cmd = args.commands[0]
		arg = args.commands[1:]
		for unit in arg:
			if unit.isdigit():
				print("Please use interactive session or enter name of the plugin")
				sys.exit(1)
		func = pm.commands[cmd]
		ret, msg = func(arg)
		sys.exit(1)

	while True:
		try:
			pm.print_base()
			line = input("Enter Command:")
			if line == '':
				continue
			if line == 'exit':
				print("bye...")
				sys.exit(1)
			cmd = line.split()[0]
			args = line.split()[1:]
			if cmd == 'list':
				continue
			pm.execute_command(cmd, args)
		except KeyError:
			print_help()
		except KeyboardInterrupt:
			print("leaving...")
			sys.exit(1)
		except Exception as e:
			print("Error occurred %s" % str(e))
