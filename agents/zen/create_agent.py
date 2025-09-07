"""CreateAgent implementation for C.R.E.A.T.E. framework prompt generation.

This module implements the CreateAgent class following development.md naming conventions:
- Agent ID: create_agent (snake_case)
- Agent Class: CreateAgent (PascalCase + "Agent" suffix)
- Knowledge Folder: /knowledge/create_agent/ (snake_case matching agent_id)
- Qdrant Collection: create_agent (snake_case matching agent_id)

The CreateAgent specializes in generating prompts using the C.R.E.A.T.E. framework:
- C (Context): Role, persona, background, goals
- R (Request): Core task, deliverable specifications
- E (Examples): Few-shot examples and demonstrations
- A (Augmentations): Frameworks, evidence, reasoning prompts
- T (Tone & Format): Voice, style, structural formatting
- E (Evaluation): Quality checks and verification

Architecture:
    This agent currently implements a placeholder pattern pending full integration
    with the BaseAgent interface and Zen MCP Server orchestration.

Dependencies:
    - typing: For type annotations
    - Future: BaseAgent interface, Zen MCP integration, Qdrant client

Called by:
    - src/main.py: FastAPI endpoint integration
    - Future: Agent registry system via dependency injection

Complexity: O(1) - Simple string operations with no algorithmic complexity

Note:
    This implementation is a placeholder that needs refactoring to align with
    the BaseAgent interface as specified in /docs/zen/02-agent-system.md
"""

import logging
from typing import Any, Dict, Tuple

from src.core.anchor_qr_evaluator import ANCHORQREvaluator, RigorLevel


class CreateAgent:
    """Agent for C.R.E.A.T.E. framework prompt generation.

    This agent handles the generation and optimization of prompts using the
    C.R.E.A.T.E. framework (Context, Request, Examples, Augmentations, Tone & Format, Evaluation).

    Attributes:
        agent_id: The unique identifier for this agent (create_agent)
        knowledge_base_path: Path to the agent's knowledge base
        qdrant_collection: Name of the Qdrant collection for this agent
    """

    def __init__(self) -> None:
        """Initialize the CreateAgent with proper naming conventions.

        Initializes the agent with configuration following the development.md standards.
        Sets up the agent_id, knowledge_base_path, and qdrant_collection according
        to the naming conventions specified in the architecture documentation.

        Time Complexity: O(1) - Simple assignment operations
        Space Complexity: O(1) - Fixed memory allocation

        Note:
            This initialization pattern will be replaced when refactoring to align
            with the BaseAgent interface which expects a config dictionary parameter.
        """
        self.agent_id = "create_agent"  # snake_case per development.md 3.1
        self.knowledge_base_path = f"/knowledge/{self.agent_id}/"  # development.md 3.9
        self.qdrant_collection = self.agent_id  # development.md 3.1
        self.logger = logging.getLogger(__name__)
        self.anchor_qr_evaluator = ANCHORQREvaluator()

    def get_agent_id(self) -> str:
        """Return the agent ID following naming conventions.

        Returns:
            The agent ID in snake_case format: 'create_agent'

        Time Complexity: O(1) - Simple attribute access
        Space Complexity: O(1) - Returns existing string reference

        Called by:
            - External systems for agent identification
            - Registry systems for agent discovery
            - Logging and monitoring systems
        """
        return self.agent_id

    def get_knowledge_path(self) -> str:
        """Return the knowledge base path following development.md conventions.

        Returns:
            Path in format: /knowledge/{agent_id}/

        Time Complexity: O(1) - Simple attribute access
        Space Complexity: O(1) - Returns existing string reference

        Called by:
            - Knowledge ingestion systems
            - RAG pipeline for knowledge retrieval
            - Configuration validation systems
        """
        return self.knowledge_base_path

    def get_qdrant_collection(self) -> str:
        """Return the Qdrant collection name following naming conventions.

        Returns:
            Collection name matching agent_id: 'create_agent'

        Time Complexity: O(1) - Simple attribute access
        Space Complexity: O(1) - Returns existing string reference

        Called by:
            - Qdrant client for vector operations
            - Collection management systems
            - Vector search and retrieval operations
        """
        return self.qdrant_collection

    def generate_prompt(
        self,
        context: dict[str, Any],
        preferences: dict[str, Any] | None = None,
        include_evaluation: bool = False,
    ) -> str | Tuple[str, Dict[str, Any]]:
        """Generate a C.R.E.A.T.E. framework optimized prompt.

        This method implements the core functionality of the CreateAgent, generating
        prompts using the C.R.E.A.T.E. framework methodology for optimal AI interaction.

        Args:
            context: Context information for prompt generation including:
                - query: User's original query/request
                - query_analysis: Analysis results from query processing
                - reasoning_depth: Desired analysis depth (basic, intermediate, comprehensive)
                - hyde_score: HyDE specificity score for enhancement decisions
            preferences: Optional user preferences for customization including:
                - tone_preference: Desired communication style
                - format_preference: Output structure preferences
                - framework_preference: Specific analytical frameworks to use
            include_evaluation: Whether to run ANCHOR-QR-8 evaluation on generated prompt

        Returns:
            If include_evaluation is True: Tuple of (formatted CREATE prompt, evaluation results dict)
            If include_evaluation is False: Just the formatted CREATE prompt string (backward compatibility)

        Time Complexity: O(n*m*k) where n is query complexity, m is knowledge base size, k is evaluation depth
        Space Complexity: O(k) where k is the generated prompt length plus evaluation data
        """
        try:
            # Extract context information
            # Extract query from various possible field names for backward compatibility
            query = context.get("query", "") or context.get("task", "") or context.get("request", "")
            query_analysis = context.get("query_analysis", {})
            reasoning_depth = context.get("reasoning_depth", "intermediate")
            
            # Handle empty context with a generic query if absolutely empty
            if not query.strip():
                if not context:  # Completely empty context
                    query = "Provide helpful assistance"
                else:
                    error_prompt = self._generate_error_prompt("Empty query provided")
                    if include_evaluation:
                        return error_prompt, {"error": "Empty query provided", "evaluation": None}
                    else:
                        return error_prompt
            
            # Build C.R.E.A.T.E. components
            context_component = self._build_context_component(query, query_analysis, preferences)
            request_component = self._build_request_component(query, reasoning_depth, query_analysis)
            examples_component = self._build_examples_component(query, query_analysis)
            augmentations_component = self._build_augmentations_component(query, query_analysis)
            tone_format_component = self._build_tone_format_component(query, preferences)
            evaluation_component = self._build_evaluation_component(reasoning_depth, query_analysis)
            
            # Assemble complete CREATE prompt
            create_prompt = f"""# C.R.E.A.T.E. Framework Enhanced Prompt

## C - Context (Role, Background, Goal)
{context_component}

## R - Request (Task, Format, Depth, Action Verbs)
{request_component}

## E - Examples (Few-Shot Prompting)
{examples_component}

## A - Augmentations (Frameworks, Evidence, Reasoning)
{augmentations_component}

## T - Tone & Format (Voice, Style, Structure)
{tone_format_component}

## E - Evaluation (Quality Assurance, Verification)
{evaluation_component}

---

**Instructions for Use**: Copy this entire C.R.E.A.T.E. framework prompt and provide it to your AI assistant to receive a comprehensive, well-structured response that meets professional standards.

*This CREATE framework prompt was generated by PromptCraft to ensure high-quality, reliable AI outputs with minimal hallucinations and appropriate sourcing for independent validation.*"""
            
            # Run ANCHOR-QR-8 evaluation if requested
            evaluation_results = {}
            if include_evaluation:
                try:
                    # Determine appropriate rigor level
                    rigor_level = self._determine_rigor_level(reasoning_depth, query_analysis)
                    
                    # Execute comprehensive evaluation
                    evaluation = self.anchor_qr_evaluator.evaluate_prompt(
                        create_prompt, context, rigor_level
                    )
                    
                    evaluation_results = {
                        "overall_score": evaluation.overall_score,
                        "overall_confidence": evaluation.overall_confidence,
                        "compliance_score": evaluation.compliance_score,
                        "rigor_level": evaluation.rigor_level.value,
                        "is_passing": evaluation.is_passing,
                        "needs_revision": evaluation.needs_revision,
                        "flags": [flag.value for flag in evaluation.all_flags],
                        "critical_issues": evaluation.critical_issues,
                        "recommendations": evaluation.improvement_recommendations[:5],  # Top 5 recommendations
                        "step_scores": {
                            step.value: result.score 
                            for step, result in evaluation.step_results.items()
                        }
                    }
                    
                    self.logger.info(
                        f"ANCHOR-QR evaluation complete: Score {evaluation.overall_score:.1f}, "
                        f"Compliance {evaluation.compliance_score:.1f}, "
                        f"Flags: {len(evaluation.all_flags)}"
                    )
                    
                except Exception as eval_error:
                    self.logger.warning(f"ANCHOR-QR evaluation failed: {eval_error}")
                    evaluation_results = {"error": f"Evaluation failed: {str(eval_error)}"}
            
            # Return based on include_evaluation flag
            if include_evaluation:
                return create_prompt, evaluation_results
            else:
                return create_prompt
            
        except Exception as e:
            self.logger.error(f"Error in CREATE prompt generation: {e}")
            error_prompt = self._generate_error_prompt(f"Generation failed: {str(e)}")
            if include_evaluation:
                return error_prompt, {"error": f"Generation failed: {str(e)}", "evaluation": None}
            else:
                return error_prompt

    def _generate_error_prompt(self, error_message: str) -> str:
        """Generate a basic prompt when full CREATE generation fails."""
        return f"""# Prompt Generation Error

An error occurred during CREATE framework prompt generation: {error_message}

Please try again with a clearer query, or contact support if the issue persists.

## Fallback Prompt Structure

**Context**: Please act as a helpful assistant
**Request**: {error_message}
**Guidance**: Provide a clear, accurate response based on the query provided
"""

    def _build_context_component(
        self, 
        query: str, 
        query_analysis: dict[str, Any], 
        preferences: dict[str, Any] | None = None
    ) -> str:
        """Build the Context (C) component following CREATE framework rules."""
        # Determine appropriate role based on query analysis
        query_type = query_analysis.get("query_type", "general")
        role = self._determine_role_from_query_type(query_type, query)
        
        # Generate persona clause (≤12 words, humanizing detail)
        persona = self._generate_persona_clause(query_type, role)
        
        # Extract background requirements
        background = self._extract_background_context(query, query_analysis)
        
        # Define clear goal
        goal = self._define_response_goal(query, query_analysis)
        
        return f"""**Role**: You are a {role}, {persona}

**Background**: {background}

**Goal**: {goal}

**Audience**: The response should be appropriate for {query_analysis.get('complexity', 'intermediate')}-level understanding."""

    def _build_request_component(
        self, 
        query: str, 
        reasoning_depth: str, 
        query_analysis: dict[str, Any]
    ) -> str:
        """Build the Request (R) component with precise deliverable specifications."""
        # Determine appropriate tier based on query complexity
        tier_info = self._select_appropriate_tier(reasoning_depth, query_analysis)
        
        # Extract strong action verbs
        action_verbs = self._extract_action_verbs(query)
        
        # Determine output format
        output_format = self._determine_output_format(query, query_analysis)
        
        return f"""**Primary Task**: {query}

**Deliverable Requirements**:
- Format: {output_format}
- Depth: {tier_info}
- Action Focus: {action_verbs}
- Scope: Comprehensive analysis addressing all aspects of the query
- Quality Standard: Professional-grade output suitable for business decision-making

**Success Criteria**: Response must be actionable, well-structured, and provide clear value to the user."""

    def _build_examples_component(self, query: str, query_analysis: dict[str, Any]) -> str:
        """Build the Examples (E) component with relevant few-shot demonstrations."""
        query_type = query_analysis.get("query_type", "general")
        
        # For now, provide structure examples - will be enhanced with knowledge base integration
        if "comparison" in query.lower() or "vs" in query.lower():
            return """### Example Structure ###
**Aspect 1 Comparison**:
- Option A: [Specific characteristic with evidence]
- Option B: [Contrasting characteristic with evidence]
- Key Differentiator: [Critical distinction that influences decisions]

### Example Quality Standard ###
Each comparison point should include:
- Specific, measurable differences
- Relevant examples or case studies
- Clear implications for the user's context"""
        
        return """### Example Response Pattern ###
**Analysis Framework**:
1. Core Concept Definition: [Clear, precise definition]
2. Key Components: [Essential elements with explanations]
3. Practical Applications: [Real-world examples and use cases]
4. Implementation Considerations: [Actionable guidance]

**Quality Indicators**: Specific details, credible sources, actionable insights"""

    def _build_augmentations_component(self, query: str, query_analysis: dict[str, Any]) -> str:
        """Build the Augmentations (A) component with frameworks and evidence requirements."""
        # Select appropriate analytical frameworks
        frameworks = self._select_analytical_frameworks(query, query_analysis)
        
        # Determine evidence requirements
        evidence_requirements = self._determine_evidence_requirements(query_analysis)
        
        return f"""**Analytical Frameworks to Apply**:
{frameworks}

**Evidence Requirements**:
{evidence_requirements}

**Advanced Reasoning**: Apply systematic analysis with clear logical progression. For complex topics, use step-by-step reasoning to build conclusions from evidence."""

    def _build_tone_format_component(
        self, 
        query: str, 
        preferences: dict[str, Any] | None = None
    ) -> str:
        """Build the Tone & Format (T) component with professional standards."""
        # Determine appropriate tone
        tone = preferences.get("tone_preference", "professional") if preferences else "professional"
        
        # Apply stylometry standards (ANCHOR-QR-7 auto-injected defaults)
        return f"""**Tone**: {tone.title()} and accessible, with authoritative expertise

**Writing Standards**:
- Moderate hedge density (5-10% of sentences) to acknowledge appropriate uncertainties
- High lexical diversity (varied vocabulary, no word appearing >2% of tokens)
- Sentence variability (average 17-22 words, with mix of short and long sentences)
- Include at least one rhetorical question to engage critical thinking
- Use narrative prose over bullet lists unless specifically requested

**Structure**: Clear heading hierarchy with logical flow from overview to specific details

**Citation Style**: Include sources and evidence attribution where claims require support"""

    def _build_evaluation_component(self, reasoning_depth: str, query_analysis: dict[str, Any]) -> str:
        """Build the Evaluation (E) component with ANCHOR-QR protocols."""
        complexity = query_analysis.get("complexity", "intermediate")
        
        # Determine appropriate rigor level
        if reasoning_depth == "comprehensive" or complexity == "complex":
            rigor_level = "Advanced"
        elif reasoning_depth == "intermediate":
            rigor_level = "Standard" 
        else:
            rigor_level = "Basic"
        
        return f"""**Quality Assurance Protocol** (ANCHOR-QR-8, {rigor_level} Rigor):

**Success Criteria**:
- Does the response fully address the original query?
- Are all claims supported by evidence or clearly marked as expert judgment?
- Is the analysis logically consistent throughout?
- Does the response provide actionable insights?
- Is the tone appropriate for the intended audience?

**Verification Requirements**:
- Check for internal contradictions
- Verify factual accuracy of key claims
- Ensure recommendations are feasible and specific
- Confirm appropriate uncertainty acknowledgment

**Quality Standards**: Professional-grade accuracy, comprehensive coverage, clear practical value"""

    # Helper methods for component building
    def _determine_role_from_query_type(self, query_type: str, query: str) -> str:
        """Determine appropriate professional role based on query analysis."""
        role_mapping = {
            "security": "cybersecurity architect",
            "technical_analysis": "senior systems analyst", 
            "analysis_request": "strategic business analyst",
            "documentation": "technical documentation specialist",
            "create_enhancement": "prompt engineering specialist",
            "implementation": "senior solution architect",
            "general_query": "subject matter expert"
        }
        
        # Enhanced domain-specific keyword detection
        query_lower = query.lower()
        
        # Security-related queries
        if any(term in query_lower for term in ["security", "threat", "vulnerability", "cyber", "attack", "defense"]):
            if "network" in query_lower or "infrastructure" in query_lower:
                return "network security specialist"
            elif "cloud" in query_lower:
                return "cloud security architect"
            else:
                return "cybersecurity architect"
        
        # Development and technical queries
        elif any(term in query_lower for term in ["api", "microservices", "docker", "kubernetes", "ci/cd", "devops"]):
            return "senior software architect"
        
        # Data and analytics queries
        elif any(term in query_lower for term in ["data", "analytics", "power bi", "sql", "database"]):
            return "senior data architect"
        
        # Implementation and how-to queries
        elif any(term in query_lower for term in ["how to", "implement", "setup", "configure"]):
            return "technical implementation specialist"
        
        # Comparison queries
        elif any(term in query_lower for term in ["compare", "vs", "versus", "difference"]):
            return "technology consultant"
        
        # Strategic and business queries
        elif any(term in query_lower for term in ["startup", "business", "strategy", "decision", "recommend"]):
            return "senior technology strategist"
        
        # Machine learning and AI queries
        elif any(term in query_lower for term in ["machine learning", "ai", "artificial intelligence", "model"]):
            return "machine learning engineer"
        
        return role_mapping.get(query_type, "senior consultant")

    def _generate_persona_clause(self, query_type: str, role: str) -> str:
        """Generate persona clause with ≤12 words and humanizing detail."""
        
        # Role-specific persona generation
        if "security" in role.lower():
            return "with 15+ years defending critical infrastructure systems"
        elif "architect" in role.lower():
            return "specializing in scalable enterprise system design"
        elif "consultant" in role.lower():
            return "with proven expertise in technology strategy"
        elif "engineer" in role.lower():
            return "experienced in production-grade system implementation"
        elif "analyst" in role.lower():
            return "focused on data-driven decision making"
        elif "specialist" in role.lower():
            return "with deep domain expertise and practical experience"
        elif "strategist" in role.lower():
            return "experienced in guiding technical business decisions"
        else:
            # Fallback based on query type
            personas = {
                "security": "with proven experience in cybersecurity domains",
                "technical_analysis": "specializing in system optimization and architecture", 
                "analysis_request": "focused on evidence-based strategic analysis",
                "documentation": "known for creating clear, actionable guidance",
                "implementation": "with hands-on experience in complex deployments",
                "general_query": "with comprehensive knowledge across domains"
            }
            return personas.get(query_type, "with deep expertise in the relevant field")

    def _determine_rigor_level(self, reasoning_depth: str, query_analysis: dict[str, Any]) -> RigorLevel:
        """Determine appropriate ANCHOR-QR evaluation rigor level."""
        complexity = query_analysis.get("complexity", "intermediate")
        
        if reasoning_depth == "comprehensive" or complexity == "complex":
            return RigorLevel.ADVANCED
        elif reasoning_depth == "basic" and complexity == "simple":
            return RigorLevel.BASIC
        else:
            return RigorLevel.STANDARD

    def _extract_background_context(self, query: str, query_analysis: dict[str, Any]) -> str:
        """Extract and format background context requirements."""
        context_elements = []
        query_lower = query.lower()
        complexity = query_analysis.get("complexity", "intermediate")
        
        # Complexity-based context
        if complexity == "complex":
            context_elements.append("This is a complex topic requiring comprehensive multi-faceted analysis with consideration of various perspectives and implications")
        elif complexity == "intermediate":
            context_elements.append("This topic requires structured analysis with attention to key factors and relationships")
        
        # Query pattern-based context
        if any(term in query_lower for term in ["compare", "vs", "versus", "difference"]):
            context_elements.append("Multiple options or approaches require systematic comparison to support informed decision-making")
        
        if any(term in query_lower for term in ["how to", "implement", "setup", "configure"]):
            context_elements.append("The user needs step-by-step guidance for practical implementation")
        
        if any(term in query_lower for term in ["security", "threat", "vulnerability"]):
            context_elements.append("Security considerations and risk factors must be thoroughly addressed")
        
        if any(term in query_lower for term in ["startup", "business", "strategy"]):
            context_elements.append("Business context and strategic implications are critical to the analysis")
        
        if any(term in query_lower for term in ["machine learning", "ai", "model"]):
            context_elements.append("Technical accuracy and practical applicability are essential for AI/ML topics")
        
        # Domain-specific context
        if "microservices" in query_lower or "architecture" in query_lower:
            context_elements.append("Architectural decisions have long-term implications for scalability and maintainability")
        
        if "ci/cd" in query_lower or "devops" in query_lower:
            context_elements.append("Implementation must consider development workflow and operational requirements")
        
        # Default context if none matched
        if len(context_elements) == 0:
            context_elements.append("The user seeks authoritative information with practical applicability")
        
        return ". ".join(context_elements) + "."

    def _define_response_goal(self, query: str, query_analysis: dict[str, Any]) -> str:
        """Define clear response goal based on query analysis."""
        if "how to" in query.lower():
            return "Provide step-by-step guidance that enables successful implementation"
        elif any(word in query.lower() for word in ["compare", "vs", "versus", "difference"]):
            return "Deliver clear comparisons that support informed decision-making"
        elif "explain" in query.lower():
            return "Provide comprehensive understanding with practical context"
        else:
            return "Deliver actionable insights that directly address the user's needs"

    def _select_appropriate_tier(self, reasoning_depth: str, query_analysis: dict[str, Any]) -> str:
        """Select appropriate CREATE framework tier based on depth and complexity."""
        complexity = query_analysis.get("complexity", "intermediate")
        
        tier_mapping = {
            ("basic", "simple"): "Tier 3: Summary (200-400 words) - Concise overview",
            ("basic", "intermediate"): "Tier 4: Overview (400-900 words) - Analyst briefing",
            ("intermediate", "simple"): "Tier 4: Overview (400-900 words) - Analyst briefing", 
            ("intermediate", "intermediate"): "Tier 6: In-Depth Analysis (2000-5000 words) - Professional memo",
            ("comprehensive", "simple"): "Tier 6: In-Depth Analysis (2000-5000 words) - Professional memo",
            ("comprehensive", "intermediate"): "Tier 8: Comprehensive Study (8000-15000 words) - Research report",
            ("comprehensive", "complex"): "Tier 9: Expert Analysis (15000-30000 words) - Detailed study"
        }
        
        return tier_mapping.get((reasoning_depth, complexity), "Tier 5: Detailed Response (900-2000 words) - Professional analysis")

    def _extract_action_verbs(self, query: str) -> str:
        """Extract and enhance action verbs from the query."""
        query_lower = query.lower()
        
        if "analyze" in query_lower or "analysis" in query_lower:
            return "Analyze, evaluate, and synthesize"
        elif "compare" in query_lower:
            return "Compare, contrast, and recommend"
        elif "explain" in query_lower:
            return "Explain, clarify, and illustrate"
        elif "implement" in query_lower or "how to" in query_lower:
            return "Guide, implement, and optimize"
        else:
            return "Examine, assess, and advise"

    def _determine_output_format(self, query: str, query_analysis: dict[str, Any]) -> str:
        """Determine appropriate output format based on query characteristics."""
        if "step" in query.lower() or "how to" in query.lower():
            return "Structured guide with clear steps and checkpoints"
        elif "comparison" in query.lower() or "vs" in query.lower():
            return "Comparative analysis with side-by-side evaluation"
        elif query_analysis.get("complexity") == "complex":
            return "Comprehensive report with executive summary and detailed sections"
        else:
            return "Professional analysis with clear structure and actionable insights"

    def _select_analytical_frameworks(self, query: str, query_analysis: dict[str, Any]) -> str:
        """Select appropriate analytical frameworks based on query type."""
        query_type = query_analysis.get("query_type", "general")
        query_lower = query.lower()
        
        frameworks = []
        
        if query_type == "security" or "security" in query_lower:
            frameworks.append("- **STRIDE Analysis**: Systematic threat modeling")
            frameworks.append("- **Defense-in-Depth**: Layered security approach")
        elif "comparison" in query_lower or "vs" in query_lower:
            frameworks.append("- **Comparative Analysis**: Systematic side-by-side evaluation")
            frameworks.append("- **Decision Matrix**: Weighted criteria assessment")
        elif query_type == "analysis_request":
            frameworks.append("- **SWOT Analysis**: Strengths, Weaknesses, Opportunities, Threats")
            frameworks.append("- **Root Cause Analysis**: Systematic problem investigation")
        
        if len(frameworks) == 0:
            frameworks.append("- **Structured Analysis**: Systematic examination of key components")
            frameworks.append("- **Evidence-Based Reasoning**: Claims supported by credible sources")
        
        return "\n".join(frameworks)

    def _determine_evidence_requirements(self, query_analysis: dict[str, Any]) -> str:
        """Determine evidence and sourcing requirements."""
        complexity = query_analysis.get("complexity", "intermediate")
        
        if complexity == "complex":
            return """- Cite authoritative sources for all factual claims
- Include recent examples or case studies where relevant  
- Acknowledge limitations and uncertainties appropriately
- Reference industry standards or best practices
- Use [ExpertJudgment] tags for professional opinions requiring domain expertise"""
        else:
            return """- Support key claims with evidence or reasoning
- Include relevant examples to illustrate concepts
- Acknowledge areas of uncertainty with appropriate hedging
- Reference credible sources where factual accuracy is critical"""
