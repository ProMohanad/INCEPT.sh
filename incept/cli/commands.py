"""Slash command registry for INCEPT.sh CLI."""

from __future__ import annotations

from collections.abc import Callable


class SlashCommandRegistry:
    """Registry of /slash commands available in the CLI."""

    def __init__(self) -> None:
        self._commands: dict[str, tuple[Callable[[str], str], str]] = {}
        self._register_defaults()

    def _register_defaults(self) -> None:
        self.register("/help", self._cmd_help, "Show available commands")
        self.register("/sysinfo", self._cmd_sysinfo, "Show system info and model path")
        self.register("/history", self._cmd_history, "Show query history")
        self.register("/clear", self._cmd_clear, "Clear the screen")
        self.register("/think", self._cmd_think, "Toggle reasoning: /think on|off")
        self.register("/explain", self._cmd_explain, "Explain a command: /explain <cmd>")
        self.register("/plugin", self._cmd_plugin, "Shell plugin info")
        self.register("/exit", self._cmd_exit, "Exit INCEPT.sh")
        # Aliases for backward compatibility
        self.register("/context", self._cmd_sysinfo, "Alias for /sysinfo")
        self.register("/safe", self._cmd_safe, "Safe mode toggle (informational)")
        self.register("/verbose", self._cmd_verbose, "Verbosity (informational)")
        self.register("/quit", self._cmd_quit, "Exit INCEPT.sh")

    def register(self, name: str, handler: Callable[[str], str], description: str) -> None:
        self._commands[name] = (handler, description)

    def has(self, name: str) -> bool:
        return name in self._commands

    def dispatch(self, name: str, args: str) -> str:
        if name not in self._commands:
            return f"  [red]✗[/red] Unknown command: {name}."
        handler, _ = self._commands[name]
        return handler(args)

    def get_command_names(self) -> list[str]:
        return list(self._commands.keys())

    def get_descriptions(self) -> dict[str, str]:
        return {name: desc for name, (_, desc) in self._commands.items()}

    # ── Built-in handlers ────────────────────────────────

    def _cmd_help(self, args: str) -> str:
        lines = [
            "",
            "  [bold cyan]🐧 INCEPT.sh Commands[/bold cyan]",
            "  [dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/dim]",
        ]
        for name, (_, desc) in self._commands.items():
            lines.append(f"  [bold]{name:14s}[/bold] [dim]{desc}[/dim]")
        lines.append("")
        lines.append("  [dim]Or just type any natural language request.[/dim]")
        lines.append("")
        return "\n".join(lines)

    def _cmd_sysinfo(self, args: str) -> str:
        from incept.core.context import run_context_snapshot
        from incept.core.model_loader import get_model_path

        try:
            snap = run_context_snapshot()
            distro = f"{snap.distro_id} {snap.distro_version}".strip()
            shell = snap.shell
            privilege = "root" if snap.is_root else "non-root"
        except Exception:
            distro = shell = privilege = "unknown"

        model = get_model_path() or "no model loaded"
        return (
            "\n"
            "  [bold cyan]System Info[/bold cyan]\n"
            f"  [dim]Distro :[/dim] {distro}\n"
            f"  [dim]Shell  :[/dim] {shell} ({privilege})\n"
            f"  [dim]Model  :[/dim] {model}\n"
        )

    def _cmd_history(self, args: str) -> str:
        # Actual history is injected by the REPL via handle_input override
        return "  [dim](no history yet)[/dim]"

    def _cmd_clear(self, args: str) -> str:
        # Handled directly in repl.run() via os.system — this stub is for /help listing
        return ""

    def _cmd_think(self, args: str) -> str:
        # Toggling is handled by the REPL — this stub is for /help listing
        arg = args.strip().lower()
        if arg in ("on", "off", ""):
            return ""
        return "  Usage: /think on|off"

    def _cmd_safe(self, args: str) -> str:
        return "  [dim]Safe mode is always active — dangerous commands are flagged automatically.[/dim]"

    def _cmd_verbose(self, args: str) -> str:
        level = args.strip().lower()
        if level in ("minimal", "normal", "detailed"):
            return f"  [green]✓[/green] Verbosity: [bold]{level}[/bold] (restart to apply)"
        return "  Usage: /verbose minimal|normal|detailed"

    def _cmd_exit(self, args: str) -> str:
        return "__exit__"

    def _cmd_quit(self, args: str) -> str:
        return "__exit__"

    def _cmd_explain(self, args: str) -> str:
        if not args.strip():
            return "  Usage: /explain <command>\n  Example: /explain find / -size +1G"
        try:
            from incept.explain.pipeline import run_explain_pipeline

            resp = run_explain_pipeline(args.strip())
            lines = [
                f"\n  [bold]Command:[/bold]  {resp.command}",
                f"  [bold]Intent:[/bold]   {resp.intent}" if resp.intent else "",
                f"  [bold]Explain:[/bold]  {resp.explanation}",
                f"  [bold]Risk:[/bold]     {resp.risk_level}\n",
            ]
            return "\n".join(ln for ln in lines if ln)
        except Exception as exc:
            return f"  [red]✗ Explain unavailable:[/red] {exc}"

    def _cmd_plugin(self, args: str) -> str:
        return (
            "\n  [bold cyan]Shell Plugin[/bold cyan]\n"
            "  [dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/dim]\n"
            "  Install:   [bold]incept plugin install[/bold]\n"
            "  Uninstall: [bold]incept plugin uninstall[/bold]\n"
            "  Binds [bold]Ctrl+I[/bold] to invoke INCEPT inline.\n"
        )
