# Vector-Based Shared Memory for Multi-Agent Research Systems: A Comprehensive Analysis

This research report explores the potential of using vector representations instead of plain text for shared memory in multi-agent research systems built on LangGraph and CrewAI. While this approach may reduce transparency, it could significantly enhance communication quality and speed among agents with different underlying LLMs and embedding mechanisms.

## The Concept of Shared Memory in Multi-Agent Systems

Shared memory serves as a critical coordination mechanism in multi-agent systems, allowing agents to exchange information and align their actions without direct communication. Traditional approaches often rely on text-based exchanges, but vector-based shared memory offers an alternative paradigm that leverages the semantic richness of embedding spaces.

### Theoretical Foundations

The concept of shared memory in multi-agent systems draws inspiration from cognitive science's Global Workspace Theory, which suggests that independent modules in the brain cooperate by broadcasting information through a global workspace[6]. In computational implementations, this translates to agents acting as independent modules that share information through a common memory space to coordinate their behavior[18].

Shared memory approaches can be categorized into two primary types:
1. **Explicit memory sharing** - where agents deliberately store and retrieve information from a common repository
2. **Implicit memory sharing** - where agents' internal states are automatically pooled and broadcast to enable coordination

The Shared Recurrent Memory Transformer (SRMT) exemplifies this approach by extending memory transformers to multi-agent settings through pooling and globally broadcasting individual working memories[1]. This mechanism enables agents to exchange information implicitly and coordinate their actions without direct communication protocols.

## Vector Representations vs. Plain Text for Shared Memory

### Potential Benefits

Vector-based shared memory offers several advantages over plain text approaches:

**Enhanced Semantic Understanding**: Vector representations can capture semantic relationships more effectively than raw text, potentially enabling more nuanced information exchange between agents[3].

**Improved Efficiency**: Research on vector storage-based memory mechanisms demonstrates significant improvements in decision quality (10-20% increase) and substantial reductions in reasoning costs (approximately 23%)[9].

**Computational Advantages**: Vector representations allow for mathematical operations that can facilitate more complex reasoning and information fusion across agents' contributions[15].

**Reduced Token Consumption**: Vector-based communication could substantially reduce token usage compared to text-based exchanges, which is particularly valuable when working with token-limited LLM APIs[8].

### Potential Drawbacks

Despite these benefits, vector-based approaches present certain challenges:

**Reduced Transparency**: As the user acknowledged, vector-based communication reduces explainability since the semantic content isn't directly human-readable[16].

**Potential Information Loss**: Converting between text and vector representations may result in some information loss, particularly for nuanced concepts[5].

**Implementation Complexity**: Establishing a common embedding space across different LLMs introduces additional technical complexity[15].

## Technical Approaches for Vector-Based Shared Memory

Several frameworks and methodologies have emerged for implementing vector-based shared memory in multi-agent systems:

### G-Designer Framework

The G-Designer approach models multi-agent systems as directed graphs where each agent is a node characterized by its language model, role, state, and available tools[8][14]. It employs Graph Neural Networks (GNNs) and Variational Graph Auto-Encoders (VGAEs) to:

1. Encode agents' features into a latent space
2. Decode an optimized, sparse communication graph tailored to specific tasks
3. Balance utility maximization, communication complexity reduction, and robustness

This framework dynamically adjusts the communication topology based on task requirements, minimizing computational and token overhead while maintaining performance[8].

### Shared Workspace Approach

The Shared Workspace (SW) model synchronizes neural modules through a common workspace where:

1. Different specialists compete to write in the shared workspace
2. All specialists can read from the current state of the workspace
3. The contents of memory slots filter and summarize input information[6]

In this approach, specialists update their states by applying dynamics functions after receiving broadcast information from the workspace, enabling higher-order interactions among neural modules[6].

### Memory-Sharing (MS) Framework

The Memory-Sharing framework utilizes a real-time memory storage and retrieval system to enhance the in-context learning process for LLM-based agents[20]. Each "memory" captures both queries and corresponding real-time responses, aggregating these from multiple agents to enrich the shared memory pool.

## Addressing Cross-Model Compatibility Challenges

The central challenge in implementing vector-based shared memory across different LLMs lies in creating a common embedding representation that works with varied tokenizers and embedding mechanisms.

### Cross-Model Alignment Techniques

Research on cross-model alignment provides promising approaches for addressing this challenge:

**Linear Transformations**: Despite the complexity of neural embedding spaces, simple linear transformations have proven surprisingly effective at aligning representation spaces between different models[15]. The research suggests that diverse models often learn to store information in similar ways, allowing for relatively straightforward alignment methods.

For example, a study on CLIP model embeddings demonstrated that linear layers are remarkably effective at performing feature space alignment, even between models with diverse architectures and training procedures[15].

**Shared Embedding Standards**: For effective cross-system sharing of embeddings, systems must align on:
- Embedding format
- Dimensionality
- Context of training
- Normalization methods (e.g., L2-normalized vs. raw embeddings)
- Tokenization approaches[3]

### Language Grounding for Vector Communication

A novel approach involves aligning the communication space between agents with an embedding space of human natural language by grounding agent communications on synthetic data generated by embodied LLMs[11]. This approach maintains task performance while accelerating the emergence of communication and enabling zero-shot generalization capabilities in ad-hoc teamwork scenarios.

## Implementation Strategies for Research Applications

For implementing vector-based shared memory in your LangGraph and CrewAI multi-agent research system, consider the following strategies:

### Common Vector Space Creation

**Option 1: Unified Embedding Model**
Implement a standalone embedding model (like SentenceBERT or MiniLM) separate from your agents' LLMs to create a standardized embedding space[8]. This approach provides consistency regardless of which LLMs your agents use.

**Option 2: Linear Transformation Hub**
Create a transformation hub that maps each LLM's native embedding space to a common reference space using linear transformations[15]. This requires maintaining transformation matrices for each LLM but allows agents to work in their native embedding spaces.

**Option 3: Task-Specific Virtual Node**
Introduce a task-specific virtual global node that is bidirectionally connected to all agent nodes, enabling a global "storage sink" and facilitating smoother information flow among agents[8]. This node can serve as a central point for aligning different embedding spaces.

### Memory Management Strategies

**Dynamic Memory Updating**
Implement a dynamic memory updating strategy based on the Ebbinghaus forgetting curve theory to efficiently manage agent memory-reinforcing critical information, forgetting unimportant data, and optimizing storage and reasoning costs[9].

**Competition-Based Writing Access**
Use a key-query-value attention mechanism to implement competition between specialists to write into the workspace, where the query is a function of the current workspace memory content, and keys and values come from the specialists[6].

**Temporal Gating Mechanism**
Introduce a temporal gating mechanism for each agent, enabling dynamic decisions on whether to receive shared information at a given time based on current observations, thus improving decision-making efficiency[2].

### Hybrid Transparency Approach

To balance efficiency with explainability:

1. Use vector representations for agent-to-agent communication
2. Maintain a parallel text-based protocol that summarizes key discussions and decisions
3. Implement a translation layer that can convert between vector and text representations when needed for human oversight

## Empirical Evidence on Performance Improvements

Several studies provide evidence supporting the potential benefits of vector-based shared memory:

The Vector Storage based Long-term Memory (VIMBank) research demonstrated that their approach significantly improved the decision quality of LLM intelligences in multi-tasking scenarios by 10-20% and reduced reasoning costs by approximately 23%[9].

The Shared Recurrent Memory Transformer (SRMT) consistently outperformed a range of reinforcement learning baselines on Partially Observable Multi-Agent Pathfinding tasks, especially under sparse rewards[13]. The shared memory approach enhanced coordination in decentralized multi-agent systems and improved generalization to more complex environments than those seen during training.

The G-Designer framework's dynamic communication topology approach reduced token consumption by up to 50% on certain tasks while maintaining or improving performance compared to static communication topologies[8][14].

## Conclusion

Vector-based shared memory represents a promising frontier for enhancing multi-agent research systems built on frameworks like LangGraph and CrewAI. While challenges exist in creating compatible embedding spaces across different LLMs, current research offers several viable approaches through linear transformations, shared embedding standards, and language grounding techniques.

The potential benefits-including improved semantic understanding, reduced token consumption, enhanced computational efficiency, and better decision quality-make this approach worthy of exploration despite the trade-offs in transparency and implementation complexity. By adopting a hybrid approach that maintains text-based summaries alongside vector-based communication, you can leverage the efficiency of vector representations while preserving explainability where needed.

For your specific research application, the integration of a common embedding layer, combined with dynamic memory management strategies and competition-based writing access, could significantly enhance the quality and speed of agent communication while addressing the challenges of working with different LLMs and tokenizers.

Sources
[1] SRMT: Shared Memory for Multi-agent Lifelong Pathfinding - arXiv https://arxiv.org/html/2501.13200v1
[2] Communication Learning in Multi-Agent Systems from Graph ... - arXiv https://arxiv.org/html/2411.00382v1
[3] Can embeddings be shared across systems? - Milvus Blog https://blog.milvus.io/ai-quick-reference/can-embeddings-be-shared-across-systems
[4] Vertex AI Agent Builder | Google Cloud https://cloud.google.com/products/agent-builder
[5] Investigating Approaches for Improving Cross-Modal Alignment in ... https://arxiv.org/html/2406.17639v1
[6] [PDF] Coordination Among Neural Modules Through a Shared Global ... https://arxiv.org/pdf/2103.01197.pdf
[7] AI Agent Memory: A Comparative Analysis of LangGraph, CrewAI ... https://dev.to/foxgem/ai-agent-memory-a-comparative-analysis-of-langgraph-crewai-and-autogen-31dp
[8] G-Designer: Architecting Multi-agent Communication Topologies via ... https://arxiv.org/html/2410.11782v1
[9] Vector Storage Based Long-term Memory Research on LLM - Sciendo https://sciendo.com/article/10.2478/ijanmc-2024-0029
[10] [PDF] Expressive Multi-Agent Communication via Identity-Aware Learning https://ojs.aaai.org/index.php/AAAI/article/view/29683/31167
[11] Language Grounded Multi-agent Reinforcement Learning ... - arXiv https://arxiv.org/abs/2409.17348
[12] How two agents communicate undirectly through a memory sharing ... https://stackoverflow.com/questions/49203279/how-two-agents-communicate-undirectly-through-a-memory-sharing-in-multi-agent-sy
[13] Shared Memory for Multi-agent Lifelong Pathfinding | OpenReview https://openreview.net/forum?id=9DrPvYCETp
[14] The Perfect Communication Protocol for Multi-Agents AI - YouTube https://www.youtube.com/watch?v=UTX8QgOTiv0
[15] [PDF] Text-To-Concept (and Back) via Cross-Model Alignment https://proceedings.mlr.press/v202/moayeri23a/moayeri23a.pdf
[16] "Communication Embeddings and Router to Support LLM-based ... https://www.tdcommons.org/dpubs_series/7395/
[17] How do you handle AI Agent's memory between sessions? - Reddit https://www.reddit.com/r/AI_Agents/comments/1htzozg/how_do_you_handle_ai_agents_memory_between/
[18] [PDF] Shared Recurrent Memory Improves Multi-agent Pathfinding https://openreview.net/pdf/a34b5d219d2632e25428d83b2ded03921af6e0e2.pdf
[19] [PDF] Learning to Infer Belief Embedded Communication - arXiv https://arxiv.org/pdf/2203.07832.pdf
[20] Memory Sharing for Large Language Model based Agents - arXiv https://arxiv.org/html/2404.09982v1
[21] is it possible to place std::vector to shared memory? - Stack Overflow https://stackoverflow.com/questions/5363602/is-it-possible-to-place-stdvector-to-shared-memory
[22] Implementing LangGraph for Multi-Agent AI Systems https://dev.to/jamiu__tijani/implementing-langgraph-for-multi-agent-ai-systems-4fck
[23] How Embeddings Extend Your AI Model's Reach - .NET https://learn.microsoft.com/en-us/dotnet/ai/conceptual/embeddings
[24] A vector-agent approach to (spatiotemporal) movement modelling ... https://www.nature.com/articles/s41598-022-22056-9
[25] SRMT: Shared Memory for Multi-agent Lifelong Pathfinding - YouTube https://www.youtube.com/watch?v=VCAr3zmrGsM
[26] How do multi-agent systems manage communication latency? - Zilliz https://zilliz.com/ai-faq/how-do-multiagent-systems-manage-communication-latency
[27] Embedding | Kernel Memory https://microsoft.github.io/kernel-memory/concepts/embedding
[28] Vectors into the Future of Mass and Interpersonal Communication ... https://pmc.ncbi.nlm.nih.gov/articles/PMC5663313/
[29] What's the best way to handle memory with AI agents? - Reddit https://www.reddit.com/r/AI_Agents/comments/1i2wbp3/whats_the_best_way_to_handle_memory_with_ai_agents/
[30] What is the role of communication in multi-agent systems? - Milvus https://milvus.io/ai-quick-reference/what-is-the-role-of-communication-in-multiagent-systems
[31] Security of AI embeddings explained - IronCore Labs https://ironcorelabs.com/ai-encryption/
[32] Rethinking Communication in an AI-Driven Ecosystem - Artefact https://www.artefact.com/blog/rethinking-communication-in-an-ai-driven-ecosystem/
[33] Mind the Gap: A Generalized Approach for Cross-Modal Embedding ... https://arxiv.org/abs/2410.23437
[34] [PDF] Adaptive Cross-Modal Embeddings for Image-Text Alignment - AAAI https://cdn.aaai.org/ojs/6915/6915-13-10144-1-10-20200525.pdf
[35] Cross-modal distribution alignment embedding network for ... https://www.sciencedirect.com/science/article/abs/pii/S0893608022000077
[36] Global Workspace Theory and System 2 AI - Part Ⅰ - Yuwei Sun https://yuweisunn.github.io/blog-9-01-22.html
[37] VTranM: Vision Transformer Explainability with Vector... - OpenReview https://openreview.net/forum?id=b5LJVjwOsB
[38] Aligning Multilingual Word Embeddings for Cross-Modal Retrieval ... https://aclanthology.org/D19-6402/
[39] [PDF] Identifying Useful Learnwares for Heterogeneous Label Spaces https://proceedings.mlr.press/v202/guo23l/guo23l.pdf
[40] Hands-On Guide to Implementing Multi-Agent Workflows Using ... https://adasci.org/hands-on-guide-to-implementing-multi-agent-workflows-using-llamaindex/
[41] Design and evaluation of a global workspace agent embodied in a ... https://www.frontiersin.org/journals/computational-neuroscience/articles/10.3389/fncom.2024.1352685/full
[42] [PDF] Explainability in Deep Learning by Means of Communication https://publikationen.uni-tuebingen.de/xmlui/bitstream/10900/133334/1/StephanAlaniz_PhD_Thesis.pdf
[43] An Effective Multi-Modal Alignment Method for Cross-Modal Recipe ... https://www.mdpi.com/2304-8158/13/11/1628
[44] Crewai vs. LangGraph: Which multi agent framework should you use? https://www.zams.com/blog/crewai-vs-langgraph
[45] Comparing AI agent frameworks: CrewAI, LangGraph, and BeeAI https://developer.ibm.com/articles/awb-comparing-ai-agent-frameworks-crewai-langgraph-and-beeai
[46] The Perfect Communication Protocol for Multi-Agents AI - YouTube https://www.youtube.com/watch?v=UTX8QgOTiv0
[47] A-Mem: Agentic Memory for LLM Agents - arXiv https://arxiv.org/html/2502.12110v2
[48] How to integrate LangGraph with AutoGen, CrewAI, and other ... https://langchain-ai.github.io/langgraph/how-tos/autogen-integration/
[49] How can I setup memory for my Multi Agent System in Langgraph https://github.com/langchain-ai/langgraph/discussions/1821
[50] Multi-Agent Systems Powered by Large Language Models - arXiv https://arxiv.org/html/2503.03800
[51] LLM Agent Orchestration: A Step by Step Guide - IBM https://www.ibm.com/think/tutorials/LLM-agent-orchestration
[52] Choosing the Right AI Agent Framework: LangGraph vs CrewAI vs ... https://www.relari.ai/blog/ai-agent-framework-comparison-langgraph-crewai-openai-swarm
[53] Hierarchical multi-agent systems with LangGraph - YouTube https://www.youtube.com/watch?v=B_0TNuYi56w
[54] langroid/langroid: Harness LLMs with Multi-Agent Programming https://github.com/langroid/langroid
[55] Long-term Memory for AI Agents - Debmalya's Substack https://debmalyabiswas.substack.com/p/long-term-memory-for-ai-agents
[56] [PDF] Communication Embeddings and Router to Support LLM-based ... https://www.tdcommons.org/cgi/viewcontent.cgi?article=8573&context=dpubs_series
[57] Scalable Communication for Multi-Agent Reinforcement Learning ... https://arxiv.org/html/2301.01919
[58] Targeted multi-agent communication algorithm based on state control https://www.sciencedirect.com/science/article/pii/S2214914722001490
[59] Real World Multi-Agent Reinforcement Learning https://vectorinstitute.ai/real-world-multi-agent-reinforcement-learning-latest-developments-and-applications/
[60] Language Grounded Multi-agent Reinforcement Learning with... https://openreview.net/forum?id=DUHX779C5q
[61] Multi-agent Systems - GitHub Pages https://langchain-ai.github.io/langgraph/concepts/multi_agent/
[62] Communicating Activations Between Language Model Agents https://openreview.net/forum?id=bFYST1MaGh
[63] lastmile-ai/mcp-agent: Build effective agents using Model ... - GitHub https://github.com/lastmile-ai/mcp-agent
[64] NeurIPS Poster Language Grounded Multi-agent Reinforcement ... https://neurips.cc/virtual/2024/poster/96086
[65] [PDF] Learning Non-linguistic Skills without Sacrificing Linguistic Proficiency https://aclanthology.org/2023.acl-long.340.pdf
[66] Understanding Q-vectors in Multi-Agent Reinforcement Learning ... https://www.linkedin.com/pulse/understanding-q-vectors-multi-agent-reinforcement-learning-singh-8mnge
[67] Unlocking AI Transparency & Trust with LLM Observability - LinkedIn https://www.linkedin.com/pulse/enhance-ai-trust-transparency-through-llm-observability-exaqode-p0b0c
[68] [PDF] An Explainable Memory-based Neural Network for Question ... https://aclanthology.org/2020.coling-main.456.pdf
[69] Best 5 Frameworks To Build Multi-Agent AI Applications - GetStream.io https://getstream.io/blog/multiagent-ai-frameworks/
[70] AI Transparency in the Age of LLMs: A Human-Centered Research ... https://hdsr.mitpress.mit.edu/pub/aelql9qy
[71] [PDF] Kelpie: an Explainability Framework for Embedding-based Link ... https://www.vldb.org/pvldb/vol15/p3566-rossi.pdf
[72] [PDF] AI Transparency in the Age of LLMs: A Human-Centered Research ... https://arxiv.org/pdf/2306.01941.pdf
[73] [PDF] Distributional memory explainable word embeddings in continuous ... http://users.dimi.uniud.it/~lauro.snidaro/wordpress/wp-content/uploads/Fusion_2019_Snidaro.pdf
[74] Joint Action Language Modelling for Transparent Policy Execution ... https://arxiv.org/html/2504.10055v1
[75] No Jargon Explanation of Embedding Models with practical use cases https://www.linkedin.com/pulse/jargon-explanation-embedding-models-practical-use-david-jitendranath-mhyfc
[76] Representation Engineering and Control Vectors - Neuroscience for ... https://hlfshell.ai/posts/representation-engineering/
[77] [PDF] Explainable Vector Based Embedding Technique Using Wikipedia http://derekgreene.com/papers/qureshi18eve.pdf
[78] OWASP's Updated Top 10 LLM Includes Vector and Embedding ... https://ironcorelabs.com/blog/2025/owasp-llm-top10-2025-update/
[79] [PDF] Embedding Heterogeneous Networks into Hyperbolic Space ... https://ojs.aaai.org/index.php/AAAI/article/view/17217/17024
[80] Recommendations for Effective Use of Concept Activation Vectors https://arxiv.org/abs/2404.03713
[81] Mitigate the Gap: Improving Cross-Modal Alignment in CLIP https://openreview.net/forum?id=aPTGvFqile
[82] Ensemble Learning for Heterogeneous Large Language Models ... https://openreview.net/forum?id=7arAADUK6D
[83] How can I setup memory for my Multi Agent System in Langgraph https://www.reddit.com/r/LangChain/comments/1fnh7mh/how_can_i_setup_memory_for_my_multi_agent_system/
[84] Exploration of LLM Multi-Agent Application Implementation Based ... https://arxiv.org/abs/2411.18241
[85] LangGraph Uncovered: Building Stateful Multi-Agent Applications ... https://dev.to/sreeni5018/langgraph-uncovered-building-stateful-multi-agent-applications-with-llms-part-i-p86
[86] Agentic AI: A Comparative Analysis of LangGraph and CrewAI https://www.linkedin.com/pulse/agentic-ai-comparative-analysis-langgraph-crewai-hardik-shah-ujdrc
[87] A Long-Term Memory Agent | 🦜️   LangChain https://python.langchain.com/docs/versions/migrating_memory/long_term_memory_agent/
[88] Multi Agent LLM Systems: GenAI Special Forces - K2view https://www.k2view.com/blog/multi-agent-llm/
[89] LLM Agents: Multi-Agent Chats with Autogen - DEV Community https://dev.to/admantium/llm-agents-multi-agent-chats-with-autogen-2j26
[90] [PDF] Situated Conversational Agents - AAAI https://cdn.aaai.org/AAAI/2007/AAAI07-329.pdf
[91] Implementing a Multi-Agent Knowledge System using Langraph and ... https://www.linkedin.com/pulse/implementing-multi-agent-knowledge-system-using-db-henry-potsangbam-qq7zc
[92] LM Transparency Tool: Interactive Tool for Analyzing Transformer ... https://ai.meta.com/research/publications/lm-transparency-tool-interactive-tool-for-analyzing-transformer-language-models/
[93] A Case Study of Static Redundant NVM Memory Write Prediction https://arxiv.org/html/2403.04337v1
