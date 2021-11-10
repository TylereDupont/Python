import subprocess

recordTypes = ['A','AAAA','ALIAS','CNAME','MX','NS','PTR','SOA','SRV','TXT','DNSKEY','DS','NSEC','NSEC3','NSEC3PARAM','RRSIG','AFSDB','CAA','CERT','DHCID','DNAME','HINFO','HTTPS','LOC','NAPTR','RP','TLSA']

target = input("Enter Domain Name ")

decodedOutput = ''
for x in recordTypes:
	if subprocess.run(['dig ' + '+short ' + target + ' ' + x] , capture_output=True, shell=True).stdout.decode() == "" :
		pass
	else :	
		decodedOutput += x + "\n" + subprocess.run(['dig ' + '+short ' + target + ' ' + x] , capture_output=True, shell=True).stdout.decode() + "\n"

print(decodedOutput)
#GROUP4!