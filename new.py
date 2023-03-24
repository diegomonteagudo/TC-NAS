# !/urs/bin/python3
import json

from datetime import datetime
now = datetime.now()
from math import floor

#fonction pour ouvrir et lire le fichier json 
def open_file(_file) :
	# Opening JSON file
	f = open(_file)
	  
	# returns JSON object as a dictionary
	data = json.load(f)
	f.close()
	return data


filename=str(input('File name? -->')) #le nom de fichier json
json_object = open_file(filename)


def write_file() :
    script="!\n\n!\n"
    script+="version 15.2\n"
    script+="service timestamps debug datetime msec\n"
    script+="service timestamps log datetime msec\n"
    script+="!\nhostname "+r['hostname']+"\n!\n"
    script+="boot-start-marker\n"
    script+="boot-end-marker\n!\n!\n!\n"
    script+="no aaa new-model\n"
    script+="no ip icmp rate-limit unreachable\n"
    script+="ip cef\n!\n"
    if r['vrf_apply']!=0:
        for x in r['vrf']:
            script+="ip vrf "+x['name']+"\n"
            script+=" route-target export "+r['bgp']['AS_number']+":"+x['id']+"\n"
            script+=" route-target import"+r['bgp']['AS_number']+":"+x['id']+"\n"
            script+=" !\n"
    script+="!\n!\n!\n!\n!\n"
    script+="no ip domain lookup\n"
    script+="no ipv6 cef\n!\n!\n"
    script+="multilink bundle-name authenticated\n"
    script+="!\n!\n!\n!\n!\n!\n!\n!\n!\n"
    script+="ip tcp synwait-time 5\n"
    script+="!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n"
    
        
    for x in r['interfaces']:
        script+="interface "+str(x['interface_name'])+"\n"
        
        if str(x['interface_name'])=="Loopback0":
            script+=" ip address "+str(r['id'])+"."+str(r['id'])+"."+str(r['id'])+"."+str(r['id'])+" 255.255.255.255"
            
        else:
            script+=" ip address "
            if x['link']<10 && r['id']>100 : #PE and connect with CE
                if x['vrf_apply']!=0:
                    script+="ip vrf forwarding "
                    for y in r['vrf']:
                        if y['id'] == x['vrf_id']:
                            script+=y['name']+"\n"
                script+="192.168."+x['link']+".1 255.255.255.0\n"
                script+=" negotiation auto\n"
                    
            elif r['id']>100 && x['link']>10 && x['link']<20 : #PE connect with P
                script+="10.10."+x['link']+".1 255.255.255.252\n"
                script+=" negotiation auto\n"
                script+=" mpls ip\n"
            elif x['link']>100 && r['id']>10 && r['id']<20 : #P connect with PE
                script+="10.10."+r['id']+".2 255.255.255.252\n"
                script+=" negotiation auto\n"
                script+=" mpls ip\n"
            elif x['link']>10 && x['link']<20 && r['id']>10 && r['id']<20 : #P connect with P
                if x['link']<r['id']:
                    script+="10.10."+x['link']+".2 255.255.255.252\n"
                else:
                    script+="10.10."+r['id']+".1 255.255.255.252\n"
                script+=" negotiation auto\n"
                script+=" mpls ip\n"
            elif r['id']<10 && x['link']>100 : #CE connect with PE
                script+="192.168."+r['id']+".2 255.255.255.0\n"
                script+=" negotiation auto\n"
        script+="!\n"
        
    if r['vrf_apply']!=0:
        for x in r['vrf']:
            script+="router ospf "+x['id']+" vrf "+x['name']
            script+=" redistribute bgp "+r['bgp']['AS_number']+" metric "+r['bgp']['AS_number']+" subnet\n"
            script+=" network "+str(r['id'])+"."+str(r['id'])+"."+str(r['id'])+".0 0.0.0.255 area 0\n"
            for y in r['interface']:
                if y['vrf_id']==x['id']:
                    script+=" network 192.168."+x['link']+".0 0.0.0.255 area 0\n"
                    script+="!\n"
            
    if r['ospf']['ospf_apply']!=0:
        script+="router ospf "+r['ospf']['process_id']+"\n"
        script+=" network "+str(r['id'])+"."+str(r['id'])+"."+str(r['id'])+".0 0.0.0.255 area 0\n"
        
        for x in r['interface']:
            if x['ospf_apply']!=0:
                if r['id']>100 && x['link']>10 && x['link']<20 : #PE connect with P
                    script+="10.10."+x['link']+".0 0.0.0.3\n"
                    
                elif x['link']>100 && r['id']>10 && r['id']<20 : #P connect with PE
                    script+="10.10."+r['id']+".0 0.0.0.3\n"
                    
                elif x['link']>10 && x['link']<20 && r['id']>10 && r['id']<20 : #P connect with P
                    if x['link']<r['id']:
                        script+="10.10."+x['link']+".0 0.0.0.3\n"
                    else:
                        script+="10.10."+r['id']+".0 0.0.0.3\n"
                    
          script+="!\n"
        
        
    if r['bgp']['bgp_apply']!=0 :
        script+="router bgp "+str(r['bgp']['AS_number'])+"\n"
        script+=" bgp log-neighbor-changes\n"
        script+=" no bgp default ipv4-unicast\n"
        script+=" neighbor "+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+" remote-as "+str(r['bgp']['AS_number'])+"\n"
        script+=" neighbor "+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+" update-source Loopback0\n"
        
        script+=" !\n"
        script+=" address-family ipv4\n"
        script+=" neighbor "+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+" activate\n"
        script+=" exit-address-family\n"
        script+=" !\n"
        
        if r['bgp']['neighbor']['vpn_apply'])!=0:
            script+=" address-family vpnv4\n"
            script+=" neighbor "+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+" activate\n"
            script+=" neighbor "+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+" send-community extended\n"
            script+=" exit-address-family\n"
            script+=" !\n"
          
        
        
        
        for y in json_object['routers'] :
            if (y['AS_number']==r['AS_number'] and y['id']!=r['id']):
                script+="  neighbor "+str(y['id'])+"::"+str(y['id'])+" activate\n"
                
        
        
        if r['border_router']!=0:
            for x in r['ebgp']['neighbors']:
                script+="  neighbor "+border_subnet+str(x['id'])+" activate\n"
                
        if r['border_router']!=0 and r['local_pref']['metric_apply']!=0:
            for x in r['local_pref']['link']:
                script+="  neighbor "+border_subnet+str(x['id'])+" route-map "+x['name']+" "+x['direction']+"\n"
        
        script+=" exit-address-family\n!\n"
        script+="ip forward-protocol nd\n!\n!\n"
        script+="no ip http server\n"
        script+="no ip http secure-server\n!\n"

        if r['IGP_protocol']=="ospf":
            script+="ipv6 router ospf "+str(r['id'])+"\n"
            script+=" router-id "
            script+=str(r['id'])
            for x in range(3):
                script+="."+str(r['id'])
            script+="\n"
            script+=" redistribute connected\n"
        elif r['IGP_protocol']=="rip":
            script+="ipv6 router rip "+ r['rip_process_name']+"\n"
            script+=" redistribute connected\n"
            
        if r['border_router']!=0 and r['local_pref']['metric_apply']!=0:
            for x in r['local_pref']['link']:
                script+="!\n!\nroute-map "+x['name']+" permit 10\n"
                script+=" set local-preference 400\n"
        script+="!\n!\n!\n!\ncontrol-plane\n!\n!\n"
        script+="line con 0\n"
        script+=" exec-timeout 0 0\n"
        script+=" privilege level 15\n"
        script+=" logging synchronous\n"
        script+=" stopbits 1\n"
        script+="line aux 0\n"
        script+=" exec-timeout 0 0\n"
        script+=" privilege level 15\n"
        script+=" logging synchronous\n"
        script+=" stopbits 1\n"
        script+="line vty 0 4\n"
        script+=" login\n!\n!\nend"
    return script		
			
#print(write_file())
for r in json_object['routers'] :
    
    #ecrire dans le fichier json
    destination=r['hostname']+".txt"
    with open(destination, "w") as outfile:
        outfile.write(write_file())
