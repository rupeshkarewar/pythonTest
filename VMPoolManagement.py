import json
import subprocess
import os.path


class VMPoolManagement:
    vm_pool_name = 'test'
    vm_pool = {}
    def __init__(self, name):
        self.vm_pool_name = name
        if not os.path.isfile(self.vm_pool_name + ".json"):
            with open(self.vm_pool_name + ".json", 'w') as jsonFile:
                json.dump(self.vm_pool, jsonFile, indent=4)

    def check_in_vm(self, vm, user):
        with open(self.vm_pool_name + ".json", "r") as jsonFile:
            data = json.load(jsonFile)
        
        if data[vm]["allocated_to"] == "":
            print(str(data[vm]) + " is already returned")
        elif data[vm]["allocated_to"] != user:
            print("A VM checked out by one user cannot be checked in by some other user.")
        else:
            print("Cleaning VM:" + vm)

            # Please uncomment below command if you have valid ip address and ssh setup on VMs in pool to execute cleanup.
            # subprocess.Popen("ssh {user}@{host} {cmd}".format(user="admin_user", host=data[vm]['ip_address'], cmd='rm -rf /tmp/*'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            data[vm]["allocated_to"] = ""

            with open(self.vm_pool_name + ".json", "w") as jsonFile:
                json.dump(data, jsonFile, indent=4)
        
    def check_out_vm(self, user):
        with open(self.vm_pool_name + ".json", "r") as jsonFile:
            data = json.load(jsonFile)

        for vm, info in data.items():
            if data[vm]["allocated_to"] == "":
                data[vm]["allocated_to"] = user
                print(vm + " is allocated to : " + user) 
                break
        else:
            print("All VMs are allocated for now. Plase wait untill someone returns VM") 

        with open(self.vm_pool_name + ".json", "w") as jsonFile:
            json.dump(data, jsonFile, indent=4)
        
        return data[vm]

    def update_pool(self, vm, action): #This is dummy function to add/remove vm to pool. It can be replaced with to call cloud API to monitor current VMs present in colud and update pool with details.
        with open(self.vm_pool_name + ".json", "r") as jsonFile:
            data = json.load(jsonFile)
        
        if action == "add":
            if type(vm) is dict:
                data.update(vm)
            else:
                print("Please give valid VM deatils")
        elif action == "remove":
            if type(vm) is str:
                print("Deleting VM:" + vm)
                del data[vm]
            else:
                print("Please give valid string for vm name")

        with open(self.vm_pool_name + ".json", "w") as jsonFile:
            json.dump(data, jsonFile, indent=4)


if __name__ == "__main__":
    vm_management = VMPoolManagement("vm_pool")
    
    for i in range(0, 5):
        vm = {
            "VM" + str(i) : {
                'ip_address':str(i) + "." + str(i) + "." + str(i) + "." + str(i),
                'allocated_to':"",}
        }
        vm_management.update_pool(vm, "add")

    vm_management.update_pool("VM4", "remove")

    # vm_info = vm_management.check_out_vm("test_user")
    # print(str(vm_info))

    # vm_management.check_in_vm("VM0", "test_user")

