# Catálogo de agentes e skills

## Fontes (verificadas em 2026-11-09)

| fonte | tipo | estrelas GitHub | licença | commit | o que veio |
|---|---|---|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | oficial Anthropic | ~190 mil | Apache-2.0 (LICENSE.txt dentro de cada skill) | 2c5958e | 13 skills |
| [wshobson/agents](https://github.com/wshobson/agents) | comunidade | ~42 mil | MIT | 9c61ab2 | 29 skills |
| [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | comunidade | ~26 mil | MIT | ed74d11 | 69 agentes |
| [OpenAEC-Foundation/Three.js-Claude-Skill-Package](https://github.com/OpenAEC-Foundation/Three.js-Claude-Skill-Package) | fundação AEC (arquitetura/engenharia/construção) | ~29 | MIT | 6c190f0 | 24 skills de Three.js (poucas estrelas, mas é a fonte mais completa e específica para 3D web; conteúdo revisado) |
| este repositório | escritos para o projeto | — | mesmo do repo | — | 14 agentes + 10 skills de engenharia de pontes (solver testado) |

Não existe hoje uma fonte de alta reputação com agentes de engenharia estrutural/pontes; por isso esses foram escritos aqui, com o cálculo validado à mão.

Avaliadas e **não copiadas**: `anthropics/skills/doc-coauthoring` e `andreahaku/openscad_claude_skill` (sem arquivo de licença); registros como claudskills.com e skills.sh (agregadores, sem garantia de origem).

## Agentes (83)

 | agente | origem | quando usar |
|---|---|---|
| `accessibility-tester` | VoltAgent | Use this agent when you need comprehensive accessibility testing, WCAG compliance verification, or assessment of assistive technology support. |
| `agent-organizer` | VoltAgent | Use when you need to break a complex task into subtasks, match each to the capabilities of available subagents, and write a concrete team/workflow plan as Markdown. |
| `ai-engineer` | VoltAgent | Use this agent when architecting, implementing, or optimizing end-to-end AI systems—from model selection and training pipelines to production deployment and monitoring. |
| `analista-de-trelicas` | projeto | Use para calcular esforços em treliças planas ou espaciais (método dos nós, das seções ou rigidez direta), reações de apoio e deslocamentos. |
| `analista-fea` | projeto | Use para análises por elementos finitos (pórtico/treliça 3D, modal, flambagem linear) quando o cálculo de treliça ideal não for suficiente, por exemplo com ligações rígid… |
| `api-designer` | VoltAgent | Use this agent when designing new APIs, creating API specifications, or refactoring existing API architecture for scalability and developer experience. Invoke when you ne… |
| `api-documenter` | VoltAgent | Use this agent when creating or improving API documentation, writing OpenAPI specifications, building interactive documentation portals, or generating code examples for A… |
| `architect-reviewer` | VoltAgent | Use this agent when you need to evaluate system design decisions, architectural patterns, and technology choices at the macro level. |
| `backend-developer` | VoltAgent | Use this agent when building server-side APIs, microservices, and backend systems that require robust architecture, scalability planning, and production-ready implementat… |
| `build-engineer` | VoltAgent | Use this agent when you need to optimize build performance, reduce compilation times, or scale build systems across growing teams. |
| `cloud-architect` | VoltAgent | Use this agent when you need to design, evaluate, or optimize cloud infrastructure architecture at scale. Invoke when designing multi-cloud strategies, planning cloud mig… |
| `code-reviewer` | VoltAgent | Use this agent when you need to conduct comprehensive code reviews focusing on code quality, security vulnerabilities, and best practices. |
| `competitive-analyst` | VoltAgent | Use when you need to analyze direct and indirect competitors, benchmark against market leaders, or develop strategies to strengthen competitive positioning and market adv… |
| `content-marketer` | VoltAgent | Use this agent when you need to develop comprehensive content strategies, create SEO-optimized marketing content, or execute multi-channel content campaigns to drive enga… |
| `context-manager` | VoltAgent | Use to organize the shared context and state that a multi-agent workflow keeps in files — deciding directory/file structure, naming conventions, what goes where, and how … |
| `cpp-pro` | VoltAgent | Use this agent when building high-performance C++ systems requiring modern C++20/23 features, template metaprogramming, or zero-overhead abstractions for systems programm… |
| `data-analyst` | VoltAgent | Use when you need to extract insights from business data, create dashboards and reports, or perform statistical analysis to support decision-making. |
| `data-engineer` | VoltAgent | Use this agent when you need to design, build, or optimize data pipelines, ETL/ELT processes, and data infrastructure. Invoke when designing data platforms, implementing … |
| `data-researcher` | VoltAgent | Use this agent when you need to discover, collect, and validate data from multiple sources to fuel analysis and decision-making. Invoke this agent for identifying data so… |
| `data-scientist` | VoltAgent | Use this agent when you need to analyze data patterns, build predictive models, or extract statistical insights from datasets. Invoke this agent for exploratory analysis,… |
| `debugger` | VoltAgent | Use this agent when you need to diagnose and fix bugs, identify root causes of failures, or analyze error logs and stack traces to resolve issues. |
| `dependency-manager` | VoltAgent | Use this agent when you need to audit dependencies for vulnerabilities, resolve version conflicts, optimize bundle sizes, or implement automated dependency updates. |
| `deployment-engineer` | VoltAgent | Use this agent when designing, building, or optimizing CI/CD pipelines and deployment automation strategies. |
| `desenhista-tecnico` | projeto | Use para produzir desenhos técnicos da ponte: vistas, cotas, lista de barras/materiais, numeração de nós e gabaritos de montagem em escala. |
| `design-bridge` | VoltAgent | Use this agent when you need to translate a DESIGN.md from the VoltAgent/awesome-design-md repository into polished Claude Code instructions for building user interfaces … |
| `devops-engineer` | VoltAgent | Use this agent when building or optimizing infrastructure automation, CI/CD pipelines, containerization strategies, and deployment workflows to accelerate software delive… |
| `docker-expert` | VoltAgent | Use this agent when you need to build, optimize, or secure Docker container images and orchestration for production environments. |
| `documentation-engineer` | VoltAgent | Use this agent when you need to create, architect, or overhaul comprehensive documentation systems including API docs, tutorials, guides, and developer-friendly content t… |
| `embedded-systems` | VoltAgent | Use when developing firmware for resource-constrained microcontrollers, implementing RTOS-based applications, or optimizing real-time systems where hardware constraints, … |
| `engenheiro-estrutural` | projeto | Use para qualquer decisão estrutural da ponte: escolha de sistema (treliça Pratt, Warren, Howe, arco), caminhos de carga, apoios, verificação de esforços e coeficientes d… |
| `error-detective` | VoltAgent | Use this agent when you need to diagnose why errors are occurring in your system, correlate errors across services, identify root causes, and prevent future failures. |
| `especialista-materiais-madeira` | projeto | Use para questões sobre propriedades de palitos de madeira, colas (PVA, epóxi, cianoacrilato), umidade, variabilidade e ensaios de caracterização de material. |
| `fastapi-developer` | VoltAgent | Use when building modern async Python APIs with FastAPI, implementing Pydantic v2 validation, dependency injection patterns, or deploying high-performance ASGI applicatio… |
| `first-principles-thinking` | VoltAgent | Use when the user wants to challenge assumptions, break down a complex problem from scratch, or approach something with first principles reasoning. Triggers on: 'first pr… |
| `frontend-developer` | VoltAgent | Use when building complete frontend applications across React, Vue, and Angular frameworks requiring multi-framework expertise and full-stack integration. |
| `fullstack-developer` | VoltAgent | Use this agent when you need to build complete features spanning database, API, and frontend layers together as a cohesive unit. |
| `game-developer` | VoltAgent | Use this agent when implementing game systems, optimizing graphics rendering, building multiplayer networking, or developing gameplay mechanics for games targeting specif… |
| `git-workflow-manager` | VoltAgent | Use this agent when you need to design, establish, or optimize Git workflows, branching strategies, and merge management for a project or team. |
| `iot-engineer` | VoltAgent | Use when designing and deploying IoT solutions requiring expertise in device management, edge computing, cloud integration, and handling challenges like massive device sc… |
| `javascript-pro` | VoltAgent | Use this agent when you need to build, optimize, or refactor modern JavaScript code for browser, Node.js, or full-stack applications requiring ES2023+ features, async pat… |
| `knowledge-synthesizer` | VoltAgent | Use when you need to mine recurring patterns from agent logs, session transcripts, and workflow history, then write grounded, evidence-cited findings that other agents or… |
| `landing-page-copywriter` | VoltAgent | Use this agent when writing or optimizing landing page copy, hero sections, CTAs, or conversion-focused funnel content for a specific audience and offer. |
| `machine-learning-engineer` | VoltAgent | Use this agent when you need to deploy, optimize, or serve machine learning models at scale in production environments. |
| `mobile-developer` | VoltAgent | Use this agent when building cross-platform mobile applications requiring native performance optimization, platform-specific features, and offline-first architecture. Use… |
| `modelador-3d-cad` | projeto | Use para criar modelos 3D paramétricos da ponte em OpenSCAD, CadQuery/build123d ou FreeCAD, e exportar STL/STEP/DXF para impressão, gabaritos de montagem ou desenhos. |
| `motion-director` | VoltAgent | Use this agent when directing, scripting, and rendering launch-quality 2D/3D motion films, UI walkthroughs, kinetic typography posters, or physics simulations in code wit… |
| `multi-agent-coordinator` | VoltAgent | Use when you need to plan how multiple concurrent subagents should communicate, sequence their work, share state through files, and handle failures — written up as a coor… |
| `nextjs-developer` | VoltAgent | Use this agent when building production Next.js 14+ applications that require full-stack development with App Router, server components, and advanced performance optimiza… |
| `node-specialist` | VoltAgent | Use this agent when you need to build, optimize, or debug Node.js backend applications, APIs, CLIs, or microservices requiring deep ecosystem knowledge and server-side Ja… |
| `otimizador-estrutural` | projeto | Use para otimizar a ponte em eficiência carga/peso: dimensionamento de seções, altura da treliça, número de painéis e redistribuição de material entre barras. |
| `performance-engineer` | VoltAgent | Use this agent when you need to identify and eliminate performance bottlenecks in applications, databases, or infrastructure systems, and when baseline performance metric… |
| `pesquisador-normas-tecnicas` | projeto | Use para pesquisar normas técnicas (ABNT, Eurocode, AASHTO), regulamentos de competições de pontes de palito e literatura científica confiável sobre estruturas e madeira. |
| `planejador-construcao` | projeto | Use para planejar a construção física da ponte: lista de materiais, quantidade de palitos e cola, sequência de montagem, gabaritos, tempos de cura e cronograma da equipe. |
| `planejador-ensaio-de-carga` | projeto | Use para planejar e registrar o ensaio de carga destrutivo ou de prova da ponte: aplicação de carga, instrumentação, segurança e registro de dados. |
| `product-manager` | VoltAgent | Use this agent when you need to make product strategy decisions, prioritize features, or define roadmap plans based on user needs and business goals. |
| `project-manager` | VoltAgent | Use this agent when you need to establish project plans, track execution progress, manage risks, control budget/schedule, and coordinate stakeholders across complex initi… |
| `projetista-de-pontes` | projeto | Use para conceber a geometria da ponte de palito: vão, altura da treliça, número de painéis, tabuleiro, contraventamento e encaixe nos apoios do ensaio. |
| `prompt-engineer` | VoltAgent | Use this agent when you need to design, optimize, test, or evaluate prompts for large language models in production systems. |
| `python-pro` | VoltAgent | Use this agent when you need to build type-safe, production-ready Python code for web APIs, system utilities, or complex applications requiring modern async patterns and … |
| `qa-expert` | VoltAgent | Use this agent when you need comprehensive quality assurance strategy, test planning across the entire development cycle, or quality metrics analysis to improve overall s… |
| `react-specialist` | VoltAgent | Use when optimizing existing React applications for performance, implementing advanced React 18+ features, or solving complex state management and architectural challenge… |
| `readme-generator` | VoltAgent | Use this agent when you need a maintainer-ready README built from exact repository reality, with deep codebase scanning, zero hallucination, and optional git commit/push … |
| `redator-relatorio-tecnico` | projeto | Use para redigir o relatório técnico/memorial de cálculo da ponte no padrão acadêmico (ABNT NBR 14724), com introdução, metodologia, cálculos, ensaio, resultados e conclu… |
| `refactoring-specialist` | VoltAgent | Use when you need to transform poorly structured, complex, or duplicated code into clean, maintainable systems while preserving all existing behavior. |
| `research-analyst` | VoltAgent | Use this agent when you need comprehensive research across multiple sources with synthesis of findings into actionable insights, trend identification, and detailed report… |
| `revisor-seguranca-estrutural` | projeto | Use para revisar de forma independente cálculos e projetos estruturais antes de construir: confere hipóteses, unidades, equilíbrio, flambagem e fatores de segurança. |
| `scientific-literature-researcher` | VoltAgent | Use when you need to search scientific literature and retrieve structured experimental data from published studies. Invoke this agent when the task requires evidence-grou… |
| `search-specialist` | VoltAgent | Use when you need to find specific information across multiple sources using advanced search strategies, query optimization, and targeted information retrieval. Invoke th… |
| `security-auditor` | VoltAgent | Use this agent when conducting comprehensive security audits, compliance assessments, or risk evaluations across systems, infrastructure, and processes. Invoke when you n… |
| `seo-specialist` | VoltAgent | Use this agent when you need comprehensive SEO optimization encompassing technical audits, keyword strategy, content optimization, and search rankings improvement. |
| `sql-pro` | VoltAgent | Use this agent when you need to optimize complex SQL queries, design efficient database schemas, or solve performance issues across PostgreSQL, MySQL, SQL Server, and Ora… |
| `task-distributor` | VoltAgent | Use when you need to design and document a task-distribution strategy across multiple agents or workers — how to split work, order queues, respect priorities and deadline… |
| `technical-writer` | VoltAgent | Use this agent when you need to create, improve, or maintain technical documentation including API references, user guides, SDK documentation, and getting-started guides. |
| `test-automator` | VoltAgent | Use this agent when you need to build, implement, or enhance automated test frameworks, create test scripts, or integrate testing into CI/CD pipelines. |
| `typescript-pro` | VoltAgent | Use when implementing TypeScript code requiring advanced type system patterns, complex generics, type-level programming, or end-to-end type safety across full-stack appli… |
| `ui-designer` | VoltAgent | Use this agent when designing visual interfaces, creating design systems, building component libraries, or refining user-facing aesthetics requiring expert visual design,… |
| `ui-ux-tester` | VoltAgent | Use this agent when you need exhaustive UI and UX functionality testing driven by documented user flows, with browser or desktop interaction tooling and structured defect… |
| `ux-microcopy-reviewer` | VoltAgent | Use this agent after changing user-facing interface text (buttons, error messages, empty states, form labels, confirmations, toasts) to review it for clarity, consistency… |
| `ux-researcher` | VoltAgent | Use this agent when you need to conduct user research, analyze user behavior, or generate actionable insights to validate design decisions and uncover user needs. Invoke … |
| `visual-asset-generator` | VoltAgent | Use this agent when you need to generate production-ready visual assets for a project — app icons, favicons, OG images, logos, wordmarks, or social media images. Invokes … |
| `visualizador-3d-web` | projeto | Use para construir visualizações 3D interativas da ponte no navegador com Three.js: modelo, cores por esforço (tração/compressão), animação de deformada e controles de câ… |
| `vue-expert` | VoltAgent | Use this agent when building Vue 3 applications that require Composition API mastery, reactivity optimization, or Nuxt 3 development with enterprise-scale performance con… |
| `workflow-orchestrator` | VoltAgent | Use when you need to design workflow and state-machine definitions — states, transitions, error handling, and compensation/rollback logic — and write them as specs or con… |

## Skills (76)

| skill | origem | quando usar |
|---|---|---|
| `accessibility-compliance` | wshobson | Implement WCAG 2.2 compliant interfaces with mobile accessibility, inclusive design patterns, and assistive technology support. Use when auditing accessibility, implement… |
| `algorithmic-art` | Anthropic | Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request creating art using code, generative art, al… |
| `analise-trelica` | projeto | Calcula esforços axiais, reações e deslocamentos de treliças 2D/3D (ponte de palito, treliça Pratt, Warren, Howe) pelo método da rigidez direta. Use sempre que precisar d… |
| `architecture-decision-records` | wshobson | Write and maintain Architecture Decision Records (ADRs) following best practices for technical decision documentation. Use when documenting significant technical decision… |
| `brand-guidelines` | Anthropic | Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and-feel. Use it when brand colors or style… |
| `brand-landingpage` | wshobson | Brand-first landing page designer — runs a brand-identity interview (colors, typography, shape language), then generates and iterates on a polished landing page via Stitc… |
| `canvas-design` | Anthropic | Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to create a poster, piece of art, design, or … |
| `changelog-automation` | wshobson | Automate changelog generation from commits, PRs, and releases following Keep a Changelog format. Use when setting up release workflows, generating release notes, or stand… |
| `code-review-excellence` | wshobson | Master effective code review practices to provide constructive feedback, catch bugs early, and foster knowledge sharing while maintaining team morale. Use when reviewing … |
| `data-storytelling` | wshobson | Transform data into compelling narratives using visualization, context, and persuasive structure. Use when presenting analytics to stakeholders, creating data reports, or… |
| `debugging-strategies` | wshobson | Master systematic debugging techniques, profiling tools, and root cause analysis to efficiently track down bugs across any codebase or technology stack. Use when investig… |
| `design-system-patterns` | wshobson | Build scalable design systems with design tokens, theming infrastructure, and component architecture patterns. Use when creating design tokens, implementing theme switchi… |
| `dimensionamento-barras-palito` | projeto | Fluxo completo para dimensionar cada barra da ponte de palito (número de palitos por barra) a partir dos esforços da treliça, verificando tração, compressão/flambagem e l… |
| `docx` | Anthropic | Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files) or Word templates (.dotx files). Triggers include: any mention of… |
| `e2e-testing-patterns` | wshobson | Master end-to-end testing with Playwright and Cypress to build reliable test suites that catch bugs, improve confidence, and enable fast deployment. Use when implementing… |
| `ensaio-de-carga` | projeto | Protocolo para ensaio de carga de modelos de ponte (prova ou ruptura): montagem, aplicação gradual da carga, medição de deslocamento, segurança, registro em CSV e análise… |
| `flambagem-euler` | projeto | Verifica barras comprimidas de palito/madeira quanto à flambagem de Euler (eixos fraco e forte) e ao esmagamento, e calcula o fator de segurança. Use para toda barra com … |
| `frontend-design` | Anthropic | Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps with aesthetic direction, typography, and making choices that… |
| `git-advanced-workflows` | wshobson | Master advanced Git workflows including rebasing, cherry-picking, bisect, worktrees, and reflog to maintain clean history and recover from any situation. Use when managin… |
| `github-actions-templates` | wshobson | Create production-ready GitHub Actions workflows for automated testing, building, and deploying applications. Use when setting up CI/CD with GitHub Actions, automating de… |
| `interaction-design` | wshobson | Design and implement microinteractions, motion design, transitions, and user feedback patterns. Use when adding polish to UI interactions, implementing loading states, or… |
| `javascript-testing-patterns` | wshobson | Implement comprehensive testing strategies using Jest, Vitest, and Testing Library for unit tests, integration tests, and end-to-end testing with mocking, fixtures, and t… |
| `kpi-dashboard-design` | wshobson | Design effective KPI dashboards with metrics selection, visualization best practices, and real-time monitoring patterns. Use this skill when building an executive SaaS me… |
| `mcp-builder` | Anthropic | Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MC… |
| `modern-javascript-patterns` | wshobson | Master ES6+ features including async/await, destructuring, spread operators, arrow functions, promises, modules, iterators, generators, and functional programming pattern… |
| `nextjs-app-router-patterns` | wshobson | Master Next.js 14+ App Router with Server Components, streaming, parallel routes, and advanced data fetching. Use when building Next.js applications, implementing SSR/SSG… |
| `nodejs-backend-patterns` | wshobson | Build production-ready Node.js backend services with Express/Fastify, implementing middleware patterns, error handling, authentication, database integration, and API desi… |
| `openscad-ponte` | projeto | Gera modelo 3D paramétrico da ponte em OpenSCAD a partir do JSON de nós e barras da skill analise-trelica, para visualizar, exportar STL (impressão 3D de gabaritos/maquet… |
| `pdf` | Anthropic | Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into o… |
| `ponte-3d-threejs` | projeto | Gera uma página HTML interativa com o modelo 3D da ponte em Three.js, com barras coloridas por esforço (tração azul, compressão vermelho) e clique para ver o valor. Use p… |
| `pptx` | Anthropic | Use this skill any time a .pptx or .potx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; read… |
| `propriedades-palito-madeira` | projeto | Referência e protocolo para obter propriedades mecânicas de palitos de madeira e colas (E, resistência à tração e compressão, densidade, resistência da colagem). Use ante… |
| `python-design-patterns` | wshobson | Python design patterns including KISS, Separation of Concerns, Single Responsibility, and composition over inheritance. Use this skill when designing a new service or com… |
| `python-performance-optimization` | wshobson | Profile and optimize Python code using cProfile, memory profilers, and performance best practices. Use when debugging slow Python code, optimizing bottlenecks, or improvi… |
| `python-project-structure` | wshobson | Python project organization, module architecture, and public API design. Use when setting up new projects, organizing modules, defining public interfaces with __all__, or… |
| `python-testing-patterns` | wshobson | Implement comprehensive testing strategies with pytest, fixtures, mocking, and test-driven development. Use when writing Python tests, setting up test suites, or implemen… |
| `react-state-management` | wshobson | Master modern React state management with Redux Toolkit, Zustand, Jotai, and React Query. Use when setting up global state, managing server state, or choosing between sta… |
| `registro-de-erros` | projeto | Como ler e atualizar o arquivo ERROS.md do repositório, que guarda erros já cometidos por Claude e pela equipe para não repeti-los. Use no início de cada tarefa e sempre … |
| `regras-competicao-ponte-palito` | projeto | Checklist para interpretar e cumprir o regulamento de uma competição de ponte de palito (vão, massa, materiais, cola, ponto de carga, critério de pontuação). Use no iníci… |
| `relatorio-tecnico-engenharia` | projeto | Modelo e regras para escrever relatório técnico / memorial de cálculo de engenharia em português no padrão ABNT (NBR 14724, NBR 6023, NBR 10520). Use para relatórios da p… |
| `responsive-design` | wshobson | Implement modern responsive layouts using container queries, fluid typography, CSS Grid, and mobile-first breakpoint strategies. Use when building adaptive interfaces, im… |
| `screen-reader-testing` | wshobson | Test web applications with screen readers including VoiceOver, NVDA, and JAWS. Use when validating screen reader compatibility, debugging accessibility issues, or ensurin… |
| `skill-creator` | Anthropic | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing sk… |
| `tailwind-design-system` | wshobson | Build scalable design systems with Tailwind CSS v4, design tokens, component libraries, and responsive patterns. Use when creating component libraries, implementing desig… |
| `theme-factory` | Anthropic | Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing pages, etc. There are 10 pre-set themes with colors/fonts that y… |
| `threejs-agents-model-optimizer` | OpenAEC | Use when optimizing 3D models for web delivery: reducing file size, compressing meshes, optimizing textures, or generating LOD. Provides a complete GLTF optimization pipe… |
| `threejs-agents-scene-builder` | OpenAEC | Use when composing a complete Three.js scene from scratch or when asked to create a 3D visualization. Provides decision trees for choosing lighting setup, materials, came… |
| `threejs-core-math` | OpenAEC | Use when working with 3D math in Three.js: vectors, matrices, quaternions, rotations, colors, or coordinate transforms. Prevents the common mistake of mutating shared vec… |
| `threejs-core-raycaster` | OpenAEC | Use when implementing mouse picking, hover detection, object selection, or line-of-sight checks in Three.js. Prevents the common mistake of raycasting every mousemove fra… |
| `threejs-core-renderer` | OpenAEC | Use when initializing a Three.js renderer, setting up the render loop, handling window resize, configuring tone mapping, or managing color spaces. Prevents the common mis… |
| `threejs-core-scene-graph` | OpenAEC | Use when creating Three.js scenes, adding objects, managing parent-child hierarchies, or organizing 3D content. Prevents the common mistake of using add() instead of atta… |
| `threejs-errors-performance` | OpenAEC | Use when a Three.js scene has performance problems: low FPS, memory leaks, too many draw calls, or high GPU memory usage. Prevents the common mistake of forgetting dispos… |
| `threejs-errors-rendering` | OpenAEC | Use when a Three.js scene renders incorrectly: black screen, invisible objects, wrong colors, z-fighting, or broken shadows. Prevents the common mistake of wrong color sp… |
| `threejs-impl-animation` | OpenAEC | Use when playing animations, crossfading between animation states, or loading skeletal animations from GLTF in Three.js. Prevents the common mistake of not calling mixer.… |
| `threejs-impl-audio` | OpenAEC | Use when adding sound to a Three.js scene: background music, 3D spatial audio, or audio visualization. Prevents the common mistake of ignoring browser autoplay policy, no… |
| `threejs-impl-drei` | OpenAEC | Use when using Drei helper components with React Three Fiber: controls, environment maps, text rendering, HTML overlays, or performance helpers. Prevents the common mista… |
| `threejs-impl-ifc-viewer` | OpenAEC | Use when loading and viewing IFC/BIM models in a Three.js scene. Prevents the common mistake of using deprecated web-ifc-three, ignoring AGPL-3.0 license implications, or… |
| `threejs-impl-lighting` | OpenAEC | Use when setting up lighting in a Three.js scene: ambient, directional, point, spot, area, or environment lighting. Prevents the common mistake of too many shadow-casting… |
| `threejs-impl-physics` | OpenAEC | Use when adding physics simulation to a Three.js scene: rigid bodies, collisions, constraints, or raycasting. Prevents the common mistake of wrong Vec3/Vector3 conversion… |
| `threejs-impl-post-processing` | OpenAEC | Use when adding post-processing effects like bloom, SSAO, depth of field, or anti-aliasing to a Three.js scene. Prevents the common mistake of mixing Three.js EffectCompo… |
| `threejs-impl-react-three-fiber` | OpenAEC | Use when building 3D scenes with React using React Three Fiber (R3F). Prevents the common mistake of mixing imperative Three.js code with R3F's declarative model, creatin… |
| `threejs-impl-shadows` | OpenAEC | Use when enabling shadows in a Three.js scene or debugging shadow artifacts like acne, peter panning, or low resolution. Prevents the common mistake of wrong shadow camer… |
| `threejs-impl-webgpu` | OpenAEC | Use when using the Three.js WebGPU renderer, node-based materials, TSL (Three Shading Language), or compute shaders. Prevents the common mistake of not checking browser s… |
| `threejs-impl-xr` | OpenAEC | Use when building VR or AR experiences with Three.js using WebXR. Prevents the common mistake of using requestAnimationFrame instead of setAnimationLoop, not handling con… |
| `threejs-syntax-controls` | OpenAEC | Use when adding camera controls to a Three.js scene: orbit, pan, zoom, fly, first-person, or object manipulation. Prevents the common mistake of forgetting controls.updat… |
| `threejs-syntax-geometries` | OpenAEC | Use when creating 3D shapes, custom geometry, or instanced meshes in Three.js. Prevents the common mistake of forgetting dispose(), not setting needsUpdate on BufferAttri… |
| `threejs-syntax-loaders` | OpenAEC | Use when loading 3D models (GLTF, FBX, OBJ), textures, or HDR environment maps in Three.js. Prevents the common mistake of not setting up DRACOLoader, wrong WASM path, or… |
| `threejs-syntax-materials` | OpenAEC | Use when choosing or configuring materials, loading textures, or setting up PBR workflows in Three.js. Prevents the common mistake of wrong color space on textures, forge… |
| `threejs-syntax-shaders` | OpenAEC | Use when writing custom GLSL shaders, creating ShaderMaterial or RawShaderMaterial, defining uniforms, or patching built-in materials with onBeforeCompile. Prevents the c… |
| `typescript-advanced-types` | wshobson | Master TypeScript's advanced type system including generics, conditional types, mapped types, template literals, and utility types for building type-safe applications. Us… |
| `visual-design-foundations` | wshobson | Apply typography, color theory, spacing systems, and iconography principles to create cohesive visual designs. Use when establishing design tokens, building style guides,… |
| `wcag-audit-patterns` | wshobson | Conduct WCAG 2.2 accessibility audits with automated testing, manual verification, and remediation guidance. Use when auditing websites for accessibility, fixing WCAG vio… |
| `web-artifacts-builder` | Anthropic | Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui). Use for complex a… |
| `web-component-design` | wshobson | Master React, Vue, and Svelte component patterns including CSS-in-JS, composition strategies, and reusable component architecture. Use when building UI component librarie… |
| `webapp-testing` | Anthropic | Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser scre… |
| `xlsx` | Anthropic | Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm,… |
