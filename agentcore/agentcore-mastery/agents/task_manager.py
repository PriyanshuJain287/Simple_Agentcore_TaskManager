"""
🤖 TASK MANAGER AGENT - COMPLETE VERSION
========================================
This agent combines:
1. AgentCore framework (if available)
2. Task management tools
3. Conversation memory
4. Event system integration
5. Advanced features

Run with: python main.py
"""

import sys
import os
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

# Add parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import AgentCore
try:
    from agentcore import Agent
    AGENTCORE_AVAILABLE = True
    print("✅ AgentCore framework available")
except ImportError:
    print("⚠️ AgentCore not installed. Using enhanced simple agent.")
    AGENTCORE_AVAILABLE = False

# Import our components
try:
    from tools.task_tools import SimpleTaskManager
    from memory.task_memory import ConversationMemory
    from core.event_bus import EventBus, Event, EventType
except ImportError as e:
    print(f"⚠️ Component import error: {e}")
    print("Creating simplified versions...")
    
    # Fallback implementations
    class SimpleTaskManager:
        def __init__(self):
            self.tasks = {}
            self.task_counter = 0
        
        def create_task(self, title, description=""):
            task_id = f"task_{self.task_counter}"
            self.task_counter += 1
            self.tasks[task_id] = {
                "id": task_id, "title": title, "description": description,
                "created_at": datetime.now().isoformat(), "completed": False
            }
            return {"status": "success", "task": self.tasks[task_id]}
        
        def list_tasks(self, show_completed=False):
            return list(self.tasks.values())
        
        def complete_task(self, task_id):
            if task_id in self.tasks:
                self.tasks[task_id]["completed"] = True
                return {"status": "success"}
            return {"status": "error"}
        
        def delete_task(self, task_id):
            if task_id in self.tasks:
                del self.tasks[task_id]
                return {"status": "success"}
            return {"status": "error"}
        
        def get_stats(self):
            return {"total": len(self.tasks)}
    
    class ConversationMemory:
        def __init__(self):
            self.conversations = []
        
        def add_conversation(self, user, agent):
            self.conversations.append({"user": user, "agent": agent})
        
        def get_recent_conversations(self, count=3):
            return self.conversations[-count:] if self.conversations else []
    
    class EventType:
        TASK_CREATED = "task_created"
        TASK_COMPLETED = "task_completed"
        AGENT_RESPONDED = "agent_responded"
    
    class Event:
        def __init__(self, event_type, source, data):
            self.type = event_type
            self.source = source
            self.data = data
    
    class EventBus:
        def __init__(self):
            self.handlers = {}
        
        def subscribe(self, event_type, handler):
            if event_type not in self.handlers:
                self.handlers[event_type] = []
            self.handlers[event_type].append(handler)
        
        def publish(self, event):
            handlers = self.handlers.get(event.type, [])
            for handler in handlers:
                try:
                    handler(event)
                except:
                    pass

# ============================================================================
# AGENT IMPLEMENTATION
# ============================================================================

class EnhancedTaskManagerAgent:
    """
    Enhanced agent with or without AgentCore.
    This is the MAIN AGENT CLASS you'll interact with.
    """
    
    def __init__(self, name: str = "TaskMaster", use_events: bool = True):
        """
        Initialize the agent with all components.
        
        Args:
            name: Agent name
            use_events: Whether to enable event system
        """
        self.name = name
        self.version = "2.0.0"
        self.start_time = datetime.now()
        
        print(f"\n{'='*60}")
        print(f"🤖 {name} Agent v{self.version}")
        print(f"{'='*60}")
        
        # Initialize components
        print("\n🚀 Initializing components...")
        
        # Core components
        self.task_manager = SimpleTaskManager()
        print("  ✅ Task Manager: Ready")
        
        self.memory = ConversationMemory(max_memory=50)
        print("  ✅ Memory System: Ready (50 conversation memory)")
        
        # Event system
        self.use_events = use_events
        if use_events:
            self.event_bus = EventBus()
            self._setup_event_handlers()
            print("  ✅ Event System: Ready")
        else:
            self.event_bus = None
            print("  ⚠️ Event System: Disabled")
        
        # AI capabilities
        self.ai_enabled = AGENTCORE_AVAILABLE
        if self.ai_enabled:
            self._init_agentcore_agent()
        else:
            print("  ⚠️ AI Engine: Simple mode (AgentCore not available)")
        
        # Statistics
        self.stats = {
            "requests_processed": 0,
            "tasks_created": 0,
            "tasks_completed": 0,
            "errors": 0,
            "start_time": self.start_time.isoformat()
        }
        
        # Tool registry
        self.tools = self._register_tools()
        
        print(f"\n✅ {name} initialized successfully!")
        print(f"   Mode: {'AI-Powered' if self.ai_enabled else 'Simple Command'}")
        print(f"   Tools available: {len(self.tools)}")
        print(f"   Memory slots: {self.memory.max_memory}")
        print(f"{'='*60}\n")
    
    # ============================================================================
    # AGENTCORE INTEGRATION (If available)
    # ============================================================================
    
    def _init_agentcore_agent(self):
        """Initialize AgentCore agent if available"""
        try:
            # Create AgentCore agent
            self.agentcore_agent = Agent(
                name=self.name,
                description="A helpful task management assistant",
                system_prompt=self._get_system_prompt(),
                model="gpt-3.5-turbo"  # You can change this
            )
            
            # Register tools with AgentCore
            self._register_agentcore_tools()
            
            print("  ✅ AI Engine: AgentCore initialized (GPT-3.5-turbo)")
        except Exception as e:
            print(f"  ❌ AI Engine failed: {e}")
            self.ai_enabled = False
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the AI"""
        return f"""
        You are {self.name}, an advanced task management assistant.
        
        YOUR CAPABILITIES:
        1. Create, list, complete, and delete tasks
        2. Remember past conversations and user preferences
        3. Provide task statistics and insights
        4. Suggest task prioritization
        
        YOUR PERSONALITY:
        - Friendly and helpful
        - Proactive in suggesting improvements
        - Concise but thorough
        - Learn from user preferences
        
        TASK FORMAT:
        - ID: task_0, task_1, etc.
        - Title: Brief description
        - Status: pending/completed
        - Created: timestamp
        
        RESPONSE GUIDELINES:
        1. Acknowledge the request
        2. Take appropriate action using tools
        3. Report results clearly
        4. Suggest next steps if relevant
        
        USER PREFERENCES (from memory):
        {self._get_user_preferences_text()}
        
        Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
    
    def _get_user_preferences_text(self) -> str:
        """Get user preferences as text for the prompt"""
        prefs = self.memory.user_preferences
        if not prefs:
            return "No specific preferences recorded yet."
        
        pref_text = []
        if prefs.get("prefers_priorities"):
            pref_text.append("• User likes to set priorities for tasks")
        if prefs.get("prefers_details"):
            pref_text.append("• User prefers detailed explanations")
        if prefs.get("prefers_brief"):
            pref_text.append("• User prefers brief responses")
        
        return "\n".join(pref_text) if pref_text else "No specific preferences recorded yet."
    
    def _register_agentcore_tools(self):
        """Register tools with AgentCore agent"""
        
        @self.agentcore_agent.register_tool
        async def create_task(title: str, description: str = "", priority: str = "medium") -> Dict:
            """Create a new task with title, description, and priority"""
            result = self.task_manager.create_task(title, description)
            
            if self.use_events:
                self.event_bus.publish(Event(
                    EventType.TASK_CREATED,
                    self.name,
                    {"task": result.get("task", {}), "priority": priority}
                ))
            
            self.stats["tasks_created"] += 1
            return result
        
        @self.agentcore_agent.register_tool
        async def list_tasks(show_completed: bool = False, priority: Optional[str] = None) -> Dict:
            """List tasks, optionally filtered by completion status and priority"""
            tasks = self.task_manager.list_tasks(show_completed)
            
            # Filter by priority if specified
            if priority:
                tasks = [t for t in tasks if t.get("priority", "medium") == priority]
            
            return {
                "status": "success",
                "tasks": tasks,
                "count": len(tasks),
                "filters": {
                    "show_completed": show_completed,
                    "priority": priority
                }
            }
        
        @self.agentcore_agent.register_tool
        async def complete_task(task_id: str) -> Dict:
            """Mark a task as completed by its ID"""
            result = self.task_manager.complete_task(task_id)
            
            if result["status"] == "success" and self.use_events:
                self.event_bus.publish(Event(
                    EventType.TASK_COMPLETED,
                    self.name,
                    {"task_id": task_id, "result": result}
                ))
            
            self.stats["tasks_completed"] += 1
            return result
        
        @self.agentcore_agent.register_tool
        async def delete_task(task_id: str) -> Dict:
            """Delete a task by its ID"""
            return self.task_manager.delete_task(task_id)
        
        @self.agentcore_agent.register_tool
        async def get_stats(detailed: bool = False) -> Dict:
            """Get task and system statistics"""
            task_stats = self.task_manager.get_stats()
            
            response = {
                "task_statistics": task_stats,
                "agent_statistics": {
                    "requests_processed": self.stats["requests_processed"],
                    "tasks_created": self.stats["tasks_created"],
                    "tasks_completed": self.stats["tasks_completed"],
                    "uptime": str(datetime.now() - self.start_time)
                }
            }
            
            if detailed:
                response["memory_statistics"] = self.memory.get_conversation_summary()
                if self.use_events:
                    response["event_statistics"] = self.event_bus.get_stats() if hasattr(self.event_bus, 'get_stats') else {}
            
            return {"status": "success", "stats": response}
        
        @self.agentcore_agent.register_tool
        async def get_help(category: Optional[str] = None) -> Dict:
            """Get help information about available commands"""
            help_info = {
                "general": "I can help you manage tasks. Try natural language commands!",
                "commands": {
                    "create": "Create a new task: 'create Buy groceries' or 'create important task to finish report'",
                    "list": "List tasks: 'list tasks', 'list completed tasks', 'list high priority tasks'",
                    "complete": "Complete a task: 'complete task_0' or 'mark the first task as done'",
                    "delete": "Delete a task: 'delete task_1'",
                    "stats": "Get statistics: 'stats' or 'show me statistics'",
                    "help": "Get help: 'help' or 'what can you do?'"
                },
                "examples": [
                    "Create a high priority task to finish the report",
                    "Show me all pending tasks",
                    "Mark task_0 as completed",
                    "What are my task statistics?",
                    "Delete the grocery shopping task"
                ]
            }
            
            if category and category in help_info:
                return {"status": "success", "help": help_info[category]}
            return {"status": "success", "help": help_info}
    
    # ============================================================================
    # TOOL REGISTRY (For both AI and simple modes)
    # ============================================================================
    
    def _register_tools(self) -> Dict[str, Dict]:
        """Register all available tools"""
        tools = {
            "create_task": {
                "function": self._tool_create_task,
                "description": "Create a new task",
                "usage": "create_task('Title', 'Description', 'priority')"
            },
            "list_tasks": {
                "function": self._tool_list_tasks,
                "description": "List tasks with filters",
                "usage": "list_tasks(show_completed=False, priority=None)"
            },
            "complete_task": {
                "function": self._tool_complete_task,
                "description": "Mark task as completed",
                "usage": "complete_task('task_id')"
            },
            "delete_task": {
                "function": self._tool_delete_task,
                "description": "Delete a task",
                "usage": "delete_task('task_id')"
            },
            "get_stats": {
                "function": self._tool_get_stats,
                "description": "Get statistics",
                "usage": "get_stats(detailed=False)"
            },
            "get_help": {
                "function": self._tool_get_help,
                "description": "Get help information",
                "usage": "get_help(category=None)"
            }
        }
        
        return tools
    
    # Tool implementations
    def _tool_create_task(self, title: str, description: str = "", priority: str = "medium") -> Dict:
        result = self.task_manager.create_task(title, description)
        
        if self.use_events:
            self.event_bus.publish(Event(
                EventType.TASK_CREATED,
                self.name,
                {"task": result.get("task", {}), "priority": priority}
            ))
        
        self.stats["tasks_created"] += 1
        return result
    
    def _tool_list_tasks(self, show_completed: bool = False, priority: Optional[str] = None) -> Dict:
        tasks = self.task_manager.list_tasks(show_completed)
        
        if priority:
            tasks = [t for t in tasks if t.get("priority", "medium") == priority]
        
        return {
            "status": "success",
            "tasks": tasks,
            "count": len(tasks)
        }
    
    def _tool_complete_task(self, task_id: str) -> Dict:
        result = self.task_manager.complete_task(task_id)
        
        if result["status"] == "success" and self.use_events:
            self.event_bus.publish(Event(
                EventType.TASK_COMPLETED,
                self.name,
                {"task_id": task_id, "result": result}
            ))
        
        self.stats["tasks_completed"] += 1
        return result
    
    def _tool_delete_task(self, task_id: str) -> Dict:
        return self.task_manager.delete_task(task_id)
    
    def _tool_get_stats(self, detailed: bool = False) -> Dict:
        task_stats = self.task_manager.get_stats()
        
        response = {
            "task_statistics": task_stats,
            "agent_statistics": {
                "requests_processed": self.stats["requests_processed"],
                "uptime": str(datetime.now() - self.start_time)
            }
        }
        
        if detailed:
            response["memory_statistics"] = self.memory.get_conversation_summary()
        
        return {"status": "success", "stats": response}
    
    def _tool_get_help(self, category: Optional[str] = None) -> Dict:
        return {"status": "success", "help": "Available commands: create, list, complete, delete, stats, help"}
    
    # ============================================================================
    # EVENT SYSTEM HANDLERS
    # ============================================================================
    
    def _setup_event_handlers(self):
        """Setup event handlers for the event bus"""
        if not self.use_events or not self.event_bus:
            return
        
        # Handler for task created events
        def handle_task_created(event: Event):
            task_data = event.data.get("task", {})
            print(f"   📝 [Event] Task created: {task_data.get('title', 'Unknown')}")
            
            # Log to memory
            self.memory.user_preferences["last_task_created"] = datetime.now().isoformat()
        
        # Handler for task completed events
        def handle_task_completed(event: Event):
            task_id = event.data.get("task_id", "unknown")
            print(f"   🎉 [Event] Task completed: {task_id}")
            
            # Update statistics
            if "tasks_completed_today" not in self.memory.user_preferences:
                self.memory.user_preferences["tasks_completed_today"] = 0
            self.memory.user_preferences["tasks_completed_today"] += 1
        
        # Handler for agent responses
        def handle_agent_responded(event: Event):
            print(f"   💬 [Event] Agent responded to user")
        
        # Subscribe handlers
        self.event_bus.subscribe(EventType.TASK_CREATED, handle_task_created)
        self.event_bus.subscribe(EventType.TASK_COMPLETED, handle_task_completed)
        
        # We'll publish AGENT_RESPONDED events in the process method
        if hasattr(EventType, 'AGENT_RESPONDED'):
            self.event_bus.subscribe(EventType.AGENT_RESPONDED, handle_agent_responded)
    
    # ============================================================================
    # MAIN PROCESSING METHODS
    # ============================================================================
    
    async def process(self, user_input: str) -> str:
        """
        Main method to process user input.
        This is what you call from your main application.
        
        Args:
            user_input: The user's message/command
            
        Returns:
            Agent's response as a string
        """
        self.stats["requests_processed"] += 1
        
        print(f"\n📥 Request #{self.stats['requests_processed']}: {user_input[:50]}...")
        
        try:
            if self.ai_enabled and self.agentcore_agent:
                # Use AgentCore AI to process
                response = await self._process_with_ai(user_input)
            else:
                # Use simple command processing
                response = await self._process_simple(user_input)
            
            # Add to memory
            self.memory.add_conversation(user_input, response)
            
            # Publish event if enabled
            if self.use_events and self.event_bus:
                self.event_bus.publish(Event(
                    EventType.AGENT_RESPONDED if hasattr(EventType, 'AGENT_RESPONDED') else EventType.TASK_CREATED,
                    self.name,
                    {"user_input": user_input[:100], "response_length": len(response)}
                ))
            
            # Save memory periodically
            if self.stats["requests_processed"] % 10 == 0:
                self.memory.save_memory()
            
            return response
            
        except Exception as e:
            self.stats["errors"] += 1
            error_msg = f"❌ Error processing request: {str(e)}"
            print(error_msg)
            return error_msg
    
    async def _process_with_ai(self, user_input: str) -> str:
        """Process using AgentCore AI"""
        # Get conversation context
        recent_conversations = self.memory.get_recent_conversations(3)
        context = ""
        
        if recent_conversations:
            context = "Recent conversation context:\n"
            for conv in recent_conversations:
                context += f"User: {conv['user']}\n"
                context += f"Assistant: {conv['agent']}\n\n"
        
        # Prepare the message with context
        message = context + f"Current user request: {user_input}"
        
        # Get AI response
        response = await self.agentcore_agent.chat(message)
        
        # Extract content
        if response and 'content' in response:
            return response['content']
        elif response and 'error' in response:
            return f"AI Error: {response['error']}"
        else:
            return "I received your request but couldn't generate a response."
    
    async def _process_simple(self, user_input: str) -> str:
        """Process using simple command parsing"""
        user_lower = user_input.lower()
        
        # Parse command
        if user_lower.startswith("create") or "new task" in user_lower:
            # Extract title
            title = "New Task"
            if "to" in user_lower:
                parts = user_lower.split("to", 1)
                title = parts[1].strip().capitalize()
            elif "create" in user_lower:
                parts = user_lower.split("create", 1)
                if len(parts) > 1:
                    title = parts[1].strip().capitalize()
            
            # Check for priority
            priority = "medium"
            if "important" in user_lower or "high priority" in user_lower:
                priority = "high"
            elif "low priority" in user_lower:
                priority = "low"
            
            result = self._tool_create_task(title, f"Created from: {user_input}", priority)
            task = result.get("task", {})
            return f"✅ Created task: {task.get('title', title)} (Priority: {priority}, ID: {task.get('id', 'N/A')})"
        
        elif "list" in user_lower and "task" in user_lower:
            show_completed = "completed" in user_lower
            priority = None
            
            if "high priority" in user_lower:
                priority = "high"
            elif "low priority" in user_lower:
                priority = "low"
            
            result = self._tool_list_tasks(show_completed, priority)
            tasks = result.get("tasks", [])
            
            if not tasks:
                return "📭 No tasks found." + (" Try creating one!" if not show_completed else "")
            
            response = f"📋 Found {len(tasks)} tasks:\n"
            for task in tasks:
                status = "✅" if task.get("completed") else "⏳"
                priority_emoji = "🔴" if task.get("priority") == "high" else "🟡" if task.get("priority") == "low" else "🔵"
                response += f"{status} {priority_emoji} {task.get('title', 'Untitled')} (ID: {task.get('id', 'N/A')})\n"
            
            return response
        
        elif "complete" in user_lower or "done" in user_lower:
            # Try to find task ID
            for word in user_input.split():
                if word.startswith("task_"):
                    result = self._tool_complete_task(word)
                    if result["status"] == "success":
                        return f"✅ Task {word} marked as completed!"
                    else:
                        return f"❌ Could not find task {word}"
            
            return "Please specify a task ID like 'task_0'"
        
        elif "delete" in user_lower or "remove" in user_lower:
            for word in user_input.split():
                if word.startswith("task_"):
                    result = self._tool_delete_task(word)
                    if result["status"] == "success":
                        return f"🗑️ Task {word} deleted!"
                    else:
                        return f"❌ Could not find task {word}"
            
            return "Please specify a task ID like 'task_0'"
        
        elif "stat" in user_lower or "report" in user_lower:
            detailed = "detailed" in user_lower or "full" in user_lower
            result = self._tool_get_stats(detailed)
            stats = result.get("stats", {})
            
            response = "📊 Statistics:\n"
            
            # Task stats
            task_stats = stats.get("task_statistics", {})
            response += f"  Tasks: {task_stats.get('total_tasks', 0)} total, "
            response += f"{task_stats.get('completed', 0)} completed, "
            response += f"{task_stats.get('pending', 0)} pending\n"
            
            # Agent stats
            agent_stats = stats.get("agent_statistics", {})
            response += f"  Agent: {agent_stats.get('requests_processed', 0)} requests processed\n"
            response += f"  Uptime: {agent_stats.get('uptime', 'N/A')}\n"
            
            if detailed:
                memory_stats = stats.get("memory_statistics", {})
                response += f"  Memory: {memory_stats.get('total_conversations', 0)} conversations stored\n"
            
            return response
        
        elif "help" in user_lower or "what can" in user_lower:
            return self.get_help_text()
        
        elif "memory" in user_lower or "history" in user_lower:
            recent = self.memory.get_recent_conversations(5)
            if not recent:
                return "📭 No conversation history yet."
            
            response = "🗣️ Recent conversations:\n"
            for i, conv in enumerate(recent, 1):
                response += f"{i}. You: {conv.get('user', '')[:40]}...\n"
                response += f"   Me: {conv.get('agent', '')[:40]}...\n"
            
            return response
        
        else:
            return self.get_help_text()
    
    # ============================================================================
    # HELPER METHODS
    # ============================================================================
    
    def get_help_text(self) -> str:
        """Get help text for the agent"""
        return f"""
🤖 {self.name} Help
{'='*40}

I can help you manage tasks! Here's what I can do:

📝 **CREATE TASKS**
  • "Create a task to buy groceries"
  • "Add important task: Finish report"
  • "New task: Call mom (high priority)"

📋 **LIST TASKS**
  • "List all tasks"
  • "Show completed tasks"
  • "List high priority tasks"
  • "What tasks do I have?"

✅ **COMPLETE TASKS**
  • "Complete task_0"
  • "Mark the first task as done"
  • "Finish task_1"

🗑️ **DELETE TASKS**
  • "Delete task_2"
  • "Remove the shopping task"

📊 **STATISTICS**
  • "Show statistics"
  • "Get detailed report"
  • "How many tasks do I have?"

💬 **SYSTEM**
  • "help" - Show this message
  • "memory" - Show conversation history
  • "exit" - Exit the agent

💡 **EXAMPLES**
  • "Create a high priority task to finish the project"
  • "Show me all pending tasks"
  • "Complete the first task and show stats"

Mode: {'🤖 AI-Powered' if self.ai_enabled else '⚡ Simple Command'}
Version: {self.version}
        """
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status information"""
        return {
            "name": self.name,
            "version": self.version,
            "ai_enabled": self.ai_enabled,
            "events_enabled": self.use_events,
            "stats": self.stats,
            "uptime": str(datetime.now() - self.start_time),
            "memory_usage": len(self.memory.conversations),
            "tools_available": list(self.tools.keys())
        }
    
    def save_state(self, filename: str = "agent_state.json"):
        """Save agent state to file"""
        state = {
            "agent": {
                "name": self.name,
                "version": self.version,
                "stats": self.stats,
                "start_time": self.start_time.isoformat()
            },
            "tasks": self.task_manager.tasks,
            "task_counter": self.task_manager.task_counter,
            "saved_at": datetime.now().isoformat()
        }
        
        try:
            with open(filename, "w") as f:
                json.dump(state, f, indent=2)
            print(f"💾 Agent state saved to {filename}")
            return True
        except Exception as e:
            print(f"❌ Failed to save state: {e}")
            return False
    
    def load_state(self, filename: str = "agent_state.json"):
        """Load agent state from file"""
        try:
            with open(filename, "r") as f:
                state = json.load(f)
            
            # Load tasks
            if "tasks" in state:
                self.task_manager.tasks = state["tasks"]
            
            if "task_counter" in state:
                self.task_manager.task_counter = state["task_counter"]
            
            print(f"📂 Agent state loaded from {filename}")
            print(f"   Loaded {len(self.task_manager.tasks)} tasks")
            return True
        except FileNotFoundError:
            print(f"📭 State file {filename} not found")
            return False
        except Exception as e:
            print(f"❌ Failed to load state: {e}")
            return False
    
    def shutdown(self):
        """Clean shutdown of the agent"""
        print(f"\n{'='*60}")
        print(f"🛑 Shutting down {self.name}...")
        
        # Save memory
        self.memory.save_memory()
        
        # Save state
        self.save_state()
        
        # Print final statistics
        uptime = datetime.now() - self.start_time
        print(f"📊 Final Statistics:")
        print(f"   • Uptime: {uptime}")
        print(f"   • Requests processed: {self.stats['requests_processed']}")
        print(f"   • Tasks created: {self.stats['tasks_created']}")
        print(f"   • Tasks completed: {self.stats['tasks_completed']}")
        print(f"   • Errors: {self.stats['errors']}")
        print(f"   • Conversations stored: {len(self.memory.conversations)}")
        
        print(f"\n👋 {self.name} shutdown complete")
        print(f"{'='*60}")

# ============================================================================
# SIMPLE STANDALONE AGENT (Fallback)
# ============================================================================

class SimpleTaskAgent:
    """
    Simple standalone agent without dependencies.
    Use this if you want the simplest possible version.
    """
    
    def __init__(self, name: str = "SimpleTaskBot"):
        self.name = name
        self.task_manager = SimpleTaskManager()
        self.history = []
        
        print(f"\n🤖 {name} - Simple Task Agent")
        print("="*40)
        print("Type 'help' for commands, 'exit' to quit\n")
    
    def handle_command(self, command: str) -> str:
        """Handle user commands"""
        cmd = command.lower().strip()
        
        # Record history
        self.history.append({"time": datetime.now().isoformat(), "cmd": cmd})
        
        if cmd == "help":
            return """
Commands:
  create [task]    - Create new task
  list             - List tasks
  complete [id]    - Complete task
  delete [id]      - Delete task
  stats            - Show statistics
  history          - Show command history
  exit             - Exit
            """
        
        elif cmd == "exit":
            return "👋 Goodbye!"
        
        elif cmd.startswith("create"):
            parts = cmd.split(" ", 1)
            if len(parts) < 2:
                return "Usage: create [task description]"
            result = self.task_manager.create_task(parts[1])
            return f"Created: {parts[1]}"
        
        elif cmd == "list":
            tasks = self.task_manager.list_tasks()
            if not tasks:
                return "No tasks."
            return "\n".join([f"{t['id']}: {t['title']}" for t in tasks])
        
        elif cmd.startswith("complete"):
            parts = cmd.split(" ", 1)
            if len(parts) < 2:
                return "Usage: complete [task_id]"
            result = self.task_manager.complete_task(parts[1])
            return "Completed!" if result["status"] == "success" else "Task not found"
        
        elif cmd.startswith("delete"):
            parts = cmd.split(" ", 1)
            if len(parts) < 2:
                return "Usage: delete [task_id]"
            result = self.task_manager.delete_task(parts[1])
            return "Deleted!" if result["status"] == "success" else "Task not found"
        
        elif cmd == "stats":
            stats = self.task_manager.get_stats()
            return f"Tasks: {stats.get('total_tasks', 0)}"
        
        elif cmd == "history":
            if not self.history:
                return "No history."
            return "\n".join([f"{h['time'][11:19]}: {h['cmd']}" for h in self.history[-5:]])
        
        else:
            return "Unknown command. Type 'help' for available commands."

# ============================================================================
# TEST FUNCTION
# ============================================================================

def test_agent():
    """Test the agent"""
    print("🧪 Testing EnhancedTaskManagerAgent...")
    
    # Create agent
    agent = EnhancedTaskManagerAgent(name="TestAgent", use_events=True)
    
    # Test commands
    test_commands = [
        "Create a task to test the agent",
        "List all tasks",
        "Create an important task: Finish testing",
        "List tasks",
        "Show statistics",
        "help"
    ]
    
    async def run_tests():
        for cmd in test_commands:
            print(f"\n{'='*40}")
            print(f"📤 Input: {cmd}")
            response = await agent.process(cmd)
            print(f"📥 Response: {response}")
            await asyncio.sleep(0.5)
    
    # Run tests
    asyncio.run(run_tests())
    
    # Show status
    print(f"\n{'='*40}")
    print("📊 Final Status:")
    status = agent.get_status()
    for key, value in status.items():
        if key != "stats":
            print(f"  {key}: {value}")
    
    # Shutdown
    agent.shutdown()

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    """
    Run this file directly to test the agent:
    python agents/task_manager.py
    """
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_agent()
    else:
        print(f"""
🤖 Task Manager Agent Module
{'='*40}

This module contains the EnhancedTaskManagerAgent class.

USAGE:
1. Import in your code:
   from agents.task_manager import EnhancedTaskManagerAgent
    
2. Create an agent:
   agent = EnhancedTaskManagerAgent(name="YourAgent")
    
3. Process requests:
   response = await agent.process("Create a task")

4. Shutdown when done:
   agent.shutdown()

OPTIONS:
  • name: Agent name (default: "TaskMaster")
  • use_events: Enable event system (default: True)

FEATURES:
  • AI-powered with AgentCore (if available)
  • Conversation memory
  • Event system
  • Task management tools
  • Statistics and reporting
  • State persistence

RUN TESTS:
  python agents/task_manager.py test
        """)