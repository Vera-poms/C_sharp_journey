using System.Collections.Concurrent;
using System.Text;

// A tiny shell for the lesson terminal. There is no real shell: each line is tokenised here and
// either handled by a built-in (confined to the session's folder) or passed to `dotnet` as an
// argument list, so nothing the learner types is ever interpreted by /bin/sh.
sealed class CliShell(Func<string, string[], string, TimeSpan, Task<ExecResult>> exec)
{
    const string Root = "/work/cli";
    const int MaxSessions = 20;
    static readonly TimeSpan IdleLimit = TimeSpan.FromMinutes(30);

    // Only the commands the lessons teach; `watch`, `tool`, `workload` etc. are not useful offline.
    static readonly HashSet<string> DotnetCommands =
    [
        "new", "build", "run", "clean", "restore", "test", "publish",
        "add", "remove", "list", "sln", "--help", "-h", "--version", "--info", "--list-sdks",
    ];

    sealed class Session
    {
        public string Dir = "";
        public string Cwd = "";
        public DateTime LastUsed = DateTime.UtcNow;
    }

    readonly ConcurrentDictionary<string, Session> sessions = new();

    public async Task<CliResponse> Run(string sessionId, string line)
    {
        var session = GetSession(sessionId);
        if (session is null)
            return new CliResponse(false, "Too many terminal sessions are open. Try again in a few minutes.", "~");

        var ok = true;
        var output = new StringBuilder();
        try
        {
            foreach (var command in SplitAnd(Tokenize(line)))
            {
                if (command.Count == 0) continue;
                var (cmdOk, text) = await RunOne(session, command);
                if (text.Length > 0) output.AppendLine(text.TrimEnd('\n', '\r'));
                if (!cmdOk) { ok = false; break; }
            }
        }
        catch (FormatException e)
        {
            return new CliResponse(false, e.Message, Prompt(session));
        }
        return new CliResponse(ok, output.ToString().TrimEnd(), Prompt(session));
    }

    async Task<(bool Ok, string Output)> RunOne(Session s, List<string> argv)
    {
        var name = argv[0];
        var args = argv.Skip(1).ToList();
        switch (name)
        {
            case "help":
                return (true, string.Join('\n',
                    "This terminal runs inside a sandbox with no internet access.",
                    "",
                    "  dotnet <command>      new, build, run, test, clean, restore, publish, list, add, remove, sln, --help, --version, --info",
                    "  pwd, ls [path], cd <path>, cat <file>, mkdir <dir>, touch <file>, rm [-r] <path>, echo <text>",
                    "  clear                 clear the screen",
                    "  cmd1 && cmd2          run cmd2 only if cmd1 succeeded",
                    "",
                    "Not available: pipes, redirects, `dotnet watch`, and downloading NuGet packages (no network)."));
            case "pwd":
                return (true, "/" + s.Cwd);
            case "echo":
                return (true, string.Join(' ', args));
            case "cd":
                return Cd(s, args.Count > 0 ? args[0] : "");
            case "ls":
                return Ls(s, args);
            case "cat":
                return Cat(s, args);
            case "mkdir":
                return Each(s, args, p => { Directory.CreateDirectory(p); });
            case "touch":
                return Each(s, args, p => { if (!File.Exists(p)) File.WriteAllText(p, ""); });
            case "rm":
                return Rm(s, args);
            case "dotnet":
                return await Dotnet(s, args);
            default:
                return (false, $"{name}: command not found. Type `help` to see what this terminal supports.");
        }
    }

    async Task<(bool, string)> Dotnet(Session s, List<string> args)
    {
        if (args.Count == 0) args.Add("--help");
        if (!DotnetCommands.Contains(args[0]))
            return (false, $"`dotnet {args[0]}` isn't available in this terminal. Try: {string.Join(", ", DotnetCommands.Where(c => !c.StartsWith('-')).Order())}.");

        var timeout = args[0] is "run" or "test" ? TimeSpan.FromSeconds(30) : TimeSpan.FromSeconds(60);
        var result = await exec("dotnet", [.. args], Path.Combine(Root, s.Dir, s.Cwd), timeout);
        var text = result.Output.TrimEnd();
        if (result.TimedOut)
            text += $"\n⏱ Stopped after {timeout.TotalSeconds:0} seconds.";
        if (result.ExitCode != 0 && args[0] == "add" && text.Contains("Unable to find package"))
            text += "\n\nThis terminal has no internet, so only a few packages are available offline:" +
                    "\nHumanizer, CommunityToolkit.Mvvm, Newtonsoft.Json (and the xunit test packages).";
        return (result.ExitCode == 0 && !result.TimedOut, text);
    }

    // ---- built-ins -------------------------------------------------------------------------

    (bool, string) Cd(Session s, string target)
    {
        if (target is "" or "~") { s.Cwd = ""; return (true, ""); }
        var full = Resolve(s, target);
        if (full is null) return (false, $"cd: {target}: outside your workspace");
        if (!Directory.Exists(full)) return (false, $"cd: {target}: No such directory");
        s.Cwd = Path.GetRelativePath(SessionRoot(s), full).Replace('\\', '/');
        if (s.Cwd == ".") s.Cwd = "";
        return (true, "");
    }

    (bool, string) Ls(Session s, List<string> args)
    {
        var target = args.FirstOrDefault(a => !a.StartsWith('-')) ?? ".";
        var full = Resolve(s, target);
        if (full is null) return (false, $"ls: {target}: outside your workspace");
        if (File.Exists(full)) return (true, Path.GetFileName(full));
        if (!Directory.Exists(full)) return (false, $"ls: {target}: No such file or directory");
        var entries = Directory.GetFileSystemEntries(full)
            .Select(e => Path.GetFileName(e) + (Directory.Exists(e) ? "/" : ""))
            .Order(StringComparer.OrdinalIgnoreCase);
        return (true, string.Join('\n', entries));
    }

    (bool, string) Cat(Session s, List<string> args)
    {
        if (args.Count == 0) return (false, "cat: missing file name");
        var sb = new StringBuilder();
        foreach (var a in args)
        {
            var full = Resolve(s, a);
            if (full is null) return (false, $"cat: {a}: outside your workspace");
            if (!File.Exists(full)) return (false, $"cat: {a}: No such file");
            if (new FileInfo(full).Length > 64 * 1024) return (false, $"cat: {a}: file too large");
            sb.Append(File.ReadAllText(full));
        }
        return (true, sb.ToString());
    }

    (bool, string) Rm(Session s, List<string> args)
    {
        var recursive = args.Any(a => a is "-r" or "-rf" or "-fr" or "-R");
        var targets = args.Where(a => !a.StartsWith('-')).ToList();
        if (targets.Count == 0) return (false, "rm: missing operand");
        return Each(s, targets, p =>
        {
            if (p == SessionRoot(s)) throw new IOException("can't remove your workspace root");
            if (Directory.Exists(p))
            {
                if (!recursive) throw new IOException("is a directory (use rm -r)");
                Directory.Delete(p, recursive: true);
            }
            else if (File.Exists(p)) File.Delete(p);
            else throw new IOException("No such file or directory");
        }, "rm");
    }

    (bool, string) Each(Session s, List<string> args, Action<string> act, string? label = null)
    {
        if (args.Count == 0) return (false, "missing operand");
        foreach (var a in args)
        {
            var full = Resolve(s, a);
            if (full is null) return (false, $"{a}: outside your workspace");
            try { act(full); }
            catch (Exception e) when (e is IOException or UnauthorizedAccessException)
            {
                return (false, $"{(label is null ? "" : label + ": ")}{a}: {e.Message}");
            }
        }
        return (true, "");
    }

    // ---- sessions & paths ------------------------------------------------------------------

    Session? GetSession(string id)
    {
        var key = new string(id.ToLowerInvariant().Where(c => char.IsAsciiLetterOrDigit(c) || c == '-').Take(40).ToArray());
        if (key.Length == 0) key = "default";

        foreach (var (k, v) in sessions)
            if (DateTime.UtcNow - v.LastUsed > IdleLimit && sessions.TryRemove(k, out var old))
                try { Directory.Delete(SessionRoot(old), recursive: true); } catch { /* best effort */ }

        if (!sessions.TryGetValue(key, out var s))
        {
            if (sessions.Count >= MaxSessions) return null;
            s = sessions.GetOrAdd(key, _ => new Session { Dir = key });
            Directory.CreateDirectory(SessionRoot(s));
        }
        s.LastUsed = DateTime.UtcNow;
        return s;
    }

    static string SessionRoot(Session s) => Path.GetFullPath(Path.Combine(Root, s.Dir));

    // Resolves `path` against the session's cwd; null if it would escape the session folder.
    static string? Resolve(Session s, string path)
    {
        var root = SessionRoot(s);
        var full = Path.GetFullPath(path.StartsWith('/') ? Path.Combine(root, path.TrimStart('/')) : Path.Combine(root, s.Cwd, path));
        return full == root || full.StartsWith(root + "/") ? full : null;
    }

    static string Prompt(Session s) => s.Cwd == "" ? "~" : "~/" + s.Cwd;

    // ---- parsing ---------------------------------------------------------------------------

    // Words split on whitespace, with '…' and "…" quoting; an unquoted # starts a comment.
    static List<string> Tokenize(string line)
    {
        var tokens = new List<string>();
        var cur = new StringBuilder();
        var inToken = false;
        char quote = '\0';
        foreach (var c in line)
        {
            if (quote != '\0')
            {
                if (c == quote) quote = '\0'; else cur.Append(c);
            }
            else if (c is '"' or '\'') { quote = c; inToken = true; }
            else if (c == '#' && !inToken) break;
            else if (char.IsWhiteSpace(c))
            {
                if (inToken) { tokens.Add(cur.ToString()); cur.Clear(); inToken = false; }
            }
            else { cur.Append(c); inToken = true; }
        }
        if (quote != '\0') throw new FormatException("Unterminated quote.");
        if (inToken) tokens.Add(cur.ToString());
        return tokens;
    }

    static IEnumerable<List<string>> SplitAnd(List<string> tokens)
    {
        var cur = new List<string>();
        foreach (var t in tokens)
        {
            if (t == "&&") { yield return cur; cur = []; }
            else if (t is "|" or ">" or ">>" or "<" or ";" or "||")
                throw new FormatException($"`{t}` isn't supported in this terminal. Run one command at a time (or chain with &&).");
            else cur.Add(t);
        }
        yield return cur;
    }
}

record CliRequest(string Session, string Command);
record CliResponse(bool Ok, string Output, string Cwd);
