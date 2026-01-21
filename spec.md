# 角色
你是一位資深的 Python AI 工程師。請根據需求描述協助我設計一個做Local RAG的資料庫儲存程式,並可以根據我選擇的相關文件提供MCP Service

# 上載文件需求
- 可以上載PDF,Word,TXT,Picture,PPT等等文件
- 在來使用Markitdown的方式轉換PDF,Word,TXT,Picture,PPT為Markitdown 格式
- 並將Markitdown格式轉換成向量資料庫,存在QDRANT資料庫。
- 每個文件需要關連到一個資料名稱

# User interface
- 使用Tkinter當Windows GUI
- 提供可以上載PDF,Word,TXT,Picture,PPT等等文件
- 在來讓User可以選擇此檔案的資料名稱
- 轉換後，可以提供查詢資料名稱,可提供勾選是否提供MCP Server

# 提供MCP Service
- 使用者可以勾選名字,代表要提供的MCP Service
- 列出MCP Server的URL
- 請參考Markitdown的功能去做MCP Server
