# Magisk Patcher CLI

Magisk Patcher CLI 是一个命令行版本的Magisk boot镜像修补工具，基于原版Magisk Patcher v4.1.0提取的核心功能。


- 🔧 **自动修补** - 自动提取Magisk APK中的必要文件并修补boot镜像
- 📱 **多架构支持** - 支持arm, arm64, x86, x86_64等多种设备架构
- 🔒 **安全选项** - 支持禁用dm-verity验证和强制加密
- 🛠️ **灵活配置** - 支持修补recovery镜像和传统SAR设备
- 🧹 **自动清理** - 修补完成后自动清理临时文件
- 📊 **详细日志** - 支持详细输出模式，便于调试

## 🚀 快速开始

### 系统要求

- Windows操作系统
- Python 3.8以上最好[只需要基础py环境]

### 安装

1. 下载项目文件到本地
2. 确保当前目录包含以下文件：
   - `magiskpatcher_cli.py` - 主程序
   - `magiskboot.exe` - Magisk boot工具
   - `cli_boot_patch.py` - 修补核心模块
   - `cli_utils.py` - 工具函数模块

### 基本用法

```bash
# 基本修补（arm64架构）
python magiskpatcher_cli.py boot.img --magisk magisk.apk --arch arm64

# 禁用验证和加密
python magiskpatcher_cli.py boot.img --magisk magisk.apk --no-verity --no-encrypt

# 修补recovery镜像
python magiskpatcher_cli.py recovery.img --magisk magisk.apk --recovery

# 详细输出模式
python magiskpatcher_cli.py boot.img --magisk magisk.apk --verbose

# 指定输出文件名
python magiskpatcher_cli.py boot.img --magisk magisk.apk --output "patched_boot.img"
```

## 📖 命令行参数

### 主要选项

| 参数 | 缩写 | 描述 | 默认值 |
|------|------|------|--------|
| `--magisk` | `-m` | Magisk APK文件路径（必需） | `自己找` |
| `--arch` | `-a` | 目标设备架构 | `arm64` |

### 修补选项

| 参数 | 描述 |
|------|------|
| `--no-verity` | 禁用dm-verity验证 |
| `--no-encrypt` | 禁用强制加密 |
| `--patch-vbmeta` | 修补vbmeta标志 |
| `--recovery` | 修补recovery镜像而不是boot镜像 |
| `--legacy-sar` | 传统SAR设备支持 |

### 其他选项

| 参数 | 缩写 | 描述 |
|------|------|------|
| `--verbose` | `-v` | 详细输出模式 |
| `--version` | - | 显示版本信息 |

## 🔧 工作流程

1. **程序启动** - 检查参数和文件存在性
2. **环境检测** - 检测系统环境和Magisk版本
3. **文件提取** - 从APK中提取必要的Magisk文件
4. **镜像解包** - 使用magiskboot工具解包boot镜像
5. **镜像修补** - 修补ramdisk和内核
6. **重新打包** - 生成修补后的boot镜像
7. **清理工作** - 自动清理临时文件

## 📁 文件结构

```
root/
├── magiskpatcher_cli.py      # 主程序
├── cli_boot_patch.py         # boot镜像修补核心模块
├── cli_utils.py              # 工具函数模块
├── magiskboot.exe            # Magisk boot工具
├── 启动.bat                   # Windows启动脚本
├── 使用说明.txt               # 详细使用说明
```

## 🐛 故障排除

### 常见问题

1. **文件不存在错误**
   - 确保boot镜像和Magisk APK文件路径正确
   - 检查文件是否完整无损

2. **架构不匹配**
   - 使用正确的设备架构参数
   - 确认boot镜像与设备架构匹配

3. **修补失败**
   - 确保boot镜像是原始未修改版本
   - 使用`--verbose`参数查看详细错误信息

4. **magiskboot工具缺失**
   - 确保当前目录包含magiskboot.exe文件
   - 或确保bin/windows/目录下有对应架构的magiskboot工具

### 错误处理

- 程序会自动检测错误并显示具体信息
- 使用`--verbose`参数可以查看详细的调试信息
- 修补失败时会显示具体失败原因

## 📄 许可证

本项目基于原版Magisk Patcher v4.1.0，遵循相应的开源协议。

## 👥 作者

- **Little** - 项目开发者
- 酷安: Little114


