from createVcenterController import create_vcenter_controller
from createVcenterCredential import create_vcenter_credential
from createVlanPool import create_vlan_pool
from createVmmDomain import create_vmm_domain
from addVmmDomainAssociation import add_vmm_domain_association

from utility import *


def lab5(modir, tenant_name, application_name):
    """Following the lab guide, we create 3Tiers application profile"""

    vlan_model = 'dynamic'
    vm_provider = 'VMware'
    vmm_domain = 'My_vCenter'
    account_profile_name = 'administrator'

    # Create a VLAN_Pool
    create_vlan_pool(modir, tenant_name+'_VALN_Pool', vlan_model, '1001', '1100')
    # Create VMM domain
    create_vmm_domain(modir, vm_provider, vmm_domain, vlan_name=tenant_name+'_VALN_Pool', vlan_mode=vlan_model)
    # Set up VMM Credential
    create_vcenter_credential(modir, vm_provider, vmm_domain, account_profile_name, 'student', 'P@ssw0rd')
    # Set up VMM Controller
    create_vcenter_controller(modir, vm_provider, vmm_domain, 'ACILab', '192.168.1.100', 'ACILab', associated_credential=account_profile_name)

    # Associating EPG to vCenter Domain.
    add_vmm_domain_association(modir, tenant_name, application_name, 'Web_EPG', vmm_domain, deployment_immediacy='immediate', resolution_immediacy='immediate')
    add_vmm_domain_association(modir, tenant_name, application_name, 'App_EPG', vmm_domain, deployment_immediacy='immediate', resolution_immediacy='immediate')
    add_vmm_domain_association(modir, tenant_name, application_name, 'DB_EPG', vmm_domain, deployment_immediacy='immediate', resolution_immediacy='immediate')


if __name__ == '__main__':
    if len(sys.argv) != 6:
        print 'Usage:', __file__, '<hostname> <username> <password> <tenant_name> <application_name>'
        sys.exit()
    else:
        hostname, username, password, tenant_name, application_name = sys.argv[1:]
        modir = apic_login(hostname, username, password)
        lab5(modir, tenant_name, application_name)
        modir.logout()