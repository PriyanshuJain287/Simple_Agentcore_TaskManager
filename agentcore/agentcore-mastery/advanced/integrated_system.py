"""
INTEGRATED SYSTEM - Combining all components
"""
import asyncio
import time
from datetime import datetime

# Import our components
from tools.task_tools import SimpleTaskManager
from memory.task_memory import ConversationMemory
from core.event_bus import EventBus, Event, EventType
from agents.task_manager import TaskManagerAgent

class IntegratedSystem:
    """System that integrates all components"""
    
    def __init__(self):
        print("=" * 60)
        print("🤖 INTEGRATED AGENT SYSTEM")
        print("=" * 60)
        
        # Initialize all components
        print("\n🚀 Initializing components...")
        
        # 1. Event Bus (communication layer)
        self.event_bus = EventBus()
        print("✅ Event Bus ready")
        
        # 2. Task Manager (data layer)
        self.task_manager = SimpleTaskManager()
        print("✅ Task Manager ready")
        
        # 3. Memory System (memory layer)
        self.memory = ConversationMemory()
        print("✅ Memory System ready")
        
        # 4. Agent (AI layer)
        self.agent