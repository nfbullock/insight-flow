# InsightFlow

Daily personalized content generation system.

## Features

### Kids
Daily learning packets for children with:
- Logic puzzles
- Riddles and brain teasers
- Educational activities
- Personalized difficulty scaling
- PDF generation for printing

### Personal (Coming Soon)
Customized daily insights and prompts for adults.

## Structure

```
insightflow/
├── kids/               # Children's daily packets
│   ├── skill/         # OpenClaw skill implementation
│   ├── content/       # Activity databases
│   └── generators/    # PDF generation code
└── personal/          # Adult insight flows (future)
```

## Setup

The skill components are symlinked into the OpenClaw workspace for execution.