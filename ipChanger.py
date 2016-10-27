# -*- coding: utf-8 -*-
#
# FileName		: ipChanger.py
# Description		: 公司内网自动寻找一个可用IP
# Version		: 0.1 beta
# Date			: 2016-10-27
# Thank			: http://blog.sina.com.cn/s/blog_62c02a630100lyuk.html
#
import os,sys,wmi,time
wmiService = wmi.WMI()
nicConfigs = wmiService.Win32_NetworkAdapterConfiguration(IPEnabled = True)
nicConfigsAll = wmiService.Win32_NetworkAdapterConfiguration()
def view(nicConfigs):
	for objNicConfig in nicConfigs:
		print (objNicConfig.Description,":",objNicConfig.SettingID)

def set_ip(nicConfig,showResult=True):
	found,intReboot = False,0
	for objNicConfig in nicConfigsAll:
		if objNicConfig.SettingID == nicConfig[0]:
			found = True;
			returnValue = objNicConfig.EnableStatic(IPAddress = [nicConfig[1]], SubnetMask = [nicConfig[2]])
			if returnValue[0] == 0:
				print ('设置IP成功')
			elif returnValue[0] == 1:
				print ('设置IP成功')
				intReboot += 1
			else:
				print ('修改IP失败: IP设置发生错误')
				exit()
			returnValue = objNicConfig.SetGateways(DefaultIPGateway = [nicConfig[3]], GatewayCostMetric = [1])
			if returnValue[0] == 0:
				print ('设置网关成功')
			elif returnValue[0] == 1:
				print ('设置网关成功')
				intReboot += 1
			else:
				print ('修改IP失败: 网关设置发生错误')
				exit()
			returnValue = objNicConfig.SetDNSServerSearchOrder(DNSServerSearchOrder = [nicConfig[4],nicConfig[5]])
			if returnValue[0] == 0:
				print ('设置DNS成功')
			elif returnValue[0] == 1:
				print ('设置DNS成功')
				intReboot += 1
			else:
				print ('修改IP失败: DNS设置发生错误')
				exit()
			if intReboot > 0:
				print ('需要重新启动计算机')
			else:
				if showResult:
					print ('')
					print ('修改后的配置为：')
					print ('IP: ', ', '.join(objNicConfig.IPAddress))
					print ('掩码: ', ', '.join(objNicConfig.IPSubnet))
					print ('网关: ', ', '.join(objNicConfig.DefaultIPGateway))
					print ('DNS: ', ', '.join(objNicConfig.DNSServerSearchOrder))
					print ('修改IP结束')
					return True
	if not found:
		print('找不到网卡: %s'%nicConfig[0])
		return False
def ping_server(server):
	result=os.system('ping '+server)
	if result:
		return True
	else:
		return False
def assign_ip(nicId,prefix,netmask,gateway,maindns,standbydns):
	if prefix[-1] != '.': prefix = prefix + '.'
	for x in range(2,253):
		tPrefix = prefix + str(x)
		print(tPrefix)
		nicConfig=[nicId,tPrefix,netmask,gateway,maindns,standbydns]
		set_ip(nicConfig,False)
		time.sleep(1)
		if ping_server(gateway):
			exit()
		else:
			pass
def argv_im(argvs):
	count = len (argvs)
	if count == 1:
		view(nicConfigs)
	elif count == 2:
		if (argvs[1] == '--list-all') or (argvs[1] == '-a') or (argvs[1] == '-all'):
			view(nicConfigsAll)
	elif count == 3:
		if (argvs[1] == '--auto-set') or (argvs[1] == '-as'):
			nicConfig = argvs[2:3:1]
			assign_ip(nicConfig[0],nicConfig[1])
	else:
		if (argvs[1] == '--set-ip') or (argvs[1] == '-s'):
			nicConfig = argvs[2:8:1]
			set_ip(nicConfig)
		else:
			argvstr = ""
			for argv in argvs:
				argvstr += argv + " "
			print ("参数非法:",argvstr)
#assign_ip({ACC6132D-9D52-4426-AF86-2E57824CEB1F},'192.168.1','225.225.225.0','192.168.1.1','8.8.8.8','8.4.4.4')
argv_im(sys.argv)