if __name__ == '__main__':
	while True:
		start = int(input('Enter the start number: '))
		end = int(input('Enter the end number: '))
		splt = int(input('Enter how many you want to run each time: '))
		result = input('Do you want to start from {} and end at {} and run {} each time, type in [y/n]: '.format(start,end,splt))
		if result == 'y':
			break
		else:
			pass
	with open ('input_list.txt','w') as f:
		f.close()
	for i in range(start,end,splt):
		with open ('input_list.txt','a') as f:
			f.write('{},{}\n'.format(i,i+splt))
			f.close()
