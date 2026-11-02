using System.Diagnostics;
using System.Text;
using System.Text.RegularExpressions;

// Compiles and runs one learner submission per request inside a throwaway copy of /opt/template.
const string TemplateDir = "/opt/template";
const string WorkRoot = "/work";
const int MaxCodeChars = 64 * 1024;
const int MaxOutputChars = 64 * 1024;
var buildTimeout = TimeSpan.FromSeconds(60);
var runTimeout = TimeSpan.FromSeconds(10);

var gate = new SemaphoreSlim(2); // at most two builds/runs at once

var app = WebApplication.CreateBuilder(args).Build();

app.MapGet("/health", () => "ok");

app.MapPost("/run", async (RunRequest req) =>
{
    if (string.IsNullOrWhiteSpace(req.Code))
        return Results.Ok(new RunResponse(false, "No code to run.", "none"));
    if (req.Code.Length > MaxCodeChars)
        return Results.Ok(new RunResponse(false, "Code is too long.", "none"));
    if (!await gate.WaitAsync(TimeSpan.FromSeconds(30)))
        return Results.StatusCode(503);

    var dir = Path.Combine(WorkRoot, Guid.NewGuid().ToString("N"));
    try
    {
        Directory.CreateDirectory(dir);
        foreach (var file in Directory.GetFiles(TemplateDir))
            File.Copy(file, Path.Combine(dir, Path.GetFileName(file)));
        await File.WriteAllTextAsync(Path.Combine(dir, "Program.cs"), req.Code);

        var build = await Exec("dotnet", ["build", "-nologo", "-v", "q", "-clp:NoSummary", "-o", "out"], dir, buildTimeout);
        if (build.TimedOut)
            return Results.Ok(new RunResponse(false, "Build timed out.", "compile"));
        if (build.ExitCode != 0)
            return Results.Ok(new RunResponse(false, CompilerErrors(build.Output), "compile"));

        var run = await Exec("dotnet", ["out/app.dll"], dir, runTimeout);
        var output = run.Output.TrimEnd();
        if (run.TimedOut)
            output += $"\n⏱ Stopped after {runTimeout.TotalSeconds:0} seconds.";
        return Results.Ok(new RunResponse(run.ExitCode == 0 && !run.TimedOut, output, "run"));
    }
    finally
    {
        gate.Release();
        try { Directory.Delete(dir, recursive: true); } catch { /* best effort */ }
    }
});

var shell = new CliShell(Exec);

app.MapPost("/cli", async (CliRequest req) =>
{
    if (req.Command is null || req.Command.Length > 1024)
        return Results.Ok(new CliResponse(false, "Command is too long.", "~"));
    if (!await gate.WaitAsync(TimeSpan.FromSeconds(30)))
        return Results.StatusCode(503);
    try { return Results.Ok(await shell.Run(req.Session ?? "default", req.Command)); }
    finally { gate.Release(); }
});

app.Run();

async Task<ExecResult> Exec(string file, string[] args, string cwd, TimeSpan timeout)
{
    var psi = new ProcessStartInfo(file)
    {
        WorkingDirectory = cwd,
        RedirectStandardInput = true,
        RedirectStandardOutput = true,
        RedirectStandardError = true,
    };
    foreach (var a in args) psi.ArgumentList.Add(a);

    using var p = Process.Start(psi)!;
    p.StandardInput.Close();

    var sb = new StringBuilder();
    void Append(string? line)
    {
        if (line is null) return;
        lock (sb) { if (sb.Length < MaxOutputChars) sb.AppendLine(line); }
    }
    p.OutputDataReceived += (_, e) => Append(e.Data);
    p.ErrorDataReceived += (_, e) => Append(e.Data);
    p.BeginOutputReadLine();
    p.BeginErrorReadLine();

    using var cts = new CancellationTokenSource(timeout);
    try
    {
        await p.WaitForExitAsync(cts.Token);
    }
    catch (OperationCanceledException)
    {
        p.Kill(entireProcessTree: true);
        await p.WaitForExitAsync();
        return new ExecResult(-1, sb.ToString(), TimedOut: true);
    }
    p.WaitForExit(); // flush the async output readers
    return new ExecResult(p.ExitCode, sb.ToString(), TimedOut: false);
}

// MSBuild prints each error several times with absolute paths; show each once, relative.
static string CompilerErrors(string buildOutput)
{
    var errors = buildOutput
        .Split('\n', StringSplitOptions.RemoveEmptyEntries)
        .Where(l => Regex.IsMatch(l, @"error \w+\d+:"))
        .Select(l => Regex.Replace(l.Trim(), @"^.*?Program\.cs", "Program.cs"))
        .Select(l => Regex.Replace(l, @"\s+\[[^\]]*\]$", ""))
        .Distinct()
        .ToList();
    return errors.Count > 0 ? string.Join("\n", errors) : buildOutput.Trim();
}

record RunRequest(string Code);
record RunResponse(bool Ok, string Output, string Stage);
record ExecResult(int ExitCode, string Output, bool TimedOut);
