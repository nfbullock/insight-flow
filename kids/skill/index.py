#!/usr/bin/env python3
"""InsightFlow Kids - Main skill implementation"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, date

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from generators.daily_packet_generator import DailyPacketGenerator, DailyPacket


class InsightFlowKids:
    """Main skill class for InsightFlow Kids"""
    
    def __init__(self):
        self.generator = DailyPacketGenerator()
        self.output_dir = Path(__file__).parent.parent / "output"
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_packets(self, for_date: str = None) -> dict:
        """Generate daily packets for all children"""
        if for_date:
            packet_date = datetime.strptime(for_date, "%Y-%m-%d").date()
        else:
            packet_date = date.today()
        
        print(f"🌟 Generating InsightFlow packets for {packet_date}...")
        
        # Generate content
        packets = self.generator.generate_daily_packets(packet_date)
        
        # Save packets as JSON for PDF generator
        results = {}
        for child_name, packet in packets.items():
            output_path = self.output_dir / f"{child_name.lower()}-{packet_date}.json"
            
            with open(output_path, 'w') as f:
                json.dump(self._packet_to_dict(packet), f, indent=2)
            
            results[child_name] = {
                "status": "generated",
                "path": str(output_path),
                "theme": packet.theme,
                "activity_count": len(packet.activities)
            }
            
            print(f"✅ {child_name}: {len(packet.activities)} activities ({packet.theme} theme)")
        
        return results
    
    def test_packet(self, child: str = "dahlia") -> dict:
        """Generate a test packet for review"""
        print(f"🧪 Generating test packet for {child}...")
        
        # Generate single packet
        profile = self.generator.load_profile(child)
        packet = self.generator._generate_packet(
            profile=profile,
            packet_date=date.today(),
            theme="ocean",  # Use ocean theme for testing
            collaborative=[]
        )
        
        # Save and return
        output_path = self.output_dir / f"test-{child}-{date.today()}.json"
        with open(output_path, 'w') as f:
            json.dump(self._packet_to_dict(packet), f, indent=2)
        
        # Also print summary
        print("\n📋 Test Packet Summary:")
        print(f"Theme: {packet.theme}")
        print(f"Activities: {len(packet.activities)}")
        for i, activity in enumerate(packet.activities, 1):
            print(f"  {i}. {activity['type']} (~{activity.get('estimated_time', '?')} min)")
        
        return {
            "status": "generated",
            "path": str(output_path),
            "packet": self._packet_to_dict(packet)
        }
    
    def update_profile(self, child: str, updates: dict) -> dict:
        """Update child profile based on feedback"""
        profile = self.generator.load_profile(child)
        
        # Apply updates
        for key, value in updates.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        
        # Save updated profile
        self.generator.save_profile(profile)
        
        return {
            "status": "updated",
            "child": child,
            "updates": updates
        }
    
    def analyze_feedback(self, feedback_data: dict) -> dict:
        """Analyze feedback to improve future generation"""
        # This would process completion times, ratings, etc.
        # and update the child profiles accordingly
        
        insights = {
            "patterns_found": [],
            "adjustments_made": [],
            "recommendations": []
        }
        
        # Example analysis
        if feedback_data.get("completion_time", 0) > 40:
            insights["patterns_found"].append("Packet took longer than target 30 minutes")
            insights["adjustments_made"].append("Reducing activity count by 1")
            insights["recommendations"].append("Monitor next packet completion time")
        
        return insights
    
    def _packet_to_dict(self, packet: DailyPacket) -> dict:
        """Convert packet dataclass to dictionary"""
        return {
            "date": packet.date,
            "child_name": packet.child_name,
            "theme": packet.theme,
            "activities": packet.activities,
            "collaborative_activities": packet.collaborative_activities,
            "parent_notes": packet.parent_notes,
            "tomorrow_teaser": packet.tomorrow_teaser,
            "special_elements": packet.special_elements,
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "version": "1.0",
                "total_activities": len(packet.activities),
                "estimated_time": sum(a.get("estimated_time", 0) for a in packet.activities)
            }
        }


def main():
    """CLI interface for the skill"""
    parser = argparse.ArgumentParser(description="InsightFlow Kids - Daily learning packets")
    parser.add_argument("command", choices=["generate", "test", "update-profile"],
                       help="Command to execute")
    parser.add_argument("--date", help="Date to generate for (YYYY-MM-DD)")
    parser.add_argument("--child", help="Child name for test/update")
    parser.add_argument("--updates", help="JSON string of profile updates")
    
    args = parser.parse_args()
    
    skill = InsightFlowKids()
    
    if args.command == "generate":
        result = skill.generate_packets(args.date)
        print(json.dumps(result, indent=2))
    
    elif args.command == "test":
        result = skill.test_packet(args.child or "dahlia")
        print(f"\n✅ Test packet saved to: {result['path']}")
    
    elif args.command == "update-profile":
        if not args.child or not args.updates:
            print("Error: --child and --updates required for update-profile")
            sys.exit(1)
        
        updates = json.loads(args.updates)
        result = skill.update_profile(args.child, updates)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()