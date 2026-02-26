# InsightFlow Kids Skill

Generates daily personalized learning packets for children.

## Usage
This skill runs automatically via cron at 5 AM to generate and print daily packets.

## Manual Commands
- `generate-packet <child>` - Generate a packet for specific child
- `test-packet` - Generate test packets for review
- `update-profile <child>` - Update child's profile based on feedback

## Components
- Content generators for each activity type
- PDF builder with consistent formatting
- Profile management and adaptation
- Shim API integration for printing