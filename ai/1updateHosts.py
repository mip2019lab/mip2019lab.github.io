import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import requests
import os
import sys
import ctypes
import subprocess
import platform
import webbrowser


class GitHubHostsTool:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub Hosts 自动更新工具")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # 设置样式
        style = ttk.Style()
        style.theme_use('clam')
        
        # 创建界面
        self.create_widgets()
        
        # 检测系统类型
        self.system = platform.system()
        self.hosts_path = self.get_hosts_path()
        
    def get_hosts_path(self):
        """根据系统返回hosts文件路径"""
        if self.system == "Windows":
            return r"C:\Windows\System32\drivers\etc\hosts"
        else:  # Linux/Mac
            return "/etc/hosts"
    
    def create_widgets(self):
        # 标题
        title_label = tk.Label(
            self.root, 
            text="🚀 GitHub Hosts 自动更新工具", 
            font=("Arial", 16, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=10)
        
        # 状态显示区域
        status_frame = tk.Frame(self.root)
        status_frame.pack(pady=5, padx=20, fill=tk.X)
        
        self.status_label = tk.Label(
            status_frame, 
            text="就绪，等待操作...", 
            font=("Arial", 10),
            fg="#7f8c8d"
        )
        self.status_label.pack(side=tk.LEFT)
        
        # 主要按钮区域
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.fetch_btn = tk.Button(
            button_frame,
            text="📥 获取最新IP",
            command=self.fetch_and_update,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        )
        self.fetch_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = tk.Button(
            button_frame,
            text="🗑️ 清空添加的内容",
            command=self.clear_github_hosts,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        self.refresh_btn = tk.Button(
            button_frame,
            text="🔄 刷新DNS缓存",
            command=self.flush_dns,
            bg="#2ecc71",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        )
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # 新增：手动打开网页按钮
        self.open_web_btn = tk.Button(
            button_frame,
            text="🌐 手动下载Hosts",
            command=self.open_github520_web,
            bg="#9b59b6",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        )
        self.open_web_btn.pack(side=tk.LEFT, padx=5)
        
        # 信息显示区域（带滚动条）
        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        info_label = tk.Label(
            info_frame, 
            text="📋 当前hosts内容（仅显示GitHub相关条目）:", 
            font=("Arial", 10, "bold"),
            anchor=tk.W
        )
        info_label.pack(anchor=tk.W)
        
        self.text_area = scrolledtext.ScrolledText(
            info_frame,
            wrap=tk.WORD,
            width=70,
            height=20,
            font=("Consolas", 9),
            bg="#f8f9fa",
            fg="#2c3e50"
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 底部状态栏
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        self.progress = ttk.Progressbar(
            bottom_frame,
            mode='indeterminate',
            length=300
        )
        self.progress.pack(side=tk.RIGHT, padx=20)
        
        # 加载已有的GitHub hosts
        self.load_current_hosts()
    
    def open_github520_web(self):
        """在默认浏览器中打开GitHub520页面"""
        url = "https://github.com/521xueweihan/GitHub520/tree/main"
        try:
            webbrowser.open(url)
            self.status_label.config(text=f"已打开网页: {url}")
        except Exception as e:
            messagebox.showerror("错误", f"无法打开浏览器: {str(e)}")
    
    def load_current_hosts(self):
        """加载当前hosts文件中的GitHub相关条目"""
        try:
            if os.path.exists(self.hosts_path):
                with open(self.hosts_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # 过滤出GitHub相关的行
                github_lines = []
                for line in content.split('\n'):
                    if 'github.com' in line or 'github' in line.lower():
                        github_lines.append(line)
                if github_lines:
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, '\n'.join(github_lines))
                    self.status_label.config(text=f"已加载 {len(github_lines)} 条GitHub相关条目")
                else:
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, "未找到GitHub相关条目")
                    self.status_label.config(text="未找到GitHub相关条目")
        except Exception as e:
            self.status_label.config(text=f"读取hosts文件失败: {str(e)}")
    
    def fetch_and_update(self):
        """获取最新IP并更新hosts文件"""
        # 禁用按钮防止重复点击
        self.fetch_btn.config(state=tk.DISABLED)
        self.status_label.config(text="正在获取最新IP...")
        self.progress.start()
        
        try:
            # 从GitHub520获取最新hosts内容
            url = "https://raw.githubusercontent.com/521xueweihan/GitHub520/main/hosts"
            response = requests.get(url, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                messagebox.showerror("错误", f"获取失败，状态码: {response.status_code}")
                return
            
            new_content = response.text
            
            # 检查是否包含有效的GitHub域名
            if 'github.com' not in new_content:
                messagebox.showerror("错误", "获取的内容不包含GitHub域名，请检查网络连接")
                return
            
            # 备份原hosts文件
            backup_path = self.hosts_path + ".backup"
            try:
                if os.path.exists(self.hosts_path):
                    with open(self.hosts_path, 'r', encoding='utf-8') as f:
                        original_content = f.read()
                    with open(backup_path, 'w', encoding='utf-8') as f:
                        f.write(original_content)
                else:
                    original_content = ""
            except Exception as e:
                messagebox.showerror("错误", f"备份hosts文件失败: {str(e)}")
                return
            
            # 写入新的hosts文件
            try:
                # 如果文件存在，先删除所有GitHub相关行，再追加新内容
                if original_content:
                    # 过滤掉已有的GitHub相关行
                    lines = original_content.split('\n')
                    filtered_lines = []
                    for line in lines:
                        # 跳过包含github的行（包括注释中的）
                        if 'github' in line.lower():
                            continue
                        filtered_lines.append(line)
                    new_hosts_content = '\n'.join(filtered_lines) + '\n\n# GitHub Hosts Start\n' + new_content + '\n# GitHub Hosts End'
                else:
                    new_hosts_content = '# GitHub Hosts Start\n' + new_content + '\n# GitHub Hosts End'
                
                # 写入文件需要管理员权限
                self.write_hosts_with_admin(new_hosts_content)
                
                # 刷新DNS缓存
                self.flush_dns()
                
                # 重新加载显示
                self.load_current_hosts()
                self.status_label.config(text="✅ 更新成功！hosts文件已更新并刷新DNS缓存")
                messagebox.showinfo("成功", "hosts文件更新成功！DNS缓存已刷新。")
                
            except PermissionError:
                messagebox.showerror("权限错误", 
                    "没有权限写入hosts文件！\n"
                    "请以管理员身份运行此程序。\n\n"
                    "Windows: 右键点击程序 -> 以管理员身份运行\n"
                    "Linux/Mac: 使用 sudo python 程序名.py")
            except Exception as e:
                messagebox.showerror("错误", f"写入hosts文件失败: {str(e)}")
                
        except requests.exceptions.Timeout:
            messagebox.showerror("超时", "连接GitHub520超时，请检查网络连接")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("网络错误", f"网络请求失败: {str(e)}")
        except Exception as e:
            messagebox.showerror("未知错误", f"发生错误: {str(e)}")
        finally:
            self.progress.stop()
            self.fetch_btn.config(state=tk.NORMAL)
    
    def write_hosts_with_admin(self, content):
        """以管理员权限写入hosts文件（Windows用ctypes，Linux/Mac用sudo）"""
        if self.system == "Windows":
            # 使用ctypes请求管理员权限
            if not ctypes.windll.shell32.IsUserAnAdmin():
                # 重新以管理员权限运行
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, " ".join(sys.argv), None, 1
                )
                sys.exit()
            else:
                with open(self.hosts_path, 'w', encoding='utf-8') as f:
                    f.write(content)
        else:
            # Linux/Mac 使用临时文件+sudo
            temp_path = "/tmp/hosts_temp"
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(content)
            # 使用sudo移动文件
            subprocess.run(['sudo', 'mv', temp_path, self.hosts_path], check=True)
            # 修复权限
            subprocess.run(['sudo', 'chmod', '644', self.hosts_path], check=True)
    
    def clear_github_hosts(self):
        """清空hosts文件中的GitHub相关条目"""
        if not messagebox.askyesno("确认", "确定要清空所有GitHub相关的hosts条目吗？"):
            return
        
        try:
            if not os.path.exists(self.hosts_path):
                messagebox.showwarning("警告", "hosts文件不存在")
                return
            
            with open(self.hosts_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 过滤掉GitHub相关的行
            lines = content.split('\n')
            filtered_lines = []
            skip_section = False
            for line in lines:
                if '# GitHub Hosts Start' in line:
                    skip_section = True
                    continue
                if '# GitHub Hosts End' in line:
                    skip_section = False
                    continue
                if not skip_section and 'github' not in line.lower():
                    filtered_lines.append(line)
            
            new_content = '\n'.join(filtered_lines)
            
            # 写入文件
            if self.system == "Windows":
                if not ctypes.windll.shell32.IsUserAnAdmin():
                    ctypes.windll.shell32.ShellExecuteW(
                        None, "runas", sys.executable, " ".join(sys.argv), None, 1
                    )
                    sys.exit()
                else:
                    with open(self.hosts_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
            else:
                temp_path = "/tmp/hosts_temp"
                with open(temp_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                subprocess.run(['sudo', 'mv', temp_path, self.hosts_path], check=True)
                subprocess.run(['sudo', 'chmod', '644', self.hosts_path], check=True)
            
            self.load_current_hosts()
            self.status_label.config(text="已清空所有GitHub相关条目")
            messagebox.showinfo("成功", "已清空所有GitHub相关hosts条目")
            
        except Exception as e:
            messagebox.showerror("错误", f"清空失败: {str(e)}")
    
    def flush_dns(self):
        """刷新DNS缓存"""
        try:
            if self.system == "Windows":
                subprocess.run(['ipconfig', '/flushdns'], check=True, capture_output=True)
                self.status_label.config(text="✅ DNS缓存已刷新 (Windows)")
            elif self.system == "Darwin":  # Mac
                subprocess.run(['sudo', 'killall', '-HUP', 'mDNSResponder'], check=True)
                self.status_label.config(text="✅ DNS缓存已刷新 (Mac)")
            else:  # Linux
                # 尝试多种Linux刷新方式
                commands = [
                    ['sudo', 'systemctl', 'restart', 'systemd-resolved'],
                    ['sudo', 'service', 'nscd', 'restart'],
                    ['sudo', 'systemctl', 'restart', 'NetworkManager']
                ]
                success = False
                for cmd in commands:
                    try:
                        subprocess.run(cmd, check=True, capture_output=True)
                        success = True
                        break
                    except:
                        continue
                if success:
                    self.status_label.config(text="✅ DNS缓存已刷新 (Linux)")
                else:
                    self.status_label.config(text="⚠️ DNS刷新命令执行失败，请手动刷新")
        except Exception as e:
            self.status_label.config(text=f"DNS刷新失败: {str(e)}")
            messagebox.showwarning("警告", f"DNS缓存刷新失败，请手动执行相关命令")


if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubHostsTool(root)
    root.mainloop()
