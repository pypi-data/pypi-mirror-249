# MainShortcuts by MainPlay YT
# https://t.me/MainPlay_YT
import MainShortcuts.addon as _a
import json as _json
import os as _os
import platform as _platform
import sys as _sys
import shutil as _shutil
from glob import glob as _glob
# Универсальные команды
class mproc:
  args=_sys.argv # Аргументы запуска программы
class mpath: # Операции с путями к файлам/папкам
  sep=_os.sep # Разделитель в пути файла
  def exists(a): # Объект существует?
    return _os.path.exists(a)
  def merge(a): # Собрать путь к объекту из массива
    return mpath.sep.join(a)
  def split(a): # Разложить путь к объекту на массив
    return a.split(mpath.sep)
  def info(a,listdir=False,listlinks=False):
    info={"dir":None,"size":None,"exists":None,"ext":None,"fullname":None,"fullpath":None,"link":None,"name":None,"path":None,"realpath":None,"split":[],"type":None,}
    info["path"]=a
    info["split"]=mpath.split(a)
    info["dir"]=mpath.merge(info["split"][:-1])
    info["fullname"]=info["split"][-1]
    if "." in info["fullname"]:
      info["ext"]=info["fullname"].split(".")[-1]
      info["name"]=".".join(info["fullname"].split(".")[:-1])
    else:
      info["ext"]=None
      info["name"]=info["fullname"]
    info["exists"]=mpath.exists(a)
    if info["exists"]:
      info["fullpath"]=_os.path.abspath(a)
      info["link"]=_os.path.islink(a)
      if info["link"]:
        info["realpath"]=_os.path.realpath(a)
      if _os.path.isfile(a):
        info["size"]=_os.path.getsize(a)
        info["type"]="file"
      elif _os.path.isdir(a):
        info["type"]="dir"
        if listdir:
          tmp=_a.listdir(a,listlinks)
          info["dirs"]=tmp["d"]
          info["files"]=tmp["f"]
          info["size"]=tmp["s"]
      else:
        info["type"]="unknown"
    return info
  def delete(p):
    info=mpath.info(p)
    if info["exists"]:
      if info["type"]=="file":
        _os.remove(p)
      elif info["type"]=="dir":
        _os.rmdir(p)
      else:
        raise Exception("Unknown type: "+info["type"])
  def copy(fr,to):
    t=mpath.info(fr)["type"]
    if t=="file":
      _shutil.copy(fr,to)
    elif t=="dir":
      _shutil.copytree(fr,to)
    else:
      raise Exception("Unknown type: "+t)
  def move(fr,to):
    _shutil.move(fr,to)
  def rename(fr,to):
    _os.rename(fr,to)
  def link(fr,to,force=False):
    if mpath.exists(to) and force:
      mpath.delete(to)
    os.symlink(fr,to)
  def format(a,b="_"):
    for i in ["/","\\"]:
      a=a.replace(i,mpath.sep)
    for i in ["\n",":","*","?","\"","<",">","|","+","%","!","@"]:
      a=a.replace(i,b)
    return a
class mos: # Операции с системой
  platform=_platform.system() # Тип ОС
def exit(code=0): # Закрытие программы с кодом
  _sys.exit(code)
class mfile: # Операции с файлами
  def read(p,encoding="utf-8"): # Прочитать текстовый файл
    if mpath.info(p)["type"]=="file":
      with open(p,"r",encoding=encoding) as f:
        t=f.read()
    else:
      t=""
    return t
  def write(p,text="",encoding="utf-8",force=False): # Записать текстовый файл
    if mpath.info(p)["type"]=="dir" and force:
      _os.remove(p)
    with open(p,"w",encoding=encoding) as f:
      f.write(f"{text}")
    return True
  def open(p): # Открыть содержимое файла
    if _os.path.exists(p):
      with open(p,"rb") as f:
        b=f.read()
    else:
      b=None
    return b
  def save(p,bin=None,force=False): # Сохранить содержимое файла
    if mpath.info(p)["type"]=="dir" and force:
      _os.remove(p)
    with open(p,"wb") as f:
      f.write(bin)
    return True
  def delete(p):
    t=mpath.info(p)["type"]
    if t=="file":
      _os.remove(p)
    else:
      raise Exception("Unknown type: "+t)
  def copy(fr,to):
    t=mpath.info(p)["type"]
    if t=="file":
      _shutil.copy(fr,to)
    else:
      raise Exception("Unknown type: "+t)
  def move(fr,to):
    t=mpath.info(p)["type"]
    if t=="file":
      _shutil.move(fr,to)
    else:
      raise Exception("Unknown type: "+t)
  def rename(fr,to):
    t=mpath.info(p)["type"]
    if t=="file":
      _os.rename(fr,to)
    else:
      raise Exception("Unknown type: "+t)
class mdir: # Операции с папками
  def create(p): # Создать папку
    if not mpath.exists(p):
      _os.makedirs(p)
    return True
  def delete(p):
    t=mpath.info(p)["dir"]
    if t=="file":
      _os.rmdir(p)
    else:
      raise Exception("Unknown type: "+t)
  def copy(fr,to):
    t=mpath.info(p)["dir"]
    if t=="file":
      _shutil.copytree(fr,to)
    else:
      raise Exception("Unknown type: "+t)
  def move(fr,to):
    t=mpath.info(p)["dir"]
    if t=="file":
      _shutil.move(fr,to)
    else:
      raise Exception("Unknown type: "+t)
  def rename(fr,to):
    t=mpath.info(p)["dir"]
    if t=="file":
      _os.rename(fr,to)
    else:
      raise Exception("Unknown type: "+t)
class mstr: # Операции с текстом
  def array2str(a):
    r=[]
    for i in a:
      r.append(str(i))
    return r
  def dict2str(d):
    r={}
    for i in d:
      r[i]=str(d[i])
    return r
  class replace:
    def multi(text=None,dict=None): # Мульти-замена {"что заменить":"чем заменить"}
      t=str(text)
      for i in dict:
        t=t.replace(i,str(dict[i]))
      return t
    def all(text=None,fr=None,to=None): # Замена пока заменяемый текст не исчезнет. МОЖЕТ ВЫЗВАТЬ ВЕЧНЫЙ ЦИКЛ
      t=str(text)
      a=str(fr)
      b=str(to)
      if a in b:
        raise endlessCycle("\""+a+"\" is contained in \""+b+"\", this causes an infinite loop")
      while a in t:
        t=t.replace(a,b)
      return t
class mjson: # Операции с JSON
  def encode(data=None,mode="c",indent=2,sort=True): # Данные в текст
    if mode in ["c","compress","min","zip"]: # Сжатый
      t=_json.dumps(data,separators=[",",":"],sort_keys=sort)
    elif mode in ["pretty","p","print","max"]: # Развёрнутый
      t=_json.dumps(data,indent=int(indent),sort_keys=sort)
    else: # Без параметров
      t=_json.dumps(data,sort_keys=sort)
    return t
  def decode(text): # Текст в данные
    return _json.loads(str(text))
  def write(p=None,data=None,encoding="utf-8",mode="c",indent=2,sort=True,force=False): # Данные в файл
    if mpath.info(p)["type"]=="dir" and force:
      _os.remove(p)
    with open(p,"w",encoding=encoding) as f:
      f.write(mjson.encode(data,mode=mode,indent=indent,sort=sort))
    return True
  def read(p,encoding="utf-8"): # Данные из файла
    with open(p,"r",encoding=encoding) as f:
      return _json.load(f)
# Команды для разных ОС
if mos.platform=="Windows": # Windows
  def clear():
    _os.system("cls")
elif mos.platform=="Linux": # Linux
  def clear():
    _os.system("clear")
elif mos.platform=="Darwin": # MacOS
  pass
else: # Неизвестный тип
  print("MainShortcuts WARN: Unknown OS \""+mos.platform+"\"")
