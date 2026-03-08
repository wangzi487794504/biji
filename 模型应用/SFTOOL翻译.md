### SFTOOL翻译

* 测试案例

  ```sh
  postman request POST 'http://localhost/v1/workflows/run' \
    --header 'Authorization: Bearer app-IxMKcEFwRlHn4iMyvBaOf66M' \
    --header 'Content-Type: application/json' \
    --body '{
  
    "inputs": {
  
   "text": "{\"text\": \"In the tapestry of life, every small choice we make weaves a thread into the larger pattern of our destiny. The early bird catches the worm, but the second mouse gets the cheese — a whimsical reminder that timing and patience often matter more than mere speed. Life is not a race to the finish line, but a journey to be savored, with moments of joy and sorrow, triumph and defeat, all contributing to the richness of our experience. We chase dreams like fireflies in the night, fleeting yet precious, holding onto hope even when the path ahead is unclear. Kindness is a language the deaf can hear and the blind can see, a universal currency that transcends borders and differences. Every sunrise brings a new opportunity to start fresh, to learn from yesterday’s mistakes, and to embrace the beauty of the present moment. The world is full of wonders waiting to be discovered, from the quiet rustle of leaves in a forest to the roar of waves on a distant shore, from the laughter of a child to the wisdom of an elder. We are all travelers on this blue planet, bound by the shared experience of being human, and it is our responsibility to care for one another and for the world we call home. Perseverance is the key to unlocking doors that seem closed, for success is not given but earned through hard work and resilience. Even in the darkest of times, there is always a glimmer of light, a reason to keep going, a promise that better days are ahead. This long passage is crafted to exceed 256 characters, specifically to test the length limit configuration in Dify, ensuring that the input validation works as expected and returns a structured error message instead of processing the overly long text through the large language model, which would waste resources and fail to meet the design requirements.\", \"source_language\": \"Englisgh\", \"target_language\": \"Chinese\", \"style_guide\": \"诗意且幽默\"}",
     "mode":"true",
    "jsonText":{}
  
  },
    "response_mode": "blocking",
    "user": "abc-123"
  
  }'
  ```

* 案例

  ```sh
  {
      "data":{
        "app": {
          "name": "操作助手",
          "setting": "设置",
          "quit": "退出"
        },
        "language": {
          "zh": "简体中文",
          "en": "English"
        },
        "user": {
          "username": "用户名",
          "password": "密码",
          "role": "角色"
        },
        "menu": {
          "sortingLabel": "分拣标签",
          "labelPrinting": "分拣标签打印",
          "handoverScan": "交接扫描",
          "manifestImport": "分拣数据导入",
          "toDoorToPortIconSetting": "到门到港图标设置"
        },
        "weighing": {
          "printAwd": "运单打印",
          "printInvoice": "发票打印",
          "remove": "移除",
          "weighing": "称重",
          "bulkImport": "批量导入重量",
          "weighingSearch": "称重结果查询",
          "print": "打印",
          "Home": "主页",
          "setting": "设置",
          "printerSetting": "打印机设置",
          "electronicScaleSetting": "电子秤设置",
          "addressBook": "通讯录",
          "printStickers": "709袋号贴纸",
          "printStickersRecord": "709袋号贴纸打印记录",
          "electronicModelManage": "电子秤型号管理",
          "platformZ": "Z平台",
          "themeSetting": "主提单设置",
          "hospitalArea": "医院区库位管理",
          "hospitalSetting": "医院区库位设置",
          "hospitalData": "医院区库位盘点数据",
          "hospitalPeddingData": "待盘点数据",
          "inventoryData": "盘点数据",
          "modifyOrder": "改单打印",
          "sortingExpress": "分拣",
          "agencyBusiness": "代理业务",
          "replaceAgency": "更换代理服务",
          "printAgencySheet": "打印代理面单",
          "searchAgencyInfo": "查询运单代理信息",
          "printAgencyTicket": "打印代理交接凭证",
          "warehouse": "末端派送管理",
          "warehouseList": "入柜列表（仓管）",
          "warehouseDetail": "派送预约明细",
          "printTicket": "打印发票",
          "customsBatches": "报关批次配置",
          "printByPieces": "订单号按件打印",
          "bjNotice": "请100%开箱查验发往中国海南省琼海市的快件",
          "iKnow": "我知道了",
          "downloadTheBoxToCheckTheCheckFile": "下载需开箱查验文件",
          "downloadTheBoxToCheckTheCheckFileTip": "请点击“需开箱查验文件”下载，确认开箱查验文件！",
          "uploadBjNotice": "请点击上传任务确认是否有要开箱查验的单",
          "forbidation": "禁止揽收",
          "packaging": "包装型号",
          "quantity": "数量",
          "PackagingService": "包装服务"
        },
        "generateInvoice": {
          "generateInvoice": "生成发票",
          "importTime": "导入时间",
          "importTask": "导入任务"
        },
        "bbd": {
          "bbd": "BBX业务"
        },
        "appMes": {
          "language": "中文",
          "homePageLang": "首页",
          "selectRole": "选择角色",
          "quit": "退出",
          "quitTips": "退出提示",
          "quitContent": "你确定要退出吗",
          "noAuth": "您还没有被赋予任何权限角色，请联系管理员授予角色权限。您确认现在退出吗?",
          "applyPermission": "权限申请",
          "applyContent": "是否进入权限申请界面?",
          "tips": "提示",
          "cancelOption": "取消",
          "submitOption": "确定",
          "operate": "操作",
          "selectRoles": "请选择角色",
          "languageList": [
            {
              "value": "zh",
              "label": "中文"
            }
          ]
        }
      },
      "source_language": "English", 
       "target_language": "Chinese", 
       "style_guide": "诗意且幽默"
  }
  ```

  

* 输入

  ![image-20260209134123220](./assets/image-20260209134123220.png)

* 条件分支

  ![image-20260209134158553](./assets/image-20260209134158553.png)

* 第一分支解析代码

  ```py
  import json
  
  def main(arg1):
      # 1. 处理 Dify 段落类型可能封装的列表
      raw_input = arg1[0] if isinstance(arg1, list) else arg1
      
      if not raw_input:
          return {"is_valid": "false", "error_msg": "输入为空"}
  
      try:
          # 核心逻辑：如果 raw_input 本身被识别为字符串且包含转义的引号
          # 我们尝试先将其解析一次，或者直接进行替换清洗
          if isinstance(raw_input, str):
              # 处理这种极其少见的 double-escape 情况
              if '\\"' in raw_input:
                  raw_input = raw_input.replace('\\"', '"')
              # 如果字符串首尾有引号，去掉它
              if raw_input.startswith('"') and raw_input.endswith('"'):
                  raw_input = raw_input[1:-1]
  
          # 2. 正式解析 JSON
          input_data = json.loads(raw_input)
          
          text = input_data.get("text", "").strip()
          
          if not text:
              return {"is_valid": "false", "error_msg": "文本内容不能为空"}
              
          return {
              "is_valid": "true",
              "text": text,
              "source_language": input_data.get("source_language", "auto"),
              "target_language": input_data.get("target_language", "zh-CN"),
              "style_guide": input_data.get("style_guide", "formal"),
              "error_msg": ""
          }
      except Exception as e:
          return {
              "is_valid": "false",
              "error_msg": f"JSON 解析失败: {str(e)}",
              "text": f"原始输入是: {str(raw_input)[:50]}" # 辅助调试
          }
  ```

* 第一分支第一个大模型

  ```txt
  # Role
  你是一个精通全球语言互译的专家，遵循“信、达、雅”原则。
  
  # Task
  将用户提供的文本翻译为目标语言。
  
  # Rules
  1. 识别语种：如果{{#1770445810303.source_language#}}为 "auto"，请自动识别原文语种。
  2. 目标语种：强制翻译为 {{#1770445810303.target_language#}}。
  3. 风格约束：严格遵循 "{{#1770445810303.style_guide#}}" 风格。
  4. 格式要求：必须输出纯 JSON，严禁包含 Markdown 标签(```json)或任何解释性文字。
  5. 翻译内容：翻译{{#1770445810303.text#}}
  
  # Output JSON Schema
  {
    "translated_text": "string // 译文",
    "detected_source_language": "string // ISO 639-1代码",
    "target_language": "{{#1770445810303.source_language#}}",
    "translation_style": "{{#1770445810303.style_guide#}}",
    "cultural_notes": "string // 如有必要，简述文化适配点",
    "confidence_score": "number // 0.0-1.0"
  }
  ```

* 第一分支第二个大模型

  ```txt
  # Role
  你是一个精通全球语言互译的专家，遵循“信、达、雅”原则。
  
  # Task
  将用户提供的文本翻译为目标语言。
  
  # Rules
  1. 识别语种：如果{{#1770445810303.source_language#}}为 "auto"，请自动识别原文语种。
  2. 目标语种：强制翻译为 {{{#1770445810303.source_language#}}。
  3. 风格约束：严格遵循 "{{#1770445810303.style_guide#}}" 风格。
  4. 格式要求：必须输出纯 JSON，严禁包含 Markdown 标签(```json)或任何解释性文字。
  5. 翻译内容：翻译{{#1770445810303.text#}}
  
  # Output JSON Schema
  {
    "translated_text": "string // 译文",
    "detected_source_language": "string // ISO 639-1代码",
    "target_language": "{{#1770445810303.source_language#}}",
    "translation_style": "{{#1770445810303.style_guide#}}",
    "cultural_notes": "string // 如有必要，简述文化适配点",
    "confidence_score": "number // 0.0-1.0"
  }
  ```

* 第一分支代码3

  ```python
  
  def main():
      # 走到这里说明：主模型报错 -> 备用模型也报错
      # 我们返回一个标准化的错误 JSON 结构
      error_response = {
          "status": "error",
          "data": None,
          "error": {
              "code": 503,
              "message": "所有翻译引擎（DeepSeek/GPT）暂时不可用，请稍后再试"
          }
      }
      
      # Dify 要求返回字典，Key 要对应你设置的输出变量名
      return {
          "final_output": error_response
      }
  ```

  

* 第一分支代码四

  ```py
  import json
  import re
  
  def main(p_res: str, s_res: str, v_err: str, f_err: dict):
      # 提前初始化三个标准输出变量
      status = "error"
      result_data = None
      error_msg = ""
  
      # 情况 1：输入校验未通过
      if v_err and v_err.strip():
          error_msg = v_err
          
      # 情况 2：全线崩溃 (处理 f_err)
      elif f_err:
          # 假设 f_err 是 {"status": "error", "error": {"message": "..."}}
          # 我们把它拆解开
          error_msg = f_err.get("error", {}).get("message", "全线服务异常")
          
      else:
          # 情况 3：模型有输出，开始清洗和解析
          raw_content = p_res if p_res else s_res
          
          if not raw_content:
              error_msg = "翻译服务未响应"
          else:
              try:
                  # 强行提取 JSON
                  match = re.search(r'\{.*\}', raw_content, re.DOTALL)
                  if match:
                      result_data = json.loads(match.group())
                      status = "success"
                      error_msg = ""
                  else:
                      error_msg = "未能在输出中找到合法的 JSON 结构"
              except Exception as e:
                  error_msg = f"输出格式错误: {str(e)}"
  
      # 重点：无论哪个分支，永远返回这三个变量
      return {
          "status": status,
          "result_data": result_data,
          "error_msg": error_msg
      }
  ```

  ![image-20260209134516478](./assets/image-20260209134516478.png)

* 条件分支

  ![image-20260209134537506](./assets/image-20260209134537506.png)

* 正确输出

  ![image-20260209134556538](./assets/image-20260209134556538.png)

* 错误输出

  ![image-20260209134629187](./assets/image-20260209134629187.png)





* 第二个分支解析

  ```py
  import json
  
  def main(arg1):
      # 1. 预先初始化所有输出变量的默认值
      # 这样无论代码走哪个分支（包括报错），都能保证返回所有变量
      is_valid = "false"
      json_object_str = "{}" # 默认给空对象的字符串
      src_lang = "auto"
      tgt_lang = "Chinese"
      style = "formal"
      error_msg = ""
  
      # 2. 处理 Dify 变量可能的封装
      raw_input = arg1[0] if isinstance(arg1, list) else arg1
      
      if not raw_input:
          error_msg = "输入为空"
          # 直接返回默认值集合
          return {
              "is_valid": is_valid,
              "json_object": json_object_str,
              "source_language": src_lang,
              "target_language": tgt_lang,
              "style_guide": style,
              "error_msg": error_msg
          }
  
      try:
          # 3. 清洗并解析 JSON
          if isinstance(raw_input, str):
              clean_input = raw_input.strip()
              # 移除 Dify 可能包裹的首尾引号
              if clean_input.startswith('"') and clean_input.endswith('"'):
                  clean_input = clean_input[1:-1]
              # 处理转义
              clean_input = clean_input.replace('\\"', '"')
              input_data = json.loads(clean_input)
          else:
              input_data = raw_input
  
          # 4. 提取数据 (针对你提供的扁平结构)
          # 获取核心 data 对象
          data_node = input_data.get("data")
          
          # 获取同层级的配置参数
          src_lang = input_data.get("source_language", "auto")
          tgt_lang = input_data.get("target_language", "Chinese")
          style = input_data.get("style_guide", "formal")
  
          if data_node is None:
              error_msg = "输入中缺少核心 'data' 字段"
          else:
              is_valid = "true"
              # 【关键修复】：将字典转为 JSON 字符串，解决 "got dict instead" 报错
              # ensure_ascii=False 保证中文不会变成 \uXXXX
              json_object_str = json.dumps(data_node, ensure_ascii=False)
  
      except Exception as e:
          error_msg = f"解析失败: {str(e)}"
          is_valid = "false"
  
      # 5. 统一返回：必须包含右侧面板定义的所有 Key
      return {
          "is_valid": is_valid,
          "json_object": json_object_str, # 注意：这里返回的是字符串
          "source_language": src_lang,
          "target_language": tgt_lang,
          "style_guide": style,
          "error_msg": error_msg
      }
  ```

  ![image-20260209140223918](./assets/image-20260209140223918.png)

* 第二个分支的大模型

  ```txt
  # Role 你是一个资深的软件国际化（i18n）专家，精通 JSON 结构处理与多语言本地化翻译。 
  # Task 将用户提供的 JSON 对象中所有最底层的 Value（字符串值）翻译为目标语言。 
  # Rules 1. **识别语种**：如果 {{#1770567896314.source_language#}} 为 "auto"，请自动识别原文语种。 2. **目标语种**：强制翻译为 {{#1770567896314.target_language#}}。 3. **风格约束**：严格遵循 "{{#1770567896314.style_guide#}}" 风格，确保符合软件 UI 交互习惯。 4. **格式要求**：必须输出纯 JSON 对象，严禁包含 Markdown 标签（如 ```json）或任何解释性文字。 5. **核心约束**： - **绝对禁止修改任何 Key**（键名）。 - 必须保持原始 JSON 的所有嵌套层级。 - 仅翻译字符串类型的 Value；若 Value 为数组，请翻译数组内的每个字符串。 - **特殊字段处理**：若对象中同时包含 `value` 和 `label` 字段，通常 `value` 是系统标识符，**严禁翻译 `value`**，仅翻译 `label`。 # Input Data {{#1770567896314.json_object#}}
  ```

* 第三个分支

  ```txt
  # Role 你是一个资深的软件国际化（i18n）专家，精通 JSON 结构处理与多语言本地化翻译。 
  # Task 将用户提供的 JSON 对象中所有最底层的 Value（字符串值）翻译为目标语言。 
  # Rules 1. **识别语种**：如果 {{source_language}} 为 "auto"，请自动识别原文语种。 2. **目标语种**：强制翻译为 {{target_language}}。 3. **风格约束**：严格遵循 "{{style_guide}}" 风格，确保符合软件 UI 交互习惯。 4. **格式要求**：必须输出纯 JSON 对象，严禁包含 Markdown 标签（如 ```json）或任何解释性文字。 5. **核心约束**： - **绝对禁止修改任何 Key**（键名）。 - 必须保持原始 JSON 的所有嵌套层级。 - 仅翻译字符串类型的 Value；若 Value 为数组，请翻译数组内的每个字符串。 - **特殊字段处理**：若对象中同时包含 `value` 和 `label` 字段，通常 `value` 是系统标识符，**严禁翻译 `value`**，仅翻译 `label`。 # Input Data {{text}}
  ```

* 代码4

  ```txt
  import json
  
  def get_all_keys(obj, prefix=''):
      """递归获取 JSON 所有路径 Key"""
      keys = set()
      if isinstance(obj, dict):
          for k, v in obj.items():
              path = f"{prefix}.{k}" if prefix else k
              keys.add(path)
              keys.update(get_all_keys(v, path))
      elif isinstance(obj, list):
          for i, item in enumerate(obj):
              path = f"{prefix}[{i}]"
              keys.update(get_all_keys(item, path))
      return keys
  
  def main(origin_obj, translated_str):
      try:
          # 1. 清洗 LLM 输出
          clean_str = translated_str.strip()
          if clean_str.startswith("```json"):
              clean_str = clean_str.split("```json")[1].split("```")[0].strip()
          elif clean_str.startswith("```"):
              clean_str = clean_str.split("```")[1].split("```")[0].strip()
              
          trans_obj = json.loads(clean_str)
          
          # 2. 获取两边的 Key 集合
          keys_origin = get_all_keys(origin_obj)
          keys_trans = get_all_keys(trans_obj)
          
          # 3. 对比差异
          missing_keys = list(keys_origin - keys_trans)
          extra_keys = list(keys_trans - keys_origin)
          
          # 重点修改：统一使用 result_data 作为 Key
          if not missing_keys and not extra_keys:
              return {
                  "status": "success",
                  "result_data": trans_obj, # 修改处
                  "error_msg": ""
              }
          else:
              error_msg = []
              if missing_keys: error_msg.append(f"缺失Key: {missing_keys[:3]}...")
              if extra_keys: error_msg.append(f"多余Key: {extra_keys[:3]}...")
              
              return {
                  "status": "warning",
                  "result_data": trans_obj, # 修改处
                  "error_msg": " | ".join(error_msg)
              }
              
      except Exception as e:
          return {
              "status": "error",
              "result_data": {}, # 修改处
              "error_msg": f"解析失败: {str(e)}"
          }
  ```

  ![image-20260209135451952](./assets/image-20260209135451952.png)

* 代码5

  ```txt
  import json
  
  def get_all_keys(obj, prefix=''):
      """递归获取 JSON 所有路径 Key"""
      keys = set()
      if isinstance(obj, dict):
          for k, v in obj.items():
              path = f"{prefix}.{k}" if prefix else k
              keys.add(path)
              keys.update(get_all_keys(v, path))
      elif isinstance(obj, list):
          for i, item in enumerate(obj):
              path = f"{prefix}[{i}]"
              keys.update(get_all_keys(item, path))
      return keys
  
  def main(origin_obj, translated_str):
      try:
          # 1. 清洗 LLM 输出
          clean_str = translated_str.strip()
          if clean_str.startswith("```json"):
              clean_str = clean_str.split("```json")[1].split("```")[0].strip()
          elif clean_str.startswith("```"):
              clean_str = clean_str.split("```")[1].split("```")[0].strip()
              
          trans_obj = json.loads(clean_str)
          
          # 2. 获取两边的 Key 集合
          keys_origin = get_all_keys(origin_obj)
          keys_trans = get_all_keys(trans_obj)
          
          # 3. 对比差异
          missing_keys = list(keys_origin - keys_trans)
          extra_keys = list(keys_trans - keys_origin)
          
          # 重点修改：统一使用 result_data 作为 Key
          if not missing_keys and not extra_keys:
              return {
                  "status": "success",
                  "result_data": trans_obj, # 修改处
                  "error_msg": ""
              }
          else:
              error_msg = []
              if missing_keys: error_msg.append(f"缺失Key: {missing_keys[:3]}...")
              if extra_keys: error_msg.append(f"多余Key: {extra_keys[:3]}...")
              
              return {
                  "status": "warning",
                  "result_data": trans_obj, # 修改处
                  "error_msg": " | ".join(error_msg)
              }
              
      except Exception as e:
          return {
              "status": "error",
              "result_data": {}, # 修改处
              "error_msg": f"解析失败: {str(e)}"
          }
  ```

  ![image-20260209135518143](./assets/image-20260209135518143.png)

* 条件分支

  ![image-20260209135536950](./assets/image-20260209135536950.png)