import tkinter as tk
import logging
import opcua
from opcua import Client
import threading
import time
from opcua import ua

logging.basicConfig(level=logging.WARN)

event = threading.Event()

def thread_function(name, client_instance):

    while 1:
        logging.warning("Thread %s: starting", name)
        time.sleep(2)

        if event.is_set():
            break

        print(client_instance.client.get_node("ns=4;i=6").get_value())

# fun definitions
class connected_client:

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.client = opcua.Client

    def OPCConnect(self,thread_fun):
        self.client = Client("opc.tcp://" + self.address + ":" + self.port + "/")
        self.client.session_timeout = 30000
        try:
            self.client.connect()
            thread_fun.start()
            print("Server connected")

        except:
            print("Connection issue")

    def OPCDisconnect(self,thread_fun):
        self.client.disconnect()
        print("Server disconnected")
        event.set()
        thread_fun.join()

    def setMESStatus(self,value):
        self.client.get_node("ns=4;i=6").set_value(ua.DataValue(ua.Variant(value, ua.VariantType.Int16)))


# OPC CLIENT
pu_client = connected_client("192.168.8.166","4840")

# thread function
x = threading.Thread(target=thread_function, args=(1,pu_client))

# app frame
window = tk.Tk()
window.geometry("640x480")
window.title("OPC Client")

# title
title = tk.Label(window, text="OPC Test Client")
title.grid(row=0, column=0, columnspan=3)

# labels MES
mes_status0 = tk.Label(master=window, text="0 - Idle")
mes_status1 = tk.Label(master=window, text="1 - Request for download")
mes_status2 = tk.Label(master=window, text="2 - Download active")
mes_status3 = tk.Label(master=window, text="3 - Download finished")
mes_status4 = tk.Label(master=window, text="4 - Ready to start")
mes_status5 = tk.Label(master=window, text="5 - Batch data reading finished")
mes_status8 = tk.Label(master=window, text="8 - N/A")

mes_status0.grid(row=5, column=0, padx=5, pady=5)
mes_status1.grid(row=6, column=0, padx=5, pady=5)
mes_status2.grid(row=7, column=0, padx=5, pady=5)
mes_status3.grid(row=8, column=0, padx=5, pady=5)
mes_status4.grid(row=9, column=0, padx=5, pady=5)
mes_status5.grid(row=10, column=0, padx=5, pady=5)
mes_status8.grid(row=11, column=0, padx=5, pady=5)

# buttons MES
button_0 = tk.Button(master=window, text="Set 0", command=lambda: pu_client.setMESStatus(0))
button_1 = tk.Button(master=window, text="Set 1", command=lambda: pu_client.setMESStatus(1))
button_2 = tk.Button(master=window, text="Set 2", command=lambda: pu_client.setMESStatus(2))
button_3 = tk.Button(master=window, text="Set 3", command=lambda: pu_client.setMESStatus(3))
button_4 = tk.Button(master=window, text="Set 4", command=lambda: pu_client.setMESStatus(4))
button_5 = tk.Button(master=window, text="Set 5", command=lambda: pu_client.setMESStatus(5))
button_8 = tk.Button(master=window, text="Set 8", command=lambda: pu_client.setMESStatus(8))

button_0.grid(row=5, column=1, padx=5, pady=5)
button_1.grid(row=6, column=1, padx=5, pady=5)
button_2.grid(row=7, column=1, padx=5, pady=5)
button_3.grid(row=8, column=1, padx=5, pady=5)
button_4.grid(row=9, column=1, padx=5, pady=5)
button_5.grid(row=10, column=1, padx=5, pady=5)
button_8.grid(row=11, column=1, padx=5, pady=5)

# labels PU
pu_status0 = tk.Label(window, text="0 - Idle")
pu_status1 = tk.Label(window, text="1 - Ready for download")
pu_status2 = tk.Label(window, text="2 - Download active")
pu_status3 = tk.Label(window, text="3 - Header data accepted")
pu_status4 = tk.Label(window, text="4 - Batch active")
pu_status5 = tk.Label(window, text="5 - Batch finished")
pu_status8 = tk.Label(window, text="8 - Error")

pu_status0.grid(row=5, column=2, padx=5, pady=5)
pu_status1.grid(row=6, column=2, padx=5, pady=5)
pu_status2.grid(row=7, column=2, padx=5, pady=5)
pu_status3.grid(row=8, column=2, padx=5, pady=5)
pu_status4.grid(row=9, column=2, padx=5, pady=5)
pu_status5.grid(row=10, column=2, padx=5, pady=5)
pu_status8.grid(row=11, column=2, padx=5, pady=5)

# connection and batch infos
server_address = tk.Entry(master=window, text="server ip", width=20)
button_connect = tk.Button(master=window, text="Connect", width=10, command=lambda: pu_client.OPCConnect(x))
button_disconnect = tk.Button(master=window, text="Disconnect", width=10, command=lambda: pu_client.OPCDisconnect(x))

batch_label = tk.Label(window, text="Batch ID")
recipe_label = tk.Label(window, text="Recipe ID")
batch_id = tk.Entry(master=window, text="batch id", width=40)
recipe_id = tk.Entry(master=window, text="recipe id", width=40)

server_address.grid(row=1, column=0, padx=5, pady=10)
button_disconnect.grid(row=1, column=2, padx=5, pady=10)
button_connect.grid(row=1, column=1, padx=5, pady=10)
batch_id.grid(row=2, column=1, padx=5, pady=5, columnspan=2)
recipe_id.grid(row=3, column=1, padx=5, pady=5, columnspan=2)
batch_label.grid(row=2, column=0, padx=5, pady=10)
recipe_label.grid(row=3, column=0, padx=5, pady=10)

window.mainloop()
