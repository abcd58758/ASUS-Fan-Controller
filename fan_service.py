#!/usr/bin/python
import api, time

hot = 0
api.wpwm("2")
while(1):
    if api.temp() > 70 and hot == 0:
        api.wfan("255")
        hot = 1
        print("hot")
    elif api.temp() <= 60 and hot == 1:
        api.wpwm("2")
        hot = 0
        print("cold")
    else: print("wait")
    time.sleep(5)
