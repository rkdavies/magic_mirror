# AgenticPlatform - Prioritized Implementation Plan

## Project Summary
**Type**: Local Multi-Agent AI Orchestration System  
**Hardware**: RTX A6000 (48GB) + Quadro RTX 6000 (24GB) = 72GB VRAM  
**Core Requirement**: 100% local, no external APIs

---

## Phase 1: Foundation (Critical Path)
**Timeline**: 1-2 days  
**Goal**: Get inference running with basic agent capability

### [ ] T1.1: Environment Verification
**Description**: Verify hardware detection, CUDA, and Docker GPU runtime  
**Acceptance Criteria**:
- `nvidia-smi` shows both GPUs with correct VRAM
- CUDA toolkit installed (nvcc --version)
- Docker with NVIDIA runtime: `docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi`

**Commands**:
```bash
nvidia-smi
nvcc --version
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi
```

### [ ] T1.2: Install Python Dependencies
**Description**: Install core requirements in Docker container  
**Acceptance Criteria**:
- Dockerfile builds successfully
- Can import langgraph, langchain, mcp inside container
- Tested via `docker-compose run --rm app python -c "import ..."`

**Commands**:
```bash
docker-compose build
docker-compose run --rm app python -c "import langgraph; import mcp; print('OK')"
```

### [ ] T1.3: Inference Engine Setup (Ollama - Faster Path)
**Description**: Install Ollama as Docker service for rapid prototyping  
**Acceptance Criteria**:
- Docker Compose runs ollama service
- Health check returns success via `curl localhost:11434/api/tags`

**Commands**:
```bash
docker-compose up -d ollama
curl http://localhost:11434/api/tags
```

### [ ] T1.4: Pull Initial Models
**Description**: Download Qwen 2.5 Coder 32B for coding agent in Docker  
**Acceptance Criteria**:
- Model pulls successfully inside ollama container
- `docker-compose exec ollama ollama list` shows model available
- ~18GB VRAM required

**Commands**:
```bash
docker-compose exec ollama ollama pull qwen2.5-coder:32b
docker-compose exec ollama ollama list
```

### [ ] T1.5: Test Inference API
**Description**: Verify OpenAI-compatible API responds  
**Acceptance Criteria**:
- Health endpoint responds
- Chat completion returns valid response

**Commands**:
```bash
curl http://localhost:11434/api/generate \
  -d '{"model": "qwen2.5-coder:32b", "prompt": "Hello", "stream": false}'
```

### [ ] T1.6: Base Agent Skeleton
**Description**: Create basic agent class with LangGraph in Docker  
**Acceptance Criteria**:
- agents/base.py exists and imports without errors in container
- Can instantiate agent with config
- No MCP tools wired in - keep it simple first
- All code committed to git

**Files to Create**:
- agents/__init__.py
- agents/base.py (from README lines 695-723)

**Test via Docker**:
```bash
docker-compose run --rm app python -c "
from agents.base import BaseAgent, AgentConfig
config = AgentConfig(name='test', model='qwen2.5-coder:32b', system_prompt='You are helpful.', tools=[])
agent = BaseAgent(config)
print('Agent initialized successfully')
"
```

### [ ] T1.7: Single Agent Execution Test
**Description**: Run a simple task through the agent  
**Acceptance Criteria**:
- Agent responds to a basic prompt
- No crashes or hung processes

**Test**:
```python
from agents.base import BaseAgent, AgentConfig
config = AgentConfig(name="test", model="qwen2.5-coder:32b", system_prompt="You are helpful.", tools=[])
agent = BaseAgent(config)
print(agent.run("What is 2+2?"))
```

---

## Phase 2: MCP Infrastructure (Docker)
**Timeline**: 1-2 days  
**Goal**: Give agents tools to interact with the world  
**Requirement**: All MCP servers run as Docker services

### [ ] T2.1: Filesystem MCP Server
**Description**: Configure filesystem MCP for workspace access  
**Acceptance Criteria**:
- npx @modelcontextprotocol/server-filesystem runs
- Tools available: read_file, write_file, list_directory

**Commands**:
```bash
npx -y @modelcontextprotocol/server-filesystem /workspace
```

### [ ] T2.2: GitHub MCP Server
**Description**: Configure GitHub MCP with token  
**Acceptance Criteria**:
- Server starts with GITHUB_TOKEN
- Tools available: get_file, create_commit, create_pull_request

**Commands**:
```bash
GITHUB_TOKEN=ghp_xxx npx -y @modelcontextprotocol/server-github
```

### [ ] T2.3: Brave Search MCP Server
**Description**: Configure web search MCP  
**Acceptance Criteria**:
- Server starts with BRAVE_API_KEY
- Tool available: brave_search

**Commands**:
```bash
BRAVE_API_KEY=xxx npx -y @modelcontextprotocol/server-brave-search
```

### [ ] T2.4: MCP Integration in Agent
**Description**: Wire MCP tools into agent execution  
**Acceptance Criteria**:
- Agent can use filesystem tools
- Agent can execute tool calls successfully

**Files to Edit**:
- agents/base.py - add MCP tool support

---

## Phase 3: Multi-Agent System
**Timeline**: 2-3 days  
**Goal**: Working orchestrator with multiple specialized agents

### [ ] T3.1: Implement Coding Agent
**Description**: Create coding agent with file/Git tools  
**Acceptance Criteria**:
- Can read/write files
- Can execute git commands
- System prompt loaded from config/agents.yaml

**Files to Create**:
- agents/coding.py

### [ ] T3.2: Implement Research Agent
**Description**: Create research agent with search tools  
**Acceptance Criteria**:
- Can search web
- Can fetch URLs
- Returns cited sources

**Files to Create**:
- agents/research.py

### [ ] T3.3: Implement Marketing Agent
**Description**: Create marketing agent  
**Acceptance Criteria**:
- Generates content in Hackshack Labs voice
- Can create social copy

**Files to Create**:
- agents/marketing.py

### [ ] T3.4: Implement Orchestrator
**Description**: Create workflow orchestration with LangGraph  
**Acceptance Criteria**:
- Can route tasks to correct agent
- Can execute sequential workflows
- Can aggregate results

**Files to Create**:
- agents/orchestrator.py (from README lines 727-754)

### [ ] T3.5: Multi-Agent Integration Test
**Description**: Test orchestration across agents  
**Acceptance Criteria**:
- Single task uses multiple agents
- Results aggregated correctly

---

## Phase 4: Production Readiness
**Timeline**: 2-3 days  
**Goal**: Stable, observable, production-ready system

### [ ] T4.1: llama-server Production Setup
**Description**: Replace Ollama with llama.cpp for performance  
**Acceptance Criteria**:
- llama-server builds with CUDA
- GPU layers load correctly
- 10-30% performance improvement over Ollama

**Commands**:
```bash
git clone https://github.com/ggerganov/llama.cpp.git
cmake -B build -DCMAKE_CUDA_ARCHITECTURES="86;90" -DLLAMA_CUBLAS=ON
cmake --build build --config Release -j$(nproc)
./build/bin/llama-server -m models/qwen2.5-coder-32b-q4_k_m.gguf -ngl 99
```

### [ ] T4.2: Download GGUF Models
**Description**: Acquire GGUF format models for llama-server  
**Acceptance Criteria**:
- qwen2.5-coder-32b-q4_k_m.gguf in models/
- qwen2.5-32b-q4_k_m.gguf in models/

**Commands**:
```bash
huggingface-cli download Qwen/Qwen2.5-Coder-32B-Instruct-GGUF qwen2.5-coder-32b-instruct-q4_k_m.gguf
# or use ollama export
```

### [ ] T4.3: GPU Configuration Scripts
**Description**: Create scripts for dual-GPU management  
**Acceptance Criteria**:
- Start script works with tensor-split
- Stop script kills processes cleanly
- Logs captured

**Files to Create**:
- scripts/start_llama_server.sh
- scripts/stop_llama_server.sh

### [ ] T4.4: Health Monitoring
**Description**: Add health check endpoints  
**Acceptance Criteria**:
- /health returns status
- GPU memory usage included in response

### [ ] T4.5: REST API (Optional)
**Description**: Expose FastAPI for external access  
**Acceptance Criteria**:
- POST /task endpoint works
- Response includes agent result

**Files to Create**:
- api/main.py

---

## Phase 5: Testing & Polish
**Timeline**: 1-2 days  
**Goal**: Reliable, tested system

### [ ] T5.1: Unit Tests
**Description**: Test agent components  
**Acceptance Criteria**:
- Test files exist for each agent
- Basic tests pass

**Files to Create**:
- tests/test_agents.py

### [ ] T5.2: Integration Tests
**Description**: Test full workflows  
**Acceptance Criteria**:
- Sequential workflow test passes
- Autonomous workflow test passes

**Files to Create**:
- tests/test_integration.py

### [ ] T5.3: Performance Benchmarking
**Description**: Measure token generation speed  
**Acceptance Criteria**:
- Benchmark script runs
- Results documented

**Files to Create**:
- scripts/benchmark.sh

---

## Docker Container Requirement

**All work products must be contained in Docker containers orchestrated by Docker Compose.**

- Every service runs in a container
- docker-compose.yml manages all orchestration
- Git pull changes on server, rebuild containers
- GPU access via Docker runtime

**Files Required**:
- `docker-compose.yml` - Service orchestration
- `Dockerfile` - Python + CUDA environment
- `.dockerignore` - Exclude large files

---

## Priority Matrix

| Priority | Task | Reason |
|----------|------|--------|
| P0 | T1.1, T1.2, T1.3 | Foundation - nothing works without these |
| P1 | T1.4, T1.5 | Inference capability |
| P1 | T1.6, T1.7 | Basic agent works |
| P2 | T2.1, T2.2 | Core MCP tools for coding agent |
| P2 | T3.1, T3.4 | Working coding agent + orchestrator |
| P3 | T2.3, T3.2 | Research capability |
| P3 | T3.3 | Marketing capability |
| P4 | T4.1, T4.2 | Production performance |
| P4 | T4.3, T4.4, T4.5 | Operational maturity |

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

## Scope Constraints (No Gold-Plating)

**NOT in Phase 1**:
- Multiple llama-server instances (keep simple first)
- vLLM exploration (llama.cpp is sufficient)
- Advanced memory persistence
- UI Dashboard
- Human-in-the-loop workflows
- Additional agent types (Finance, HR, etc.)

**Basic implementations acceptable**:
- Single Ollama instance first (upgrade to llama-server later)
- Sequential workflows before complex parallel ones
- Basic error handling before sophisticated retry logic

---

## Acceptance Criteria Summary

1. [ ] `nvidia-smi` shows 72GB VRAM across 2 GPUs
2. [ ] Ollama serves qwen2.5-coder:32b
3. [ ] Agent responds to basic prompt
4. [ ] Filesystem MCP tools work
5. [ ] Orchestrator routes to coding agent
6. [ ] Sequential workflow executes
7. [ ] llama-server runs with CUDA
8. [ ] Performance benchmarked

---

*Document Version: 1.0*  
*Created: March 26, 2026*
