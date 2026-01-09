"""
MAIN APPLICATION - Run this to start the agent
"""
import asyncio
import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from agents.task_manager import EnhancedTaskManagerAgent
    AGENT_AVAILABLE = True
except ImportError as e:
    print(f"❌ Error importing agent: {e}")
    AGENT_AVAILABLE = False

def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("🤖 ENHANCED TASK MANAGER AGENT")
    print("=" * 60)
    print("A complete agent system with AI, memory, and events")
    print("=" * 60)

async def main():
    """Main async function"""
    print_banner()
    
    if not AGENT_AVAILABLE:
        print("❌ Could not import agent. Please check the installation.")
        return
    
    # Create agent
    print("\n🚀 Creating agent...")
    agent = EnhancedTaskManagerAgent(
        name="TaskMaster Pro",
        use_events=True  # Enable event system
    )
    
    print("\n🎯 Ready! Type your commands below.")
    print("   Type 'help' for commands, 'exit' to quit")
    print("-" * 60)
    
    # Load previous state if exists
    agent.load_state()
    
    # Main interaction loop
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
            
            # Handle special commands
            if user_input.lower() == "exit":
                print("\n🛑 Shutting down agent...")
                agent.shutdown()
                break
            
            elif user_input.lower() == "help":
                print(agent.get_help_text())
                continue
            
            elif user_input.lower() == "status":
                status = agent.get_status()
                print("\n📊 Agent Status:")
                for key, value in status.items():
                    if key != "stats":
                        print(f"  {key}: {value}")
                continue
            
            elif user_input.lower() == "save":
                agent.save_state()
                print("💾 State saved!")
                continue
            
            elif user_input.lower() == "clear":
                print("\n" * 100)
                continue
            
            # Process with agent
            print("🤔 Processing...")
            response = await agent.process(user_input)
            
            # Print response
            print(f"\n🤖 {agent.name}: {response}")
            
        except KeyboardInterrupt:
            print("\n\n🛑 Interrupted by user. Shutting down...")
            agent.shutdown()
            break
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()

def run_simple():
    """Run simple version if async fails"""
    from agents.task_manager import SimpleTaskAgent
    
    print("\n⚡ Running in Simple Mode")
    print("="*40)
    
    agent = SimpleTaskAgent()
    
    while True:
        try:
            cmd = input("\nCommand: ").strip()
            if not cmd:
                continue
            
            response = agent.handle_command(cmd)
            print(f"Response: {response}")
            
            if cmd.lower() == "exit":
                break
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    try:
        if AGENT_AVAILABLE:
            asyncio.run(main())
        else:
            run_simple()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        print("🔄 Falling back to simple mode...")
        run_simple()