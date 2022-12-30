# maltiverse-module-openai
Demonstration of how Maltiverse and OpenAI can be integrated.

When given an IOC, such as an IP address, Maltiverse enriches the indicator with context information, and then OpenAI is used to generate a report with recommendations on how to address the specific threat.

Example:

INPUT:
py .\maltiverse-module-openai1.py -i 117.253.148.116

OUTPUT:

[+] Looking for 117.253.148.116

[+] Maltiverse response: IOC type ip with the follow threats associated Malware Download and Mail Spammer

[+] Question to OpenAI: I'm a cyber threat analyst, give me a short report about what I have to do with the malicious ip 117.253.148.116 used in campaigns Malware Download and Mail Spammer and a list of recomendations for IT administrators should take to prevent traffic to this ip.

[+] Recomendation from OpenAI:

Malicious IP Report:

IP Address: 117.253.148.116

Campaigns: Malware Download and Mail Spammer

Description: This malicious IP address has been used in campaigns to download malware and send out mail spam. It is likely that this IP address is being used by a malicious actor to spread malicious content or conduct other malicious activities.

Recommendations for IT Administrators:
1. Block traffic from this IP address at the firewall level.
2. Monitor network traffic for any suspicious activity originating from this IP address.
3. Implement anti-malware software on all systems connected to the network to detect and prevent any malicious activity originating from this IP address.
4. Educate users on the dangers of downloading files or clicking links from unknown sources, as these could be associated with this malicious IP address or similar ones used by the same actor(s).
5. Regularly update security patches and software versions on all systems connected to the network, as outdated versions can be vulnerable to attacks originating from this IP address or similar ones used by the same actor(s).
