"""Module 1: C# and .NET Foundations."""
from .lesson_kit import *  # noqa: F401,F403

# ─── Module 1, lesson 1: What is C# and .NET? ───

WHAT_IS_READING = [
    h2("What is C#?"),
    p("C# (pronounced \"C sharp\") is a modern, general-purpose programming language created at Microsoft and first released in 2002. It is **statically typed** (the compiler checks the kinds of values you use before the program runs), **object-oriented**, and increasingly mixes in ideas from functional programming such as pattern matching and records. The language is open source and evolves every year; the current version, C# 14, ships with .NET 10."),
    p("People choose C# because it sits in a sweet spot: it is much safer and more structured than scripting languages, but far less ceremony than languages like C++. The compiler is strict, the tooling is excellent, and the same skills carry from web servers to desktop apps to games."),
    h2("What is .NET?"),
    p("C# is only the language. **.NET** is the platform that runs C# programs and gives you a huge library of ready-made building blocks: reading files, talking over the network, working with dates, JSON, collections, and much more. Think of C# as the grammar and .NET as the toolbox and the engine."),
    note("If you are coming from Python, the closest comparison is: C# is to .NET what Python the language is to the CPython interpreter plus its standard library. The big difference is that C# is compiled and type-checked before it runs, so many mistakes are caught while you type instead of while a user is clicking around."),
    h2("How your code becomes a running program"),
    p("You write C# source code in text files ending in `.cs`. A compiler translates it into an intermediate form called **IL** (Intermediate Language), stored in a `.dll` file. When you run the program, the .NET **runtime** (called the CLR, Common Language Runtime) turns that IL into machine code for your specific processor using a **JIT** (just-in-time) compiler, and also manages memory for you through a garbage collector."),
    code("""
// 1. You write:        Program.cs        (C# source code)
// 2. The compiler makes: app.dll         (IL, portable across Windows/macOS/Linux)
// 3. The runtime (CLR):  JIT-compiles IL to machine code as the program runs
// 4. Your CPU:           executes the machine code
"""),
    p("Because IL is not tied to one operating system, the same compiled program can run on Windows, macOS, and Linux as long as the .NET runtime is installed there. For special cases such as tiny command-line tools, .NET can also compile ahead of time (called Native AOT), but you do not need that as a beginner."),
    h2("SDK versus runtime"),
    p("Two terms trip up almost every newcomer. The **runtime** is what you need to *run* a .NET program. The **SDK** (Software Development Kit) is what you need to *build* one: it contains the compiler, the `dotnet` command-line tool, and templates, and it also includes a runtime. As a developer you install the SDK; the people who use your finished program may only need the runtime (or nothing at all if you package everything together)."),
    code("""
dotnet --list-sdks
// Output (yours will differ): 10.0.100 [C:\\Program Files\\dotnet\\sdk]

dotnet --list-runtimes
// Output (yours will differ): Microsoft.NETCore.App 10.0.0 [C:\\Program Files\\dotnet\\shared\\Microsoft.NETCore.App]
"""),
    h2("What can you build with C# and .NET?"),
    p("Almost anything: web sites and APIs with ASP.NET Core, desktop apps with WPF, WinForms, or .NET MAUI, command-line tools, background services, cloud functions, automation scripts, and games (the Unity engine uses C# for scripting). This course starts with console programs because they let you focus on the language itself, then builds up to desktop apps in the final module."),
    h2("A few words on versions"),
    p("You will see names like .NET Framework, .NET Core, and .NET 10 online, and they are not the same thing. **.NET Framework** (up to 4.8) is the older, Windows-only implementation that is now in maintenance mode. **.NET Core** was the cross-platform rewrite; it was renamed to plain **.NET** starting with version 5. A new .NET version arrives every November. Even-numbered releases such as .NET 10 are **LTS** (long-term support) releases that receive three years of support, which makes them the safe choice for learning and for production."),
    warn("Old tutorials and Stack Overflow answers often target .NET Framework. If a guide tells you to use `Web.config`, `System.Web`, or install a project type only available in Visual Studio for Windows, it is probably about the old platform. Prefer material that says .NET 6 or newer."),
    p("Here is the smallest complete C# program in modern .NET. You will write it yourself in lesson 1.3, so do not worry about the details yet:"),
    code("""
Console.WriteLine("Hello from C#!");
// Output: Hello from C#!
"""),
    tip("You do not need to memorize any of this vocabulary today. Keep one picture in mind: your C# code is compiled to IL, and the .NET runtime runs it. The terms will become familiar as you use them."),
    link("Read more on Microsoft Learn: What is .NET?", "https://learn.microsoft.com/en-us/dotnet/core/introduction"),
]

# ─── Module 1, lesson 2: Installing the .NET SDK ───

INSTALL_READING = [
    h2("What you need to get started"),
    p("To write and run C# you need two things: the **.NET SDK** (the compiler and tools) and a **code editor**. Both are free. The SDK is the essential part; you could write C# in Notepad if you had to, but a good editor gives you error squiggles, auto-complete, and a debugger, which makes learning much faster."),
    h2("Installing on Windows"),
    p("The quickest route on Windows 10 or 11 is `winget`, the package manager that ships with Windows. Open Windows Terminal or PowerShell and run:"),
    code("""
winget install Microsoft.DotNet.SDK.10
"""),
    p("Alternatively, download the installer from the .NET download page at dotnet.microsoft.com/download and double-click it. Installing the full Visual Studio IDE with the \".NET desktop development\" workload also installs an SDK for you."),
    h2("Installing on macOS and Linux"),
    p("On macOS, download the installer for your chip (Apple silicon or Intel) from the same download page, or use Homebrew. On Linux, most distributions publish the SDK in their package repositories; the package name looks like `dotnet-sdk-10.0`. Check the install guide on Microsoft Learn for your exact distribution, because the commands differ between Ubuntu, Fedora, Debian, and others."),
    code("""
# macOS with Homebrew
brew install --cask dotnet-sdk

# Ubuntu / Debian style (package availability depends on your release)
sudo apt-get update
sudo apt-get install -y dotnet-sdk-10.0
"""),
    h2("Verify the installation"),
    p("Close and reopen your terminal, then ask the `dotnet` tool for its version. If the install worked you will see a version number starting with 10:"),
    code("""
dotnet --version
// Output (yours may differ slightly): 10.0.100

dotnet --info
// Prints the SDK version, installed runtimes, and your operating system
"""),
    warn("The most common problem is `dotnet` is not recognized as a command. Your terminal reads the PATH environment variable only when it starts, so a terminal that was open during the install will not see the new tool. Close every terminal window (and restart VS Code if you use its built-in terminal) and try again."),
    note("You can have several SDK versions installed side by side. `dotnet --version` tells you which one is active in the current folder. A `global.json` file can pin a project to a specific SDK, but you will not need that for now."),
    h2("Choosing an editor"),
    p("**Visual Studio Code** is a lightweight, free editor that runs on Windows, macOS, and Linux. Install the **C# Dev Kit** extension (identifier `ms-dotnettools.csdevkit`), which brings in the C# language support, a solution explorer, and a test runner. **Visual Studio** (the Community edition is free for learners and small teams) is a full IDE for Windows with the most powerful debugger and designers; make sure you install a version recent enough to support .NET 10. **JetBrains Rider** is a popular paid alternative."),
    code("""
code --install-extension ms-dotnettools.csdevkit
"""),
    tip("If you are unsure, pick VS Code with C# Dev Kit. It works the same on every operating system, which means the instructions in this course match what you see on screen. Every concept in the course works identically in any of the editors."),
    p("To confirm everything works end to end, create and run a throwaway project. You will understand each command by the end of lesson 1.4:"),
    code("""
dotnet new console -o Hello
cd Hello
dotnet run
// Output: Hello, World!
"""),
    link("Read more on Microsoft Learn: Install .NET on Windows", "https://learn.microsoft.com/en-us/dotnet/core/install/windows"),
]

# ─── Module 1, lesson 3: Your First Program ───

FIRST_PROGRAM_READING = [
    h2("The smallest C# program"),
    p("In modern C#, a complete program can be a single line. When you create a console project with `dotnet new console`, the file `Program.cs` contains this:"),
    code("""
Console.WriteLine("Hello, World!");
// Output: Hello, World!
"""),
    p("`Console` is a class from the .NET library that represents the terminal window. `WriteLine` is a **method** (a named action) on it, and the text inside the parentheses is the **argument** you hand to that action. The dot connects the two: \"on the Console, do WriteLine\". The trailing semicolon ends the **statement**, the way a period ends a sentence."),
    h2("Top-level statements"),
    p("You may have seen older C# examples that wrap everything in a class with a `Main` method. Since C# 9 you can skip that: the statements you write at the top of the file become the program's entry point automatically. These are called **top-level statements**, and a project can have them in only one file. They are perfect for learning because there is nothing between you and the code you care about."),
    code("""
// The older, explicit form. Both programs do exactly the same thing.
class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("Hello, World!");
    }
}
"""),
    note("Python programmers: top-level statements feel like a Python script, but remember that C# is compiled. The whole file is checked first, so a typo on the last line stops the program from running at all, rather than crashing halfway through."),
    h2("using directives and implicit usings"),
    p("Classes live in **namespaces**, which work like folders. `Console` lives in the `System` namespace, so its full name is `System.Console`. A `using System;` line at the top of a file lets you write the short name. In modern .NET projects, `ImplicitUsings` is switched on, which adds the most common namespaces (`System`, `System.IO`, `System.Linq`, `System.Collections.Generic`, and a few more) to every file for you. That is why `Console.WriteLine` works without any `using` line in this course."),
    h2("Write, WriteLine, and escape sequences"),
    p("`Console.WriteLine` prints text and then moves to a new line. `Console.Write` prints text and stays on the same line. Text in quotes is called a **string literal**. Inside a string, a backslash starts an **escape sequence**, a special code for a character you cannot type directly."),
    code("""
Console.Write("Loading");
Console.Write("...");
Console.WriteLine("done");
// Output: Loading...done

Console.WriteLine("Line one\\nLine two");
// Output:
// Line one
// Line two

Console.WriteLine("Name:\\tAda");        // \\t is a tab
Console.WriteLine("She said \\"hi\\"");  // \\" is a literal quote
Console.WriteLine("C:\\\\dev\\\\hello");    // \\\\ is a literal backslash
// Output: C:\\dev\\hello
"""),
    h2("Comments"),
    p("Comments are notes for humans; the compiler ignores them. Use `//` for a single line and `/* ... */` for a block. A comment starting with `///` is an XML documentation comment that editors show in tooltips when you hover over a method. Write comments to explain *why* you did something, not to repeat what the code already says."),
    code("""
// This is a single-line comment.
Console.WriteLine("Visible");   // A comment can also follow code.

/* This comment
   spans several lines. */
"""),
    h2("C# is picky, and that is helpful"),
    p("C# is **case-sensitive**: `Console` and `console` are different names. Every statement ends with a semicolon, and curly braces must come in matching pairs. Whitespace and blank lines do not change the meaning of your code, so use them freely to keep it readable. When you break a rule, the compiler reports an error with a code like `CS1002` and the line number, and the program will not run until you fix it."),
    warn("A very common beginner mistake is writing `console.writeline(\"Hi\");` in lowercase, or forgetting the semicolon. Errors such as `CS0103: The name 'console' does not exist in the current context` and `CS1002: ; expected` almost always mean a typo. Read the line number in the message and look at the line just above it too, because a missing semicolon is often reported on the next line."),
    tip("When you see a compiler error, fix only the first one and rebuild. Later errors are frequently side effects of the first and disappear on their own."),
    link("Read more on Microsoft Learn: Hello World", "https://learn.microsoft.com/en-us/dotnet/csharp/tour-of-csharp/tutorials/hello-world"),
]

FIRST_PROGRAM_CODEALONG = codealong(
    "Code Along: Hello, C#",
    "Type each step into one Program.cs file, in order. The steps build on each other, so keep everything from the earlier steps.",
    [
        step(
            "Say hello",
            "Start with the classic first program. Notice the quotes around the text and the semicolon at the end.",
            """
// My first C# program
Console.WriteLine("Hello, C#!");
""",
        ),
        step(
            "Write versus WriteLine",
            "`Write` keeps the cursor on the same line, while `WriteLine` ends the line. Add these below your first line to see the difference.",
            """
Console.Write("Compiling");
Console.Write("...");
Console.WriteLine(" done");
""",
        ),
        step(
            "Escape sequences",
            "Use `\\n` for a new line, `\\t` for a tab, and `\\\"` for a quote character inside a string.",
            """
Console.WriteLine("First line\\nSecond line");
Console.WriteLine("Column A\\tColumn B");
Console.WriteLine("He said \\"C# is fun\\"");
""",
        ),
        step(
            "Comments and the full name",
            "Comments are ignored by the compiler. Here the full name `System.Console` does the same thing as `Console`, which shows that `Console` lives in the `System` namespace.",
            """
/* Block comments can span
   several lines. */
System.Console.WriteLine("Full name works too"); // Same as Console.WriteLine
""",
        ),
        step(
            "Print a small banner",
            "Combine what you have learned to print a three-line banner. A backslash in a string must be doubled, so `\\\\` prints one backslash.",
            """
Console.WriteLine("+----------------+");
Console.WriteLine("|  C:\\\\journey    |");
Console.WriteLine("+----------------+");
""",
        ),
    ],
)

FIRST_PROGRAM_LAB = lab(
    "Lab: Welcome Banner",
    "Beginner",
    "Write a small program that prints a welcome message using Write, WriteLine, and escape sequences. The output must match exactly, so pay attention to spaces and punctuation.",
    [
        "Start with a comment on the first line (any text you like), then print the line `=== C# Journey ===` with `Console.WriteLine`.",
        "Print `Name:` followed by a tab character and then `Ada` on one line, using the `\\t` escape sequence.",
        "Print a line that contains the text `Quote: \"Hello, C#!\"`, with the double quotes included in the output, using `\\\"`.",
        "Print the line `Path: C:\\dev\\hello` (single backslashes in the output) using `\\\\`.",
        "Using three separate `Console.Write` / `Console.WriteLine` calls, print `Loading`, then `...`, then `done` so that they appear on one line as `Loading...done`.",
        "Finally, print `Line one` and `Line two` on two separate lines using a single `Console.WriteLine` call and the `\\n` escape sequence.",
    ],
    "=== C# Journey ===\nName:\tAda\nQuote: \"Hello, C#!\"\nPath: C:\\dev\\hello\nLoading...done\nLine one\nLine two",
    "Each escape sequence starts with a backslash inside the quotes. For the loading line, the first two calls use Console.Write (no line break) and only the last one uses Console.WriteLine. Remember that the name `Console` starts with a capital C.",
)

FIRST_PROGRAM_SOLUTION = r'''// Welcome banner
Console.WriteLine("=== C# Journey ===");
Console.WriteLine("Name:\tAda");
Console.WriteLine("Quote: \"Hello, C#!\"");
Console.WriteLine("Path: C:\\dev\\hello");
Console.Write("Loading");
Console.Write("...");
Console.WriteLine("done");
Console.WriteLine("Line one\nLine two");
'''

# ─── Module 1, lesson 4: The dotnet CLI ───

CLI_READING = [
    h2("One tool for the whole workflow"),
    p("Everything you do outside the editor, such as creating a project, building it, running it, adding libraries, and running tests, goes through a single command-line program: `dotnet`. Editors like Visual Studio and VS Code call the same commands behind their buttons, so learning the CLI (command-line interface) means you understand what the buttons are doing, and you can work anywhere there is a terminal."),
    code("""
dotnet --help          # list all commands
dotnet new --help      # help for one command
dotnet --version       # the active SDK version
"""),
    h2("dotnet new: create a project"),
    p("`dotnet new` creates files from a **template**. The most important templates for this course are `console` (a command-line app), `classlib` (a reusable library), and `xunit` (a test project). Use `-o` to choose the output folder (it is created for you) and `-n` to set the project name."),
    code("""
dotnet new list                    # see every installed template
dotnet new console -o Hello        # creates Hello/Hello.csproj and Hello/Program.cs
cd Hello
"""),
    h2("What a project looks like"),
    p("A project is a folder with a **project file** ending in `.csproj` plus your `.cs` source files. The project file is a small XML document that tells the compiler what to build. Open the one the console template created and you will see something like this:"),
    code("""
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net10.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
  </PropertyGroup>

</Project>
"""),
    p("`OutputType` says the result is an executable program. `TargetFramework` chooses the .NET version (`net10.0`). `ImplicitUsings` is the setting from lesson 1.3 that gives you `System` and friends for free, and `Nullable` turns on the compiler's null-safety checks, which you will meet in module 2."),
    h2("dotnet run and dotnet build"),
    p("`dotnet run` compiles your project (if anything changed) and starts it. `dotnet build` only compiles. The compiler output goes into a `bin` folder, and temporary files go into `obj`; both are generated, so you never edit them and you normally do not commit them to source control."),
    code("""
dotnet build                       # compile only; output goes to bin/Debug/net10.0/
dotnet build -c Release            # optimized build for shipping
dotnet run                         # build (if needed) and run
dotnet run -- Ada 42               # everything after -- goes to your program as arguments
"""),
    warn("Run these commands from the folder that contains the `.csproj` file (or pass the path with `--project`). If you are one folder too high you will see `Couldn't find a project to run`, and if you forget the `--` before your own arguments, `dotnet` may try to interpret them as options for itself."),
    h2("dotnet add package: use libraries from NuGet"),
    p("Most real programs use code that other people wrote. **NuGet** is the public package catalog for .NET, and `dotnet add package` downloads a package and records it in your `.csproj` file. The download step is called a **restore**, and `dotnet build` and `dotnet run` perform it automatically when needed."),
    code("""
dotnet add package Humanizer       # adds a <PackageReference> to the .csproj
dotnet remove package Humanizer    # removes it again
dotnet list package                # show what the project uses
"""),
    h2("dotnet test and dotnet watch"),
    p("`dotnet test` builds a test project and runs every test in it, reporting how many passed. You create one with a template such as `dotnet new xunit` and connect it to your code with `dotnet add reference`. `dotnet watch` wraps another command and re-runs it every time you save a file, which gives you a fast feedback loop while you experiment."),
    code("""
dotnet new xunit -o Hello.Tests
dotnet add Hello.Tests reference Hello/Hello.csproj
dotnet test                        # run the tests (from a folder with a test project or solution)

dotnet watch run                   # re-run the program whenever a .cs file is saved
"""),
    tip("`dotnet watch run` is the best way to follow along with this course locally. Keep a terminal open next to your editor, edit and save, and the new output appears immediately."),
    h2("Passing arguments and returning an exit code"),
    p("A console program receives its command-line arguments in a variable called `args`, which top-level statements create for you automatically. A program can also end with a number called an **exit code**: `0` conventionally means success and anything else means failure. Scripts and build servers check this number to decide whether the step worked."),
    code("""
Console.WriteLine($"Number of arguments: {args.Length}");
return 0;   // exit code 0 = success
// Run with: dotnet run -- Ada 42
// Output: Number of arguments: 2
"""),
    note("Other commands you will meet later: `dotnet publish` creates a folder you can deploy to another machine, `dotnet new sln` creates a solution file that groups several projects, and `dotnet clean` deletes build output. In .NET 10 you can also run a single C# file directly with `dotnet run file.cs`, without creating a project first."),
    link("Read more on Microsoft Learn: .NET CLI overview", "https://learn.microsoft.com/en-us/dotnet/core/tools/"),
]

CLI_CODEALONG = codealong(
    "Code Along: Program Arguments and Exit Codes",
    "These steps use the variable `args` and an exit code, the two ways a console program talks to the dotnet CLI. Type them into one Program.cs file. In this runner `args` is empty, but with `dotnet run -- Ada 42` it would hold two items.",
    [
        step(
            "Announce the program",
            "Start with a short message so you can tell when the program started.",
            """
Console.WriteLine("Tool started");
""",
        ),
        step(
            "Count the arguments",
            "`args` is an array of text values supplied by whoever ran the program. `args.Length` is how many there are.",
            """
Console.WriteLine($"Number of arguments: {args.Length}");
""",
        ),
        step(
            "Check for no arguments",
            "A comparison produces a `bool`. Here it tells you whether the user passed anything at all.",
            """
bool noArguments = args.Length == 0;
Console.WriteLine($"Ran without arguments: {noArguments}");
""",
        ),
        step(
            "Return an exit code",
            "End the program with `return 0;` to report success. This must be the last statement in the file. After running with `dotnet run` you can read the code from your shell with `echo $?` (macOS/Linux) or `echo $LASTEXITCODE` (PowerShell).",
            """
Console.WriteLine("Tool finished");
return 0;
""",
        ),
    ],
)

LESSONS = {
    (1, 1): lesson(
        subtitle="Understand what C# and .NET are, how your code becomes a running program, and which .NET version to learn.",
        reading=WHAT_IS_READING,
    ),
    (1, 2): lesson(
        subtitle="Install the .NET 10 SDK on your computer, verify it from the terminal, and choose an editor.",
        reading=INSTALL_READING,
    ),
    (1, 3): lesson(
        subtitle="Write and run your first C# program, and learn how statements, comments, and escape sequences work.",
        reading=FIRST_PROGRAM_READING,
        codealong=FIRST_PROGRAM_CODEALONG,
        lab=FIRST_PROGRAM_LAB,
    ),
    (1, 4): lesson(
        subtitle="Use the dotnet command line to create, build, run, extend, test, and watch a project.",
        reading=CLI_READING,
        codealong=CLI_CODEALONG,
    ),
}

# Reference solutions, used only by verify_content.py (never sent to the learner).
SOLUTIONS = {
    (1, 3): FIRST_PROGRAM_SOLUTION,
}
