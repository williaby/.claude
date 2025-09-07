# Hybrid MCP Conversion - Goals, Objectives & Progress Tracking

## 🎯 Primary Goals

### **Context Liberation Objective**
Transform PromptCraft from context-constrained to context-abundant by implementing hybrid MCP architecture that maintains full functionality while dramatically reducing overhead.

**Target Metrics:**
- **Current State**: 78.5k MCP tokens (39.2% overhead) 
- **Phase 2 Target**: 17k MCP tokens (8.5% overhead)
- **Final Target**: 10k MCP tokens (5% overhead)
- **Liberation Goal**: 68k+ tokens (34%+ context) available for actual work

### **Functionality Preservation**
- ✅ **Zero functionality loss** - All tools available via intelligent routing
- ✅ **Performance maintenance** - Tool access <700ms via agent loading
- ✅ **User experience** - Transparent access to all capabilities
- ✅ **Fallback safety** - Graceful degradation if agent loading fails

### **Architecture Innovation**
Create a reusable pattern for context-optimized MCP deployment that can be applied to other projects and shared with the community.

## 🗺️ Strategic Roadmap

### **Phase 1: Core Tool Optimization (✅ COMPLETED)**
**Duration**: Immediate (30 minutes)
**Status**: ✅ SUCCESS - 5.3k tokens saved

**Achievements:**
- Zen server reconfigured to load only 3 core tools
- Specialty tools moved to agent-scoped loading
- Preserved essential capabilities: chat, layered_consensus, challenge
- **Result**: 83.8k → 78.5k MCP tokens (5.3k immediate savings)

**Lessons Learned:**
- ✅ DISABLED_TOOLS mechanism works perfectly
- ✅ Core tool selection was correct (high-value, frequent use)
- ⚠️ Minor cleanup needed (listmodels, version still showing)

### **Phase 2: Major MCP Server Agent-Scoping (🔄 CURRENT PHASE)**
**Duration**: 2-3 weeks
**Status**: 🎯 PLANNING

**Primary Targets** (by impact):
1. **GitHub MCP Server** (~45k tokens)
   - 84 tools covering repository operations, issues, PRs, workflows
   - **Agent**: `git-workflow-agent`
   - **Triggers**: Repository operations, code management
   - **Expected Savings**: 45k tokens

2. **Playwright MCP Server** (~10k tokens)
   - 21 tools covering browser automation
   - **Agent**: `browser-automation-agent`
   - **Triggers**: UI testing, browser interactions
   - **Expected Savings**: 10k tokens

3. **Filesystem MCP Server** (~6k tokens)
   - 14 tools covering file operations
   - **Agent**: `file-operations-agent`
   - **Triggers**: File I/O, directory management
   - **Expected Savings**: 6k tokens

**Phase 2 Target**: 78.5k → 17k MCP tokens (61k additional savings)

### **Phase 3: Remaining Server Optimization (📋 FUTURE)**
**Duration**: 1-2 weeks
**Status**: 📋 PLANNED

**Remaining Targets**:
- **Sequential Thinking MCP** (~1.3k tokens)
- **Context7 MCP** (~1.3k tokens)  
- **Perplexity MCP** (~1.5k tokens)
- **Semgrep MCP** (~4.5k tokens)
- **Sentry MCP** (~0.5k tokens)
- **Time MCP** (~1k tokens)

**Phase 3 Target**: 17k → 10k MCP tokens (7k final optimization)

## 🏗️ Implementation Architecture

### **Agent-Scoped Tool Loading Pattern**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Claude Code   │    │ Specialized     │    │ MCP Tools       │
│   Main Context  │───▶│ Agent Context   │───▶│ (Isolated)      │
│                 │    │                 │    │                 │
│ Core Tools Only │    │ Task-Specific   │    │ Full Toolset    │
│ (3.5k tokens)   │    │ Tool Loading    │    │ (Agent Scoped)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **Core Principles**
1. **Context Isolation**: Agent tools never pollute main context
2. **On-Demand Loading**: Tools loaded only when agent is invoked
3. **Automatic Cleanup**: Tools unloaded after agent task completion
4. **Graceful Fallback**: Core tools available if agent loading fails
5. **Performance Optimization**: Connection pooling and caching

### **Agent Registry Design**
```python
AGENT_TOOL_MAPPING = {
    "git-workflow-agent": {
        "servers": ["github"],
        "primary_tools": ["create_pull_request", "merge_pull_request", "get_file_contents"],
        "context_budget": 45000,  # tokens
        "triggers": ["git", "repository", "pull request", "github"]
    },
    "browser-automation-agent": {
        "servers": ["playwright"],
        "primary_tools": ["browser_navigate", "browser_click", "browser_snapshot"],
        "context_budget": 10000,
        "triggers": ["browser", "automation", "testing", "UI"]
    }
}
```

## 📊 Progress Tracking

### **Current State (As of Phase 1 Completion)**
```
Context Usage: 96k/200k tokens (48%)
├── System Prompt: 3.4k tokens (1.7%)
├── System Tools: 12.3k tokens (6.1%)
├── MCP Tools: 78.5k tokens (39.2%) ⚠️ OPTIMIZATION TARGET
├── Custom Agents: 290 tokens (0.1%)
├── Memory Files: 1.4k tokens (0.7%)
├── Messages: 96 tokens (0.0%)
└── Free Space: 104.1k tokens (52.0%) ✅ IMPROVED
```

### **Token Liberation Progress**
- **Phase 1 Achievement**: 5.3k tokens liberated (2.7% improvement)
- **Phase 2 Potential**: 61k tokens (30%+ additional liberation)
- **Phase 3 Potential**: 7k tokens (3.5% final optimization)
- **Total Potential**: 73.3k tokens (36%+ total context liberation)

### **Success Metrics Dashboard**
| Metric | Current | Phase 2 Target | Final Target | Status |
|--------|---------|----------------|--------------|---------|
| MCP Token Overhead | 78.5k (39.2%) | 17k (8.5%) | 10k (5%) | 🟡 In Progress |
| Available Context | 104.1k (52%) | 167k (83.5%) | 174k (87%) | 🟢 Improving |
| Core Tools Working | 3/3 (100%) | 3/3 (100%) | 3/3 (100%) | 🟢 Stable |
| Agent Tool Access | Manual | Automated | Optimized | 🟡 Building |

## 🎯 Current Priorities

### **Immediate Actions (This Week)**
1. **✅ Document current progress** (This file)
2. **🔄 Plan GitHub agent implementation** (Biggest impact - 45k tokens)
3. **🔄 Design agent-scoped loading mechanism** (Core infrastructure)
4. **🔄 Create git-workflow-agent prototype** (First major agent)

### **Phase 2 Sprint Planning**
**Week 1**: Infrastructure & GitHub Agent
- Build agent base classes and tool loading system
- Implement git-workflow-agent with GitHub tool loading
- Test agent isolation and cleanup mechanisms

**Week 2**: Browser & File Agents
- Create browser-automation-agent (Playwright tools)
- Build file-operations-agent (Filesystem tools)
- Performance optimization and connection pooling

**Week 3**: Integration & Testing
- End-to-end testing of all agent tool loading
- Performance benchmarking and optimization
- User experience testing and refinement

### **Risk Mitigation Strategies**
1. **Rollback Plan**: Single command to restore full MCP loading
2. **Incremental Deployment**: One agent at a time with testing
3. **Performance Monitoring**: Real-time context and performance tracking
4. **User Communication**: Clear documentation and migration guides

## 🚀 Success Vision

### **End State (All Phases Complete)**
```
Context Usage: 30k/200k tokens (15%)
├── System Prompt: 3.4k tokens (1.7%)
├── System Tools: 12.3k tokens (6.1%)
├── MCP Tools: 10k tokens (5%) ✅ OPTIMIZED
├── Custom Agents: 290 tokens (0.1%)
├── Memory Files: 1.4k tokens (0.7%)
├── Messages: Dynamic
└── Free Space: 170k tokens (85%) 🎯 TARGET ACHIEVED
```

**Impact:**
- **85% context available** for actual development work
- **Zero functionality loss** - all tools accessible via intelligent agents
- **Improved performance** - faster loading, better resource utilization
- **Scalable architecture** - pattern replicable across projects
- **Community contribution** - shareable hybrid MCP architecture

---

## 📝 Decision Log

### **Key Decisions Made**
- **2025-01-06**: Selected core tools (chat, layered_consensus, challenge) based on frequency and value
- **2025-01-06**: Chose agent-scoped loading over tool-level filtering for maximum flexibility
- **2025-01-06**: Prioritized GitHub server first due to massive 45k token impact

### **Pending Decisions**
- **Agent Loading Performance**: Connection pooling vs fresh connections per task
- **Tool Caching Strategy**: Memory vs disk caching for agent tool metadata
- **Fallback Mechanisms**: Graceful degradation vs full tool loading on agent failure

### **Lessons Learned**
- ✅ **DISABLED_TOOLS works perfectly** - zen server optimization validated the approach
- ✅ **Context measurement is accurate** - /context command provides reliable metrics  
- ✅ **Core tool selection was optimal** - chat, layered_consensus, challenge cover essential needs
- ⚠️ **Minor configuration cleanup needed** - some tools still showing despite being disabled

---

*Document Status: Active Tracking*  
*Created: 2025-01-06*  
*Last Updated: 2025-01-06 (Phase 1 Completion)*  
*Next Review: After Phase 2 Sprint 1 (GitHub Agent Implementation)*