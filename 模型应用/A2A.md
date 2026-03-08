#### A2A

* **智能体的爆发与“碎片化”困境**：随着大语言模型的发展，各种AI代理（Agent）层出不穷。但它们大多由不同厂商、基于不同框架开发，彼此之间无法通信和协作，形成了“代理孤岛”。要完成一个复杂的任务（比如跨国差旅预订），需要协调多个应用，但当前的技术现状却很难实现这一点。

  * 假设一位新员工Alice入职一家跨国公司，需要在入职第一天就完成以下事项：

    1. **HR智能体**：录入员工信息，确定入职日期、部门、职级。
    2. **IT智能体**：根据职级分配电脑、创建企业邮箱和系统权限。
    3. **财务智能体**：根据入职日期设置工资单、报销权限。
    4. **行政智能体**：安排工位、预订入职培训会议室。
    5. **差旅智能体**：如果员工需要当天出差（例如去分公司参加培训），还需预订机票和酒店，且必须符合公司差旅政策。

    这些智能体可能来自不同部门甚至不同供应商（如HR系统来自Workday，IT系统来自ServiceNow，财务系统来自SAP，差旅系统来自Concur）。它们各自拥有独立的数据库、业务规则和状态机。

  * 为什么MCP无法单独完成？

    - **MCP的角色**：MCP可以让一个“总控智能体”调用各个系统的工具。比如，总控智能体通过MCP调用HR系统的API获取信息，再调用IT系统的API创建账号。这确实能实现部分自动化。
    - **MCP的局限**：
      - **缺乏自主协商能力**：当IT智能体发现需要更高权限审批（例如Alice需要特殊软件，但IT政策要求经理审批），IT智能体无法主动与HR智能体或经理的智能体进行多轮协商，只能被动等待总控智能体处理。总控智能体必须硬编码所有异常情况，变得臃肿且难以维护。
      - **无法保护内部逻辑**：每个部门的智能体都有自己复杂的业务规则（例如：财务智能体的报销规则、差旅智能体的政策合规判断）。MCP要求总控智能体直接调用它们的API，这意味着各部门必须暴露内部API的细节，可能泄露商业逻辑。
      - **状态同步困难**：任务可能耗时数小时（例如等待经理审批）。MCP的简单请求-响应模式难以跟踪长时间运行的任务状态，而每个智能体内部的状态变化需要跨系统同步。

* **从单打独斗到团队协作的需求**：与其试图创造一个全能的“超级代理”，不如让一群**专业化的“专科代理”** 相互协作，共同完成复杂任务。这就像一个公司需要不同部门（销售、财务、法务）协同工作一样，智能体也需要一套通用的协作语言，A2A正是为此而生。



* 有了A2A协议，各部门的智能体可以独立存在，并通过标准化的报文相互通信：

  1. **任务发起**：HR智能体创建一个“入职任务”（Task），并通过A2A向其他智能体广播或定向发送子任务。
  2. **并行处理**：
     - IT智能体收到任务后，根据职级分配权限，并返回`working`状态。
     - 财务智能体同时处理工资单设置，返回`completed`。
     - 行政智能体安排工位，但发现会议室冲突，返回`input-required`，询问HR是否可以调整时间。
  3. **协商解决**：HR智能体收到`input-required`后，可以回复新的时间，行政智能体重新安排。
  4. **跨智能体触发**：当所有基础任务完成后，差旅智能体自动被触发。它根据Alice的入职时间和出差需求，调用外部机票API查询，但发现预算超标。差旅智能体主动向财务智能体发送请求，询问是否可临时提高预算（通过A2A报文传递“预算例外请求”）。财务智能体根据政策自动审批或转给人工。
  5. **结果聚合**：所有智能体完成任务后，最终将结果（工位号、电脑型号、机票信息等）汇总给HR智能体，生成一份完整的入职报告。

  在这个过程中，每个智能体都是自主的，它们通过A2A交换标准化的任务和状态信息，但**无需暴露各自的内部API细节**。财务智能体无需知道IT智能体如何分配电脑，只需知道最终结果；IT智能体的审批流程完全由其内部管理，其他智能体只需知道任务状态是“等待审批”即可。

  

* 总结

  * MCP适合**“一个智能体调用多种工具”**的场景，而A2A适合**“多个智能体像团队一样协作”**的场景。
  * 当任务需要跨部门、跨系统，且涉及自主协商、长期状态跟踪、保护内部逻辑时，多智能体协作（A2A）就是必需的。
  * 没有A2A，你就只能写一个极其复杂的“万能总控”，而有了A2A，专业智能体各司其职，整个系统变得灵活、可扩展且易于维护。



* A2A协议的格式

  * 要了解A2A（Agent-to-Agent）协议的报文信息，最直接的方式是从它的**核心数据结构**和**通信流程**入手。A2A协议旨在让不同的AI代理能互相通信和协作，它定义了一套标准化的"报文"格式，你可以把它想象成代理之间交流的"通用语言"。

  * 官方git文档：https://github.com/a2aproject/A2A

  * 网站：https://a2a-protocol.org/latest/#get-started-with-a2a

  * A2A协议中最重要的报文结构：

    它是一个JSON格式的元数据文档，描述了代理的身份和能力。客户端通过获取Agent Card来发现代理并知道如何与它通信。

    * Agent Card通常托管在代理服务器的`/.well-known/agent.json`路径下。用于描述当前Agent的信息，一个典型的Agent Card包含以下信息：

    ```json
    {
      "name": "数据分析助手",
      "description": "专门用于数据分析和统计计算的智能体",
      "url": "http://localhost:8000", // 代理的服务端点
      "provider": {
        "organization": "某科技公司"
      },
      "version": "1.0.0",
      "protocolVersion": "0.3.0",
      "capabilities": {
        "streaming": false,      // 是否支持流式响应
        "pushNotifications": false
      },
      "skills": [                // 代理具备的具体技能
        {
          "name": "数据查询",
          "description": "根据自然语言查询数据",
          "inputModes": ["text/plain"],
          "outputModes": ["application/json"]
        }
      ]
    }
    ```

    * 根据 A2A 协议（版本 0.3.0）的常见规范，Agent Card 的完整字段及必选性如下表所示。其中，顶级字段用粗体表示，嵌套字段用缩进表示。

      | 字段                        | 类型    | 必选     | 说明                                      |
      | :-------------------------- | :------ | :------- | :---------------------------------------- |
      | **name**                    | string  | **是**   | 代理的名称                                |
      | **description**             | string  | **是**   | 代理的功能描述                            |
      | **url**                     | string  | **是**   | 代理服务的端点 URL                        |
      | **provider**                | object  | 否       | 提供方信息                                |
      | └─ organization             | string  | 否       | 组织名称                                  |
      | **version**                 | string  | **是**   | 代理的版本号                              |
      | **protocolVersion**         | string  | **是**   | 使用的 A2A 协议版本，如 "0.3.0"           |
      | **capabilities**            | object  | **是**   | 代理支持的能力                            |
      | └─ streaming                | boolean | 否       | 是否支持流式响应（默认 false）            |
      | └─ pushNotifications        | boolean | 否       | 是否支持推送通知（默认 false）            |
      | └─ requireAuth              | boolean | 否       | 是否需要认证（默认 false）                |
      | └─ supportsCancellation     | boolean | 否       | 是否支持取消任务（默认 false）            |
      | └─ supportsStatePersistence | boolean | 否       | 是否支持任务状态持久化（默认 false）      |
      | **skills**                  | array   | **是**   | 代理具备的技能列表，至少包含一项          |
      | └─ name                     | string  | **是**   | 技能名称                                  |
      | └─ description              | string  | **是**   | 技能描述                                  |
      | └─ inputModes               | array   | **是**   | 支持的输入格式，如 `["text/plain"]`       |
      | └─ outputModes              | array   | **是**   | 支持的输出格式，如 `["application/json"]` |
      | └─ parameters               | object  | 否       | 技能的参数定义（JSON Schema）             |
      | └─ examples                 | array   | 否       | 调用示例                                  |
      | **authentication**          | object  | 否       | 认证方式（如果代理需要认证）              |
      | └─ schemes                  | array   | 条件必选 | 认证方案列表，如 `["bearer"]`             |
      | └─ bearerFormat             | string  | 否       | Bearer 令牌的格式说明，如 "JWT"           |
      | **defaultInputModes**       | array   | 否       | 全局默认输入格式，技能可覆盖              |
      | **defaultOutputModes**      | array   | 否       | 全局默认输出格式，技能可覆盖              |
      | **metadata**                | object  | 否       | 自定义元数据，用于扩展                    |

      > **说明**：
      >
      > - `skills` 数组至少需要包含一个技能，每个技能必须提供 `name`、`description`、`inputModes`、`outputModes`。
      > - `capabilities` 中的子字段均为可选，但通常建议明确声明以避免歧义。
      > - 如果提供了 `authentication` 对象，则必须指定 `schemes`（如 `["bearer"]`）。
      
    * 基本通信接口，所有 JSON-RPC 请求**必须**遵循标准的 JSON-RPC 2.0 格式：

      ```json
      {
        "jsonrpc": "2.0",
        "id": "unique-request-id",
        "method": "category/action",
        "params": { /* method-specific parameters */ }
      }
      ```
    
      
    
    ### 💬 Message：通信的基本单元
    
    这是代理之间交流的"一句话"。一个`Message`对象代表一次对话的轮次，它必须包含`role`（角色）和`parts`（内容部分）。
    
    一个典型的用户消息报文如下：
    
    json
    
    ```
    {
      "role": "user",
      "parts": [
        {
          "type": "text",
          "text": "请分析一下上个月的销售数据"
        }
        // 还可以包含 FilePart, DataPart 等其他类型的内容
      ],
      "messageId": "msg-12345" // 可选的消息ID
    }
    ```
    
    
    
    *参考自搜索结果中的示例* 
    
    ### 📦 Task：代理的工作单元
    
    A2A协议是"异步优先"的，意味着一个请求可能会被作为一个任务（`Task`）来处理，特别是对于耗时较长的操作。`Task`对象包含了任务的整个生命周期状态。
    
    当你向一个代理发送消息时，它通常会返回一个Task对象，让你可以查询任务进度。一个任务的报文结构如下：
    
    json
    
    ```
    {
      "id": "task-001",               // 任务的唯一标识
      "status": {
        "state": "working"             // 状态可以是：submitted, working, input-required, completed, failed, canceled
      },
      "history": [                     // 此任务相关的历史消息
        {
          "role": "user",
          "parts": [{ "type": "text", "text": "分析数据" }]
        }
      ],
      "artifacts": [                   // 任务产出的最终成果
        {
          "name": "分析报告",
          "parts": [{ "type": "text", "text": "这里是分析结果..." }]
        }
      ]
    }
    ```
    
    
    
    *参考自搜索结果中的示例* 
    
    ### 🧩 Part：消息的组成部分
    
    这是构成`Message`或`Artifact`的最小单位，使得消息内容可以非常灵活。一个`Message`可以由多个不同类型的`Part`组成。
    
    常见的Part类型包括：
    
    - **`TextPart`**：纯文本内容。
    - **`FilePart`**：文件引用，可以包含文件的URL或MIME类型。
    - **`DataPart`**：结构化的数据，如JSON。
    
    ### 🚀 一个完整的通信报文示例
    
    下面是一个使用JSON-RPC 2.0协议发送消息的完整请求报文示例。这是A2A协议最常用的传输方式。
    
    **请求报文 (Client -> Server):**
    
    json
    
    ```
    {
      "jsonrpc": "2.0",
      "id": 1,
      "method": "message/send",          // A2A定义的方法名
      "params": {
        "message": {
          "role": "user",
          "parts": [
            {
              "type": "text",
              "text": "帮我预订一张明天去北京的火车票"
            }
          ]
        }
        // 可以包含其他参数，如 taskId 等
      }
    }
    ```
    
    
    
    *参考自搜索结果中的示例* 
    
    **响应报文 (Server -> Client):**
    
    json
    
    ```
    {
      "jsonrpc": "2.0",
      "id": 1,
      "result": {
        "id": "task-0829",                // 服务器创建了一个任务来跟踪这个请求
        "status": { "state": "working" },
        "artifacts": []                    // 任务进行中，暂无最终成果
      }
    }
    ```
    
    
    
    *参考自搜索结果中的示例* 
    
    了解这些基础报文结构后，如果你想进一步探索，可以关注以下几点：
    
    - **发现机制**：核心是获取并解析`Agent Card` 。
    - **交互模式**：除了简单的`message/send`，还有支持实时更新的`message/stream` 。
    - **任务管理**：可以通过`tasks/get`、`tasks/cancel`等方法来管理正在进行的任务 。