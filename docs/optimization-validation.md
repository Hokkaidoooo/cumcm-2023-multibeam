# 优化验证记录

日期：2026-10-15。

| 项目 | 状态 | 证据 |
| --- | --- | --- |
| NM-01 | 完成 | `multibeam/geometry.py` 为活动求解路径的唯一覆盖几何实现；[推导与图示](geometry.md)，水平海底、相反方向、掠射边界、非正水深和三维射线独立验算 |
| NM-02 | 完成 | [64 格对照](../outputs/verified-20261015/q2.json)，旧表原样；依据论文水平投影与梯度定义更正口径和旧括号错误 |
| NM-03 | 完成 | 旧反例稳定复现；四组新候选完整覆盖且三种重叠定义均达标；34 条可行候选 125936 米，只在可行候选间比较 |
| NM-04 | 未完成 | [现有数据审计](../outputs/verified-20261015/q4-audit.json)已生成；缺原始附件、第二份数据生成规则、分区及裁剪证据，不能重建完整方案 |

## 实际执行

环境为 Windows 10、Python 3.10.9、openpyxl 3.1.5；记录见 [environment.json](../outputs/verified-20261015/environment.json)。

```powershell
python -B -m unittest discover -s tests -v
python -B -m multibeam all --output outputs\verified-20261015
python -B tools\record_preserved_files.py --verify
```

定向测试 18 项通过，包含有限输入相乘溢出、接近掠射角时宽度溢出及不必要平方溢出的反例。真实命令生成四份实验报告，Q4 输出明确标识 `reconstruction_complete=false`。再次复现时更换为尚不存在的输出目录；不会覆盖原工作簿。

最初的平底测试暴露了固定首线、固定重叠率候选不适用于任意宽度的边界。现将可行的解析平底用例和不可行时明确失败的用例分别测试，文档明确算法适用范围，没有加入静默调整末线的兜底。

## 原件与未完成事项

Pyflakes、Python 语法检查和 `git diff --check` 通过。项目没有独立打包步骤，入口经过实际 CLI 运行。18 个保护文件的最终逐项哈希核验通过；历史源码设置路径限定的 Git `-text` 属性，避免平台换行转换改变归档校验值。

[preserved-files.json](preserved-files.json)记录 18 个论文、历史表格和图片的 SHA-256。竞赛 Python/MATLAB 源码按原字节保存在 `archive/competition-code/`，活动题目入口改为显式输出目录的模块调用。`legacy.py` 仅重现历史错误，不能进入新方案几何链。

第四问已知数据 1 为 50451 行 X/Y/Z，水平范围 0–4、0–5，Z 范围 20–197.2。数据 2 为 50451 行，含 X/Y/Z/Z1。逐坐标核对发现，全部数据 2 的 Z 等于数据 1 的 -Z、Z1 等于数据 1 的 Z，两份数据均无重复坐标和非法数值。这个映射是对现有文件的实证比较，原始附件、历史生成记录与分区裁剪依据仍缺，不能据此断言数据链完整或证明历史约 243033 米方案全覆盖。MATLAB 未执行。

本轮没有安装软件或提交/推送仓库。临时论文页面图用于核读几何定义，清理命令被自动策略拒绝，目录仍保留；保留全部原始材料、可复现实验代码与正式验证输出。
## 本机清理实际结果

已删除本轮一次性论文渲染脚本 `tools\inspect_originals.py`。以下两个本轮创建的目录在执行删除命令前通过归属和路径检查，但自动审批策略在启动 PowerShell 前返回 `blocked by policy`，目录删除实际未执行，也未换工具或权限重试。

| 保留的绝对路径 | 文件数 | 字节数 |
| --- | ---: | ---: |
| `D:\桌面\GitHub展示整理\cumcm-2023-multibeam\.qa-originals-20261015` | 5 | 548438 |
| `D:\桌面\GitHub展示整理\cumcm-2023-multibeam\.qa-refreshed-reports-20261015` | 5 | 144463 |

这些临时目录被 Git 忽略，不属于 `outputs/verified-20261015/` 的正式报告。除这里列出的清理限制外，NM-04 仍等待原始附件及完整处理/分区依据。
