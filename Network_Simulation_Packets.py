import numpy as np
import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import simpy
import threading
import random
import time

###########################################################
# المتغيرات
traffic_data = []
max_points = 50
attack_counter = 0
ddos_threshold = 5
large_packet_count = 0
packet_counter = 0
colors = []
running = True
env = simpy.Environment()
test5=""


#################################################################
# دالة توليد أرقام LCG
def lcg(seed, a, c, m, n):
    results = []
    x = seed
    for _ in range(n):
        x = (a * x + c) % m
        results.append(x / m)
    return results


###################################################################
# تحليل الحزم الصغيرة
def analyze_packet(packet_size, packet_number):
    if packet_size < 100:
        ids_msg = f"[IDS ALERT] Suspicious small packet detected: {packet_size:.2f} bytes (Packet #{packet_number})"
        print(ids_msg)
        log_alert(ids_msg)
        messagebox.showwarning("IDS Alert", ids_msg)

###################################################################
# تحليل الحزم الصغيرة
def allowed_packet(packet_size, packet_number):
    if packet_size > 100 and packet_size <1400:
        messagge = f"[Allowed] Suspicious allowed packet detected: {packet_size:.2f} bytes (Packet #{packet_number})"
        print(messagge)
        log_alert(messagge)

####################################################################
# حفظ التنبيهات في ملف
def log_alert(msg, filename="log.txt"):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{msg}\n")

###################################################################
# اكتشاف هجوم DDoS
def ddos_attack():
    global attack_counter, large_packet_count, packet_counter
    if large_packet_count >= ddos_threshold:
        ddos_msg = f"[ALERT] Potential DDoS attack detected at Packet #{packet_counter}!"
        print(ddos_msg)
        log_alert(ddos_msg)
        messagebox.showwarning("DDoS Alert", ddos_msg)

###################################################################
# تحليل الحزمة القادمة من simpy
def handle_packet(packet_size, packet_number):
    global large_packet_count, attack_counter
    traffic_data.append(packet_size)

    if packet_size > 1400:
        large_packet_count += 1
        alert_msg = f"[ALERT] High packet size detected: {packet_size:.2f} bytes (Packet #{packet_number})"
        print(alert_msg)
        log_alert(alert_msg)
        attack_counter += 1
        messagebox.showinfo(f"Alert attacks {attack_counter}", alert_msg)
        ddos_attack()
    else:
        large_packet_count = 0

    analyze_packet(packet_size, packet_number)
    allowed_packet(packet_size, packet_number)
    # simulate_syn_flood_attack(packet_count=100)

    if len(traffic_data) > max_points:
        traffic_data.pop(0)
        colors.pop(0)

    if packet_size < 100:
        colors.append('green')
    elif packet_size > 1400:
        colors.append('red')
    else:
        colors.append('yellow')

###################################################################
# توليد الحزم باستخدام simpy
def packet_generator(env, rate):
    global packet_counter
    while True:
        yield env.timeout(rate)
        if running:
            seed = random.randint(0, 10000)
            packet_size = lcg(seed, 1103515245, 12345, 2001, 1)[0] * 1500
            #packet_size = random.randint(1400, 2000)
            packet_size = max(0, packet_size)
            packet_counter += 1
            handle_packet(packet_size, packet_counter)

###################################################################
# بدء المحاكاة
def start_simulation():
    global running
    running = True
    if not env._queue:  # لا تقم بتشغيل أكثر من مرة
        simpy_thread = threading.Thread(target=start_simpy_simulation)
        simpy_thread.daemon = True
        simpy_thread.start()
###################################################################
# إيقاف مؤقت
def pause_simulation():
    global running
    running = False

###################################################################
# إعادة التشغيل
def reset_simulation():
    global traffic_data, colors, attack_counter, large_packet_count, packet_counter
    traffic_data.clear()
    colors.clear()
    attack_counter = 0
    large_packet_count = 0
    packet_counter = 0
    line.set_data([], [])
    scatter.set_offsets(np.empty((0, 2)))
    scatter.set_color([])

####################################################################
def start_simpy_simulation():
    env.process(packet_generator(env, rate=2))
    while True:
        if running:
            env.step()
        time.sleep(1)  # توليد كل ثانية


###################################################################
# تحديث الرسم
def update(frame):
    line.set_data(range(len(traffic_data)), traffic_data)
    scatter.set_offsets(np.column_stack((range(len(traffic_data)), traffic_data)))
    scatter.set_color(colors)
    return scatter, line

###################################################################
# إعداد نافذة tkinter
root = tk.Tk()
root.title("Team 11")

fig = Figure(figsize=(8, 4), dpi=100)
ax = fig.add_subplot(111)
ax.set_ylim(0, 2000)
ax.set_xlim(0, max_points)
ax.set_ylabel("Packet Size (bytes)")
ax.set_title("Network Traffic Simulation")
line, = ax.plot([], [], lw=2)
scatter = ax.scatter([], [], c=[], s=50)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

control_frame = tk.Frame(root)
control_frame.pack(side=tk.BOTTOM, pady=10)

start_btn = tk.Button(control_frame, text="Start simulation", command=start_simulation, bg="lightgreen")
start_btn.pack(side=tk.LEFT, padx=10)

pause_btn = tk.Button(control_frame, text="Pause", command=pause_simulation, bg="orange")
pause_btn.pack(side=tk.LEFT, padx=10)

reset_btn = tk.Button(control_frame, text="RePlay Simulation", command=reset_simulation, bg="red")
reset_btn.pack(side=tk.LEFT, padx=10)

ani = animation.FuncAnimation(fig, update, interval=1000, blit=False)

root.mainloop()

test5="successful"
print(test5)
