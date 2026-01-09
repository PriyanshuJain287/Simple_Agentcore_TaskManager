# 🤖 AgentCore Task Manager

A comprehensive AI-powered task management system built with Python, featuring multiple agent architectures, memory systems, and event-driven processing.

## 🌟 Features

- **Multi-Agent Architecture**: Simple and enhanced agent implementations
- **Task Management**: Create, complete, delete, and track tasks with statistics
- **Memory System**: Persistent conversation and task memory
- **Event-Driven**: Real-time event processing and monitoring
- **Flexible LLM Integration**: Support for OpenAI and other providers
- **State Persistence**: Automatic saving and loading of agent state
- **Interactive CLI**: User-friendly command-line interface

## 🏗️ Project Structure

```
agentcore-mastery/
├── agents/                 # Agent implementations
│   ├── task_manager.py    # Enhanced task manager agent
│   └── __init__.py
├── advanced/              # Advanced multi-agent systems
│   ├── integrated_example.py
│   ├── integrated_system.py
│   ├── multi_agent.py
│   └── orchestrator.py
├── config/                # Configuration files
│   └── agent_config.yaml
├── core/                  # Core system components
│   ├── event_bus.py      # Event system
│   ├── monitoring.py     # System monitoring
│   ├── state_manager.py  # State management
│   └── __init__.py
├── llm/                   # LLM provider integrations
│   ├── providers.py      # LLM provider implementations
│   └── __init__.py
├── memory/                # Memory systems
│   ├── task_memory.py    # Task and conversation memory
│   └── __init__.py
├── tools/                 # Task management tools
│   ├── task_tools.py     # Core task operations
│   └── __init__.py
├── utils/                 # Utility functions
│   ├── decorators.py     # Function decorators
│   ├── validators.py     # Input validation
│   └── __init__.py
├── main.py               # Main application entry point
├── simple_agent.py       # Simple agent (no dependencies)
└── requirements.txt      # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/PriyanshuJain287/Simple_Agentcore_TaskManager.git
   cd Simple_Agentcore_TaskManager
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

### Running the Application

#### Option 1: Enhanced Agent (Recommended)
```bash
python main.py
```

#### Option 2: Simple Agent (No dependencies)
```bash
python simple_agent.py
```

## 💡 Usage Examples

### Basic Task Management
```
You: create Buy groceries
🤖 TaskMaster Pro: ✅ Created: Buy groceries

You: create Write report:Finish the quarterly report
🤖 TaskMaster Pro: ✅ Created: Write report
📝 Description: Finish the quarterly report

You: list tasks
🤖 TaskMaster Pro: 📋 Your Tasks:
⏳ Buy groceries (ID: task_0)
⏳ Write report (ID: task_1)
   📝 Finish the quarterly report

You: complete task_0
🤖 TaskMaster Pro: ✅ Task completed: Buy groceries

You: stats
🤖 TaskMaster Pro: 📊 Task Statistics:
   Total tasks: 2
   Completed: 1
   Pending: 1
   Completion rate: 50%
```

### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `create [task]` | Create a new task | `create Buy milk` |
| `create [task]:[desc]` | Create task with description | `create Report:Write monthly report` |
| `list tasks` | Show pending tasks | `list tasks` |
| `list completed tasks` | Show completed tasks | `list completed tasks` |
| `complete [task_id]` | Mark task as completed | `complete task_0` |
| `delete [task_id]` | Delete a task | `delete task_1` |
| `stats` | Show task statistics | `stats` |
| `status` | Show agent status | `status` |
| `help` | Show help message | `help` |
| `save` | Save current state | `save` |
| `exit` | Exit the application | `exit` |

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Agent Configuration
AGENT_NAME=TaskMaster Pro
USE_EVENTS=true
MEMORY_ENABLED=true
```

### Agent Configuration
Modify `config/agent_config.yaml` to customize agent behavior:

```yaml
agent:
  name: "TaskMaster Pro"
  model: "gpt-3.5-turbo"
  temperature: 0.7
  max_tokens: 1000

features:
  events: true
  memory: true
  persistence: true
  monitoring: true

task_management:
  auto_save: true
  completion_tracking: true
  statistics: true
```

## 🏛️ Architecture

### Agent Types

1. **Simple Agent** (`simple_agent.py`)
   - No external dependencies
   - Basic task management
   - Immediate execution
   - Perfect for testing and learning

2. **Enhanced Agent** (`agents/task_manager.py`)
   - Full AgentCore integration
   - Advanced memory system
   - Event-driven architecture
   - LLM-powered responses

### Core Components

- **Event Bus**: Handles system-wide event communication
- **Memory System**: Stores conversation history and task data
- **State Manager**: Manages agent state persistence
- **Task Tools**: Core task management operations
- **LLM Providers**: Abstraction layer for different AI models

## 🔌 Extending the System

### Adding New Commands

1. Extend the command handler in `simple_agent.py` or `agents/task_manager.py`
2. Add corresponding tool functions in `tools/task_tools.py`
3. Update help text and documentation

### Adding New LLM Providers

1. Create a new provider class in `llm/providers.py`
2. Implement the required interface methods
3. Register the provider in the configuration

### Custom Event Handlers

```python
from core.event_bus import EventBus, Event, EventType

# Create custom event handler
def handle_task_created(event: Event):
    print(f"New task created: {event.data['title']}")

# Register handler
event_bus = EventBus()
event_bus.subscribe(EventType.TASK_CREATED, handle_task_created)
```

## 🧪 Testing

Run the simple agent to test basic functionality:

```bash
python simple_agent.py
```

Test commands:
```
create Test task
list tasks
complete task_0
stats
exit
```

## 📦 Dependencies

- **openai**: OpenAI API integration
- **pydantic**: Data validation and settings management
- **python-dotenv**: Environment variable management
- **PyYAML**: YAML configuration file support
- **termcolor**: Colored terminal output
- **agentcore**: Core agent framework
- **bedrock-agentcore**: Enhanced agent capabilities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Priyanshu Jain**
- Email: priyanshu.jain@somaiya.edu
- GitHub: [@PriyanshuJain287](https://github.com/PriyanshuJain287)

## 🙏 Acknowledgments

- Built with the AgentCore framework
- Inspired by modern AI agent architectures
- Thanks to the open-source community for tools and libraries

## 📚 Additional Resources

- [AgentCore Documentation](https://agentcore.dev)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Python Best Practices](https://docs.python.org/3/tutorial/)

---

⭐ **Star this repository if you find it helpful!**