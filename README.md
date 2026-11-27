# FDEBOK — Forward Deployed Engineer Body of Knowledge

## 前线部署工程师知识体系指南

> 把 AI 能力转化为可衡量业务成果的实践框架。

随着模型能力不断提升，企业 AI 落地的关键挑战，正从“模型能做什么”转向“如何在真实业务约束下交付、运行并持续创造价值”。FDEBOK 将前线部署工程师（Forward Deployed Engineer，FDE）的工作整理为一套可学习、可实践、可复用的知识体系。

FDE 不是前端工程师（FE）。FDE 深入客户现场，端到端承担问题理解、方案构建、生产交付和经验沉淀，以真实业务结果检验交付成效。

本指南介绍 FDE 的岗位职责、能力要求与职业发展，并提供适用于企业 AI 项目的交付方法和现场工具。

[阅读指南源码](https://github.com/fdebok/handbook/blob/main/index.html) · [项目仓库](https://github.com/fdebok/handbook)

## 检索名称与相关说法

FDEBOK 的中文主名称是“前线部署工程师知识体系指南”，也可按常见检索习惯称为“前线部署工程师知识体系手册”“FDE 指南”或“FDE 手册”。相关检索问题包括：FDE 是什么、FDE 岗位职责与工作内容、FDE 能力模型与职业发展、如何成为 FDE，以及企业 AI 项目交付、落地、评测与运维。英文检索词包括 Forward Deployed Engineer guide/handbook、FDE learning path、enterprise AI delivery guide。英文名称为 Forward Deployed Engineer Body of Knowledge；Customer Engineer、Field Engineer 等是相关岗位，不应与 FDE 当作完全同义词。

## 指南一览

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

Use this handbook to understand FDE responsibilities, develop the skills the work requires, and apply a practical delivery approach to enterprise AI projects.

The handbook brings together 22 chapters, ten knowledge domains, a six-stage delivery lifecycle with four decision gates, an L1–L5 competency framework, diagnoses and remedies for 20 common challenges, and nine ready-to-use field templates.

It covers the full path from discovering valuable use cases and assessing real-world constraints to engineering, evaluation, launch, operations, and reusable product capabilities.

[Read the handbook source](https://github.com/fdebok/handbook/blob/main/index.html) · [Repository](https://github.com/fdebok/handbook)

## Website build and language routes / 网站构建与语言路由

The Chinese source page is `/`; the English edition is published as a separate, pre-rendered page at `/en/`. Platform-specific static introductions are generated at `/share/zh/wechat/`, `/share/zh/douyin/`, `/share/en/facebook/`, `/share/en/linkedin/`, and `/share/en/x/`. These share pages provide platform-specific Open Graph/Twitter preview copy and a clear route to the full handbook; they are marked `noindex` and canonicalize to the relevant language edition to avoid thin duplicate search results. Share pages contain no JavaScript and use a restrictive content-security policy that disallows scripts and embedded objects. The Pages workflow builds `dist/` with `python3 scripts/build_site.py --output-dir dist`, then deploys that directory. The generated pages should not be edited directly: update the translation map and `share-content-data` JSON in `index.html`. A local build requires Python 3 and Node.js. Run the focused tests with `node tests/test_share_ui.js`, `node tests/test_color_theme.js`, and `python3 -m unittest discover -s tests -p 'test_*.py'`.

中文源页面位于 `/`，英文版在发布时预渲染为独立静态页面 `/en/`。另生成微信、抖音、Facebook、LinkedIn、X 五个静态分享介绍页，分别位于 `/share/zh/wechat/`、`/share/zh/douyin/`、`/share/en/facebook/`、`/share/en/linkedin/`、`/share/en/x/`。每页提供平台适配的 Open Graph/Twitter 展示文案及通往完整指南的入口；微型页设置 `noindex` 并 canonical 回对应语言的完整指南，避免薄内容重复收录。微型页不含 JavaScript，并配置限制脚本、嵌入对象等来源的内容安全策略。Pages 工作流运行 `python3 scripts/build_site.py --output-dir dist` 生成并部署。不要直接编辑生成页；如需修订英译或分享文案，请更新 `index.html` 中的 `ENG` 英译表或 `share-content-data` JSON。本地构建需要 Python 3 和 Node.js。可运行 `node tests/test_share_ui.js`、`node tests/test_color_theme.js` 与 `python3 -m unittest discover -s tests -p 'test_*.py'` 执行对应测试。

After deployment, the Pages workflow submits the canonical Chinese and English URLs to [IndexNow](https://www.indexnow.org/documentation); this can accelerate discovery by participating search engines but does not guarantee indexing and does not replace webmaster-console submission. Site owners should verify the domain and submit `/sitemap.xml` in [Google Search Console](https://search.google.com/search-console/), [Bing Webmaster Tools](https://www.bing.com/webmasters/), and [Baidu Search Resource Platform](https://ziyuan.baidu.com/). The public IndexNow verification key is served from the site root.

每次部署后，Pages 工作流会通过 [IndexNow](https://www.indexnow.org/documentation) 提交中英文规范页；参与的搜索引擎可据此更快发现更新，但不保证收录，也不能替代站长平台提交。站点所有者应完成域名验证，并分别在 [Google Search Console](https://search.google.com/search-console/)、[Bing Webmaster Tools](https://www.bing.com/webmasters/) 与 [百度搜索资源平台](https://ziyuan.baidu.com/) 提交 `/sitemap.xml`。IndexNow 验证文件按协议公开放在站点根目录。

The FDEBOK identity pairs a bold, readable dotted FDE monogram with a subtle globe grid, a slim gold rim, and a white-and-mint surface from the site palette. The full FDEBOK wordmark remains explicit beside the monogram. The coordinated mark is used in the SVG favicon, Apple touch icon, homepage and share-page logos, and localized 1200×630 social preview cards. Versioned v6 asset URLs help browsers and social apps fetch the refreshed artwork. PNG assets are rendered from `scripts/render_brand_artwork.py` (requires system Cairo and Pango libraries); the A/P/M badge crops use the approved design reference in `assets/fdebok-badges-approved-v28-source.png`, which is not published to the site. The SVG files are the scalable logo masters.

FDEBOK's A/P/M badge program is for FDE practitioners and is reviewed by the FDEBOK volunteer team at no charge. A (Engineer) requires FDE practitioner status, a recommendation, and a theory assessment. P (Professional) requires the same conditions plus a practical project-delivery assessment and peer review. M (Master) requires the P-level conditions plus verifiable professional experience or project endorsement. Badge-status checks are handled manually by email at `x@fdebok.com`. These badges record learning and practice; they are not government qualifications or industry-wide certifications, and are separate from the handbook's L1–L5 self-assessment and any employer endorsement.

On mobile, one tap on Share opens the native share sheet with the language-specific guide URL and a non-tracking `share=brand-v6` cache-busting query; the page's canonical URL remains query-free. Recipient apps can then build a rich preview from the Open Graph title, description, and social card. The compact copy fallback remains visible behind the native sheet and can copy a suggested message plus link if needed. After returning, the page explains that only the destination app can confirm sending. WeChat, Douyin, and other apps may require another in-app choice (such as a recipient or feed) and a final confirmation; a web page cannot automate or observe those private app steps. Desktop keeps platform previews, separate copy actions, QR codes, and public share composers where available. No platform SDK or share-specific tracking is added; the aggregate site-visit counter is unchanged.

FDEBOK 品牌标识以高对比、易辨识的虚线节点构成 FDE 字母，背景采用低对比环球网格；纤细金色外缘、白色球面与薄荷绿网格沿用网站现有配色。图形标记旁保留完整的 FDEBOK 字标。标识统一应用于 SVG 网站图标、苹果主屏图标、首页与分享页，并更新中英文 1200×630 社交预览卡。品牌资源使用 v6 版本化 URL，帮助浏览器与社交 App 获取新图稿。可用 `python3 scripts/render_brand_artwork.py` 重绘 PNG（需系统安装 Cairo 与 Pango）；SVG 为可缩放标识源文件。

FDEBOK A/P/M 徽章面向 FDE 从业者，由 FDEBOK 志愿者团队免费审核发放。A（工程师级）须具备 FDE 从业者身份，并通过推荐和理论测评；P（专业级）还须通过项目交付实践考核与同行互评；M（大师级）须满足 P 级条件，并提供可核验的从业经验或项目背书。徽章状态通过 `x@fdebok.com` 邮件人工核验。徽章用于记录学习与实践成果，不属于政府职业资格或行业统一认证，也不代表雇主背书；A/P/M 与指南 L1–L5 自查体系相互独立。

手机端点击“分享”一次即调起系统原生分享面板（设备支持 Web Share 时），只传递语言对应的指南 URL，并附不参与统计的 `share=brand-v6` 参数，帮助社交 App 刷新缓存的分享卡；规范 canonical URL 不带该参数。微信等目标 App 根据 Open Graph 元数据生成卡片预览；精简复制面板留在网页下方，若系统分享不可用或未完成，可复制推荐配文与链接。返回网页后会明确提示：只有目标 App 能确认是否真正发送。微信、抖音等 App 可能还要求在其内部选择联系人/朋友圈并最终确认；网页无法自动代替或监测这些私有流程。电脑端保留平台预览、分别复制、二维码及可用的公开分享入口。不接入平台 SDK、不新增分享追踪，全站访问计数保持不变。

Readers can switch among the original Classic Blue & Gold, Pine & Copper, and Graphite & Silver themes from the reading/bookmark panel. The selection is stored in this browser's local storage only; it is not uploaded or synchronized.

---

FDEBOK：让一线交付经验成为可复用的工程能力。

## 许可 / License

本仓库及指南原创内容按 MIT License 许可，详见 [LICENSE](./LICENSE)。允许商业使用、修改、分发及销售；分发副本或实质部分时，须附带版权声明和许可声明。第三方内容仍适用其各自许可；MIT 不授予 FDEBOK 名称、标志或商标权。

This repository and the handbook's original content are licensed under the MIT License; see [LICENSE](./LICENSE). Commercial use, modification, redistribution, and sale are permitted. Copies or substantial portions must include the copyright and permission notice. Third-party material remains subject to its own license; the MIT License does not grant rights to the FDEBOK name, logo, or trademarks.
