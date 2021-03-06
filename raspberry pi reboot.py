import RPi.GPIO as GPIO
import os
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)

public_ips = ['8.8.8.8', '8.8.4.4', '208.67.222.222', '4.2.2.2', '1.1.1.1']


while True:
	GPIO.output(11,GPIO.HIGH)
	response = os.system("ping -c 1 " + "10.0.10.1") # re-enable in future and add failure logic
	if response == 0:  #re-enable in future and add failure logic
			list = []
			for ip in public_ips:
					response = os.system("ping -c 1 " + ip)
					time.sleep(1)
					list.append(response)
			if 0 in list:
					list.clear()
					print("Could reach an IP - Restarting Loop")
					continue
			else:
					list.clear()
					print("Could not reach an IP - Waiting 15 seconds to test again")
					time.sleep(15)
					while True: #TRY TO PING AGAIN. If fails, kill power
							print("Starting to ping again")
							list = []
							for ip in public_ips:
									response = os.system("ping -c 1 " + ip)
									list.append(response)
							if 0 in list:
									list.clear()
									print("Ping #2 successful - breaking loop")
									break
							else:
									print("Could not ping after #2 attempt - removing power")
									GPIO.output(11,GPIO.LOW) #CHANGE BACK AFTER TO HIGH
									#write to file the time and have another script running that will email files up when it detects them
									print("Waiting 150 seconds")
									time.sleep(15) #- wait 2.5 mins with modem off
									GPIO.output(11,GPIO.HIGH) #CHANGE BACK TO LOW AFTER - brings device back online
									print("Power re-applied - waiting 450 seconds")
									time.sleep(45) #- wait 5 to 10 mins? then try to ping again. If can ping, BREAK
									print("Trying to ping again after power removed and restored")
									list = []
									for ip in public_ips:
											response = os.system("ping -c 1 " + ip)
											list.append(response)
									if 0 in list:
											print("Ping was successful after reboot - breaking loop")
											list.clear()
											break
									else:
											print("Ping after reboot unsuccessful - removing power again for continuous loop")
											while True: #FIX THE TIM HERE TO power down 2.5 mins and want 7.5 - BUT EVERY 30 MINS
													GPIO.output(11,GPIO.LOW) #CHANGE BACK AFTER TO HIGH
													print("Waiting for 150 seconds again")
													time.sleep(15)
													GPIO.output(11,GPIO.HIGH) #CHANGE BACK TO LOW AFTER - brings device back online
													print("Power re-applied AGAIN - waiting 450 seconds")
													time.sleep(45) #- wait 5 to 10 mins? then try to ping again. If can ping, BREAK
													list = []
													for ip in public_ips:
															response = os.system("ping -c 1 " + ip)
															list.append(response)
													if 0 in list:
															list.clear()
															print("After X reboot we can ping again - breaking continuous loop") #add a counter here so $
															break
													else:
															print("Still cannot ping after x reboot - continuing power cycle loop")
															list.clear()
															time.sleep(15) #change to 1500 seconds or around 30 mins after
															continue
									#if can't ping power off device for 5 mins, then let boot for 10
									#if still can't ping then kill power every 30 mins, then have it boot for 10 then test again
	else:
			print("CANNOT REACH GATEWAY")
