import platform
import zipfile
from os import chmod
from sys import stderr

def retTypeAndMachine():
    ostype = platform.system().lower()
    if ostype.find("cygwin") >= 0:
        ostype = "windows"
    machine = platform.machine().lower()
    if machine == 'aarch64_be' \
        or machine == 'armv8b' \
        or machine == 'armv8l':
        machine = 'aarch64'
    if machine == 'i386' or machine == 'i686':
        machine = 'x86'
    if machine == "amd64":
        machine = 'x86_64'
    return ostype, machine

def getMagiskApkVersion(fname: str) -> str | None:
    valid_flag = False
    magisk_ver_code = "00000"
    try:
        with zipfile.ZipFile(fname, 'r') as z:
            for i in z.filelist:
                if "util_functions.sh" in i.filename:
                    valid_flag = True
                    for line in z.read(i).splitlines():
                        if b"MAGISK_VER_CODE" in line:
                            magisk_ver_code = line.split(b"=")[1]
            if not valid_flag: 
                return None
    except Exception as e:
        print(f"读取Magisk APK失败: {e}", file=stderr)
        return None
    
    return magisk_ver_code

def convertVercode2Ver(value: str) -> str:
    if isinstance(value, bytes):
        value = value.decode('utf-8')
    
    if len(value) >= 3:
        return value[0:2] + "." + value[2:3]
    else:
        return value

def parseMagiskApk(apk: str, arch:["arm64", "arm", "x86", "x86_64"]="arm64", log=stderr):
    def archconv(a):
        ret = a
        match a:
            case "arm64":
                ret = "arm64-v8a"
            case "arm":
                ret = "armeabi-v7a"
        return ret
    
    def archto32(a):
        ret = a
        match a:
            case "arm64-v8a":
                ret = "armeabi-v7a"
            case "x86_64":
                ret = "x86"
        return ret

    def saveto(bytes, path):
        with open(path, 'wb') as f:
            f.write(bytes)

    print("- 开始解压需要的文件...", file=log)
    
    arch = archconv(arch)
    os_type, p = retTypeAndMachine()
    pp = "x86_64"
    if p == "aarch64":
        pp = "arm64-v8a"
    elif p == "arm":
        pp = "armeabi-v7a"
    
    try:
        with zipfile.ZipFile(apk) as z:
            for l in z.filelist:
                if "stub.apk" in l.filename:
                    saveto(z.read(l), "stub.apk")
                    print("  ✓ 提取 stub.apk", file=log)
                
                if os_type != 'windows':
                    if f"lib/{pp}/libmagiskboot.so" in l.filename:
                        import os
                        os.makedirs("bin", exist_ok=True)
                        saveto(z.read(l), "bin/magiskboot")
                        chmod("bin/magiskboot", 0o755)
                        print(f"  ✓ 提取 magiskboot (平台: {pp})", file=log)

                if f"lib/{arch}/libmagiskinit.so" in l.filename:
                    try:
                        saveto(z.read(f"lib/{archto32(arch)}/libmagisk32.so"), "magisk32")
                        print("  ✓ 提取 magisk32", file=log)
                    except:
                        print("  ⚠ 无法提取 magisk32", file=log)
                    
                    if arch in ["arm64-v8a", "x86_64"]:
                        try:
                            saveto(z.read(f"lib/{arch}/libmagisk64.so"), "magisk64")
                            print("  ✓ 提取 magisk64", file=log)
                        except:
                            print("  ⚠ 无法提取 magisk64", file=log)
                    
                    try:
                        saveto(z.read(f"lib/{arch}/libmagiskinit.so"), "magiskinit")
                        print("  ✓ 提取 magiskinit", file=log)
                    except:
                        print("  ⚠ 无法提取 magiskinit", file=log)
    
    except Exception as e:
        print(f"解压Magisk APK失败: {e}", file=log)
        return False
    
    print("✓ 文件提取完成", file=log)
    return True

if __name__ == "__main__":
    print("Utils模块测试")
    os_type, arch = retTypeAndMachine()
    print(f"系统: {os_type}, 架构: {arch}")
    
    test_ver = "26100"
    print(f"版本代码 {test_ver} -> 版本号 {convertVercode2Ver(test_ver)}")