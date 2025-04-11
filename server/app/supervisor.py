import os, time, csv, json
from importlib import import_module, util
import importlib
from app.mqtt_app import get_latest_sensor_y, send_u, control_mode
from flask_socketio import emit
from datetime import datetime

latest_sim = {}
SIMS_DIR = "instance/simulations"

def load_user_code(stu_number):
    from app import mqtt
    file_path = os.path.join('instance/uploads/',stu_number, stu_number+'py')

    if not os.path.exists(file_path):
        return None, {'success':False, 'message':'File not found'}

    module = importlib.util.spec_from_file_location(stu_number+'',file_path)

    if not hasattr(module,'reference') or not hasattr(module,'controller') or not hasattr(module,'Ts'):
        return None, {'success':False,'message':"Invalid file format. Missing reference or controller."}

    return module, None

def run_sim(stu_number):
    from app import socketio
    module, error = load_user_code(stu_number)
    if error:
        return error
    reference_signal = module.reference
    controller = module.controller
    Ts = module.Ts
    result = []
    time_start = time.time()
    try:
        for r in reference_signal:
            ping = int(time.time())
            y = get_latest_sensor_y()
            if y is None:
                return
            try: 
                u = controller(r,y) if callable(controller) else None
            except TypeError as e:
                return
            if not isinstance(u,(int,float)):
                return
            send_u(u)
            timestamp = time.time() - time_start
            data = [timestamp,r,u,y] #[t,r,y,u]
            result.append(data)
            pong = int(time.time())
            remaining_time = (Ts/1000) - (pong - ping)
            if remaining_time > 0:
                socketio.sleep(remaining_time)
            socketio.emit("sim_update", json.dumps({'timestamp':time.time()-time_start,'reference': r, 'sensor':y, 'actuator':u}))
    finally: 
        control_mode('local')

        stu_dir = os.path.join(SIMS_DIR,stu_number)
        os.makedirs(stu_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S') 
        file_path = os.path.join(stu_dir, f"{stu_number}_experiment_{timestamp}.csv")

        csvfile = open(file_path, 'w', newline="")
        writer = csv.writer(csvfile)
        writer.writerow(["Time", "Reference", "Actuator", "Sensor"])
        writer.writerows(result)
        csvfile.close()

        socketio.emit('sim_end',{'message':'experiment end'})
    print('run_sim - '+ stu_number)
    return