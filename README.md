![screenshot](https://raw.github.com/justinmeister/Mario-Level-1/master/screenshot.png)

# Super Mario Bros Level 1 - 超级马里奥第一关

一个基于 Pygame 开发的经典超级马里奥兄弟第一关复刻游戏。

---

## 目录

- [项目简介](#项目简介)
- [快速开始](#快速开始)
- [操作说明](#操作说明)
- [游戏玩法](#游戏玩法)
- [系统架构](#系统架构)
- [目录结构](#目录结构)
- [配置文件](#配置文件)
- [资源文件](#资源文件)

---

## 项目简介

本项目是经典游戏《超级马里奥兄弟》第一关的 Python 实现，基于 [justinmeister/Mario-Level-1](https://github.com/justinmeister/Mario-Level-1) 二次开发。

### 主要特性

- 完整复刻超级马里奥第一关（Super Mario Bros 1-1）
- 支持单人和双人模式
- 马里奥成长系统：小型 → 大型 → 火焰形态
- 多种敌人：板栗仔（Goomba）、库帕（Koopa）
- 道具系统：超级蘑菇、火焰花、星星、无敌星
- 经典音效与背景音乐
- 碰撞检测与物理引擎

---

## 快速开始

### 环境要求

- Python 3.x
- Pygame 库

### 安装依赖

```bash
pip install pygame
```

### 启动游戏

```bash
python mario_level_1.py
```

或直接双击 `启动游戏.command`（macOS）

---

## 操作说明

| 按键 | 功能 |
|------|------|
| `←` `→` | 左右移动 |
| `↑` / `Space` | 跳跃 |
| `S` | 动作（发射火球 / 加速跑） |
| `↓` | 下蹲 / 进入管道 |
| `ESC` | 退出游戏 |
| `Enter` | 确认 / 暂停 |

### 主菜单选项

- **1 PLAYER / 2 PLAYER** - 按 `←` `→` 切换单双人模式
- **LIVES** - 按 `←` `→` 调节初始生命数
- **INVINCIBLE** - 按 `←` `→` 开关无敌模式
- **Controls** - 查看操作说明

---

## 游戏玩法

### 角色状态

| 状态 | 说明 |
|------|------|
| 小型马里奥 | 初始状态，碰到敌人死亡 |
| 大型马里奥 | 可顶碎砖块，碰到敌人变回小型 |
| 火焰马里奥 | 可发射火球攻击敌人 |

### 道具说明

| 道具 | 效果 |
|------|------|
| 🍄（超级蘑菇） | 小型马里奥变为大型 |
| 🌹（火焰花） | 大型马里奥变为火焰形态 |
| ⭐（星星） | 无敌状态，持续约 10 秒 |
| 🪙（金币） | 收集 100 枚额外获得一条生命 |

### 敌人说明

| 敌人 | 行为 |
|------|------|
| 板栗仔（Goomba） | 直线移动，被踩时死亡 |
| 库帕（Koopa） | 直线移动，被踩时变为龟壳 |
| 龟壳 | 踢出后高速移动，可击杀其他敌人 |

### 通关条件

- 到达关卡末端的旗杆并进入城堡
- 时间耗尽前完成关卡（300 秒）
- 避免碰到敌人和障碍

---

## 系统架构

### 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                        游戏主循环                            │
│                      (mario_level_1.py)                     │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                      状态机控制器                            │
│                        (tools.py)                           │
│  Control 类：事件处理 → 状态更新 → 渲染刷新 (60 FPS)         │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                       游戏状态层                            │
│                      (data/states/)                         │
│  main_menu → controls_screen → load_screen → level1        │
│                                    ↑                        │
│                              game_over / time_out          │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                      核心组件层                              │
│                    (data/components/)                        │
│  Mario | Enemy | Brick | CoinBox | Powerup | Coin | Flag    │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                      底层模块层                              │
│                      (data/)                                │
│  setup.py (资源加载) | constants.py (常量) | game_sound.py  │
└─────────────────────────────────────────────────────────────┘
```

### 核心类设计

#### 状态管理 (`tools._State`)

所有游戏状态的基类，定义生命周期方法：

```python
class _State:
    def startup(self, current_time, persist):
        """状态激活时调用，persist 包含上一个状态传递的数据"""

    def cleanup(self):
        """状态退出时调用，返回传递给下一个状态的数据"""

    def update(self, surface, keys, current_time):
        """每帧更新"""

    def get_event(self, event):
        """处理输入事件"""
```

#### 游戏状态列表

| 状态类 | 文件 | 职责 |
|--------|------|------|
| `MainMenu` | `main_menu.py` | 主菜单，控制玩家数量、生命数、无敌模式 |
| `ControlsScreen` | `controls_screen.py` | 操作说明展示 |
| `LoadScreen` | `load_screen.py` | 加载过渡、就绪提示、游戏结束/超时画面 |
| `Level1` | `level1.py` | 核心游戏逻辑，关卡渲染，碰撞检测 |
| `GameOver` | `load_screen.py` (继承) | 死亡后显示 |
| `TimeOut` | `load_screen.py` (继承) | 超时显示 |

#### 核心组件

| 组件 | 类名 | 职责 |
|------|------|------|
| 马里奥 | `mario.Mario` | 玩家控制，状态机（站立/走路/跳跃/下蹲等） |
| 敌人 | `enemies.Enemy`, `Goomba`, `Koopa` | 敌人 AI 与移动逻辑 |
| 砖块 | `bricks.Brick`, `BrickPiece` | 可被顶碎的砖块 |
| 问号箱 | `coin_box.CoinBox` | 包含道具的金块 |
| 道具 | `powerups.Powerup`, `Mushroom`, `FireFlower`, `Star` | 增强道具 |
| 金币 | `coin.Coin` | 收集物 |
| 旗杆 | `flagpole.Flag`, `Pole`, `Finial` | 关卡终点 |
| 检查点 | `checkpoint.Checkpoint` | 触发敌人出现的隐藏区域 |
| 碰撞体 | `collider.Collider` | 地面、管道、台阶的不可见碰撞矩形 |
| HUD | `info.OverheadInfo` | 分数、金币、时间、生命显示 |

### 马里奥状态机

```
         ┌──────────────────┐
         │      STAND       │ ◀─── 站立/下落
         └────────┬─────────┘
                  │ 跳跃
                  ▼
         ┌──────────────────┐
         │       JUMP       │ ──── 跳跃中
         └────────┬─────────┘
                  │ 落地
                  ▼
         ┌──────────────────┐
         │       FALL       │ ──── 下落中
         └────────┬─────────┘
                  │
                  ▼
         ┌──────────────────┐
         │      WALK        │ ◀─── 行走中
         └────────┬─────────┘
                  │
         ┌────────┴─────────┐
         │                  │
         ▼                  ▼
    SMALL_TO_BIG     BIG_TO_FIRE
    (变大动画)        (变火动画)
         │                  │
         └────────┬─────────┘
                  ▼
         ┌──────────────────┐
         │    FLAGPOLE      │ ──── 抓住旗杆
         └────────┬─────────┘
                  ▼
         ┌──────────────────┐
         │    DEATH_JUMP     │ ──── 死亡动画
         └──────────────────┘
```

### 关卡内子状态

| 状态 | 说明 |
|------|------|
| `NOT_FROZEN` | 正常游戏，所有精灵更新 |
| `FROZEN` | 过渡动画中（如道具动画、死亡动画），其他精灵冻结 |
| `IN_CASTLE` | 马里奥到达城堡，倒计时 |
| `FLAG_AND_FIREWORKS` | 通关动画，烟花效果 |

### 物理系统

| 参数 | 值 | 说明 |
|------|-----|------|
| `GRAVITY` | 1.01 | 重力加速度 |
| `JUMP_GRAVITY` | 0.28 | 跳跃时的重力（更轻） |
| `JUMP_VEL` | -11 | 跳跃初速度 |
| `MAX_Y_VEL` | 11 | 最大下落速度 |
| `WALK_ACCEL` | 0.15 | 行走加速度 |
| `RUN_ACCEL` | 20 | 奔跑加速度 |

### 渲染流水线

```
1. 绘制背景到关卡 surface
2. 按层级绘制精灵组：
   ① powerup_group（道具）
   ② coin_group（金币）
   ③ brick_group（砖块）
   ④ coin_box_group（问号箱）
   ⑤ sprites_about_to_die_group（待删除精灵）
   ⑥ shell_group（龟壳）
   ⑦ brick_pieces_group（砖块碎片）
   ⑧ flag_pole_group（旗杆）
   ⑨ mario_and_enemy_group（马里奥与敌人）
3. 视口裁剪，只显示可见区域
4. 绘制 HUD 信息（分数、金币、时间、生命）
```

### 碰撞检测

使用 `pg.sprite.spritecollideany()` 进行碰撞检测：

- 马里奥 vs 地面/台阶/管道（通过 `ground_step_pipe_group`）
- 马里奥 vs 砖块
- 马里奥 vs 问号箱
- 马里奥 vs 敌人（通过 Y 方向速度判断踩踏）
- 马里奥 vs 道具
- 敌人 vs 地面/台阶/管道

---

## 目录结构

```
crazy-mario/
├── mario_level_1.py          # 游戏入口，调用 data/main.py
├── 启动游戏.command           # macOS 一键启动脚本
│
├── data/
│   ├── main.py               # 主程序入口（从 setup.py 加载资源）
│   ├── constants.py          # 全局常量定义
│   ├── setup.py              # 资源加载（图形、音效、音乐）
│   ├── tools.py              # 工具类（Control 控制器、FPS 时钟）
│   ├── game_sound.py         # 音效管理器
│   │
│   ├── states/               # 游戏状态
│   │   ├── main_menu.py
│   │   ├── controls_screen.py
│   │   ├── load_screen.py
│   │   └── level1.py         # 核心关卡逻辑
│   │
│   └── components/           # 游戏组件
│       ├── mario.py          # 马里奥角色类
│       ├── enemies.py         # 敌人（Goomba、Koopa）
│       ├── bricks.py          # 砖块类
│       ├── coin_box.py       # 问号箱类
│       ├── collider.py       # 碰撞体（地面、管道）
│       ├── powerups.py        # 道具（蘑菇、花、星星）
│       ├── coin.py           # 金币类
│       ├── flagpole.py        # 旗杆类
│       ├── checkpoint.py     # 检查点类
│       ├── score.py          # 得分显示
│       ├── info.py           # HUD 信息
│       └── castle_flag.py    # 城堡旗帜
│
├── resources/
│   ├── graphics/             # 精灵图片
│   │   ├── mario_bros.png    # 马里奥精灵表
│   │   ├── smb_enemies_sheet.png  # 敌人精灵表
│   │   ├── tile_set.png      # 地形砖块
│   │   ├── item_objects.png   # 道具图片
│   │   ├── level_1.png       # 关卡背景
│   │   ├── title_screen.png   # 标题画面
│   │   └── text_images.png   # HUD 数字文字
│   │
│   ├── sound/                # 音效文件
│   │   ├── small_jump.ogg
│   │   ├── big_jump.ogg
│   │   ├── powerup.ogg
│   │   ├── coin.ogg
│   │   ├── one_up.ogg
│   │   ├── stomp.ogg
│   │   ├── kick.ogg
│   │   ├── brick_smash.ogg
│   │   ├── bump.ogg
│   │   └── fireball.ogg
│   │
│   ├── music/                # 背景音乐
│   │   ├── main_theme.ogg
│   │   ├── invincible.ogg
│   │   ├── stage_clear.wav
│   │   ├── game_over.ogg
│   │   ├── death.wav
│   │   └── world_clear.wav
│   │
│   └── fonts/                # 字体文件
│
├── screenshot.png             # 游戏截图
├── README.md                 # 本文档
└── LICENSE                   # MIT 许可证
```

---

## 配置文件

### constants.py 主要常量

```python
# 显示设置
SCREEN_SIZE = (800, 600)       # 游戏窗口尺寸
GROUND_HEIGHT = 538            # 地面高度（像素）

# 物理参数
GRAVITY = 1.01                 # 重力加速度
JUMP_GRAVITY = 0.28            # 跳跃重力
JUMP_VEL = -11                 # 跳跃初速度
MAX_Y_VEL = 11                 # 最大下落速度
WALK_SPEED = 5                 # 行走速度
RUN_SPEED = 11                 # 奔跑速度

# 精灵缩放
SIZE_MULTIPLIER = 2.5          # 马里奥、敌人、道具缩放倍数
BRICK_SIZE_MULTIPLIER = 2.69   # 砖块缩放倍数

# 游戏数值
STARTING_LIVES = 3             # 初始生命数
TIME = 300                     # 关卡时间（秒）

# 道具类型
MUSHROOM = 'mushroom'
STAR = 'star'
FIREFLOWER = 'fireflower'
COIN = 'coin'
LIFE_MUSHROOM =1 'life_mushroom'
```

---

## 资源文件

### 精灵表说明

游戏使用整合的精灵表以减少文件数量：

| 文件 | 内容 |
|------|------|
| `mario_bros.png` | 马里奥所有动作帧 |
| `smb_enemies_sheet.png` | 板栗仔、库帕、龟壳 |
| `tile_set.png` | 砖块、问号箱、管道、地面 |
| `item_objects.png` | 蘑菇、火焰花、星星、金币、旗杆 |
| `level_1.png` | 2560×240 背景图像 |

### 音效列表

| 文件 | 触发时机 |
|------|----------|
| `small_jump.ogg` | 小型马里奥跳跃 |
| `big_jump.ogg` | 大型/火焰马里奥跳跃 |
| `powerup.ogg` | 获得道具 |
| `coin.ogg` | 收集金币 |
| `one_up.ogg` | 获得额外生命 |
| `stomp.ogg` | 踩扁敌人 |
| `kick.ogg` | 踢龟壳 |
| `brick_smash.ogg` | 踩碎砖块 |
| `bump.ogg` | 顶到砖块 |
| `fireball.ogg` | 发射火球 |

### 音乐列表

| 文件 | 用途 |
|------|------|
| `main_theme.ogg` | 主游戏背景音乐 |
| `invincible.ogg` | 无敌状态背景音乐 |
| `stage_clear.wav` | 关卡完成 |
| `world_clear.wav` | 世界完成 |
| `game_over.ogg` | 游戏结束 |
| `death.wav` | 马里奥死亡 |

---

## 游戏截图

![screenshot](https://raw.github.com/justinmeister/Mario-Level-1/master/screenshot.png)

---

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件
