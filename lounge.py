#!/usr/bin/env python3
import json
import requests
import sys

key = "FVRighYFcjsFtyvZPWipiTK6VAoGnaX3wLt2d2N7MEgPPeB9qC"
basedata = {"token":{"id":key},}
head = {'Content-Type': 'application/json'}


def lightcontrol(args, basedata):
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


def usage():
    print('''
Usage: lounge (destination) (function) (argument)
Following this chart
Destination     Function        Argument
projector
                status
                power
                                on
                                off
                input
                                composite
                                comp1
                                comp2
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
                                off
    ''')
    sys.exit()


def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        usage()

    if sys.argv[1]=="lights":
        basedata['lights'] = dict()
        lightcontrol(sys.argv, basedata)
        encod = json.dumps(basedata)
        r = requests.put('http://aforargroom.csh.rit.edu:5000/lounge/lights', data = encod, headers = head)
    else:
        usage()

    if r.status_code == 200:
        print("Success")
    else:
        print("Fail, status code %d" % r.status_code)


if __name__ == "__main__" :
    main()
