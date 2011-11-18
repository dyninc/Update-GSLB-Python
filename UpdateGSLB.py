''' 
   An example script which will add a newly created web server into a GSLB (Dynect Traffic Manager) for a specific region
   The script uses the DynectDNS library and specifically imports DynectRest from it
   
   The credentials are read out of a configuration file in the same directory named credentials.cfg in the format:
   
   [Dynect]
   user : user_name
   customer : customer_name
   password: password
   
   
   The script has the following usage: "python UpdateGSLB.py zone fqdn region ip"
   
   zone - zone of the GSLB (ie: myzone.net)
   fqdn - the fully qualified domain name of the GSLB (ie: testgslb.myzone.net)
   region - the region to add the ip address to. If there is a space in the region, for example US East, replace the space with %20 (ie: US%20East)
   ip - the ip address of the server (ie: 1.2.3.4)
   
'''

import sys
import ConfigParser
from DynectDNS import DynectRest

if (len(sys.argv) != 5):
	sys.exit("Incorrect Arguments. \n\nUsage: python UpdateGSLB.py zone fqdn region ip\n\n**If there is a space in region replace the space with %20") 

config = ConfigParser.ConfigParser()
try:
	config.read('credentials.cfg')
except:
	sys.exit("Error Reading Config file")

dynect = DynectRest()

# Log in
arguments = {
	'customer_name':  config.get('Dynect', 'customer', 'none'),
	'user_name':  config.get('Dynect', 'user', 'none'),  
	'password':  config.get('Dynect', 'password', 'none'),
}
response = dynect.execute('/Session/', 'POST', arguments)

if response['status'] != 'success':
	sys.exit("Incorrect credentials")

zone =  sys.argv[1]
fqdn =  sys.argv[2]
region =  sys.argv[3]
args = { 'address' :  sys.argv[4] }

# Perform action
response = dynect.execute('/GSLBRegionPoolEntry/' + zone + "/" + fqdn + "/" + region, 'POST', args)
post_reply = response['data']

# Log out, to be polite
dynect.execute('/Session/', 'DELETE')