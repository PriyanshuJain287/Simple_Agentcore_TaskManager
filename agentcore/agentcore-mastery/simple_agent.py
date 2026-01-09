"""
SIMPLE AGENT - No AgentCore required!
Run this immediately to see results.
"""
import json
from datetime import datetime
from tools.task_tools import SimpleTaskManager

class SimpleAgent:
    """The simplest possible agent - understand this first!"""
    
    def __init__(self):
        print("🤖 Initializing Simple Agent...")
        self.task_manager = SimpleTaskManager()
        self.conversation_history = []
        print("✅ Simple Agent ready! Type 'help' for commands.\n")
    
    def handle_command(self, command: str) -> str:
        """Handle user commands - this is the CORE LOGIC"""
        command_lower = command.lower().strip()
        
        # Record conversation
        self.conversation_history.append({
            "time": datetime.now().isoformat(),
            "user": command,
            "agent": None  # Will be filled after response
        })
        
        # HELP command
        if command_lower == "help":
            return self.show_help()
        
        # EXIT command
        elif command_lower == "exit":
            return "👋 Goodbye! See you next time."
        
        # LIST command variations
        elif "list" in command_lower and "task" in command_lower:
            if "completed" in command_lower:
                tasks = self.task_manager.list_tasks(show_completed=True)
            else:
                tasks = self.task_manager.list_tasks()
            
            if not tasks:
                return "📭 You have no tasks. Create one with 'create [task name]'"
            
            response = "📋 Your Tasks:\n"
            for task in tasks:
                status = "✅" if task["completed"] else "⏳"
                response += f"{status} {task['title']} (ID: {task['id']})\n"
                if task.get("description"):
                    response += f"   📝 {task['description']}\n"
            return response
        
        # CREATE command
        elif command_lower.startswith("create"):
            # Extract task title after "create"
            parts = command.split(" ", 1)
            if len(parts) < 2:
                return "❓ Please specify a task: 'create Buy groceries'"
            
            title = parts[1].strip()
            
            # Check for description
            if ":" in title:
                title_parts = title.split(":", 1)
                title = title_parts[0].strip()
                description = title_parts[1].strip()
            else:
                description = ""
            
            result = self.task_manager.create_task(title, description)
            return f"✅ Created: {title}" + (f"\n📝 Description: {description}" if description else "")
        
        # COMPLETE command
        elif command_lower.startswith("complete"):
            parts = command.split(" ", 1)
            if len(parts) < 2:
                return "❓ Please specify task ID: 'complete task_0'"
            
            task_id = parts[1].strip()
            result = self.task_manager.complete_task(task_id)
            return result.get("message", "Task completed")
        
        # DELETE command
        elif command_lower.startswith("delete"):
            parts = command.split(" ", 1)
            if len(parts) < 2:
                return "❓ Please specify task ID: 'delete task_0'"
            
            task_id = parts[1].strip()
            result = self.task_manager.delete_task(task_id)
            return result.get("message", "Task deleted")
        
        # STATS command
        elif command_lower == "stats":
            stats = self.task_manager.get_stats()
            return (
                f"📊 Task Statistics:\n"
                f"   Total tasks: {stats['total_tasks']}\n"
                f"   Completed: {stats['completed']}\n"
                f"   Pending: {stats['pending']}\n"
                f"   Completion rate: {stats['completion_rate']:.0%}"
            )
        
        # HISTORY command
        elif command_lower == "history":
            if not self.conversation_history:
                return "📭 No conversation history yet."
            
            response = "🗣️ Conversation History:\n"
            for i, entry in enumerate(self.conversation_history[-5:]):  # Last 5
                if entry["agent"]:
                    response += f"{i+1}. You: {entry['user'][:50]}...\n"
                    response += f"   Bot: {entry['agent'][:50]}...\n"
            return response
        
        # Unknown command
        else:
            return (
                "🤔 I didn't understand that. Try:\n"
                "  • 'create Buy groceries'\n"
                "  • 'list tasks'\n"
                "  • 'complete task_0'\n"
                "  • 'stats'\n"
                "  • 'help' for all commands"
            )
    
    def show_help(self) -> str:
        """Show help message"""
        return """
🤖 SIMPLE AGENT - COMMAND REFERENCE:

📝 TASK MANAGEMENT:
  • create [task]           - Create a new task
  • create [task]:[desc]    - Create task with description
  • list tasks             - Show pending tasks
  • list completed tasks   - Show completed tasks
  • complete [task_id]     - Mark task as completed
  • delete [task_id]       - Delete a task

📊 SYSTEM:
  • stats                 - Show task statistics
  • history               - Show conversation history
  • help                  - Show this help message
  • exit                  - Exit the agent

💡 EXAMPLES:
  • create Buy milk
  • create Write report:Finish the quarterly report
  • list tasks
  • complete task_0
  • stats
"""

def main():
    """Run the simple agent - MAIN ENTRY POINT"""
    print("=" * 60)
    print("🤖 SIMPLE TASK AGENT v1.0")
    print("=" * 60)
    
    # Create agent
    agent = SimpleAgent()
    
    # Main interaction loop
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
            
            # Handle command
            response = agent.handle_command(user_input)
            
            # Store agent response in history
            if agent.conversation_history:
                agent.conversation_history[-1]["agent"] = response
            
            # Print response
            print(f"\nBot: {response}")
            
            # Check for exit
            if user_input.lower() == "exit":
                break
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()