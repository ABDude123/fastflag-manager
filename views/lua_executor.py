from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QTextEdit, QLabel, QMessageBox, QComboBox, QListWidget)
from PyQt6.QtCore import Qt
import os
import ctypes
import win32process
import win32gui
import win32con
import win32api
import psutil
import requests
from pathlib import Path

class LuaExecutor:
    def __init__(self):
        self.dll_path = self._prepare_dll()
        self.dll = ctypes.WinDLL(str(self.dll_path))
        
    def _prepare_dll(self) -> Path:
        """Download or load the required DLL"""
        dll_path = Path("resources/executor.dll")
        if not dll_path.exists():
            # Download DLL from secure source
            dll_url = "your_secure_dll_url_here"
            os.makedirs(dll_path.parent, exist_ok=True)
            response = requests.get(dll_url)
            with open(dll_path, 'wb') as f:
                f.write(response.content)
        return dll_path
        
    def inject(self, script: str) -> bool:
        """Inject Lua script into Roblox"""
        try:
            # Find Roblox process
            process = self._get_roblox_process()
            if not process:
                raise Exception("Roblox process not found")
                
            # Get process handle
            handle = win32api.OpenProcess(
                win32con.PROCESS_ALL_ACCESS,
                False,
                process.pid
            )
            
            # Prepare script for injection
            script_bytes = script.encode('utf-8')
            script_len = len(script_bytes)
            
            # Allocate memory in target process
            mem = win32process.VirtualAllocEx(
                handle,
                None,
                script_len,
                win32con.MEM_COMMIT | win32con.MEM_RESERVE,
                win32con.PAGE_READWRITE
            )
            
            # Write script to allocated memory
            win32process.WriteProcessMemory(
                handle,
                mem,
                script_bytes,
                script_len
            )
            
            # Call DLL injection function
            result = self.dll.InjectLua(
                handle.handle,
                mem,
                script_len
            )
            
            # Cleanup
            win32process.VirtualFreeEx(handle, mem, 0, win32con.MEM_RELEASE)
            win32api.CloseHandle(handle)
            
            return result == 1
            
        except Exception as e:
            print(f"Injection error: {str(e)}")
            return False
            
    def _get_roblox_process(self):
        """Get Roblox process"""
        for proc in psutil.process_iter(['name', 'pid']):
            if proc.info['name'] == 'RobloxPlayerBeta.exe':
                return proc
        return None

class LuaExecutorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.executor = LuaExecutor()
        self.setup_ui()
        self.load_scripts()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Script editor
        editor_layout = QHBoxLayout()
        
        # Script list
        self.script_list = QListWidget()
        self.script_list.itemClicked.connect(self.load_script)
        editor_layout.addWidget(self.script_list, stretch=1)
        
        # Script editor
        editor_panel = QVBoxLayout()
        self.script_editor = QTextEdit()
        self.script_editor.setPlaceholderText("Enter Lua script here...")
        editor_panel.addWidget(QLabel("Script Editor:"))
        editor_panel.addWidget(self.script_editor)
        
        # Script type selector
        self.script_type = QComboBox()
        self.script_type.addItems(["Universal", "Game-Specific"])
        editor_panel.addWidget(self.script_type)
        
        editor_layout.addLayout(editor_panel, stretch=2)
        layout.addLayout(editor_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.inject_btn = QPushButton("Inject")
        self.inject_btn.clicked.connect(self.inject_script)
        
        self.save_btn = QPushButton("Save Script")
        self.save_btn.clicked.connect(self.save_script)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.script_editor.clear)
        
        button_layout.addWidget(self.inject_btn)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.clear_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def load_scripts(self):
        """Load sample scripts"""
        self.scripts = {
            "ESP": """
                -- ESP Script
                local ESP = loadstring(game:HttpGet("https://kiriot22.com/releases/ESP.lua"))()
                ESP:Toggle(true)
                ESP.Players = true
                ESP.Boxes = true
                ESP.Names = true
            """,
            "Aimbot": """
                -- Basic Aimbot
                local Players = game:GetService("Players")
                local LocalPlayer = Players.LocalPlayer
                local Camera = workspace.CurrentCamera
                local RunService = game:GetService("RunService")
                
                local function getClosestPlayer()
                    local closestPlayer = nil
                    local shortestDistance = math.huge
                    
                    for _, player in ipairs(Players:GetPlayers()) do
                        if player ~= LocalPlayer and player.Character and
                           player.Character:FindFirstChild("Humanoid") and
                           player.Character.Humanoid.Health > 0 then
                            local pos = Camera:WorldToViewportPoint(player.Character.Head.Position)
                            local magnitude = (Vector2.new(pos.X, pos.Y) - Vector2.new(Camera.ViewportSize.X/2, Camera.ViewportSize.Y/2)).magnitude
                            
                            if magnitude < shortestDistance then
                                closestPlayer = player
                                shortestDistance = magnitude
                            end
                        end
                    end
                    
                    return closestPlayer
                end
                
                RunService.RenderStepped:Connect(function()
                    local closest = getClosestPlayer()
                    if closest and closest.Character then
                        Camera.CFrame = CFrame.new(Camera.CFrame.Position, closest.Character.Head.Position)
                    end
                end)
            """,
            "Infinite Jump": """
                -- Infinite Jump
                local Player = game:GetService'Players'.LocalPlayer
                local UIS = game:GetService'UserInputService'
                
                _G.JumpHeight = 50
                
                function Action(Object, Function) if Object ~= nil then Function(Object) end end
                
                UIS.InputBegan:connect(function(UserInput)
                    if UserInput.UserInputType == Enum.UserInputType.Keyboard and UserInput.KeyCode == Enum.KeyCode.Space then
                        Action(Player.Character.Humanoid, function(self)
                            if self:GetState() == Enum.HumanoidStateType.Jumping or self:GetState() == Enum.HumanoidStateType.Freefall then
                                Action(self.Parent.HumanoidRootPart, function(self)
                                    self.Velocity = Vector3.new(0, _G.JumpHeight, 0)
                                end)
                            end
                        end)
                    end
                end)
            """,
            "Speed Hack": """
                -- Speed Hack
                local Player = game:GetService'Players'.LocalPlayer
                local Humanoid = Player.Character.Humanoid
                
                _G.SpeedHack = true
                _G.Speed = 100
                
                game:GetService'RunService'.RenderStepped:Connect(function()
                    if _G.SpeedHack then
                        Humanoid.WalkSpeed = _G.Speed
                    end
                end)
            """
        }
        
        for name in self.scripts:
            self.script_list.addItem(name)
            
    def load_script(self, item):
        """Load selected script into editor"""
        script_name = item.text()
        if script_name in self.scripts:
            self.script_editor.setText(self.scripts[script_name])
            
    def save_script(self):
        """Save current script"""
        try:
            name, ok = QInputDialog.getText(
                self,
                "Save Script",
                "Enter script name:"
            )
            if ok and name:
                self.scripts[name] = self.script_editor.toPlainText()
                self.script_list.addItem(name)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save script: {str(e)}")
            
    def inject_script(self):
        """Inject current script"""
        try:
            script = self.script_editor.toPlainText()
            if not script.strip():
                raise ValueError("Script is empty")
                
            if self.executor.inject(script):
                QMessageBox.information(
                    self,
                    "Success",
                    "Script injected successfully!"
                )
            else:
                QMessageBox.warning(
                    self,
                    "Warning",
                    "Failed to inject script. Make sure Roblox is running."
                )
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to inject script: {str(e)}"
            )