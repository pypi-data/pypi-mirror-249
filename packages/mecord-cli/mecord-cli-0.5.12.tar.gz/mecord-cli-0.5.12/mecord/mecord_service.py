import os
import sys
import time
import signal
import subprocess, multiprocessing
import json
import platform
import math
from pathlib import Path
from urllib.parse import *
import socket
import calendar
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
from threading import Thread, current_thread, Lock
import pkg_resources
from pkg_resources import get_distribution

from mecord import store
from mecord import xy_pb
from mecord import task 
from mecord import utils
from mecord import taskUtils
from mecord import progress_monitor
from mecord import mecord_widget

thisFileDir = os.path.dirname(os.path.abspath(__file__)) 
pid_file = os.path.join(thisFileDir, "MecordService.pid")
stop_file = os.path.join(thisFileDir, "stop.now")
stop_thread_file = os.path.join(thisFileDir, "stop.thread")
class MecordService:
    def __init__(self):
        self.THEADING_LIST = []

    def start(self, isProduct=False, threadNum=1, autoUpgrade=False):
        if os.path.exists(pid_file):
            #check pre process is finish successed!
            with open(pid_file, 'r') as f:
                pre_pid = str(f.read())
            if len(pre_pid) > 0:
                if utils.process_is_zombie_but_cannot_kill(int(pre_pid)):
                    print(f'start service fail! pre process {pre_pid} is uninterruptible sleep')
                    env = "test"
                    if isProduct:
                        env = "[us,sg]"
                    taskUtils.notifyWechatRobot(env, {
                        "msgtype": "text",
                        "text": {
                            "content": f"机器<{socket.gethostname()}>无法启动服务 进程<{pre_pid}>为 uninterruptible sleep"
                        }
                    })
                    return False
        with open(pid_file, 'w') as f:
            f.write(str(os.getpid()))
        signal.signal(signal.SIGTERM, self.stop)
        store.save_product(isProduct)
        store.save_multithread(threadNum)
        store.writeDeviceInfo(utils.deviceInfo())
        _clearTask()
        for i in range(0, threadNum):
            self.THEADING_LIST.append(MecordThread(str(i+1)))
        self.THEADING_LIST.append(MecordStateThread(isProduct))
        if autoUpgrade:
            self.THEADING_LIST.append(MecordPackageThread(isProduct))
        while (os.path.exists(stop_file) == False):
            time.sleep(10)
        print("prepare stop")
        with open(stop_thread_file, 'w') as f:
            f.write("")
        for t in self.THEADING_LIST:
            t.markStop()
        for t in self.THEADING_LIST:
            t.join()
        if pid_file and os.path.exists(pid_file):
            os.remove(pid_file)
        if os.path.exists(stop_thread_file):
            os.remove(stop_thread_file)
        if os.path.exists(stop_file):
            os.remove(stop_file)
        store.save_product(False)
        store.save_multithread(1)
        taskUtils.offlineNotify(isProduct)
        print("MecordService has ended!")

    def is_running(self):
        if pid_file and os.path.exists(pid_file):
            with open(pid_file, 'r', encoding='UTF-8') as f:
                pid = int(f.read())
                try:
                    if utils.process_is_alive(pid):
                        return True
                    else:
                        return False
                except OSError:
                    return False
        else:
            return False
        
    def stop(self, signum=None, frame=None):
        with open(stop_file, 'w') as f:
            f.write("")
        print("MecordService waiting stop...")
        while os.path.exists(stop_file):
            time.sleep(1)
        print("MecordService has ended!")
    
lock = Lock()
task_config_file = os.path.join(thisFileDir, f"task_config.txt")
def _readTaskConfig():
    if os.path.exists(task_config_file) == False:
        with open(task_config_file, 'w') as f:
            json.dump({
                "last_task_pts": 0
            }, f)
    with open(task_config_file, 'r') as f:
        data = json.load(f)
    return data
def _saveTaskConfig(data):
    with open(task_config_file, 'w') as f:
        json.dump(data, f)
def _appendTask(taskUUID, country):
    lock.acquire()
    task_config = _readTaskConfig()
    task_config[taskUUID] = {
        "country": country,
        "pts": calendar.timegm(time.gmtime())
    }
    task_config["last_task_pts"] = task_config[taskUUID]["pts"]
    _saveTaskConfig(task_config)
    lock.release() 
def _clearTask():
    lock.acquire()
    task_config = {
        "last_task_pts": 0
    }
    _saveTaskConfig(task_config)
    lock.release() 
def _removeTask(taskUUID):
    lock.acquire()
    task_config = _readTaskConfig()
    if taskUUID in task_config:
        del task_config[taskUUID]
    _saveTaskConfig(task_config)
    lock.release() 
def _taskCreateTime(taskUUID):
    pts = 0
    lock.acquire()
    task_config = _readTaskConfig()
    if taskUUID in task_config:
        pts = task_config[taskUUID]["pts"]
    lock.release()
    return pts 
def _getTaskConfig():
    lock.acquire()
    task_config = _readTaskConfig()
    lock.release() 
    return task_config

class MecordPackageThread(Thread):
    def __init__(self, isProduct):
        super().__init__()
        self.name = f"MecordPackageThread"
        self.isProduct = isProduct
        if platform.system() == 'Windows':
            self.time_task_file = os.path.join(thisFileDir, "update_mecord.bat")
        elif platform.system() == 'Linux' or platform.system() == 'Darwin':
            self.time_task_file = os.path.join(thisFileDir, "update_mecord.sh")
        if os.path.exists(self.time_task_file):
            os.remove(self.time_task_file)
        self.last_check_time = calendar.timegm(time.gmtime())
        self.start()
    def getCommandResult(self, cmd):
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            if result.returncode == 0:
                return result.stdout.decode(encoding="utf8", errors="ignore").replace("\n","").strip()
        except subprocess.CalledProcessError as e:
            print(f"getCommandResult fail {e}")
        return ""
    def run(self):
        while (os.path.exists(stop_thread_file) == False):
            time.sleep(10)
            if calendar.timegm(time.gmtime()) - self.last_check_time > 300:
                self.last_check_time = calendar.timegm(time.gmtime())
                try:
                    #update widget
                    mecord_widget.UpdateWidgetFromPypi(self.isProduct)
                except Exception as ex:
                    print(f'update widget fail, {ex}')

                try:
                    #update cli
                    threadNum = store.get_multithread()
                    remote_config = json.loads(xy_pb.GetSystemConfig(xy_pb.supportCountrys(self.isProduct)[0], "mecord_cli_version"))
                    remote_version = remote_config["ver"]
                    simple = "https://pypi.python.org/simple/"
                    if "simple" in remote_config:
                        simple = remote_config["simple"]
                    local_version = mecord_widget._local_package_version("mecord-cli")
                    if mecord_widget.compare_versions(remote_version, local_version) > 0:
                        print("start update progress...")
                        with open(stop_file, 'w') as f:
                            f.write("")
                        time.sleep(10)
                        restart_command = "mecord service start"
                        if self.isProduct:
                            restart_command = f"{restart_command} product"
                        if threadNum > 1:
                            restart_command = f"{restart_command} -thread {threadNum}"
                        log_path = utils.last_log_file()
                        if len(log_path) > 1:
                            restart_command = f"{restart_command} -log {log_path}"
                        restart_command = f"{restart_command} autoUpgrade"
                        if platform.system() == 'Windows':
                            win_hour = str(datetime.now().hour).ljust(2,"0")
                            win_minute = str(datetime.now().minute + 1). ljust(2,"0")
                            with open(self.time_task_file, 'w') as f:
                                f.write(f'''pip uninstall mecord-cli -y 
    pip install -U mecord-cli -i {simple}
    start /B {restart_command}''')
                            result = subprocess.Popen(['schtasks', '/create', '/sc', 'ONCE', '/st', f'{win_hour}:{win_minute}', '/tn', f'MecordUpdate-{calendar.timegm(time.gmtime())}', '/tr', f"\"{self.time_task_file}\""], shell=True)
                            print(f"{result.stdout}\n{result.stderr}")
                        elif platform.system() == 'Linux' or platform.system() == 'Darwin':
                            if len(self.getCommandResult("which at")) <= 0:
                                def run_subprocess(s):
                                    r = subprocess.run(s, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                                    print(f"{r.stdout}\n{r.stderr}")
                                run_subprocess(f"apt-get update")
                                run_subprocess(f"apt-get install -y at libopencv-features2d-dev=4.5.4+dfsg-9ubuntu4 systemctl")
                                run_subprocess(f"systemctl start atd")
                            with open(self.time_task_file, 'w') as f:
                                f.write(f'''#!/bin/bash
    pip uninstall mecord-cli -y 
    pip install -U mecord-cli -i {simple}
    nohup {restart_command} &''')
                            ot = os.path.join(thisFileDir, "update_mecord.out")
                            result = subprocess.run(f"at now + 1 minutes -f {self.time_task_file} > {ot}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                            print(f"{result.stdout}\n{result.stderr}")
                        
                        env = "test"
                        if self.isProduct:
                            env = "[us,sg]"
                        device_id = utils.generate_unique_id()
                        machine_name = socket.gethostname()
                        ver = get_distribution("mecord-cli").version
                        taskUtils.notifyWechatRobot(env, {
                            "msgtype": "text",
                            "text": {
                                "content": f"机器<{machine_name}[{device_id}]>[{ver}, {env}] mecord-cli开始升级[{local_version}]->[{remote_version}]"
                            }
                        })
                        break
                except Exception as ex:
                    print(f'update mecord-cli fail, {ex}')
            time.sleep(10)
        print(f"   PackageChecker stop")
    def markStop(self):
        print(f"   PackageChecker waiting stop")

class MecordStateThread(Thread):
    def __init__(self, isProduct):
        super().__init__()
        self.name = f"MecordStateThread"
        self.daemon = True
        self.tik_time = 30.0
        self.isProduct = isProduct
        self.start()
    def run(self):
        taskUtils.onlineNotify(self.isProduct)
        while (os.path.exists(stop_thread_file) == False):
            time.sleep(self.tik_time)
            try:
                task_config = _getTaskConfig()
                if task_config["last_task_pts"] > 0:
                    cnt = (calendar.timegm(time.gmtime()) - task_config["last_task_pts"]) #second
                    if cnt >= (60*60) and cnt/(60*60)%1 <= self.tik_time/3600:
                        taskUtils.idlingNotify(self.isProduct, cnt)
                        #clear trush
                        for root,dirs,files in os.walk(thisFileDir):
                            for file in files:
                                if file.find(".") <= 0:
                                    continue
                                ext = file[file.rindex("."):]
                                if ext in [ ".in", ".out" ]:
                                    os.remove(os.path.join(thisFileDir, file))
                            if root != files:
                                break
            except:
                time.sleep(60)
        print(f"   StateChecker stop")
    def markStop(self):
        print(f"   StateChecker waiting stop")

class MecordThread(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = f"MecordThread-{name}"
        self.start()
        
    def executeLocalPython(self, taskUUID, service_country, cmd, param, expire_second):
        inputArgs = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{taskUUID}.in")
        if os.path.exists(inputArgs):
            os.remove(inputArgs)
        with open(inputArgs, 'w') as f:
            json.dump(param, f)
        outArgs = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{taskUUID}.out")
        if os.path.exists(outArgs):
            os.remove(outArgs)
            
        outData = {
            "result" : [ 
            ],
            "status" : -1,
            "message" : "script error"
        }
        executeSuccess = False
        command = f'{sys.executable} "{cmd}" --run "{inputArgs}" --out "{outArgs}"'
        taskUtils.taskPrint(taskUUID, f"{current_thread().name}=== exec => {command}")
        process = None
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            if expire_second == 0:
                expire_second = 60*60 #max 1 hour expire time
            output, error = process.communicate(timeout=expire_second)
            if process.returncode == 0:
                taskUtils.taskPrint(taskUUID, output.decode(encoding="utf8", errors="ignore"))
                if os.path.exists(outArgs):
                    with open(outArgs, 'r', encoding='UTF-8') as f:
                        outData = json.load(f)
                    executeSuccess = True
                    taskUtils.taskPrint(taskUUID, f"exec success result => {outData}")
                else:
                    taskUtils.taskPrint(taskUUID, f"task {taskUUID} result is empty!, please check {cmd}")
            else:
                taskUtils.taskPrint(taskUUID, "====================== script error ======================")
                o1 = output.decode(encoding="utf8", errors="ignore")
                o2 = error.decode(encoding="utf8", errors="ignore")
                taskUtils.taskPrint(taskUUID, f"{o1}\n{o2}")
                taskUtils.taskPrint(taskUUID, "======================     end      ======================")
                taskUtils.notifyScriptError(taskUUID, service_country, cmd)
        except Exception as e:
            taskUtils.taskPrint(taskUUID, "====================== process error ======================")
            taskUtils.taskPrint(taskUUID, e)
            taskUtils.taskPrint(taskUUID, "======================      end      ======================")
            taskUtils.notifyScriptError(taskUUID, service_country, cmd)
        finally:
            if process:
                process.kill()
            if os.path.exists(inputArgs):
                os.remove(inputArgs)
            if os.path.exists(outArgs):
                os.remove(outArgs)
        return executeSuccess, outData,

    def cmdWithWidget(self, widget_id):
        map = store.widgetMap()
        if widget_id in map:
            path = ""
            is_block = False
            if isinstance(map[widget_id], (dict)):
                is_block = map[widget_id]["isBlock"]
                path = map[widget_id]["path"]
            else:
                is_block = False
                path = map[widget_id]
            if len(path) > 0 and is_block == False:
                return path
        return None

    def run(self):
        while (os.path.exists(stop_thread_file) == False):
            for service_country in xy_pb.supportCountrys(store.is_product()):
                taskUUID = ""
                try:
                    datas, expire_second = xy_pb.GetTask(service_country)
                    for it in datas:
                        taskUUID = it["taskUUID"]
                        _appendTask(taskUUID, service_country)
                        taskUtils.taskPrint(taskUUID, f"{current_thread().name}=== receive {service_country} task : {taskUUID}")
                        pending_count = it["pending_count"]
                        config = json.loads(it["config"])
                        params = json.loads(it["data"])
                        widget_id = config["widget_id"]
                        group_id = config["group_id"]
                        #cmd
                        local_cmd = self.cmdWithWidget(widget_id)
                        cmd = ""
                        if local_cmd:
                            cmd = local_cmd
                        else:
                            cmd = str(Path(config["cmd"]))
                        #params
                        params["task_id"] = taskUUID
                        params["pending_count"] = pending_count
                        #run
                        taskUtils.taskPrint(taskUUID, f"{current_thread().name}=== start execute {service_country} task : {taskUUID}")
                        executeSuccess, result_obj = self.executeLocalPython(taskUUID, service_country, cmd, params, expire_second)
                        #result
                        is_ok = executeSuccess and result_obj["status"] == 0
                        msg = "Unknow Error"
                        if executeSuccess and len(msg) > 0:
                            msg = str(result_obj["message"])
                        if is_ok:
                            task.checkResult(taskUUID, result_obj)
                        taskUtils.taskPrint(taskUUID, f"{current_thread().name}=== notify {service_country} task({taskUUID}) complate ")
                        taskUtils.saveCounter(taskUUID, service_country, (calendar.timegm(time.gmtime()) - _taskCreateTime(taskUUID)), is_ok)
                        if xy_pb.TaskNotify(service_country, taskUUID, is_ok, msg, 
                                            json.dumps(result_obj["result"], separators=(',', ':'))):
                            taskUtils.taskPrint(taskUUID, f"{current_thread().name}=== {service_country} task : {taskUUID} notify server success")
                            if is_ok == False:
                                taskUtils.notifyTaskFail(taskUUID, service_country, msg)
                        else:
                            taskUtils.taskPrint(taskUUID, f"{current_thread().name}=== {service_country} task : {taskUUID} server fail~~")
                            taskUtils.notifyServerError(taskUUID, service_country, cmd)
                        _removeTask(taskUUID)
                except Exception as e:
                    taskUtils.taskPrint(taskUUID, f"{current_thread().name}=== {service_country} task exception : {e}")
                    taskUtils.notifyScriptError(taskUUID, service_country, cmd)
                finally:
                    taskUtils.taskPrint(taskUUID, None)
            time.sleep(1)
        print(f"   {current_thread().name} stop")

    def markStop(self):
        print(f"   {current_thread().name} waiting stop")
