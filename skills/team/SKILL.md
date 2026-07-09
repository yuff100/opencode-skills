---
name: team
description: >-
  /team [N] —— 创建多Agent协作团队。当用户要求并行开发、多人协作、或任务需要拆分为多个独立子任务时使用。
  N为teammate数量（1-10，默认5），你自己作为lead不计入。
version: 1.0.0
metadata:
  author: Fisher Yu
---

# /team [N]

参数: $ARGUMENTS
- 第一个数字: teammate数量（1-10，默认5）
- 其余文字: 任务描述（未提供则从对话上下文推断）

用TeamCreate创建团队，用TaskCreate分配任务，团队有哪些角色、每个角色数量、协作模式需要你自己探索。注意，总角色数量不要超过N位。
