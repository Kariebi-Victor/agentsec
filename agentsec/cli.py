
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from agentsec.agent import run_agent
from agentsec.reporter import generate_reports


console = Console()


def main():
    console.print(
        Panel.fit(
            "[bold cyan]AgentSec v1.0[/bold cyan]\n"
            "AI-Powered Application Security Testing"
        )
    )

    console.print("\n[cyan]Starting assessment...[/cyan]\n")

    result = run_agent()

    console.print("\n[bold]Security Assessment[/bold]\n")
    console.print(Markdown(result["assessment"]))

    json_path, html_path = generate_reports(result)

    console.print("\n[bold green]Assessment completed.[/bold green]")
    console.print(f"[cyan]JSON Report:[/cyan] {json_path}")
    console.print(f"[cyan]HTML Report:[/cyan] {html_path}")


if __name__ == "__main__":
    main()
