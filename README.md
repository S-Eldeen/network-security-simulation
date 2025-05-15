🔍 What does it do?
 This system simulates live network traffic and intelligently analyzes packet behavior to:
Detect high-risk packets (e.g., large payloads – potential DDoS)
Flag abnormally small packets (e.g., potential port scans)
Log and visually track normal traffic vs suspicious activity
Alert the user with real-time pop-up warnings
📊 Features I Implemented:
📈 Real-time data visualization using matplotlib (line chart + scatter plot)
🌐 Packet simulation using SimPy (discrete event simulation)
🧠 Packet classification:
Red = Potential DDoS (packet > 1400 bytes)
Green = Suspicious small packet (packet < 100 bytes)
Yellow = Normal traffic
🔐 Custom LCG (Linear Congruential Generator) RNG instead of NumPy for packet size generation – showing full control over the randomization process.
📦 IDS Logic (Intrusion Detection System) with custom rules
🧾 Automatic logging to log.txt
🧠 GUI built using Tkinter with controls for Start, Pause, and Reset
🧩 Why is this important?
 Understanding how network anomalies behave — and how to simulate them — is key to building smarter detection systems. This project gave me hands-on experience in:
Real-time data analysis
Threat modeling
Working with event-driven simulation
Data visualization in cybersecurity contexts
