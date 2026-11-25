# DeepHand — 面向机器人学习时代的开源触觉灵巧手

<div align="center">

**16 总自由度 · 13 主动自由度 · 283 个三轴触觉单元 · 约 700 g · BOM ≈ $3,000 · 装配 < 3 小时**

*开源触觉灵巧手平台 —— 直驱低阻抗 · 原生集成触觉 · 全栈软件开放*

本项目为 UCLA RoMeLa 实验室 **MIDAS Hand** 的一比一复刻与中文社区版，项目更名为 **DeepHand**。

</div>

---

## 目录

- [项目介绍](#项目介绍)
- [项目背景与研发过程](#项目背景与研发过程)
- [核心参数](#核心参数)
- [与同类灵巧手对比](#与同类灵巧手对比)
- [仓库结构](#仓库结构)
- [复现方法：从零搭建一只 DeepHand](#复现方法从零搭建一只-deephand)
  - [第一步：物料采购](#第一步物料采购)
  - [第二步：3D 打印结构件](#第二步3d-打印结构件)
  - [第三步：机械装配](#第三步机械装配)
  - [第四步：控制 API 安装与调试](#第四步控制-api-安装与调试)
  - [第五步：首次 homing 标定](#第五步首次-homing-标定)
  - [第六步：触觉传感器接入](#第六步触觉传感器接入)
  - [第七步：MuJoCo 仿真](#第七步mujoco-仿真)
  - [第八步：摄像头遥操作](#第八步摄像头遥操作)
- [常见问题排查](#常见问题排查)
- [研究前瞻](#研究前瞻)
- [致谢与许可](#致谢与许可)

---

## 项目介绍

**DeepHand** 是一款全开源的拟人化触觉灵巧手平台，一比一复刻自加州大学洛杉矶分校（UCLA）RoMeLa 机器人与机构实验室（Dennis Hong 教授团队）于 2026 年发布的 **MIDAS Hand**（*Modular low-Impedance Directly-driven Anthropomorphic Sensing Hand*，arXiv:2607.14487）。

它的设计目标是：在**单一平台**上同时满足机器人学习研究对末端执行器的全部核心诉求——

1. **人形尺度**：整机 205 × 120 × 55 mm，重约 700 g，接近成年人手，无需占用小臂空间即可挂载于常见 6/7 自由度机械臂末端（只需打印一个转接件）。
2. **原生触觉**：四指指尖集成帕西尼（PaXini）GEN3 三轴触觉传感器，共 **283 个触觉单元（taxel）**，可同时感知法向压力、横向剪切力与滑移信号，最高 83.3 Hz。
3. **直驱低阻抗**：13 台相同的 ROBOTIS Dynamixel XM335-T323-T 伺服电机**直驱**刚性连杆，无绳索传动，支持反向驱动（可用手直接拨动手指），减少绳驱方案的张紧、标定与维护负担。
4. **模块化低成本**：食指/中指/无名指为完全相同的可拆卸模块，换指 **< 15 分钟**；BOM 成本约 **$3,000**；熟练后整机装配 **< 3 小时**。
5. **全栈开放**：CAD（Onshape/STEP）、BOM、装配文档、PCB 工程、Python 控制 API、MuJoCo 仿真模型、人手重定向与摄像头遥操作工具链全部开源。

项目已通过 **10,000+ 次手指开合**耐久性测试，并具备硬件一致性重复测试数据。

### 能做什么？

- **灵巧在手操作**：握持剪刀连续开合、不放下工具的情况下用指间配合调整物体位姿
- **触觉力控闭环**：接触发生瞬间实时反馈受力变化，支撑滑移检测与柔顺抓取
- **视觉遥操作**：单个摄像头识别 MediaPipe 人手关键点 → 重定向 → 真机/仿真
- **模仿学习数据采集**：关节 + 触觉同步数据流，直接对接机器人学习训练管线
- **Sim2Real**：MuJoCo 全手模型（含 PIP–DIP 闭环连杆约束）与真机同步

---

## 项目背景与研发过程

### 为什么需要一只"够得着"的触觉灵巧手？

灵巧操作算法是数据饥渴型的，但现有硬件长期在四个维度上互相妥协：

- **商业灵巧手**（Allegro、Sharpa、Wuji 等）：性能强但价格昂贵、封闭，难以修改；
- **开源灵巧手**（LEAP Hand、RUKA、ORCA、CRAFT 等）：多数缺少触觉，或采用腱驱结构，绳索磨损与重复标定使长期实验维护成本高。

MIDAS Hand（即本仓库 DeepHand 的原型）的答案是**直驱 + 原生触觉 + 3D 打印模块化 + 全栈软件**的组合拳：

| 设计决策 | 解决的问题 |
|---|---|
| 直驱低阻抗（无绳驱） | 消除绳索张紧/磨损/标定维护；反向驱动特性让手指可以直接用手外力拨动，人机交互安全柔顺 |
| DIP 被动交叉四连杆耦合 | 非拇指指的 DIP 关节经四连杆与 PIP 欠驱动耦合，用 13 个主动自由度实现 16 个关节自由度，逼近人手包络抓取形态 |
| 指尖三轴触觉阵列 | 让机器人不仅知道"手指在哪"，还知道"接触是否发生、力往哪个方向变化"——滑移检测与力控闭环的硬件前提 |
| 全电机内置掌部 | 全部 13 台电机与电控集成在手部空间内，无需占用小臂空间，换机械臂只需一个 3D 打印转接件 |
| 相同电机 × 相同指模块 | 单一型号电机（XM335-T323-T）×13；食/中/无名指为同一模块，备件、维修、替换成本极低 |

### 研发与开源过程（时间线）

1. **概念与机构设计**：确定直驱 + 被动耦合连杆方案，完成 Onshape 参数化 CAD 设计；
2. **电控集成**：设计掌部 TTL 配电/通信板 PCB（见 `communication_board/`），13 台 Dynamixel 菊花链 + 帕西尼 GEN3 高速触觉板；
3. **软件栈开发**：`deephand_api`（电机/触觉驱动与标定）→ `deephand_mujoco`（全手 MJCF/URDF 仿真）→ `deephand_retargeter`（dex-retargeting 封装）→ `deephand_teleop`（MediaPipe 摄像头遥操作）；
4. **耐久性与一致性测试**：10,000+ 次开合、重复性标定测试；
5. **全栈开源发布**：CAD/BOM/装配指南/PCB/四软件仓库全部公开，与 ROBOTIS、帕西尼合作推出官方采购套装（Dynamixel Bundle ≈ $2,557 + 触觉开发套件），论文投稿 ICRA；
6. **社区复刻**：本项目（DeepHand）即在官方开源文件基础上的一比一复刻中文社区版，代码逻辑与硬件设计完全一致，仅作项目更名与中文文档补全。

---

## 核心参数

| 参数 | 数值 |
|---|---|
| 总自由度 | 16 DoF（13 主动 + 3 被动） |
| 驱动 | 13 × Dynamixel XM335-T323-T（直驱） |
| 触觉 | 283 个三轴 taxel（拇指 127 + 食/中/无名指各 52），最高 83.3 Hz |
| 尺寸 | 205 × 120 × 55 mm |
| 重量 | ≈ 700 g |
| BOM | ≈ $3,000 |
| 装配时间 | < 3 小时（熟练） |
| 换指时间 | < 15 分钟 |
| 耐久性 | 10,000+ 次手指开合测试 |

**触觉分布**（来自 `deephand_api` 硬件布局表）：

| 手指 | 传感器型号 | 触觉单元数 | 板卡设备地址 |
|---|---|---|---|
| 拇指 | PX6AX-GEN3-DP-M2826-Omega | 127 | 1 |
| 食指 | PX6AX-GEN3-DP-S2015-Elite | 52 | 2 |
| 中指 | PX6AX-GEN3-DP-S2015-Elite | 52 | 3 |
| 无名指 | PX6AX-GEN3-DP-S2015-Elite | 52 | 4 |

## 与同类灵巧手对比

| 平台 | 人形尺度 | 直驱 | 三轴触觉 | 成本 |
|---|---|---|---|---|
| LEAP Hand | — | — | — | ≈ $2K |
| RUKA v2 | ✓ | —（腱驱） | — | — |
| ORCA Hand | ✓ | — | 可选 | $6K–9K |
| Allegro | — | — | — | 贵 |
| Sharpa / Wuji | ✓ | — | 部分 | 商业封闭 |
| **DeepHand (MIDAS)** | ✓ | ✓ | ✓（283 taxel） | **≈ $3K** |

---

## 仓库结构

```text
deephand/
├── deephand_api/          # 核心 Python API：13 路 Dynamixel 控制 + 帕西尼触觉驱动、homing/标定、Qt 可视化
├── deephand_mujoco/       # MuJoCo 全手仿真：MJCF/URDF/STL 网格、交互式/无头仿真入口、PIP-DIP 闭环约束
├── deephand_retargeter/   # 人手重定向：dex-retargeting 封装、landmark 适配、中性标定、被动耦合模式
├── deephand_teleop/       # 摄像头遥操作：MediaPipe 捕捉 → 重定向 → 打印/MuJoCo/真机 后端
└── communication_board/   # 掌部通信/配电板 PCB：原理图、BOM、贴片坐标、STEP、Gerber、源文件
```

> 硬件侧资源（Onshape 可编辑 CAD、整手 STEP、3MF 打印板、BOM、装配视频与指南）见原型项目官网 midas-hand.com 的 Parts / CAD / Assembly 分区。

---

## 复现方法：从零搭建一只 DeepHand

### 第一步：物料采购

**执行器与电控**（ROBOTIS 官方 "MIDAS Hand Bundle"，约 $2,557.26）：

| 物品 | 数量 |
|---|---|
| Dynamixel XM335-T323-T 伺服电机 | 13 |
| Dynamixel 入门套件（U2D2 / U2D2 电源套件） | 1 |
| 机器人线缆 X3P 180 mm | 10 |

**触觉传感器**（帕西尼 "MIDAS HAND 合作款" 开发套件）：

| 物品 | 数量 |
|---|---|
| PX6AX-GEN3-DP-S2015-Elite 指尖传感器（20×15×10 mm） | 3 |
| PX6AX-GEN3-DP-M2826-Omega 指尖传感器（28×26×14 mm） | 1 |
| DF53-DF53 280 mm 触觉传感器连接线 | 4 |
| 高速通信集成板（32×34 mm） | 1 |

**结构件**：全部 3D 打印件（Onshape CAD → STEP/3MF 下载打印）+ 标准紧固件（BOM 清单给出供应商与替代件）。国内复刻可按 BOM 在淘宝/立创商城采购紧固件，电机与触觉传感器亦可分别通过 ROBOTIS 授权代理与帕西尼感知（深圳）采购。

### 第二步：3D 打印结构件

1. 从 CAD 区下载整手 STEP 或分板 3MF；
2. 推荐 Bambu Lab（拓竹）系列打印机；CAD 视频教程演示如何将源 CAD 复制到个人工作区并按你的打印机公差调整配合面；
3. 关键配合面（连杆孔、电机安装止口）建议按公差测试件先校准，打印后去毛刺。

### 第三步：机械装配

按官网 Assembly 分区的装配顺序视频操作：

1. 单指模块装配（食/中/无名指为同一模块，装一个即掌握三个）；
2. 拇指模块装配；
3. 电机装入掌部框架，接线（X3P 菊花链）；
4. 通信板安装（PCB 文件见 `communication_board/`，含原理图 PDF、BOM/CPL CSV、Gerber）；
5. 整手总装。熟练后全程 < 3 小时。

### 第四步：控制 API 安装与调试

```bash
git clone https://github.com/open-embodied/deephand.git
cd deephand/deephand_api

python3 -m venv .venv
source .venv/bin/activate
pip install .            # 开发模式用 pip install -e .
```

授予串口权限并检查适配器路径：

```bash
sudo usermod -aG dialout "$USER"   # 重新登录后生效
ls /dev/serial/by-id/*
```

**USB 延迟优化（重要）**：FTDI 芯片（U2D2）默认 16 ms USB 串口延迟会把控制环卡在约 62.5 Hz。安装持久化 udev 规则：

```bash
./setup_dynamixel_latency.sh
```

**冒烟测试**（默认电机 ID 0–12，可 `--motors 0,1,2,3` 测子集；运行时勿开 Dynamixel Wizard，它会占用串口）：

```bash
python examples/smoke_test.py
python -m deephand_api --help   # 电机扫描、实时位置读取、homing、触觉重标定等子命令
```

**最小示例**：

```python
from deephand_api import HandConfig, DeepHand
import numpy as np

config = HandConfig.load()

with DeepHand(config) as hand:
    print(hand.ping())
    print(hand.verify_models())
    hand.configure(enable_torque=True)
    hand.set_positions(np.zeros(13))
    print(hand.read_pos())
```

### 第五步：首次 homing 标定

装配完成并通过冒烟测试后，必须先执行 homing：电机依次推向各自的机械硬限位，结合 CAD 偏置计算软件零点并保存。

```bash
python -m deephand_api --home          # 全部 13 电机
# 或部分标定：--home-thumb / --home-fingers
```

- 标定保存在**主机** `~/.deephand/config.yaml`（换电脑需重新 homing）；
- 需要重新 homing 的时机：首次装配后、更换电机舵盘/连杆后、电机原始位置与关节零点的物理关系变化后、更换主机后；
- 平时启动程序无需每次 homing，直接加载已保存配置即可。

### 第六步：触觉传感器接入

帕西尼板经 USB 连接（通常 `/dev/ttyACM0`，921600 波特率），单板时自动检测端口。

```python
from deephand_api import HandConfig, DeepHand, PaxiniConfig, PaxiniHandSensor

hand_config = HandConfig.load()
tactile = PaxiniHandSensor(PaxiniConfig())   # 自动检测端口

with DeepHand(hand_config, tactile_sensor=tactile) as hand:
    hand.configure(enable_torque=True)
    hand.recalibrate_tactile()    # 重标零——确保此时没有任何物体接触传感器！
    data = hand.read_tactile()    # {手指名: ndarray (N, 3)}，列为 [Fx, Fy, Fz]，单位 N
    fz = hand.read_tactile_fz()   # 各触觉单元法向力
```

> **习惯要求**：每次连接后、无接触状态下先调一次 `recalibrate()` 重置零点；调用瞬间的任何接触都会成为新零点。

**Qt 可视化/录制/回放工具**：

```bash
pip install ".[qt]"
python -m deephand_api.tactile.paxini_tactile_qt            # 实时流
python -m deephand_api.tactile.paxini_tactile_qt --csv rec.csv            # 录制
python -m deephand_api.tactile.paxini_tactile_qt --replay-only --csv rec.csv  # 回放
```

**控制模式说明**：默认运行模式为 **5（电流基位置控制）**——仍以位置为目标，但用 Goal Current 作为力矩上限，接触时会"让步"而非死顶，适合机器人学习、遥操作与抓取。其他模式（0 电流 / 1 速度 / 3 位置 / 16 PWM）适用场景见 `deephand_api/README.md`。做遥操作演示时建议关闭运动规划（`profile_velocity_rad_s=None, profile_acceleration_rad_s2=None`）以获得最大响应性。

### 第七步：MuJoCo 仿真

```bash
cd deephand/deephand_mujoco
python assets/simulate_whole_hand.py                     # 交互式查看器
python assets/simulate_whole_hand.py --no-viewer --steps 1000   # 无头冒烟测试
```

三个非拇指手指使用 MJCF `equality/connect` 约束闭合 PIP–DIP 连杆环（不使用查找表）。资产包含 `assets/deephand_description/deephand_whole_hand.xml`（MJCF）、`deephand_hand_urdf.urdf` 与 STL 网格。

### 第八步：摄像头遥操作

```bash
cd deephand/deephand_teleop
pip install -e ../deephand_api
pip install -e ../deephand_retargeter
pip install -e .

midas 位置见各 README；真机遥操作默认入口：
midas-hand-teleop            # 硬件后端：/dev/ttyUSB0，350 mA 限流，50 Hz 指令插值
midas-hand-teleop --backend print    # 只打印重定向后的关节目标（无硬件联调）
midas-hand-teleop --show --backend print --debug-targets   # 摄像头叠加调试
```

交互要点：

- `--show` 模式下摆出希望对应 DeepHand 零位的姿势按 `c` 捕获中性标定，按 `r` 清除；
- MuJoCo 模型为右手；左手输入会自动镜像到右手约定；镜像摄像头画面需加 `--selfie`；
- MediaPipe 模型 `hand_landmarker.task` 首次运行自动缓存到 `~/.cache/deephand_teleop/`。

**遥操作数据流**：MediaPipe 摄像头输入 → `deephand_retargeter`（向量法重定向，仅主动关节；被动 DIP 可选 `pip_dip_lookup` 查表填充）→ 输出适配器 → 打印 / MuJoCo / 真机后端。

---

## 常见问题排查

| 现象 | 处理 |
|---|---|
| 扫描不到电机 | 检查 U2D2 供电（电机需独立 11.1V 供电）、菊花链接线、串口是否被 Dynamixel Wizard 占用 |
| 控制频率上不去 | 运行 `setup_dynamixel_latency.sh` 将 USB 延迟从 16 ms 降至 1 ms |
| 触觉读数漂移 | 在无接触状态下调用 `recalibrate()` 重置零点；检查接地与线缆 |
| 手指方向反了 | 关节方向遵循右手定则（拇指沿舵盘轴）；重新执行 homing |
| 更换电脑后位置异常 | 标定存于主机 `~/.deephand/config.yaml`，换机必须重新 `--home` |
| 某根手指损坏 | 食/中/无名指为相同模块，15 分钟内整指替换 |

---

## 研究前瞻

1. **触觉驱动的操作智能**：283 个三轴 taxel 提供法向力 + 剪切力 + 滑移信号，是滑移检测、接触状态估计、触觉 SLAM 与"手感"表征学习的理想数据源；关节 + 触觉同步流可直接对接模仿学习与强化学习训练管线。
2. **Sim2Real 闭环**：MuJoCo 全手模型包含真实 PIP–DIP 连杆闭环约束，配合直驱低阻抗执行器的可反驱特性，触觉仿真的接触保真度与真机一致性将持续改善，支撑"仿真训练 → 真机部署"的触觉策略迁移。
3. **数据采集生态**：团队计划推出适配的外骨骼式数据采集设备，收集更高质量多模态灵巧操作数据；摄像头遥操作（MediaPipe，零外设成本）+ 双模态（MANUS 手套）管线为大规模数据集提供低成本入口。
4. **本体演进方向**：触觉覆盖将从指尖向指腹与掌心延伸（支撑包络抓取与滑移识别），五指版本在规划中；电机动态特性标定、耐久性基准与装配文档持续完善。
5. **生态位**：以 ≈ $3K 的价位，DeepHand 有望像 LEAP Hand 一样成为机器人学习实验室的"默认末端"——已有 UCLA 多间实验室、UC Berkeley BAIR、NVIDIA GEAR Lab、京都工艺纤维大学等展开接入与合作。
6. **国产化替代路线**：执行器可探索国产一体化关节模组替换 XM335；触觉可对接帕西尼、他山科技、蓝点触控等国产三轴触觉方案；通信板 PCB 文件完全开放，可自主改板，进一步压低成本。

---

## 致谢与许可

- 原型项目：**MIDAS Hand** — UCLA RoMeLa（Dennis Hong 教授团队），作者：Alvin Zhu*、Mingzhu Zhu*、Beom Jun Kim*、Quanyou Wang*、Jose Victor S. H. Ramos*、Dennis Hong（*同等贡献）
- 原型论文：[arXiv:2607.14487](https://arxiv.org/abs/2607.14487) · 原型官网：[midas-hand.com](https://midas-hand.com) · 原型 GitHub：[midas-hand-org](https://github.com/midas-hand-org)
- 本仓库为其一比一复刻中文社区版（项目更名 DeepHand），代码与硬件设计逻辑与上游一致；遵循上游 **MIT License**，各子目录 LICENSE 已保留并注明原始出处。
- 引用请优先引用上游 MIDAS Hand 论文与仓库。
