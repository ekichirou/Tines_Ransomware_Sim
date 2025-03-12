# Tines Ransomware Simulation
This is a passion project that is a part of the [YDWWT](https://www.tines.com/you-did-what-with-tines/spring-2025/) event.
### Credits
> I would like to thank [1Doomdie1](https://github.com/1Doomdie1) for their support with the Tines integration.
> 
### What is the purpose of this project?
> The goal of this project is to simulate ransomware behavior in a controlled environment to evaluate how security platforms and teams detect, respond to, and mitigate potential threats. By emulating real-world attack patterns, this simulation helps security professionals:  
>
> - **Assess Detection Capabilities**: Test how effectively security tools identify malicious encryption and exfiltration activities.  
> - **Enhance Incident Response**: Provide blue teams with hands-on experience in responding to ransomware attacks.  
> - **Improve Security Controls**: Identify gaps in monitoring, logging, and automated threat mitigation.  
>
> This project is designed to be a safe and ethical way to refine security defenses without exposing systems to real-world threats.
> 
### How does the project work?
> This project leverages the Tines platform to generate a ransomware profile, including a ransom note, URLs, encryption keys, number of files, and other configurable settings. These settings are then applied to a custom-made PowerShell .NET template, which provides a PowerShell one-liner to invoke the simulation.  
>
> The PowerShell .NET template performs the following actions:  
> - Creates dummy `.xlsx` files on the user's desktop.  
> - Archives the files, converts the archive to BASE64, and exfiltrates it.  
> - Collects basic system information and exfiltrates it.  
> - Encrypts the generated files and leaves a ransom note.  
>
> Additionally, the project includes a **Python FastAPI** backend and an **HTML-based dashboard** to visually simulate the ransomware exfiltrated data.  
> The Tines profiler also generates a **PowerShell one-liner** for decryption.
> 
### Rules
> Specific rules have been applied to this simulation to ensure it remains both realistic and safe:  
> 1. **No spreading** – The ransomware simulation does not propagate across systems.  
> 2. **No domain interaction** – No domain enumeration or network reconnaissance is performed.  
> 3. **No encryption of legitimate files** – Only generated dummy files are encrypted.  
> 4. **Simulation runs on the Desktop** – All actions are limited to the Desktop for easier observation and containment.
>
### Instalation and Usage
##### Dashboard server
1. Download the repository and install the required dependencies by running: `pip install fastapi uvicorn requests`
2. Navigate to the Dashboard folder and run ./run.sh to start the server.
3. Access the dashboard by visiting: `http://<SERVER_IP>:5000/dashboard`
##### Tines Server
1. Import the story into your Tines tenant.
2. Create Tines credentials for HTTP requests.
3. Modify the **enc_decrypter_cmd** to point to your **Decrypter** webhook.
4. Create an API key.
5. Update the server.py file with:
  - The generated API key.
  - The API endpoints of the three notes. (*Run the **Get Notes** HTTP request to retrieve note IDs*)
6. Create two resources and update the **Response** of both the Encrypter and Decrypter webhooks.
7. Modify the `Success - Update` HTTP Requests:
  - Under `Encrypter.ps1`, update with the Encrypter resource.
  - Under `Decrypter.ps1`, update with the Decrypter resource.
  - In `Clear - Update`, use the Encrypter resource.</br>
(*Run the **Get Resource** HTTP request to retrieve resource IDs*).
