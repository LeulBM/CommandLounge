#!/usr/bin/env python3
import json
import requests
import sys

# keyinfo is a .py file that defines a variable apikey
import keyinfo


# create necessary header and empty JSON body for HTTP request
basedata = {"token":{"id":keyinfo.apikey},}
head = {'Content-Type': 'application/json'}


# main flow of program
def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        usage()

    if sys.argv[1]=="lights":
        basedata['lights'] = dict()
        light_control(sys.argv, basedata)

    elif sys.argv[1] == "projector":
        projector_control(sys.argv, basedata)
    else:
        usage()


# given that sys.argv[1] is lights, this constructs basedata to be a light request with the rest ofthe arguments
def light_control(args, basedata):
    if len(args) != 4:
        usage()

    if args[2] == "l1":
        if args[3] == 'on':
            basedata['lights']["L1"] = True
        elif args[3] == 'off' :
            basedata['lights']["L1"] = False
        else:
            usage()

    elif args[2] == "l2":
        if args[3] == 'on':
            basedata['lights']["L2"] = True
        elif args[3] == 'off':
            basedata['lights']["L2"] = False
        else:
            usage()

    elif args[2] == 'both':
        if args[3] == 'on':
            basedata['lights']["L1"] = True
            basedata['lights']["L2"] = True
        elif args[3] == 'off':
            basedata['lights']["L1"] = False
            basedata['lights']["L2"] = False
        else:
            usage()

    else:
        usage()

    # basedata now contains full body, convert it to JSON, send the request, and save the response in r
    encod = json.dumps(basedata)
    r = requests.put('http://aforargroom.csh.rit.edu:5000/lounge/lights', data = encod, headers = head)

    check_exit_code(r)


def projector_control(args, basedata):
    if args[2] == "status":
        if len(args) == 4:
            usage()
        else:
            r=requests.get('http://lforlounge.csh.rit.edu:5000/lounge/projector')
            print(json.dumps(r.json(), sort_keys=True, indent = 4))

    elif len(args) != 4:
        usage()

    elif args[2] == "power":
        basedata['power'] = dict()
        if args[3] == "on":
            basedata['power']['state'] = True
        elif args[3] == "off":
            basedata['power']['state'] = False
        else:
            usage()
        encod = json.dumps(basedata)
        r = requests.put('http://lforlounge.csh.rit.edu:5000/lounge/projector/power', data = encod, headers = head)
        check_exit_code(r)

    elif args[2] == "input":
        basedata['input'] = dict()
        if args[3] == "hdmi1":
            basedata['input']['select'] = 'HDMI'
        elif args[3] == "hdmi2":
            basedata['input']['select'] = 'HDMI2'
        elif args[3] == 'component':
            basedata['input']['select'] = 'Component'
        elif args[3] == 'computer1':
            basedata['input']['select'] = 'Computer1'
        elif args[3] == 'computer2':
            basedata['input']['select'] = 'Computer2'
        else:
            usage()
        encod = json.dumps(basedata)
        r = requests.put('http://lforlounge.csh.rit.edu:5000/lounge/projector/input', data = encod, headers = head)
        check_exit_code(r)

    elif args[2] == "blank":
        basedata['blank'] = dict()
        if args[3] == "true":
            basedata['blank']['state'] = 'true'
        elif args[3] == 'false':
            basedata['blank']['state'] = 'false'
        else:
            usage()
        encod = json.dumps(basedata)
        r = requests.put('http://lforlounge.csh.rit.edu:5000/lounge/projector/blank', data = encod, headers = head)
        check_exit_code(r)





def check_exit_code(a):
    # 200 is the code for a successful HTTP request
    if a.status_code == 200:
        print("Success")
    # Any other response denotes failure, allow user to understand with the error code
    else:
        print("Failure, status code %d" % a.status_code)




# Called when improper arguments are passed, whether that is too many, too few, or plain
# wrong input is given. Gives guide to user and exits the program with sys.exit()
def usage():
    print('''Usage: lounge (destination) (function) (argument)
Following this chart
Destination     Function        Argument
projector
                status
                power
                                on
                                off
                input
                                component
                                computer1
                                computer2
                                hdmi1
                                hdmi2
                blank
                                true
                                false
reciever
                status
                input
                                hdmi1
                                hdmi2
                                hdmi3
                                hdmi4
                volume
                                1-127
                mute
                                true
                                false
lights
                l1
                                on
                                off
                l2
                                on
                                off
                both
                                on
                                off
radiator
                status
                fan
                                on
                                off''')
    sys.exit()


# Ensure that main is run when the program is made an executable
if __name__ == "__main__" :
    main()
