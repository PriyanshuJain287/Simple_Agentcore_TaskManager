"""
Simple event system - Understand events before using AgentCore's
"""
from typing import Dict, List, Any, Callable
from datetime import datetime
from enum import Enum

class EventType(Enum):
    """Types of events in our system"""
    TASK_CREATED = "task_created"
    TASK_COMPLETED = "task_completed"
    TASK_DELETED = "task_deleted"
    AGENT_STARTED = "agent_started"
    AGENT_RESPONDED = "agent_responded"
    ERROR_OCCURRED = "error_occurred"

class Event:
    """A simple event object"""
    
    def __init__(self, event_type: EventType, source: str, data: Dict[str, Any]):
        self.type = event_type
        self.source = source
        self.data = data
        self.timestamp = datetime.now()
        self.id = f"event_{self.timestamp.timestamp()}"
    
    def __str__(self):
        return f"[{self.timestamp.strftime('%H:%M:%S')}] {self.type.value}: {self.data.get('message', '')}"

class EventBus:
    """
    Simple event bus - allows different parts of system to communicate
    without knowing about each other
    """
    
    def __init__(self):
        # Dictionary: event_type -> list of handler functions
        self.handlers: Dict[EventType, List[Callable]] = {event_type: [] for event_type in EventType}
        self.event_history: List[Event] = []
        print("🚌 Event Bus initialized")
    
    def subscribe(self, event_type: EventType, handler: Callable):
        """Subscribe a function to handle events of a specific type"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        
        self.handlers[event_type].append(handler)
        print(f"✅ Subscribed handler to {event_type.value}")
    
    def publish(self, event: Event):
        """Publish an event to all subscribed handlers"""
        print(f"📤 Publishing event: {event}")
        self.event_history.append(event)
        
        # Call all handlers for this event type
        handlers = self.handlers.get(event.type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                print(f"❌ Handler error: {e}")
    
    def get_recent_events(self, count: int = 10) -> List[Event]:
        """Get recent events"""
        return self.event_history[-count:] if self.event_history else []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get event bus statistics"""
        stats = {
            "total_events": len(self.event_history),
            "events_by_type": {},
            "handlers_by_type": {}
        }
        
        # Count events by type
        for event in self.event_history:
            event_type = event.type.value
            stats["events_by_type"][event_type] = stats["events_by_type"].get(event_type, 0) + 1
        
        # Count handlers by type
        for event_type, handlers in self.handlers.items():
            stats["handlers_by_type"][event_type.value] = len(handlers)
        
        return stats

# Example handlers
def log_event_to_console(event: Event):
    """Simple handler that logs events to console"""
    print(f"   📝 Logging: {event}")

def notify_on_task_completion(event: Event):
    """Handler that reacts to task completion"""
    if event.type == EventType.TASK_COMPLETED:
        task_data = event.data.get("task", {})
        print(f"   🎉 Task completed celebration: {task_data.get('title', 'Unknown')}!")

# Let's test the event system
if __name__ == "__main__":
    print("🧪 Testing Event System...")
    
    # Create event bus
    bus = EventBus()
    
    # Subscribe handlers
    bus.subscribe(EventType.TASK_CREATED, log_event_to_console)
    bus.subscribe(EventType.TASK_COMPLETED, log_event_to_console)
    bus.subscribe(EventType.TASK_COMPLETED, notify_on_task_completion)
    
    # Publish some events
    print("\n📤 Publishing events:")
    
    bus.publish(Event(
        EventType.TASK_CREATED,
        "test",
        {"task": {"title": "Learn Event System", "id": "task_1"}, "message": "Task created"}
    ))
    
    bus.publish(Event(
        EventType.AGENT_STARTED,
        "system",
        {"agent": "TestAgent", "message": "Agent started"}
    ))
    
    bus.publish(Event(
        EventType.TASK_COMPLETED,
        "user",
        {"task": {"title": "Learn Event System", "id": "task_1"}, "message": "Task completed"}
    ))
    
    # Show statistics
    print("\n📊 Event Bus Statistics:")
    stats = bus.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n✅ Event system test completed!")