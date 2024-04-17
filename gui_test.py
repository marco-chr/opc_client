import tkinter as tk
import logging
import opcua
from opcua import Client
import threading
import time
from opcua import ua

# logging setting
logging.basicConfig(level=logging.WARN)

event = threading.Event()
pu_status = 0
mes_status = 0

# thread running in parallel to read pu_status
def thread_function(name, client_instance, mes_statuses, pu_statuses, batch_id_entry, recipe_id_entry):

    old_pu_status = 0
    old_mes_status = 0

    while 1:
        logging.warning("Thread %s: running", name)
        time.sleep(1)

        if event.is_set():
            break

        # read opc value for pu_status and mes_status
        global pu_status
        pu_status = client_instance.client.get_node("ns=4;i=7").get_value()
        global mes_status
        mes_status = client_instance.client.get_node("ns=4;i=6").get_value()

        batch_id_text = batch_id_entry.get()
        recipe_id_text = recipe_id_entry.get()

        if mes_status == 2 and pu_status == 2:
            client_instance.client.get_node("ns=4;i=14").set_value(ua.DataValue(ua.Variant(batch_id_text, ua.VariantType.String)))
            client_instance.client.get_node("ns=4;i=15").set_value(ua.DataValue(ua.Variant(recipe_id_text, ua.VariantType.String)))

        # if old value is different from actual value it resets all label text to black
        if pu_status != old_pu_status:
            for i in range(0,7):
                pu_statuses[i].config(fg="black")
                old_pu_status = pu_status

        # setting label text color to match pu_status value
        match pu_status:
            case 0:
                pu_statuses[0].config(fg="red")
            case 1:
                pu_statuses[1].config(fg="red")
            case 2:
                pu_statuses[2].config(fg="red")
            case 3:
                pu_statuses[3].config(fg="red")
            case 4:
                pu_statuses[4].config(fg="red")
            case 5:
                pu_statuses[5].config(fg="red")
            case 8:
                pu_statuses[6].config(fg="red")

        # if old value is different from actual value it resets all label text to black
        if mes_status != old_mes_status:
            for i in range(0,7):
                mes_statuses[i].config(fg="black")
                old_mes_status = mes_status

        # setting label text color to match mes_status value
        match mes_status:
            case 0:
                mes_statuses[0].config(fg="red")
            case 1:
                mes_statuses[1].config(fg="red")
            case 2:
                mes_statuses[2].config(fg="red")
            case 3:
                mes_statuses[3].config(fg="red")
            case 4:
                mes_statuses[4].config(fg="red")
            case 5:
                mes_statuses[5].config(fg="red")
            case 8:
                mes_statuses[6].config(fg="red")


# client class to manage opc tag writes, connection and disconnection
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
        global mes_status
        mes_status = value


# OPC CLIENT
pu_client = connected_client("192.168.8.166","4840")


###################################################### GUI START #############################################################

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

mes_statuses = [mes_status0, mes_status1, mes_status2, mes_status3, mes_status4, mes_status5, mes_status8]

for i in range(0,7):
    mes_statuses[i].grid(row=5+i, column=0, padx=5, pady=5)

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

pu_statuses = [pu_status0, pu_status1, pu_status2, pu_status3, pu_status4, pu_status5, pu_status8]

for i in range(0,7):
    pu_statuses[i].grid(row=5+i, column=2, padx=5, pady=5)

# connection and batch infos
# server_address = tk.Entry(master=window, text="server ip", width=20)
button_connect = tk.Button(master=window, text="Connect", width=10, command=lambda: pu_client.OPCConnect(x))
button_disconnect = tk.Button(master=window, text="Disconnect", width=10, command=lambda: pu_client.OPCDisconnect(x))

batch_label = tk.Label(window, text="Batch ID")
recipe_label = tk.Label(window, text="Recipe ID")
batch_id = tk.Entry(master=window, text="batch id", width=30)
recipe_id = tk.Entry(master=window, text="recipe id", width=30)

# server_address.grid(row=1, column=0, padx=5, pady=10)
button_disconnect.grid(row=1, column=2, padx=5, pady=10)
button_connect.grid(row=1, column=1, padx=5, pady=10)
batch_id.grid(row=2, column=1, padx=5, pady=5, columnspan=2)
recipe_id.grid(row=3, column=1, padx=5, pady=5, columnspan=2)
batch_label.grid(row=2, column=0, padx=5, pady=10)
recipe_label.grid(row=3, column=0, padx=5, pady=10)

###################################################### GUI END #############################################################

# thread function to process in parallel opc tags
x = threading.Thread(target=thread_function, args=("reading pu_status",pu_client, mes_statuses, pu_statuses, batch_id, recipe_id))

window.mainloop()
