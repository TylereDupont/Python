#Format: dig {target} {record type}

#Import required modules
import subprocess

#Initialize array with record types to scan
recordTypes = ['A','AAAA','ALIAS','CNAME','MX','NS','PTR','SOA','SRV','TXT','DNSKEY','DS','NSEC','NSEC3','NSEC3PARAM','RRSIG','AFSDB','CAA','CERT','DHCID','DNAME','HINFO','HTTPS','LOC','NAPTR','RP','TLSA']

#Save user input to target variable
target = input("Enter Domain Name ")

#Initialize final output variable
decodedOutput = ''

#Loop through every item in recordTypes and skip if blank or add to final output
for x in recordTypes:
	#Check if record type is empty. If so skip adding it to the final string
	if subprocess.run(['dig ' + '+short ' + target + ' ' + x] , capture_output=True, shell=True).stdout.decode() == "" :
		pass
	else :
		#Add record type and record to final string
		decodedOutput += x + "\n" + subprocess.run(['dig ' + '+short ' + target + ' ' + x] , capture_output=True, shell=True).stdout.decode() + "\n"

#Final Output
print(decodedOutput)
print("GROUP4!")