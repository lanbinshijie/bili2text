# Bili2Text v3 开发文档

## 项目结构

```
+-- src                     -- + 源代码
|  +-- utils                --  - 工具函数
|  |  +-- audioTools.py     --      + 音频处理工具
|  |  +-- videoTools.py     --      + 视频处理工具
|  |  +-- textTools.py      --      + 文本处理工具
|  +-- webserver            --  - Web服务器
|  |  +-- db                --      + 数据库
|  |  |  +-- service.py     --          + 数据库服务
|  |  +-- server.py         --      + 服务器
|  |  +-- templates         --      - 模板
|  |  |  +-- ...pages       --          + 网页
|  +-- core.py              --  - 核心
+ requirements.txt          -- - 依赖
+ main.py                   -- - 主程序入口
```