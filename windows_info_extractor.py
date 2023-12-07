import wmi
import win32api
import win32security
import win32con
import win32cred
import win32crypt
import win32net
import win32evtlog
import time

c = wmi.WMI()

def write_file(title, message):
  with open(title, 'a') as f:
    f.write(f'\n{message}\n')

def get_sys_info():
  for os in c.Win32_OperatingSystem():
    osys = os.Caption,
    version = os.Version,
    mem_size = os.TotalVisibleMemorySize, 
    sys_dir = os.SystemDirectory,
    os_arch = os.OSArchitecture,
    users_num = os.NumberOfUsers
    sys_message = f'SYSTEM INFORMATION:\n Operating system: {osys} Version: {version}\n Total memory size: {mem_size}\n System directory: {sys_dir}\n System Architecture: {os_arch} Number of users: {users_num}'
    write_file('output.txt', sys_message)

def get_address():
  for interface in c.Win32_NetworkAdapterConfiguration(IPEnabled=1):
    for ip_address in interface.IPAddress:
      description = interface.Description
      mac_addr = interface.MACAddress
      ip_addr = ip_address
      address_message = f'Network interface:\n {description}\n MAC address: {mac_addr}\n IP address: {ip_addr}'
      write_file('output.txt', address_message)

def get_process():
  process_monitor = c.Win32_Process.watch_for("creation")
  t_end = time.time() + 60
  while time.time() < t_end:
    try:
      process = process_monitor()
      session_id = process.SessionId
      pid = process.ProcessId
      parent_pid = process.ParentProcessId
      expath = process.ExecutablePath
      owner = process.GetOwner()
      description = process.Description
      privileges = get_privileges()
      process_message = f'PROCESS:\n SessionID: {session_id}\n PID/ParentPID: {pid, parent_pid}\n Executable Path: {expath}\n Description: {description}\n Owner: {owner}\n Privileges: {privileges}'
      write_file('output.txt', process_message)
    except Exception as proc_err:
      proc_err_message = f'Something went wrong with processes analysis: {proc_err}'
      write_file('output.txt', proc_err_message)
      pass

def get_privileges():
  token = win32security.OpenProcessToken(win32api.GetCurrentProcess(), win32con.TOKEN_QUERY)
  privileges = win32security.GetTokenInformation(token, win32security.TokenPrivileges)
  privs = ''
  for priv_id, flags in privileges:
    if flags == (win32security.SE_PRIVILEGE_ENABLED | win32security.SE_PRIVILEGE_ENABLED_BY_DEFAULT):
      privs += f'{win32security.LookupPrivilegeName(None, priv_id)}'
  return privs      
 
def get_credentials():
  creds = []
  try:
    creds = win32cred.CredEnumerate(None, 1)
  except Exception:
    pass
  if not creds:
    not_cred_message = "Credentials not found"
    write_file('output.txt', not_cred_message)
    return
  for package in creds:
    try:
      target = package['TargetName']
      creds_info = win32cred.CredRead(target, win32cred.CRED_TYPE_GENERIC)
      creds_message = f'CREDENTIALS:\n {creds_info}'
      write_file('output.txt', creds_message)
    except Exception as cred_err:
      cred_err_message = f'Something went wrong with credentials retrieve: {cred_err}'
      write_file('output.txt', cred_err_message)
      pass
        
def get_logs():
  host = None
  logType = 'Security'
  handle = win32evtlog.OpenEventLog(host, logType)
  flags= win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
  while True:
    try:
      events = win32evtlog.ReadEventLog(handle, flags,0)
      if events:
        for event in events:
          category = event.EventCategory
          time = event.TimeGenerated
          source_name = event.SourceName
          id = event.EventID
          type = event.EventType
          data = event.StringInserts
          if data:
            ev_data = event.Data.decode('utf-8')
            for msg in data:
              mess = msg
              log_message = f'LOGS:\n Event Category: {category}\n Time Generated: {time}\n Source Name: {source_name}\n Event ID: {id}\n Event Type: {type}\n Event Data: {ev_data}\n {mess}'
              write_file('output.txt', log_message)
    except Exception as logs_err:
      logs_err_message = f'Something went wrong with log analysis: {logs_err}'
      write_file('output.txt', logs_err_message)
      pass
    break

if __name__ == "__main__":
  get_sys_info()
  get_address()
  get_process()
  get_credentials()
  get_logs()
