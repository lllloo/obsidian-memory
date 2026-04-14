---
title: "Introducing dotLLM - Building an LLM Inference Engine in C# | Konrad 'Dev Nerd' Kokosa"
source: "https://kokosa.dev/blog/2026/dotllm/?fbclid=IwY2xjawRLLvdleHRuA2FlbQIxMQBzcnRjBmFwcF9pZBAyMjIwMzkxNzg4MjAwODkyAAEeXCuZQBxcUU_wur9DtqEMStHUx-nBlz8IrTn8Q6deHI7gVtHG_h8_mLnCEbg_aem_SKphMi8AQQUVaYE82NEURg"
author:
  - "[[Konrad Kokosa]]"
published: 2026-04-14
created: 2026-04-14
description: "How I built a ground-up LLM inference engine in .NET 10, and what I learned about AI-assisted (not vibe-coded) development along the way."
tags:
  - "clippings"
---
![](https://kokosa.dev/assets/img/dotllm-hero.gif)

If you’ve been building.NET applications and wanted to run LLMs locally, your options have been… limited. You could wrap [llama.cpp](https://github.com/ggml-org/llama.cpp) through [LLamaSharp](https://github.com/SciSharp/LLamaSharp), deal with [ONNX Runtime](https://onnxruntime.ai/docs/get-started/with-csharp.html), or orchestrate calls to external Python services. None of these are fully satisfying if you want to run LLM inference purely in.NET.

So I built my own.

Over the past two months I’ve been building [dotLLM](https://dotllm.dev/) - a ground-up, high-performance LLM inference engine written natively in C#/.NET 10. Not a wrapper. Not bindings. A full implementation: GGUF model loading, tokenization, attention, sampling, SIMD-optimized CPU inference, CUDA GPU acceleration, an OpenAI-compatible API server, and a built-in chat UI. This week I’ve published the [first preview release](https://github.com/kkokosa/dotLLM/releases) (v0.1.0-preview.2).

This post covers three things: **what** dotLLM is, **why** I built it, and **how** AI-assisted development - Claude Code, Codex, and Gemini working together in a structured workflow - made it possible for a single developer to ship this in about two months.

## What is dotLLM?

### The short version

dotLLM is a native C#/.NET 10 LLM inference engine. It runs transformer-based models - Llama, Mistral, Phi, Qwen (and more in future) - from GGUF files, with SIMD-optimized CPU, CUDA GPU backend, or hybrid/offloading mode. It exposes an OpenAI-compatible API, ships as a CLI tool and as NuGet packages you can embed in your own applications.

The key word is **native**. All orchestration, model loading, tokenization, sampling, scheduling, and CPU compute is implemented in pure C#. The only native code is a thin CUDA library for GPU kernels, loaded via PTX through the CUDA Driver API (P/Invoked).

### Architecture

dotLLM is organized as a layered architecture where each layer depends only on the layers below:

```
graph TD
    subgraph "User-Facing"
        CLI["DotLLM.Cli<br/><small>CLI tool</small>"]
        ChatUI["Built-in Chat UI<br/><small>Browser-based</small>"]
        Server["DotLLM.Server<br/><small>OpenAI-compatible API</small>"]
    end

    subgraph "Engine"
        Eng["DotLLM.Engine<br/><small>KV-cache, scheduler, samplers,<br/>constraints, speculative decoding</small>"]
    end

    subgraph "Model Layer"
        Models["DotLLM.Models<br/><small>GGUF loader, Llama, Mistral,<br/>Phi, Qwen, DeepSeek</small>"]
        Tokenizers["DotLLM.Tokenizers<br/><small>BPE, SentencePiece,<br/>Jinja2 chat templates</small>"]
    end

    subgraph "Compute"
        CPU["DotLLM.Cpu<br/><small>SIMD / AVX2 / AVX-512</small>"]
        CUDA["DotLLM.Cuda<br/><small>PTX kernels, cuBLAS</small>"]
    end

    Core["DotLLM.Core<br/><small>ITensor, IBackend, IModel,<br/>ISamplerStep, IDecodingConstraint</small>"]

    CLI --> Server
    ChatUI --> Server
    Server --> Eng
    CLI --> Eng
    Eng --> Models
    Eng --> Tokenizers
    Models --> CPU
    Models --> CUDA
    CPU --> Core
    CUDA --> Core
    Models --> Core
    Tokenizers --> Core
    Eng --> Core
```
```
#mermaid-1776177175170{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#ccc;}#mermaid-1776177175170 .error-icon{fill:#a44141;}#mermaid-1776177175170 .error-text{fill:#ddd;stroke:#ddd;}#mermaid-1776177175170 .edge-thickness-normal{stroke-width:2px;}#mermaid-1776177175170 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-1776177175170 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-1776177175170 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-1776177175170 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-1776177175170 .marker{fill:lightgrey;stroke:lightgrey;}#mermaid-1776177175170 .marker.cross{stroke:lightgrey;}#mermaid-1776177175170 svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#mermaid-1776177175170 .label{font-family:"trebuchet ms",verdana,arial,sans-serif;color:#ccc;}#mermaid-1776177175170 .cluster-label text{fill:#F9FFFE;}#mermaid-1776177175170 .cluster-label span,#mermaid-1776177175170 p{color:#F9FFFE;}#mermaid-1776177175170 .label text,#mermaid-1776177175170 span,#mermaid-1776177175170 p{fill:#ccc;color:#ccc;}#mermaid-1776177175170 .node rect,#mermaid-1776177175170 .node circle,#mermaid-1776177175170 .node ellipse,#mermaid-1776177175170 .node polygon,#mermaid-1776177175170 .node path{fill:#1f2020;stroke:#81B1DB;stroke-width:1px;}#mermaid-1776177175170 .flowchart-label text{text-anchor:middle;}#mermaid-1776177175170 .node .label{text-align:center;}#mermaid-1776177175170 .node.clickable{cursor:pointer;}#mermaid-1776177175170 .arrowheadPath{fill:lightgrey;}#mermaid-1776177175170 .edgePath .path{stroke:lightgrey;stroke-width:2.0px;}#mermaid-1776177175170 .flowchart-link{stroke:lightgrey;fill:none;}#mermaid-1776177175170 .edgeLabel{background-color:hsl(0, 0%, 34.4117647059%);text-align:center;}#mermaid-1776177175170 .edgeLabel rect{opacity:0.5;background-color:hsl(0, 0%, 34.4117647059%);fill:hsl(0, 0%, 34.4117647059%);}#mermaid-1776177175170 .labelBkg{background-color:rgba(87.75, 87.75, 87.75, 0.5);}#mermaid-1776177175170 .cluster rect{fill:hsl(180, 1.5873015873%, 28.3529411765%);stroke:rgba(255, 255, 255, 0.25);stroke-width:1px;}#mermaid-1776177175170 .cluster text{fill:#F9FFFE;}#mermaid-1776177175170 .cluster span,#mermaid-1776177175170 p{color:#F9FFFE;}#mermaid-1776177175170 div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:12px;background:hsl(20, 1.5873015873%, 12.3529411765%);border:1px solid rgba(255, 255, 255, 0.25);border-radius:2px;pointer-events:none;z-index:100;}#mermaid-1776177175170 .flowchartTitleText{text-anchor:middle;font-size:18px;fill:#ccc;}#mermaid-1776177175170 :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}ComputeModel LayerEngineUser-FacingDotLLM.Cpu
SIMD / AVX2 / AVX-512DotLLM.Cuda
PTX kernels, cuBLASDotLLM.Models
GGUF loader, Llama, Mistral,
Phi, Qwen, DeepSeekDotLLM.Tokenizers
BPE, SentencePiece,
Jinja2 chat templatesDotLLM.Engine
KV-cache, scheduler, samplers,
constraints, speculative decodingDotLLM.Cli
CLI toolBuilt-in Chat UI
Browser-basedDotLLM.Server
OpenAI-compatible APIDotLLM.Core
ITensor, IBackend, IModel,
ISamplerStep, IDecodingConstraint
```

Each project ships as a separate NuGet package. `DotLLM.Core` defines all abstractions (`ITensor`, `IBackend`, `IModel`, `ISamplerStep`, etc.) while concrete implementations live in their respective projects. You pull in only what you need.

### Key features

**Performance:**

- **Zero-alloc inference** - all tensor data uses `NativeMemory.AlignedAlloc` (64-byte aligned). No managed heap allocations on the hot path (well, “the best” effort so far). (Almost) no allocs, no GC triggered.
- **SIMD vectorization for CPU backend** - `TensorPrimitives` for standard operations, hand-tuned `System.Runtime.Intrinsics` for quantized matmul, RMSNorm, RoPE, softmax operations. AVX2 and AVX-512 with scalar fallbacks.
- **CUDA GPU backend** - PTX kernels loaded via the CUDA Driver API with cuBLAS HGEMM for prefill, custom quantized GEMV for decode, and FP16 activation pipeline. Supports full GPU inference, hybrid CPU/GPU layer offloading, and KV-cache quantization.
- **Memory-mapped model loading** - GGUF files loaded via `MemoryMappedFile`. OS demand-paging means multi-GB models load in milliseconds.
- **Quantized inference** - FP16, Q8\_0, Q4\_K\_M and other GGUF formats with fused scale-int dot-product kernels operating directly on quantized blocks.

**Serving:**

- **OpenAI-compatible API** - `/v1/chat/completions`, `/v1/completions`, tool calling, structured output, streaming SSE via ASP.NET.
- **Speculative decoding** - draft-verify-accept loop with KV-cache rollback for higher throughput.
- **Structured output** - FSM/PDA-based constrained decoding guaranteeing valid JSON, JSON Schema, regex, and GBNF grammar.

**Extensibility:**

- **Pluggable backends** - `IBackend` interface with separate packages (CPU, CUDA, future ROCm).
- (planned) **LoRA adapters** - runtime loading, no weight merging, concurrent multi-adapter serving.
- (planned) **Diagnostic hooks** - zero-cost `IInferenceHook` for activation capture, logit lens, SAE integration.
- (planned) **OpenTelemetry** - `System.Diagnostics.Metrics` + `Activity` for throughput, latency, and per-request tracing.

Here’s a minimal streaming generation example:

```csharp
using var gguf = GgufFile.Open(modelPath);
var config = GgufModelConfigExtractor.Extract(gguf.Metadata);
using var model = TransformerModel.LoadFromGguf(gguf, config);
var tokenizer = GgufBpeTokenizerFactory.Load(gguf.Metadata);

var generator = new TextGenerator(model, tokenizer);
var options = new InferenceOptions
{
    SamplerSteps =
    [
        new TemperatureSampler(0.8f),
        new TopKSampler(40),
        new TopPSampler(0.95f)
    ],
    StopConditions = [new EosStopCondition(tokenizer.EosTokenId)],
    MaxTokens = 128
};

await foreach (var token in generator.GenerateStreamingTokensAsync(prompt, options))
    Console.Write(token.Text);
```

And here’s what the CLI looks like for a quick generation run with SmolLM-135M:

```
-- dotllm | Llama 30L/576H | Q8_0 | 16 threads | greedy ──────────────────
The capital of France is Paris. Paris is a city of romance and culture,

╭──────────────────────────────────────────────────────────────────────────╮
│  Generation Complete                                      163.27 tok/s  │
│                                                                         │
│  Prefill            12.3 ms       6 tokens       487.80 tok/s           │
│  Decode             91.8 ms      15 tokens       163.40 tok/s           │
│  Sampling            0.1 ms      15 tokens                              │
│  Total             104.2 ms      21 tokens       201.54 tok/s           │
│  Load              456.7 ms                                             │
│                                                                         │
│  Weights         136.73 MiB      (memory-mapped)                        │
│  KV Cache        158.20 MiB      (192 slots)                            │
╰──────────────────────────────────────────────────────────────────────────╯
```

There is also build-in `serve` command to host simple chat UX for testing and research:

<video controls=""><source src="https://kokosa.dev/assets/img/dotllm-chat-ui.mp4" type="video/mp4"></video>

### Performance reality check

Let’s be honest about where dotLLM stands today. While performance has been a key design consideration from day one (zero-alloc hot paths, SIMD kernels, memory-mapped loading), the primary focus so far has been closing the feature set — getting the full inference pipeline, constrained decoding, tool calling, speculative decoding, and the API server working correctly. Dedicated performance polishing is coming. Here are CPU benchmarks against llama.cpp (AMD Ryzen 9 5950X, 16 threads, same models and quantizations):

**Decode throughput (tok/s)** - the metric that matters most for interactive chat:

| Model | Quant | dotLLM | llama.cpp | Ratio |
| --- | --- | --- | --- | --- |
| SmolLM-135M | Q4\_K\_M | 279.1 | 334.7 | 0.83x |
| SmolLM-135M | Q8\_0 | 197.7 | 255.9 | 0.77x |
| Llama 3.2 1B | Q4\_K\_M | 32.4 | 48.9 | 0.66x |
| Llama 3.2 1B | Q8\_0 | 25.0 | 31.0 | 0.81x |
| Llama 3.2 3B | Q4\_K\_M | 15.4 | 19.6 | 0.79x |
| Llama 3.2 3B | Q8\_0 | 9.9 | 11.2 | 0.88x |

On decode, dotLLM reaches **66-88% of llama.cpp** throughput. Decode is largely memory-bandwidth-bound, and C# with SIMD intrinsics can get reasonably close to saturating the memory bus.

**Prefill is a different story** - dotLLM is roughly 2-5x slower than llama.cpp across the board. Prefill is compute-bound, and llama.cpp has years of hand-tuned GEMM kernels. We hit a specific wall here (outer-product tiled matmul vs. RyuJIT register pressure) which I’ll describe in the lessons learned section below.

The CUDA backend is functional but still early - it currently underperforms CPU on small models due to launch overhead, and the kernel tuning work is ongoing.

This is a preview release. If you need maximum throughput today, llama.cpp is faster. The gap will narrow.

## Why build this?

If out-of-the-box performance is not easily achieved, why build this at all? A few reasons, starting with the most important:

**Understanding by building.** I’ve been writing about LLM internals on this blog - [temperature and sampling](https://kokosa.dev/blog/2026/temperature/), [logprobs](https://kokosa.dev/blog/2026/logprobs/), learning a lot on my own. At some point, it makes you want to implement the whole pipeline. Building dotLLM was the logical next step to accelerate learning: implementing the entire inference pipeline from GGUF parsing through attention to token generation, seeing every allocation and every SIMD instruction up close. And it will generate A LOT of other blog posts…😇

**Seeing how far AI-assisted development can go.** This was also, explicitly, an experiment. **Not vibe coding** - not “prompt and pray” loop. Structured, documented, reviewed AI-assisted development where a human makes the architectural decisions and AI handles implementation within well-defined boundaries. I wanted to find out what a solo developer can realistically build in one-two months with this approach. The answer surprised me.

**Creating a platform for research and experimentation.** Building from the ground up with this goal in mind means the architecture is open to experimentation - adding new features, deeper diagnostics, and interpretability tools into the inference pipeline. All outside the gold-standard HuggingFace monopoly. In.NET 😍

**Proving the platform.** There’s a persistent assumption that systems-level performance work requires C, C++, or Rust. Twenty years of.NET performance work has taught me that’s not always true. C# with `NativeMemory`, `System.Runtime.Intrinsics`, `MemoryMappedFile`, and `Span<T>` gives you genuine control over memory and compute. dotLLM is a proof point.

**The.NET ecosystem gap is real.** If you’re building.NET applications and want local LLM inference, your choices are wrappers (LLamaSharp wrapping llama.cpp), limited runtimes (ONNX Runtime with restricted model support), or orchestration layers (Semantic Kernel, which is about chaining calls, not running inference). Enterprise.NET shops that want to run models in production without Python or C++ dependencies have no native option. dotLLM fills that gap, but it will take a LOT of time to treat it as a serious replacement.

> dotLLM is not meant to replace llama.cpp or vLLM in production - at least not yet. It’s built for.NET developers who want native inference without leaving their ecosystem, and for researchers and experimenters who want to explore LLM internals from C#. And everyone who wants to understand how to build a LLM inference engine from scratch.

## How AI built an AI engine

![](https://kokosa.dev/assets/img/dotllm-git-log.png)

Let me be upfront: nearly every commit in dotLLM’s git history has a `Co-Authored-By: Claude Opus 4.6` line. This project would not exist in its current form without AI assistance. But the story of *how* that assistance was structured is more interesting than the fact that it was used.

### The development methodology

dotLLM was built over ~60 implementation steps organized into 7 phases, documented in a detailed [`ROADMAP.md`](https://github.com/kkokosa/dotLLM/blob/main/docs/ROADMAP.md). Each phase was a discrete unit of work with clear scope and acceptance criteria:

- **Phase 1** - End-to-end single-token generation (GGUF loader, dequantization, CPU ops, tokenizer, attention, KV-cache, sampling)
- **Phase 2** - Practical local inference (Q4\_K\_M, chat templates, streaming, multi-threading, additional architectures)
- **Phase 3** - CPU performance (tiled attention, SIMD tuning, NUMA awareness, operator fusion)
- **Phase 4** - GPU acceleration (CUDA backend, hybrid CPU/GPU, KV-cache quantization)
- **Phase 5** - Constrained decoding and API (JSON/schema/regex/grammar, tool calling, server, chat UI, prompt caching)
- **Phase 6** - Improved serving (warm-up, Native AOT, paged KV-cache, speculative decoding)
- **Phase 7** - Diagnostics and interpretability (logprobs, hooks, logit lens - in progress)

Every step started as a GitHub issue. Every issue lived on a branch named `issue/{number}-{short-description}`. Every PR closed its issue and updated the roadmap. This was relentlessly boring discipline, and it was the single most important factor in the project’s success.

After the initial release, just before making the repository public, I also ran a series of “Waves” - systematic quality passes across the entire codebase:

- **Wave 1** (P0): Security and crash fixes - path traversal, CUDA shared memory guards, hybrid GPU edge cases
- **Wave 2** (P1): Quick correctness and consistency fixes
- **Wave 3**: Presentation cleanup - remove dead code, label stubs, fix samples
- **Wave 4**: Server hardening - request validation, LINQ removal from hot paths
- **Wave 5** was skipped - it was earmarked for batch-serving improvements that depend on Phase 9 (continuous batching), which isn’t implemented yet
- **Wave 6**: CUDA kernel rewrite - tiled softmax, vectorization, grid-stride loops
- **Wave 7**: CPU performance - TopK sampler optimization, AVX2 gap filling, schema cache tuning

Those “waves” are a bunch of findings that come from in-depth reviews from other models, grouped into GitHub issues.

### ROADMAP.md and CLAUDE.md - the highest-ROI investments

If there’s one takeaway from this experiment, it’s this: **the time you spend writing structured documentation for AI is not overhead - it IS the development methodology.**

`ROADMAP.md` was the backbone. Each of the ~60 steps had a feature name, a description, key files to modify, and dependencies on other steps. This gave both me and the AI a shared understanding of what to build next, in what order, and why. Without it, AI would be coding in circles - solving the wrong problem, building features in the wrong order, missing dependencies.

The roadmap also forced me to think through the architecture upfront. When you have to discuss things like *“Step 31: CUDA backend - PTX kernels loaded via CUDA Driver API, no native shared library, cuBLAS HGEMM for prefill, custom quantized GEMV for decode”* before writing any code, you’ve already made the hard decisions. And learnt a lot.

`CLAUDE.md` was the project’s “constitution” - 180+ lines defining how AI should work in this codebase. Here are some actual rules from it:

```markdown
**Native .NET first** - All orchestration, model loading, tokenization, sampling, scheduling, CPU compute in pure C#.

**Unmanaged memory for tensors** - \`NativeMemory.AlignedAlloc\` (64-byte). Zero GC allocations on inference hot path.

**Hybrid GPU architecture** - Thin native C/CUDA lib via \`[LibraryImport]\`. GPU memory as opaque \`IntPtr\` - tensor data never crosses P/Invoke boundary.
```

And specific coding rules:

```markdown
**NEVER** allocate managed arrays for tensor data. Use \`NativeMemory.AlignedAlloc\` (64-byte for AVX-512, 32-byte for AVX2).

SIMD: Foundation is \`System.Numerics.Tensors.TensorPrimitives\` for standard ops. Hot inner loops: \`System.Runtime.Intrinsics\` - prefer cross-platform \`Vector128<T>\`/\`Vector256<T>\`, use platform-specific only when measurably faster. **Always provide scalar fallback.
```

Beyond `CLAUDE.md`, there were **22 detailed design documents** in `/docs/` - one for each major subsystem like `ARCHITECTURE`, `QUANTIZATION`, `ATTENTION`, `CUDA`, and more. The rule was simple: AI reads the relevant spec before touching a module.

This **documentation-first** approach had a compound effect. Every implementation step could reference the roadmap for scope, the design docs for architecture, and `CLAUDE.md` for coding conventions. The AI wasn’t guessing - it was implementing within well-defined constraints.

### Claude Code as implementation partner

[Claude Code](https://claude.ai/code) with Opus 4.6 (1M context) was the primary implementation tool from the project start. The workflow was built around six custom [Claude Code skills](https://docs.anthropic.com/en/docs/claude-code/skills) that automated the development lifecycle:

- **`/plan-step`** - looks for a given roadmap step in `ROADMAP.md` plus relevant docs from `/docs/`, enters plan mode, and produces a step-by-step implementation plan for my approval before any code is written.
- **`/create-pr`** - commits remaining changes, pushes the branch, and creates a PR with a detailed description following project conventions.
- **`/apply-pr-comments`** - reads review comments from Codex, Gemini, or human reviewers, analyzes them, enters plan mode so I can approve the fixes before any code changes.
- **`/finish-pr-comments`** - after fixes are applied and tested, commits the changes, pushes to the PR branch, and replies to each reviewer comment with what was fixed and the commit hash.
- **`/merge-pr`** - squash-merges the PR into main, deletes the remote branch, and switches to an updated local main.
- **`/plan-issue`** - similar to `plan-step` but for less frequent case when we start from an issue, not a roadmap’s step.

There was also a GitHub Actions workflow that responds to `@claude` mentions in PRs and issues, enabling asynchronous interaction.

The typical flow for a feature looked like this: I’d run `/plan-step` (or `/plan-issue`), review and adjust the plan, then let Claude implement it step by step while I reviewed each change. The key insight is that **planning was always a separate, human-approved step** before implementation began. Most of the work and brainstorming happened there.

### Codex and Gemini as PR reviewers

Every PR was also reviewed by [Codex](https://chatgpt.com/codex) and [Gemini](https://ai.google.dev/) triggered manually via mentions of `@codex` and `@gemini` in PR comments.

Gemini was powered by a custom Python bot ([`.github/scripts/gemini_bot.py`](https://github.com/kkokosa/dotLLM/blob/main/.github/scripts/gemini_bot.py)) with retry logic and configurable thinking budgets. A separate [GEMINI.md](https://github.com/kkokosa/dotLLM/blob/main/GEMINI.md) file defined its review persona.

The review findings were not cosmetic. They caught genuinely critical bugs that could have shipped. Just as examples:

- **KV-cache quantization** (PR #75): Codex caught a **ring-buffer indexing bug** (window reads used linear indexing instead of ring indices, producing garbage after wrap-around) or a **pinned buffer scope issue** (pointers from `fixed` blocks used after the scope exited), and a **shared-state race condition** (per-layer eviction progress stored in a shared counter)
- **JSON Schema constrained decoding** (PR #79): Found a **cache key collision** (string substates not included in the hash, collapsing distinct parser states) and a **unicode escape flag preservation bug** (`\u` parsing wiped the key-string flag)
- **Wave 6 CUDA kernel rewrite** (PR #114): Gemini identified thread underutilization in GEMV kernels and uncoalesced memory reads - architectural issues that Codex’s code-level analysis didn’t surface

Once Codex and Gemini leave their comments, the remaining skills close the loop. `/apply-pr-comments` reads all review comments on the current PR, analyzes them, and enters plan mode — so I can approve which fixes to make before any code changes. This prevents blindly applying every suggestion without human judgment on what’s worth addressing versus deferring.

After the fixes are implemented and tested, straightforward `/finish-pr-comments` commits the changes, pushes to the PR branch, and has the Claude Code bot (`dotllm-claude-code-bot`) reply to each reviewer comment with what was fixed and the corresponding commit hash.

This creates a **fully traceable chain**: Codex/Gemini finds a bug -> Claude fixes it -> the reply references the exact commit. The PR thread becomes a complete audit trail.

![](https://kokosa.dev/assets/img/dotllm-codex-review.png)

Finally, `/merge-pr` squash-merges the PR into main, deletes the remote branch, and checks out an updated local main. The entire cycle - from roadmap step to merged PR - typically took one Claude Code session.

### Lessons learned

**What worked brilliantly:**

- **The implementation is correct.** This is the most obvious finding to overlook. But here it is - this setup really worked! Step by step, we were progressing with the implementation, making it more and more sophisticated. And the moment when for the first time I saw an answer from the real model - it felt like magic! Reaching 80-90% of llama.cpp CPU decode performance is a thing, too.
- **`ROADMAP.md` was the highest-ROI time investment.** Planning structured documentation saved many hours of correcting misdirected AI implementation. The documentation *is* the development methodology - it’s not overhead, it’s the thing that makes AI-assisted development work at all. Without the roadmap, the AI has no sense of direction.
- **Two-role separation: implementation vs. review.** Claude wrote the code. Codex and Gemini reviewed it independently. The AI that writes the code should not be the only AI that reviews it. Different models have genuinely different blind spots - Codex and Gemini almost never flagged the same issues.
- **No [Ralph Wiggum loop](https://github.com/anthropics/claude-code/blob/main/plugins/ralph-wiggum/README.md) or other YOLO mode.** I really wanted to *drive* the work, not *fire & forget* it to burn tokens. It worked out perfectly for me. The single task took around several minutes, up to 30-40, so you could return to them from time to time, during breaks whilst waiting for something else. Great background work.

**Where AI struggled:**

- **Fundamental architectural decisions.** Which attention strategy to use, how to structure the GPU interop layer, whether to use PagedAttention kernels or staging-buffer gather - these required human judgment informed by comparing to llama.cpp, vLLM, and the research literature. AI can implement an architecture, but it’s less reliable at choosing between architectures.
- **The prefill throughput gap.** This is the biggest remaining performance wall - but to be fair, it’s not really an AI failure per se. It might be AI struggling to workaround platform’s out-of-the-box behaviours. The 2-5x prefill gap you saw in the benchmarks comes down to one unfinished roadmap step: Step 26, the outer-product tiled matmul. The current batched GEMM (Step 11) uses an inner-product formulation - it tiles over M but still computes one output element at a time. It delivered a 2.2x prefill speedup when implemented. But the “outer-product” approach would share one activation load across all weight-row dot products: a 4x3 AVX2 tile with 12 YMM accumulators. Problem: due to AI that tile needs ~23 YMM registers, but AVX2 only has 16. RyuJIT spills to stack, and the spills eat the reuse benefit the tile was designed to get. AI was actually *very good* at experimenting here — it iterated through multiple tile sizes, inspected the JIT disassembly for spills, and methodically narrowed down the root cause. The options now seems to be: AVX-512 (32 ZMM registers, fits comfortably), a native C microkernel via `[LibraryImport]` (what llamafile/tinyBLAS does), or a smaller tile with partial reuse. I’ve left this for a much more manual, still AI-assisted, research phase - it needs careful benchmarking and disassembly analysis rather than the “plan step, implement, make PR” cadence that worked for the rest of the project.
- **Keeping it within the guiderails.** Small but very annoying. No matter how many times, and in how many places, I ask him to avoid compound tool calls (esp. `cd D:\github\ai\dotLLM && git ...`) it eventually ignores it, breaking the permissions. It breaks the flow, as instead of an autonomous work it got stuck waiting for permission for tools that otherwise should be accepted (like allowed GitHub read-only commands etc). Now I think I need pre-tool hook that checks that💡
- **Claude Code got really stuck 2-3 times.** There were a few times when implementing a step took a lot of struggle. Implementing, retrying, failing, in a loop that took literally hours (!). But even more surprising is the fact that he eventually did it. With some of my help and brainstorming, but it was mostly his async work trying to figure it out.

## What’s next

dotLLM is at v0.1.0-preview.2 - explicitly a preview. The foundations are solid, but there’s a long road ahead:

- **Phase 7** (in progress): Diagnostic hooks, logit lens, Sparse Autoencoders (SAE) integration, LoRA adapters
- **Phase 8** (planned): MLA attention (DeepSeek), SmolLM3, Gemma 4, Mixture of Experts
- **Phase 9** (planned): Production serving - continuous batching, prefix sharing, advanced scheduling. This will be fun🔥

After those Phases I will consider feature set (mostly) done and start to focus on performance more and more.

BTW, the project is [GPLv3](https://github.com/kkokosa/dotLLM/blob/main/LICENSE) and contributions are welcome! There is still a lot to do. The codebase has 22 design docs, a detailed roadmap, and a CLAUDE.md that makes it easy for both human and AI contributors to get oriented quickly.

- **GitHub**: [github.com/kkokosa/dotLLM](https://github.com/kkokosa/dotLLM)
- **Website**: [dotllm.dev](https://dotllm.dev/)
- **NuGet packages**: `DotLLM.Engine`, `DotLLM.Cpu`, `DotLLM.Cuda`, `DotLLM.Server`, and more
- **Discussions**: [GitHub Discussions](https://github.com/kkokosa/dotLLM/discussions)

## Closing

Two things are true at once. First:.NET can do native, systems-level AI work. Zero-GC inference, SIMD-vectorized kernels, memory-mapped model loading, paged KV-cache, speculative decoding - all in C#. The platform is more capable than many give it credit for.

Second: a solo developer can build something of this scope in two months with AI assistance - but only with relentless structure. The roadmap, the design docs, the CLAUDE.md constitution, the dual-review workflow - take any of these away and the productivity collapses. AI amplifies discipline; it doesn’t replace it.

If you’re a.NET developer curious about LLM inference, or a researcher who wants to explore model internals from C#, [give dotLLM a try](https://github.com/kkokosa/dotLLM). File issues. Break things. Tell me what’s missing.