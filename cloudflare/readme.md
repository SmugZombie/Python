# This project has been moved to its own repository.
https://github.com/SmugZombie/Cloudflareapi.py

#Cloudflare API

Basic Commands:<br>
<strong>Create a new Zone</strong> : python cloudflareapi.py -d example.xyz -a create<br>
<strong>List DNS For a Zone</strong> : python cloudflareapi.py -d example.xyz -a list<br>
<strong>Create new DNS Record For a Zone</strong> : python cloudflareapi.py -d example.xyz -a add -r <RECORD_TYPE> -H <HOST> -c <RECORD_CONTENT><br>
<strong>Delete a DNS Record From a Zone</strong> : python cloudflareapi.py -d example.xyz -a delete -i <RECORD_ID><br>
