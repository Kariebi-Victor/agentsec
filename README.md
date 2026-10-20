# AgentSec

**A locally hosted, LLM-powered application security testing agent for authorization vulnerabilities.**

AgentSec demonstrates how an AI agent can orchestrate predefined security checks, analyze their results, and generate structured vulnerability reports.

The project uses **Ollama**, **Qwen3**, **Python**, and **FastAPI** to provide a self-contained testing environment without requiring a paid LLM API.

## Features

- Local LLM inference using Ollama
- LLM-driven security tool selection and execution
- Broken Object Level Authorization (BOLA/IDOR) detection
- Broken Function Level Authorization (BFLA) detection
- JSON and HTML vulnerability reports
- Automated security tests using pytest
- Restricted tool execution with an explicit allowlist

## Architecture

```text
                  ┌──────────────────┐
                  │   AgentSec CLI   │
                  └────────┬─────────┘
                           │
                  ┌────────▼─────────┐
                  │  Ollama / Qwen3  │
                  │   Local LLM      │
                  └────────┬─────────┘
                           │ Tool calls
                  ┌────────▼─────────┐
                  │ Tool Dispatcher  │
                  │   (Allowlist)    │
                  └────────┬─────────┘
                           │
                 ┌─────────┴─────────┐
                 │                   │
          ┌──────▼──────┐     ┌──────▼──────┐
          │ IDOR Check  │     │ Admin Check │
          └──────┬──────┘     └──────┬──────┘
                 │                   │
                 └─────────┬─────────┘
                           │
                  ┌────────▼─────────┐
                  │ Local FastAPI    │
                  │ Vulnerable API   │
                  └──────────────────┘
```

The agent selects from predefined tools rather than executing arbitrary commands or HTTP requests.

## Security Checks

| Check | Description | OWASP API Security |
|---|---|---|
| BOLA / IDOR | Tests whether one authenticated user can access another user's record | API1:2023 |
| BFLA | Tests whether a regular user can access an administrative endpoint | API5:2023 |

The included API intentionally contains both vulnerabilities for demonstration purposes.

## Getting Started

### Prerequisites

- Python 3.9+
- Ollama
- Qwen3 4B model

### Installation

Clone the repository:

```bash
git clone https://github.com/Kariebi-Victor/agentsec.git
cd agentsec
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Download the local model:

```bash
ollama pull qwen3:4b
```

### Running AgentSec

Start Ollama in one terminal:

```bash
ollama serve
```

Start the intentionally vulnerable API in another terminal:

```bash
python -m uvicorn vulnerable_api.main:app --host 127.0.0.1 --port 8000
```

Run the security agent:

```bash
python -m agentsec.cli
```

AgentSec will execute its authorization checks and generate a security assessment.

## Reporting

The agent generates two report formats:

```text
reports/
├── agentsec-report.json
└── agentsec-report.html
```

The JSON report contains structured vulnerability findings, including affected endpoints, evidence, severity classifications, and remediation recommendations.

The HTML report provides a readable assessment suitable for review and demonstration.

To open the HTML report on macOS:

```bash
open reports/agentsec-report.html
```

## Testing

Run the automated test suite while the local FastAPI server is running:

```bash
python -m pytest tests/ -v
```

The tests validate authorization detection, invalid-token handling, report generation, and HTML escaping.

## Security Design

AgentSec implements several constraints:

- **Tool allowlisting:** The LLM can request only explicitly defined security functions.
- **Local target restriction:** Security checks are configured for the local demonstration API.
- **Evidence-based reporting:** Structured findings are generated from security-check results rather than unsupported LLM claims.
- **Untrusted response handling:** HTML output escapes potentially unsafe content.
- **Iteration limits:** The agent's tool-calling loop has a maximum number of iterations.

## Limitations

AgentSec v1.0.0 is a proof of concept, not a general-purpose penetration testing framework.

It currently supports two predefined authorization checks against a known local API. It does not perform autonomous endpoint discovery, generalized vulnerability detection, or testing of arbitrary external applications.

The LLM-generated assessment should be reviewed by a security professional. Severity classifications are predefined for the demonstration scenarios.

## Future Improvements

- Dynamic endpoint discovery
- Additional vulnerability checks
- Configurable test identities and authorization policies
- More robust agent planning and recovery
- CI/CD integration
- SARIF reporting

## Disclaimer

AgentSec is intended for security education and testing of systems you own or are explicitly authorized to assess. The included vulnerable API should only be run in a controlled local environment.

## License

MIT
