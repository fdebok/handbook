# FDEBOK — Forward Deployed Engineer Body of Knowledge

## 前线部署工程师知识体系手册

> 把 AI 能力转化为可衡量业务成果的实践框架。

随着模型能力不断提升，企业 AI 落地的关键挑战，正从“模型能做什么”转向“如何在真实业务约束下交付、运行并持续创造价值”。FDEBOK 将前线部署工程师（Forward Deployed Engineer，FDE）的工作整理为一套可学习、可实践、可复用的知识体系。

FDE 不是前端工程师（FE）。FDE 深入客户现场，端到端承担问题理解、方案构建、生产交付和经验沉淀，以真实业务结果检验交付成效。

[阅读手册源码](https://github.com/fdebok/handbook/blob/main/index.html) · [项目仓库](https://github.com/fdebok/handbook)

## 手册一览

| 内容 | 覆盖范围 |
| --- | --- |
| 知识体系 | 22 章，涵盖角色认知、能力模型、组织与商业模式、工程实践及成长评估 |
| 十大知识域 | 从场景识别、现场诊断、数据治理，到评测、上线运维与产品反哺 |
| 交付生命周期 | 6 个阶段、4 道门径：勘察、定标、建造、验证、运行、复制 |
| 能力框架 | 4 项能力基座、2 项贯穿约束，以及 L1–L5 五级能力标尺 |
| 痛点与风险 | 20 类高频企业痛点的症状、根因与处方，以及风险登记和止损判据 |
| 一线工具 | 9 份现场模板，覆盖场景价值、环境体检、评测、交付、运行和交接 |

## 内容结构

1. **认知基础**：FDE 的定义、角色边界、价值模型与组织归属。
2. **能力模型**：能力基座、职级标尺和技术／非技术技能矩阵。
3. **十大知识域**：
   - 场景识别与价值定义
   - 现场诊断与环境勘察
   - 数据接入与知识治理
   - 权限、安全与合规
   - 方案设计与快速验证
   - 智能体与模型工程实现
   - 评测与质量保障
   - 上线、验收与交接
   - 运行期运维与持续迭代
   - 沉淀与产品反哺
4. **交付生命周期**：六阶段交付流程、阶段交付物、责任矩阵与工期模型。
5. **组织与商业模式**：团队编制、协作机制、计价方式与规模化路径。
6. **企业痛点诊断**：二十类高频问题及风险止损方法。
7. **前沿专题**：智能体工程化、上下文与检索、私有化与离线交付、组织治理、成本与性能工程。
8. **工具箱与成长评估**：九份可直接使用的模板、学习地图、招聘考察与个人自查。
9. **附录**：术语速查、全域检查项、三种阅读路径，以及组织级落地清单。

## 适合谁

- **FDE 与 AI 工程师**：建立从需求澄清到生产运行的完整交付方法。
- **技术负责人和交付团队**：设计团队能力、交付流程、质量门禁与复用机制。
- **产品、解决方案与咨询团队**：厘清协作边界，让现场洞察有效回流到产品和组织能力。
- **正在推进企业 AI 的组织**：系统识别落地约束、验证业务价值并管理交付风险。

## 推荐阅读路径

- **项目遇到阻塞**：从相关知识域和检查项入手，结合痛点诊断与现场模板定位问题。
- **搭建交付团队**：阅读能力模型、生命周期、团队编制、商业模式与规模化章节。
- **个人能力成长**：从 L1–L5 能力标尺和技能矩阵开始，结合学习地图与自查题制定计划。

## English

FDEBOK is a practical body of knowledge for **Forward Deployed Engineers (FDEs)**—engineers who work close to customers, own problems end to end, and turn AI capabilities into production systems with measurable business outcomes.

The handbook brings together 22 chapters, ten knowledge domains, a six-stage delivery lifecycle with four decision gates, an L1–L5 competency framework, diagnoses and remedies for 20 common challenges, and nine ready-to-use field templates.

It covers the full path from discovering valuable use cases and assessing real-world constraints to engineering, evaluation, launch, operations, and reusable product capabilities.

[Read the handbook source](https://github.com/fdebok/handbook/blob/main/index.html) · [Repository](https://github.com/fdebok/handbook)

## Website build and language routes / 网站构建与语言路由

The Chinese source page is `/`; the English edition is published as a separate, pre-rendered page at `/en/`. Platform-specific static introductions are generated at `/share/zh/wechat/`, `/share/zh/douyin/`, `/share/en/facebook/`, `/share/en/linkedin/`, and `/share/en/x/`. These share pages provide platform-specific Open Graph/Twitter preview copy and a clear route to the full handbook; they are marked `noindex` and canonicalize to the relevant language edition to avoid thin duplicate search results. Share pages contain no JavaScript and use a restrictive content-security policy that disallows scripts and embedded objects. The Pages workflow builds `dist/` with `python3 scripts/build_site.py --output-dir dist`, then deploys that directory. The generated pages should not be edited directly: update the translation map and `share-content-data` JSON in `index.html`. A local build requires Python 3 and Node.js. Run the focused tests with `node tests/test_share_ui.js`, `node tests/test_color_theme.js`, and `python3 -m unittest discover -s tests -p 'test_*.py'`.

中文源页面位于 `/`，英文版在发布时预渲染为独立静态页面 `/en/`。另生成微信、抖音、Facebook、LinkedIn、X 五个静态分享介绍页，分别位于 `/share/zh/wechat/`、`/share/zh/douyin/`、`/share/en/facebook/`、`/share/en/linkedin/`、`/share/en/x/`。每页提供平台适配的 Open Graph/Twitter 展示文案及通往完整手册的入口；微型页设置 `noindex` 并 canonical 回对应语言的完整手册，避免薄内容重复收录。微型页不含 JavaScript，并配置限制脚本、嵌入对象等来源的内容安全策略。Pages 工作流运行 `python3 scripts/build_site.py --output-dir dist` 生成并部署。不要直接编辑生成页；如需修订英译或分享文案，请更新 `index.html` 中的 `ENG` 英译表或 `share-content-data` JSON。本地构建需要 Python 3 和 Node.js。可运行 `node tests/test_share_ui.js`、`node tests/test_color_theme.js` 与 `python3 -m unittest discover -s tests -p 'test_*.py'` 执行对应测试。

On mobile, one tap on Share opens the device's native share sheet when Web Share is supported. If sharing is unavailable or the browser is an embedded app webview, a compact fallback lets readers copy the suggested text and canonical handbook URL together. Desktop keeps the platform-specific preview, separate copy actions, QR codes, and public share composers for Facebook, LinkedIn, and X. WeChat and Douyin do not expose a universal web API for invoking their in-app forwarding menus, so the site does not promise a fake deep link. No platform SDK or share-specific tracking is added. The existing aggregate site-visit counter remains unchanged.

Readers can switch among the original Classic Blue & Gold palette, Pine & Copper, and Graphite & Silver from the reading/bookmark panel. The selection is stored in this browser's local storage only; it is not uploaded or synchronized.

手机端点击“分享”一次即可调起浏览器/系统原生分享面板（设备支持 Web Share 时）；若浏览器不支持或处于 App 内嵌网页，则显示精简兜底面板，可一键复制推荐配文与手册正式链接。电脑端保留平台专属预览、配文/链接分别复制、二维码，以及 Facebook、LinkedIn 和 X 的公开分享入口。微信、抖音未提供通用网页接口来直接调用其 App 内转发菜单，因此不伪造“直达分享”。不接入平台 SDK、不新增分享追踪，现有全站累计访问统计保持不变。

读者可在阅读/书签面板中选择原有“典雅蓝金”、新增“松柏铜金”或“墨石紫银”配色。选择仅保存在当前浏览器本地，不会上传或跨设备同步。

---

FDEBOK：让一线交付经验成为可复用的工程能力。

## 许可 / License

本仓库及手册原创内容按 MIT License 许可，详见 [LICENSE](./LICENSE)。允许商业使用、修改、分发及销售；分发副本或实质部分时，须附带版权声明和许可声明。第三方内容仍适用其各自许可；MIT 不授予 FDEBOK 名称、标志或商标权。

This repository and the handbook's original content are licensed under the MIT License; see [LICENSE](./LICENSE). Commercial use, modification, redistribution, and sale are permitted. Copies or substantial portions must include the copyright and permission notice. Third-party material remains subject to its own license; the MIT License does not grant rights to the FDEBOK name, logo, or trademarks.
