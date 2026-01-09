"""
Simple memory system to remember conversations
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Any
from collections import deque

class ConversationMemory:
    """Remember conversations and user preferences"""
    
    def __init__(self, max_memory: int = 100):
        self.max_memory = max_memory
        self.conversations = deque(maxlen=max_memory)
        self.user_preferences = {}
        self.load_memory()
        
        print(f"🧠 Memory initialized (stores up to {max_memory} conversations)")
    
    def load_memory(self):
        """Load memory from file if it exists"""
        if os.path.exists("memory.json"):
            try:
                with open("memory.json", "r") as f:
                    data = json.load(f)
                    # Convert back to deque
                    self.conversations = deque(data.get("conversations", []), 
                                              maxlen=self.max_memory)
                    self.user_preferences = data.get("preferences", {})
                    print(f"📂 Loaded {len(self.conversations)} past conversations")
            except Exception as e:
                print(f"⚠️ Could not load memory: {e}")
    
    def save_memory(self):
        """Save memory to file"""
        data = {
            "conversations": list(self.conversations),
            "preferences": self.user_preferences,
            "saved_at": datetime.now().isoformat()
        }
        
        try:
            with open("memory.json", "w") as f:
                json.dump(data, f, indent=2)
            print("💾 Memory saved to disk")
        except Exception as e:
            print(f"⚠️ Could not save memory: {e}")
    
    def add_conversation(self, user_input: str, agent_response: str):
        """Add a conversation to memory"""
        conversation = {
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "agent": agent_response,
            "tokens": len(user_input.split()) + len(agent_response.split())
        }
        
        self.conversations.append(conversation)
        
        # Extract preferences from conversation
        self._extract_preferences(user_input, agent_response)
    
    def _extract_preferences(self, user_input: str, agent_response: str):
        """Extract user preferences from conversation"""
        user_lower = user_input.lower()
        
        # Check for priority mentions
        if any(word in user_lower for word in ["important", "urgent", "critical", "high priority"]):
            self.user_preferences["prefers_priorities"] = True
        
        # Check for detail level preference
        if "detailed" in user_lower or "more info" in user_lower:
            self.user_preferences["prefers_details"] = True
        elif "brief" in user_lower or "short" in user_lower:
            self.user_preferences["prefers_brief"] = True
    
    def get_recent_conversations(self, count: int = 5) -> List[Dict]:
        """Get recent conversations"""
        return list(self.conversations)[-count:] if self.conversations else []
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get summary of conversations"""
        if not self.conversations:
            return {"total": 0, "message": "No conversations yet"}
        
        total = len(self.conversations)
        total_tokens = sum(conv["tokens"] for conv in self.conversations)
        oldest = self.conversations[0]["timestamp"] if self.conversations else "N/A"
        newest = self.conversations[-1]["timestamp"] if self.conversations else "N/A"
        
        return {
            "total_conversations": total,
            "total_tokens": total_tokens,
            "time_span": f"{oldest[:10]} to {newest[:10]}",
            "average_tokens": total_tokens // total if total > 0 else 0,
            "preferences": self.user_preferences
        }
    
    def clear_memory(self):
        """Clear all memory"""
        self.conversations.clear()
        self.user_preferences = {}
        print("🧹 Memory cleared")

# Let's test the memory system
if __name__ == "__main__":
    print("🧪 Testing Memory System...")
    
    memory = ConversationMemory(max_memory=5)
    
    # Add some test conversations
    memory.add_conversation("Create an important task", "Created important task")
    memory.add_conversation("List all tasks", "Here are your tasks...")
    memory.add_conversation("Give me detailed report", "Detailed report generated")
    
    # Show recent conversations
    print("\n📝 Recent conversations:")
    for conv in memory.get_recent_conversations():
        print(f"  • {conv['user'][:30]}...")
    
    # Show summary
    print("\n📊 Summary:")
    summary = memory.get_conversation_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # Save memory
    memory.save_memory()
    
    print("\n✅ Memory test completed!")