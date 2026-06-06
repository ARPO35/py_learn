# Python 学习 CLI

本上下文描述一个面向 Python 初学者的命令行学习工具。它围绕按章节组织的练习，让学习者在本地答题目录中完成、运行并提交答案。

## Language

**Exercise（练习）**:
学习者完成的一道最小学习单位，包含说明、答题入口、提示和测试要求。
_Avoid_: Question, Problem

**Exercise ID（练习编号）**:
用于唯一定位一个 **Exercise** 的章节内编号。
_Avoid_: 题号, Problem ID

**Chapter（章节）**:
按学习主题组织的一组 **Exercise**。
_Avoid_: Category, Module

**Workspace（答题目录）**:
学习者当前编写和运行某个 **Exercise** 答案的本地目录。
_Avoid_: Project directory, Working directory

**Exercise Source（原始练习）**:
不可被学习者答题进度覆盖的 **Exercise** 基准内容，以文件夹形式保存该练习的说明、答题入口和专有验证脚本。
_Avoid_: Template, Original problem

**Exercise Metadata（练习元数据）**:
由 **Exercise Source** 自身声明的标题、归属章节、顺序和验证入口等描述信息。
_Avoid_: External index, Registry row

**Inherited Exercise Metadata（继承练习元数据）**:
由上层文件夹声明、可被下层 **Exercise Source** 继承的章节相关元数据。
_Avoid_: Global index, Parent config

**Attempt Snapshot（答题进度快照）**:
学习者在某个 **Exercise** 上留下的可恢复答题状态。
_Avoid_: Backup, History

**Resume（恢复练习）**:
把某个 **Exercise** 的 **Attempt Snapshot** 恢复到 **Workspace**。
_Avoid_: Go, Load

**Save（保存进度）**:
用当前 **Workspace** 的答题内容覆盖对应 **Exercise** 的 **Attempt Snapshot**。
_Avoid_: Sync, Backup

**Switch（切换练习）**:
让 **Workspace** 承载另一个 **Exercise**。
_Avoid_: Navigate, Open

**Submit（提交验证）**:
使用独立于调试输入的验证输入评估当前 **Exercise** 答案。
_Avoid_: Commit, Git commit

**Validation Case（验证用例）**:
用于评估 `py_learn` 的输入、期望返回值或期望输出。
_Avoid_: Test script, Judge logic

**Learning Material（学习材料）**:
复制到 **Workspace** 供学习者阅读但默认不进入 **Attempt Snapshot** 的说明或素材文件。
_Avoid_: Answer file, Validation file

## Relationships

- 一个 **Chapter** 包含一个或多个 **Exercise**。
- 一个 **Exercise** 有且只有一个 **Exercise ID**。
- 一个 **Workspace** 同一时间承载零个或一个正在答题的 **Exercise**。
- 多个 **Workspace** 可以独立承载不同的 **Exercise**。
- 一个 **Exercise Source** 可以被复制到多个 **Workspace**。
- 一个 **Exercise Source** 自身声明对应的 **Exercise Metadata**。
- **Exercise Metadata** 由 **Exercise Source** 内的 `exercise.toml` 声明。
- 上层文件夹也可以通过 `exercise.toml` 声明 **Inherited Exercise Metadata**。
- `exercise.toml` 通过 `type = "exercise"` 或 `type = "chapter"` 区分 **Exercise Metadata** 与 **Inherited Exercise Metadata**。
- 下层 **Exercise Source** 会继承上层文件夹中的 **Inherited Exercise Metadata**。
- 继承 **Exercise Metadata** 只发生在扫描时的内存模型中，不会把上层元数据写入下层文件。
- 继承 **Exercise Metadata** 按字段合并；下层只覆盖自己声明的字段，未声明字段继续使用上层值。
- **Exercise Source** 自身声明的 **Exercise Metadata** 优先级高于继承而来的元数据。
- 一个 **Attempt Snapshot** 属于一个 **Exercise**，并可恢复到一个 **Workspace**。
- **Resume** 从 **Attempt Snapshot** 恢复内容到 **Workspace**。
- **Save** 用当前 **Workspace** 内容覆盖当前 **Exercise** 的 **Attempt Snapshot**。
- **Switch** 到另一个 **Exercise** 前会先 **Save** 当前 **Workspace**。
- 对当前 **Exercise** 执行 **Resume** 不会先 **Save** 当前 **Workspace**。
- 对当前 **Exercise** 执行 **new** 不会先 **Save** 当前 **Workspace**。
- **Submit** 不表示 Git 提交，也不表示上传到远程平台。
- **Submit** 通过验证后会自动 **Save** 当前 **Workspace**。
- **Exercise** 的答案入口统一为 `py_learn` 函数。
- **Exercise** 可以通过 `py_learn` 的返回值或执行期间的输出进行验证。
- **Exercise Source** 的专有验证文件负责声明 **Validation Case**，CLI 负责统一执行 `py_learn`、捕获输出、比较结果和展示报告。
- 同一个 **Exercise Source** 使用一个验证文件同时声明调试用和提交验证用 **Validation Case**。
- 验证文件保留在 **Exercise Source** 中，由 CLI 自动调用，不会复制到 **Workspace**。
- **Exercise Source** 可以包含随练习复制到 **Workspace** 的 **Learning Material**。
- **Learning Material** 默认不进入 **Attempt Snapshot**。
- `q.md` 是默认 **Learning Material**，默认不会被 **Save** 写入 **Attempt Snapshot**。
- 每个 **Exercise Source** 可以声明 `.plignore`，用于描述 **Save** 时不进入 **Attempt Snapshot** 的文件。
- `.plignore` 会被复制进 **Workspace** 的 `.pl` 状态目录，而不是复制到 **Workspace** 根目录。
- **Save** 使用黑名单模型：保存 **Workspace** 中除 `.plignore` 匹配项和内部状态目录外的答题内容。
- **Switch** 清理 **Workspace** 时只删除 `.pl` 状态中记录的 CLI 管理文件，不使用通配符清理，也不删除未被记录的用户文件。
- **Exercise Source** 默认可以使用扁平目录组织，也可以被放入更深层文件夹中，发现机制不应依赖固定目录深度。
- **Exercise Metadata** 可以完全自描述，也可以由上层文件夹的继承元数据补全章节相关信息。
- 从 **Exercise Source** 开始新的 **Exercise** 不会删除已有 **Attempt Snapshot**。
- **Workspace** 的未保存修改不会自动覆盖 **Attempt Snapshot**。

## Example dialogue

> **Dev:** “用户执行 `pl resume B1.2` 时，我们是在修改原始题目吗？”
> **Domain expert:** “不是。`B1.2` 定位到一个 **Exercise**，工具把这个 **Exercise** 的 **Attempt Snapshot** 恢复到 **Workspace**；如果要重新开始，则从 **Exercise Source** 复制。”

## Flagged ambiguities

- “题目”在用户界面中可以继续使用，但领域模型中统一称为 **Exercise（练习）**。
- “go”曾被用于表达切换并恢复进度，现统一称为 **Resume（恢复练习）**。
- “new”表示从 **Exercise Source** 开始，不删除已有 **Attempt Snapshot**。
- “new”在当前 **Exercise** 内表示放弃未保存修改并从 **Exercise Source** 重新开始；如需保留当前内容，用户应先执行 **Save**。
- “resume”在当前 **Exercise** 内表示放弃未保存修改并恢复上一次 **Attempt Snapshot**；跨 **Exercise** 时表示先保存当前进度再恢复目标进度。
- “commit”容易和 Git 提交混淆，提交验证统一称为 **Submit（提交验证）**，CLI 使用 `pl submit`。
