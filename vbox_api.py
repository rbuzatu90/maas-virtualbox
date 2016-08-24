#!/usr/bin/python
import flask
import os
import re
import subprocess
import sys

app = flask.Flask(__name__)

vbox_bin = "/usr/local/bin/VBoxManage"

def _get_matching_vmx_path(path, mac_address):
    propper_mac_address = mac_address.upper().replace(":", "")
    for root, dirs, file_names in os.walk(path):
        for file_name in file_names:
            if os.path.splitext(file_name)[1].lower() == '.vbox':
                vmx_path = os.path.join(root, file_name)
                with open(vmx_path, 'rb') as f:
                    for l in f:
                        if l.find(propper_mac_address) == -1:
                            return vmx_path

def _execute_process(args):
    p = subprocess.Popen(args,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=False)
    (out, err) = p.communicate()
    return (out, err, p.returncode)

@app.route('/vmrun/vm/status/<string:vm>',
           methods = ['GET'])
def get_vm_status(vm):
    running_vms = get_running_vms()
    vm_name = get_vm_bymac_address(vm)
    if vm_name not in running_vms:
        print "VM %s is off" %vm
        return "off"
    elif vm_name in running_vms:
        print "VM %s is running" %vm
        return "on"
    else:
        print "error"
        return "error"

@app.route('/vmrun/vm/find_by_mac_address/<string:mac_address>',
           methods = ['GET'])
def get_vm_bymac_address(mac_address):
    all_vms = get_all_vms()
    running_vms = get_running_vms()
    #print running_vms
    matched_vm = ''
    for vm in all_vms:
        args = [vbox_bin, "showvminfo"]
        args.append(vm)
        cmd = args
        vm_info = _execute_process(cmd)
        if vm_info[0].find(mac_address.replace(":", "").upper()) != -1:
            matched_vm = vm
            print "Matched VM: ", vm, matched_vm
    if not matched_vm:
        print "No VM found with MAC:", mac_address
        return "error"
    else:
        print ""
        return matched_vm

def get_all_vms():
    args = [vbox_bin, "list", "vms"]
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    (out, err) = p.communicate()
    try:
        all_vms=out.split('"')[1::2]
    except:
        print "error"
    return all_vms

def get_running_vms():
    args = [vbox_bin, "list", "runningvms"]
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    (out, err) = p.communicate()
    try:
        running_vms=out.split('"')[1::2]
    except:
        print "error"
    return running_vms

@app.route('/vmrun/vm/start/<string:mac_address>', methods = ['POST', 'GET'])
def start_vm(mac_address):
    vm = get_vm_bymac_address(mac_address)
    print vm
    args = [vbox_bin, "startvm", "--type", "headless", vm]
    print args
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    (out, err) = p.communicate()
    print out, err
    print "Swtiched to on"
    return "Swtiched to on"


@app.route('/vmrun/vm/stop/<string:mac_address>', methods = ['POST', 'GET'])
def stop_vm(mac_address):
    vm = get_vm_bymac_address(mac_address)
    print vm
    args = [vbox_bin, "controlvm", vm, "poweroff"]
    print args
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    (out, err) = p.communicate()
    print out, err
    print "Swtiched to off"
    return "Swtiched to off"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6000, debug = True)
