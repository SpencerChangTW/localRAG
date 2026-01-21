"""
Tkinter GUI 應用程式
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import subprocess
import sys
import os
from typing import List

from document_processor import DocumentProcessor
from vector_db import VectorDatabase
import config


class LocalRAGApp:
    def __init__(self, root):
        """初始化 GUI 應用程式"""
        self.root = root
        self.root.title("Local RAG 文件管理系統")
        self.root.geometry("900x700")
        
        # 初始化核心組件
        self.processor = DocumentProcessor()
        self.vector_db = VectorDatabase()
        self.mcp_process = None
        
        # 設定 GUI
        self._setup_ui()
        
        # 載入現有資料
        self._refresh_data_list()
        
    def _setup_ui(self):
        """設定 UI 元件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # ===== 上傳區域 =====
        upload_frame = ttk.LabelFrame(main_frame, text="文件上傳", padding="10")
        upload_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # 選擇檔案按鈕
        ttk.Button(upload_frame, text="選擇檔案", command=self._select_file).grid(
            row=0, column=0, padx=5, pady=5
        )
        
        # 顯示選擇的檔案
        self.file_label = ttk.Label(upload_frame, text="未選擇檔案", foreground="gray")
        self.file_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # 資料名稱輸入
        ttk.Label(upload_frame, text="資料名稱:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.data_name_entry = ttk.Entry(upload_frame, width=40)
        self.data_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # 上傳按鈕
        self.upload_btn = ttk.Button(upload_frame, text="上傳並處理", command=self._upload_file, state="disabled")
        self.upload_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # ===== 資料列表區域 =====
        data_frame = ttk.LabelFrame(main_frame, text="已儲存的資料", padding="10")
        data_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # 資料列表（含勾選框）
        list_container = ttk.Frame(data_frame)
        list_container.pack(fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(list_container)
        scrollbar.pack(side="right", fill="y")
        
        self.data_listbox = tk.Listbox(list_container, selectmode="multiple", yscrollcommand=scrollbar.set)
        self.data_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.data_listbox.yview)
        
        # 刪除按鈕
        ttk.Button(data_frame, text="刪除選中的資料", command=self._delete_selected).pack(pady=5)
        
        # ===== MCP Server 區域 =====
        mcp_frame = ttk.LabelFrame(main_frame, text="MCP Server 控制", padding="10")
        mcp_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        main_frame.columnconfigure(1, weight=1)
        
        # 選中的資料顯示
        ttk.Label(mcp_frame, text="已選擇的資料:").pack(anchor="w", pady=(5, 0))
        self.selected_data_text = scrolledtext.ScrolledText(mcp_frame, height=6, width=40, wrap="word", state="disabled")
        self.selected_data_text.pack(fill="both", expand=True, pady=5)
        
        # 按鈕框架
        button_frame = ttk.Frame(mcp_frame)
        button_frame.pack(fill="x", pady=5)
        
        # Start 按鈕
        self.start_mcp_btn = ttk.Button(button_frame, text="▶ Start Server", command=self._start_mcp_server, style="Accent.TButton")
        self.start_mcp_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        # Stop 按鈕
        self.stop_mcp_btn = ttk.Button(button_frame, text="⏹ Stop Server", command=self._stop_mcp_server, state="disabled")
        self.stop_mcp_btn.pack(side="left", expand=True, fill="x", padx=(5, 0))
        
        # MCP Server 狀態
        self.mcp_status_label = ttk.Label(mcp_frame, text="● 未啟動", foreground="gray", font=("", 10, "bold"))
        self.mcp_status_label.pack(pady=5)
        
        # MCP Server 連接資訊
        ttk.Label(mcp_frame, text="連接資訊:", font=("", 9, "bold")).pack(anchor="w", pady=(10, 0))
        self.mcp_command_text = scrolledtext.ScrolledText(mcp_frame, height=3, width=40, wrap="word", state="disabled")
        self.mcp_command_text.pack(fill="x", pady=5)
        
        # 綁定列表選擇事件，更新已選資料顯示
        self.data_listbox.bind('<<ListboxSelect>>', self._update_selected_data_display)
        
        # ===== 狀態/日誌區域 =====
        log_frame = ttk.LabelFrame(main_frame, text="操作日誌", padding="10")
        log_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, wrap="word")
        self.log_text.pack(fill="both", expand=True)
        
    def _log(self, message: str):
        """添加日誌訊息"""
        self.log_text.config(state="normal")
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")
        
    def _select_file(self):
        """選擇檔案"""
        filetypes = [
            ("所有支援格式", " ".join([f"*{ext}" for ext in config.SUPPORTED_EXTENSIONS.keys()])),
            ("PDF 文件", "*.pdf"),
            ("Word 文件", "*.docx *.doc"),
            ("文字檔案", "*.txt"),
            ("圖片", "*.jpg *.jpeg *.png"),
            ("PowerPoint", "*.pptx *.ppt"),
        ]
        
        filename = filedialog.askopenfilename(
            title="選擇要上傳的文件",
            filetypes=filetypes
        )
        
        if filename:
            if self.processor.is_supported_file(filename):
                self.selected_file = filename
                self.file_label.config(text=os.path.basename(filename), foreground="black")
                self.upload_btn.config(state="normal")
                self._log(f"已選擇檔案: {os.path.basename(filename)}")
            else:
                messagebox.showerror("錯誤", "不支援的檔案格式")
                
    def _upload_file(self):
        """上傳並處理檔案"""
        if not hasattr(self, 'selected_file'):
            messagebox.showwarning("警告", "請先選擇檔案")
            return
            
        data_name = self.data_name_entry.get().strip()
        if not data_name:
            messagebox.showwarning("警告", "請輸入資料名稱")
            return
        
        # 在背景執行緒中處理
        self.upload_btn.config(state="disabled")
        self._log(f"開始處理檔案: {os.path.basename(self.selected_file)}")
        
        def process_thread():
            try:
                # 處理文件
                result = self.processor.process_document(self.selected_file, data_name)
                
                # 插入資料庫
                count = self.vector_db.insert_documents(
                    chunks=result['chunks'],
                    embeddings=result['embeddings'],
                    file_name=result['file_name'],
                    data_name=data_name
                )
                
                # 更新 UI
                self.root.after(0, lambda: self._upload_complete(data_name, count))
                
            except Exception as e:
                self.root.after(0, lambda: self._upload_error(str(e)))
        
        threading.Thread(target=process_thread, daemon=True).start()
        
    def _upload_complete(self, data_name: str, count: int):
        """上傳完成回調"""
        self._log(f"✓ 成功處理並儲存: {data_name} ({count} 個分塊)")
        self.upload_btn.config(state="normal")
        self.data_name_entry.delete(0, "end")
        self.file_label.config(text="未選擇檔案", foreground="gray")
        self._refresh_data_list()
        messagebox.showinfo("成功", f"文件已成功儲存到資料庫\n分塊數量: {count}")
        
    def _upload_error(self, error_msg: str):
        """上傳錯誤回調"""
        self._log(f"✗ 錯誤: {error_msg}")
        self.upload_btn.config(state="normal")
        messagebox.showerror("錯誤", f"處理失敗: {error_msg}")
        
    def _refresh_data_list(self):
        """重新載入資料列表"""
        self.data_listbox.delete(0, "end")
        data_names = self.vector_db.get_all_data_names()
        for name in data_names:
            self.data_listbox.insert("end", name)
        self._log(f"已載入 {len(data_names)} 個資料名稱")
        # 更新已選資料顯示
        self._update_selected_data_display()
        
    def _delete_selected(self):
        """刪除選中的資料"""
        selected_indices = self.data_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("警告", "請先選擇要刪除的資料")
            return
            
        selected_names = [self.data_listbox.get(i) for i in selected_indices]
        
        if messagebox.askyesno("確認", f"確定要刪除這些資料嗎?\n{', '.join(selected_names)}"):
            for name in selected_names:
                count = self.vector_db.delete_by_data_name(name)
                self._log(f"已刪除: {name} ({count} 個分塊)")
            self._refresh_data_list()
            messagebox.showinfo("成功", "已刪除選中的資料")
    
    def _update_selected_data_display(self, event=None):
        """更新已選資料的顯示"""
        selected_indices = self.data_listbox.curselection()
        selected_names = [self.data_listbox.get(i) for i in selected_indices]
        
        self.selected_data_text.config(state="normal")
        self.selected_data_text.delete("1.0", "end")
        
        if selected_names:
            display_text = f"共選擇 {len(selected_names)} 個資料:\n\n"
            for i, name in enumerate(selected_names, 1):
                display_text += f"{i}. {name}\n"
            self.selected_data_text.insert("1.0", display_text)
        else:
            self.selected_data_text.insert("1.0", "未選擇任何資料\n\n請在左側列表中點選要提供 MCP 服務的資料")
        
        self.selected_data_text.config(state="disabled")
            
            
    def _start_mcp_server(self):
        """啟動 MCP Server (stdio 模式 - 標準 MCP 協議)"""
        # 取得選中的資料名稱
        selected_indices = self.data_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("警告", "請先在左側列表選擇要提供服務的資料\n\n提示: 可以按住 Ctrl 鍵多選")
            return
            
        selected_names = [self.data_listbox.get(i) for i in selected_indices]
        
        # 啟動 MCP Server 程序（stdio 模式）
        try:
            cmd = [sys.executable, "mcp_server.py"] + selected_names
            self.mcp_process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=os.path.dirname(__file__) if os.path.dirname(__file__) else os.getcwd()
            )
            
            # 儲存選中的資料名稱供顯示
            self.current_mcp_data = selected_names
            
            # 更新 UI
            self.start_mcp_btn.config(state="disabled")
            self.stop_mcp_btn.config(state="normal")
            self.mcp_status_label.config(text="● 運行中", foreground="green")
            
            # 顯示連接資訊 - stdio 模式
            mcp_info = f"MCP Server 已啟動\n\n"
            mcp_info += f"模式: stdio (標準 MCP 協議)\n\n"
            mcp_info += f"服務資料: {', '.join(selected_names)}\n\n"
            mcp_info += f"配置方式:\n"
            mcp_info += f"參考 MCP_USAGE.md 配置 Claude Desktop 或 GitHub Copilot"
            
            self.mcp_command_text.config(state="normal")
            self.mcp_command_text.delete("1.0", "end")
            self.mcp_command_text.insert("1.0", mcp_info)
            self.mcp_command_text.config(state="disabled")
            
            self._log(f"✓ MCP Server 已啟動 (stdio 標準協議)")
            self._log(f"  服務資料: {', '.join(selected_names)}")
            self._log(f"  進程 ID: {self.mcp_process.pid}")
            
        except Exception as e:
            messagebox.showerror("錯誤", f"啟動 MCP Server 失敗:\n{str(e)}")
            self._log(f"✗ MCP Server 啟動失敗: {str(e)}")
            import traceback
            traceback.print_exc()
            
    def _stop_mcp_server(self):
        """停止 MCP Server"""
        if hasattr(self, 'mcp_process') and self.mcp_process:
            try:
                self.mcp_process.terminate()
                self.mcp_process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.mcp_process.kill()
                self.mcp_process.wait()
            except Exception as e:
                self._log(f"停止時發生錯誤: {e}")
            finally:
                self.mcp_process = None
        
        # 更新 UI
        self.start_mcp_btn.config(state="normal")
        self.stop_mcp_btn.config(state="disabled")
        self.mcp_status_label.config(text="● 未啟動", foreground="gray")
        
        self.mcp_command_text.config(state="normal")
        self.mcp_command_text.delete("1.0", "end")
        self.mcp_command_text.insert("1.0", "Server 已停止")
        self.mcp_command_text.config(state="disabled")
        
        self._log("MCP Server 已停止")
            
    def cleanup(self):
        """清理資源"""
        if self.mcp_process:
            self._stop_mcp_server()


def main():
    """主程式入口"""
    root = tk.Tk()
    app = LocalRAGApp(root)
    
    # 關閉視窗時清理資源
    def on_closing():
        app.cleanup()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
