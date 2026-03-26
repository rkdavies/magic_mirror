# AgenticPlatform - Phase 1 Plan (Revised)

**Project**: AgenticPlatform - Local Multi-Agent Orchestration System  
**Original Requirements**: 100% local inference, autonomous agents, no external APIs  
**Timeline**: 1-2 days  
**Persona**: Senior Project Manager (realistic scope, no gold-plating)

---

## Goal
Get inference running with a basic agent that can respond to prompts. Nothing more.

---

## Development Tasks

### [ ] Task 1: Verify Hardware and CUDA
**Description**: Confirm both GPUs are detected and CUDA is available  
**Acceptance Criteria**:
- `nvidia-smi` shows 72GB total VRAM across 2 GPUs
- `nvcc --version` returns CUDA version
- GPU indices confirmed for later use

**Commands**:
```bash
nvidia-smi
nvcc --version
```

**Agent Persona**: System Engineer (any dev can run this)

---

### [ ] Task 2: Docker Environment Setup
**Description**: Create Docker Compose infrastructure for the project  
**Acceptance Criteria**:
- docker-compose.yml created
- Project builds and starts without errors
- All work products contained in Docker
- Can git pull and run `docker-compose up` on server

**Files to Create**:
- `docker-compose.yml` - Main orchestration
- `Dockerfile` - Python + CUDA environment
- `.dockerignore` - Exclude models, logs, venv

**Reference**: Container orchestration requirement

**Agent Persona**: DevOps Engineer (infrastructure as code)

---

### [ ] Task 3: Install Python Dependencies
**Description**: Install core requirements in Dockerfile  
**Acceptance Criteria**:
- requirements.txt installed during build
- `docker-compose run --rm app python -c "import langgraph; import mcp; print('OK')"` succeeds

**Commands**:
```bash
docker-compose build
docker-compose run --rm app python -c "import langgraph; import mcp; print('OK')"
```

**Agent Persona**: Developer (standard Python environment setup)

---

### [ ] Task 4: Ollama in Docker
**Description**: Set up Ollama as a Docker service  
**Acceptance Criteria**:
- ollama service runs in container
- Accessible via localhost:11434
- Model can be pulled inside container

**Files to Update**:
- docker-compose.yml - Add ollama service

**Commands**:
```bash
docker-compose up -d ollama
docker-compose exec ollama ollama pull qwen2.5-coder:32b
```

**Agent Persona**: DevOps Engineer (system software installation)

---

### [ ] Task 5: Test Inference API
**Description**: Verify the inference API responds correctly  
**Acceptance Criteria**:
- API returns valid JSON response
- Model generates coherent output
- No authentication errors

**Commands**:
```bash
curl http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model": "qwen2.5-coder:32b", "prompt": "What is 2+2?", "stream": false}'
```

**Agent Persona**: QA Engineer (verification testing)

---

### [ ] Task 6: Create Base Agent Skeleton
**Description**: Create basic LangGraph agent class in Docker container  
**Acceptance Criteria**:
- agents/base.py exists and imports without errors
- Can instantiate with AgentConfig
- No MCP tools wired in - keep it simple first
- All code committed to git

**Files to Create**:
- agents/__init__.py
- agents/base.py (simplified from README lines 695-723)

**Reference**: README.md Section 7, Step 3.1

**Agent Persona**: MCP Builder (agent infrastructure, even without MCP tools yet)

---

### [ ] Task 7: Test Single Agent Execution
**Description**: Run a simple task through the agent end-to-end in Docker  
**Acceptance Criteria**:
- Agent responds to basic prompt
- Response is coherent
- No crashes or hung processes
- Tested via docker-compose

**Test Code**:
```bash
docker-compose run --rm app python -c "
from agents.base import BaseAgent, AgentConfig
config = AgentConfig(
    name='test',
    model='qwen2.5-coder:32b',
    system_prompt='You are a helpful coding assistant.',
    tools=[]
)
agent = BaseAgent(config)
result = agent.run('What is Python?')
print(result)
"
```

**Agent Persona**: QA Engineer (integration testing)

---

## Git Workflow Requirements

**All code must be git-managed**:
- `git clone` the repository on the server
- `git pull` to update changes
- `docker-compose build` to rebuild after code changes

**Directory Structure**:
```
AgenticPlatform/
├── .git/
├── docker-compose.yml
├── Dockerfile
├── .dockerignore
├── agents/
├── config/
├── docs/
├── requirements.txt
└── README.md
```

**Excluded from Git** (via .gitignore):
- `models/` - Model files (too large)
- `logs/` - Runtime logs
- `__pycache__/` - Python cache
- `.env` - Secrets

---

## What's NOT in Phase 1

Per specification: "100% local, autonomous AI agent workforce for coding, research, marketing"

- MCP servers (save for Phase 2 - per IMPLEMENTATION_PLAN T2.1-T2.4)
- llama.cpp build (defer to Phase 4 - more complex)
- Multiple agents (save for Phase 3)
- Orchestrator workflow (save for Phase 3)
- REST API (Phase 4 or later)
- GGUF model download (Phase 4 - llama-server requirement)

**Basic implementation acceptable**:
- Single Ollama container (upgrade to llama-server later)
- Single model (add more as needed)
- Simple agent without tools first

---

## Quality Requirements

- [ ] All work products in Docker containers
- [ ] docker-compose orchestrates all services
- [ ] Code committed to git before server deployment
- [ ] No background processes in startup commands (no `&`)
- [ ] Tasks are implementable in 30-60 minutes each
- [ ] Acceptance criteria are testable/verifiable
- [ ] No new dependencies beyond requirements.txt

---

## Technical Notes

**Docker Architecture**:
```yaml
services:
  app:
    build: .
    volumes:
      - ./agents:/app/agents
      - ./config:/app/config
    depends_on:
      - ollama
  
  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama_models:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 2
              capabilities: [gpu]
```

**API Endpoint**: http://localhost:11434 (Ollama default)

**Model Memory**: Qwen 2.5 Coder 32B uses ~18GB VRAM at Q4_K_M

**Next Phase Focus** (Phase 2):
- MCP server infrastructure (filesystem, github, brave-search)
- Connect tools to agent

---

## Alignment Notes

This Phase 1 plan aligns with IMPLEMENTATION_PLAN.md tasks:
- T1.1 (Task 1), T1.2 (Task 2), T1.3 (Task 3), T1.4 (Task 4), T1.5 (Task 5), T1.6-T1.7 (Tasks 6-7)

Key deviations from original PHASE1_PLAN:
- Uses Ollama instead of llama-server (realistic - start simple)
- Defers MCP to Phase 2 (per IMPLEMENTATION_PLAN T2.x)
- Single model instead of multiple (per "no gold-plating")
- **Added Docker container requirement** (per user request)

---

*Document Version: 1.2*  
*Revised: March 26, 2026*  
*By: Senior Project Manager*
