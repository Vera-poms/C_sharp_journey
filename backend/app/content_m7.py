"""Module 7: Intermediate C# Patterns."""
from .lesson_kit import *  # noqa: F401,F403

# ─── 7.1 Delegates and Events ───

DELEGATES_READING = [
    h2("Passing behavior around"),
    p("""So far you have passed **data** into methods: numbers, strings, lists. A **delegate** lets you pass *behavior*: a reference to a method that can be stored in a variable, handed to another method, and called later. LINQ's `Where(n => n > 10)` from the last module was doing exactly that; the lambda is a delegate."""),
    p("""A delegate type describes a method shape: its parameter types and return type. Any method with a matching shape can be assigned to it."""),
    code(r'''
delegate int BinaryOp(int a, int b);     // a custom delegate type

static int Add(int a, int b) => a + b;

BinaryOp op = Add;                // point the variable at a method
Console.WriteLine(op(3, 4));      // Output: 7  (call it like a method)
op = (a, b) => a * b;             // or at a lambda
Console.WriteLine(op(3, 4));      // Output: 12
'''),
    h2("Action, Func, and Predicate"),
    p("""You rarely need to declare your own delegate types, because .NET ships generic ones for nearly every shape. `Action` is for methods that return nothing (`void`). `Func` is for methods that return a value, and its **last** type argument is the return type. `Predicate<T>` is a method that takes a `T` and returns `bool`."""),
    code(r'''
Action<string> shout = text => Console.WriteLine(text.ToUpper());
Func<int, int, int> add = (a, b) => a + b;     // two ints in, int out
Func<double> pi = () => 3.14159;               // nothing in, double out
Predicate<int> isEven = n => n % 2 == 0;

shout("hello");                  // Output: HELLO
Console.WriteLine(add(2, 3));    // Output: 5
Console.WriteLine(pi());         // Output: 3.14159
Console.WriteLine(isEven(10));   // Output: True
'''),
    h2("Lambdas"),
    p("""A **lambda expression** is a method with no name, written inline as `parameters => body`. If the body is a single expression, that is the return value. For several statements use braces and `return`. Lambdas can also read local variables from the code around them; this is called **capturing**."""),
    code(r'''
int threshold = 10;
Func<int, bool> isBig = n => n > threshold;   // captures 'threshold'
Console.WriteLine(isBig(15));                 // Output: True

Func<int, string> describe = n =>
{
    if (n < 0) return "negative";
    return n == 0 ? "zero" : "positive";
};
Console.WriteLine(describe(-3));              // Output: negative
'''),
    p("""The real payoff is writing methods that accept behavior, so one method can do many jobs:"""),
    code(r'''
static List<int> Filter(List<int> items, Predicate<int> keep)
{
    var result = new List<int>();
    foreach (int item in items)
    {
        if (keep(item)) result.Add(item);
    }
    return result;
}

var nums = new List<int> { 1, 2, 3, 4, 5, 6 };
Console.WriteLine(string.Join(", ", Filter(nums, n => n % 2 == 0)));  // Output: 2, 4, 6
Console.WriteLine(string.Join(", ", Filter(nums, n => n > 4)));       // Output: 5, 6
'''),
    warn("""**Common mistake:** a lambda captures the **variable**, not a copy of its value. If you change `threshold` after creating `isBig`, the lambda sees the new number the next time it is called. This is the same effect that surprised you with LINQ's deferred execution."""),
    h2("Events: publish and subscribe"),
    p("""An **event** is a delegate with safety rails, built for the **publisher/subscriber** pattern. The publisher announces 'something happened' without knowing or caring who is listening. Subscribers register a handler method. Outside code can only add (`+=`) or remove (`-=`) handlers; it cannot call the event or wipe out other people's subscriptions. That is the difference between an `event` and a public delegate field."""),
    p("""The standard shape uses `EventHandler<TEventArgs>`: a handler receives `object? sender` (who raised it) and an arguments object carrying the details."""),
    code(r'''
class ThresholdReachedEventArgs : EventArgs
{
    public int Total { get; }
    public ThresholdReachedEventArgs(int total) => Total = total;
}

class Counter
{
    public event EventHandler<ThresholdReachedEventArgs>? ThresholdReached;
    private int _total;
    private readonly int _threshold;

    public Counter(int threshold) => _threshold = threshold;

    public void Add(int amount)
    {
        _total += amount;
        if (_total >= _threshold)
        {
            ThresholdReached?.Invoke(this, new ThresholdReachedEventArgs(_total));
        }
    }
}

var counter = new Counter(10);
void OnReached(object? sender, ThresholdReachedEventArgs e) =>
    Console.WriteLine($"Reached {e.Total}!");

counter.ThresholdReached += OnReached;     // subscribe
counter.Add(12);                           // Output: Reached 12!
counter.ThresholdReached -= OnReached;     // unsubscribe
counter.Add(1);                            // (no output)
'''),
    p("""The `?.Invoke(...)` matters: an event with no subscribers is `null`, and calling it directly would throw `NullReferenceException`. `?.` means 'call it only if someone is listening'."""),
    warn("""**Common mistake:** forgetting to unsubscribe. The publisher holds a reference to every subscriber, so a subscriber that never calls `-=` cannot be cleaned up while the publisher lives, and its handler keeps running. Also note you can only unsubscribe a **named** method or a stored delegate; `-=` with a fresh lambda does not remove the earlier lambda."""),
    tip("""Handlers run in the order they subscribed, on the same thread that raised the event, one after another. If a handler throws, the remaining handlers do not run."""),
    link("Read more on Microsoft Learn: Events", "https://learn.microsoft.com/en-us/dotnet/csharp/events-overview"),
]

DELEGATES_CODEALONG = codealong(
    "Code Along: Delegates, Lambdas, and Events",
    "Type each step into one Program.cs in order. Steps that declare a type go at the bottom of the file.",
    [
        step(
            "Action, Func, and Predicate",
            "Store behavior in variables. `Func` lists its return type last; `Action` returns nothing; `Predicate<T>` returns a bool.",
            r'''
Action<string> shout = text => Console.WriteLine(text.ToUpper());
Func<int, int, int> add = (a, b) => a + b;
Predicate<int> isEven = n => n % 2 == 0;

shout("hello delegates");
Console.WriteLine($"2 + 3 = {add(2, 3)}");
Console.WriteLine($"Is 10 even? {isEven(10)}");
''',
        ),
        step(
            "Pass a lambda to your own method",
            "Write a method that accepts a `Predicate<int>`, then call it with different lambdas. Also see a lambda capture a local variable.",
            r'''
List<int> Filter(List<int> items, Predicate<int> keep)
{
    var result = new List<int>();
    foreach (int item in items)
    {
        if (keep(item)) result.Add(item);
    }
    return result;
}

var nums = new List<int> { 1, 2, 3, 4, 5, 6 };
Console.WriteLine($"Evens: {string.Join(", ", Filter(nums, n => n % 2 == 0))}");
int min = 4;
Console.WriteLine($"At least {min}: {string.Join(", ", Filter(nums, n => n >= min))}");
''',
        ),
        step(
            "Declare a publisher",
            "Add the event arguments record and the `Counter` class at the **bottom** of the file. The event is raised with `?.Invoke` so it is safe when nobody is subscribed.",
            r'''
class ThresholdReachedEventArgs : EventArgs
{
    public int Total { get; }
    public ThresholdReachedEventArgs(int total) => Total = total;
}

class Counter
{
    public event EventHandler<ThresholdReachedEventArgs>? ThresholdReached;
    private int _total;
    private readonly int _threshold;

    public Counter(int threshold) => _threshold = threshold;

    public void Add(int amount)
    {
        _total += amount;
        Console.WriteLine($"Total is now {_total}");
        if (_total >= _threshold)
        {
            ThresholdReached?.Invoke(this, new ThresholdReachedEventArgs(_total));
        }
    }
}
''',
            at="bottom",
        ),
        step(
            "Subscribe",
            "Create a counter, subscribe a named handler with `+=`, and add numbers until the threshold is crossed.",
            r'''
var counter = new Counter(10);

void OnReached(object? sender, ThresholdReachedEventArgs e)
{
    Console.WriteLine($"  Event: threshold reached at {e.Total}");
}

counter.ThresholdReached += OnReached;
counter.Add(4);
counter.Add(8);
''',
        ),
        step(
            "Add a second subscriber, then unsubscribe",
            "Several subscribers can listen to one event. Remove one with `-=` and notice it no longer runs.",
            r'''
counter.ThresholdReached += (sender, e) => Console.WriteLine("  Second listener also heard it");
counter.Add(1);

counter.ThresholdReached -= OnReached;
Console.WriteLine("Unsubscribed the first handler");
counter.Add(1);
''',
        ),
    ],
)

DELEGATES_LAB = lab(
    "Lab: Thermostat Events",
    "Intermediate",
    "Build a publisher that raises an event when its temperature changes, and attach and detach subscribers. Follow the names and the order of statements exactly.",
    [
        "At the bottom of the file declare a class `TemperatureChangedEventArgs` that inherits `EventArgs` and has two read-only properties `int Old` and `int New` set by a constructor `(int oldValue, int newValue)`; and a class `Thermostat` with a public `event EventHandler<TemperatureChangedEventArgs>? TemperatureChanged;`",
        "`Thermostat` has a private field starting at `20` and a method `SetTemperature(int value)`. If `value` equals the current value it does nothing. Otherwise it stores the new value and raises the event with the old and new values (use `?.Invoke`)",
        "In the program: create a `Thermostat`. Subscribe a **named local method** `Log` that prints `Logger: <Old> -> <New>`. Subscribe a second handler `Alarm` (also a named method) that uses a `Predicate<int> tooHot = t => t > 30;` and prints `ALARM: <New> is too hot!` when `tooHot(e.New)` is true. Subscribe `Log` first, then `Alarm`",
        "Call `SetTemperature` with 25, then 25 again, then 31. Then unsubscribe `Alarm` with `-=` and call `SetTemperature(35)`",
        "Finally create `Func<int, int> toFahrenheit = c => c * 9 / 5 + 32;` and print `35 C = ` followed by `toFahrenheit(35)` and ` F`",
    ],
    """
Logger: 20 -> 25
Logger: 25 -> 31
ALARM: 31 is too hot!
Logger: 31 -> 35
35 C = 95 F
""",
    "The class needs `private int _current = 20;`. Raise the event with `TemperatureChanged?.Invoke(this, new TemperatureChangedEventArgs(old, value));`. Local methods used with `+=` and `-=` need a signature of `(object? sender, TemperatureChangedEventArgs e)`. The second `SetTemperature(25)` prints nothing because the value did not change.",
)

DELEGATES_SOLUTION = r'''
var thermostat = new Thermostat();
var tooHot = new Predicate<int>(t => t > 30);

void Log(object? sender, TemperatureChangedEventArgs e)
{
    Console.WriteLine($"Logger: {e.Old} -> {e.New}");
}

void Alarm(object? sender, TemperatureChangedEventArgs e)
{
    if (tooHot(e.New))
    {
        Console.WriteLine($"ALARM: {e.New} is too hot!");
    }
}

thermostat.TemperatureChanged += Log;
thermostat.TemperatureChanged += Alarm;

thermostat.SetTemperature(25);
thermostat.SetTemperature(25);
thermostat.SetTemperature(31);
thermostat.TemperatureChanged -= Alarm;
thermostat.SetTemperature(35);

Func<int, int> toFahrenheit = c => c * 9 / 5 + 32;
Console.WriteLine($"35 C = {toFahrenheit(35)} F");

class TemperatureChangedEventArgs : EventArgs
{
    public int Old { get; }
    public int New { get; }
    public TemperatureChangedEventArgs(int oldValue, int newValue)
    {
        Old = oldValue;
        New = newValue;
    }
}

class Thermostat
{
    public event EventHandler<TemperatureChangedEventArgs>? TemperatureChanged;
    private int _current = 20;

    public void SetTemperature(int value)
    {
        if (value == _current) return;
        int old = _current;
        _current = value;
        TemperatureChanged?.Invoke(this, new TemperatureChangedEventArgs(old, value));
    }
}
'''

# ─── 7.2 async and await ───

ASYNC_READING = [
    h2("Why async?"),
    p("""Most programs spend much of their time **waiting**: for a web server to answer, for a file to be read from disk, for a database. While a normal method waits, its thread sits blocked and can do nothing else. In a desktop app that means a frozen window; in a web server it means fewer requests handled at once."""),
    p("""**Asynchronous** code lets a method say 'I am waiting; go do something else and come back to me when it is ready.' This is for **I/O-bound** work (waiting on the outside world). It is different from **CPU-bound** work (heavy calculation), where the processor is genuinely busy and `async` alone does not make it faster. For that you offload work to another thread with `Task.Run`."""),
    h2("Task and Task<T>"),
    p("""A `Task` represents an operation that may still be running; think of it as a receipt for work in progress. `Task` means 'completes with no result' (like `void`), and `Task<T>` means 'will eventually produce a `T`'. An `async` method returns one of these."""),
    code(r'''
async Task<int> GetNumberAsync()
{
    await Task.Delay(100);     // pretend this is a slow network call
    return 42;
}

async Task SayHelloAsync()
{
    await Task.Delay(50);
    Console.WriteLine("Hello after a short wait");
}
'''),
    p("""`await` is the key word. It means 'pause **this method** until the task finishes, but do not block the thread while waiting'. When the task completes, the method resumes right after the `await` and you get the result. Only methods marked `async` can contain `await`. By convention, async method names end in `Async`."""),
    h2("Top-level await"),
    p("""Your `Program.cs` top-level statements may use `await` directly. The compiler quietly turns them into an `async Task Main`, so you can write the following with no ceremony."""),
    code(r'''
int number = await GetNumberAsync();
Console.WriteLine($"Got {number}");       // Output: Got 42
await SayHelloAsync();                    // Output: Hello after a short wait
'''),
    h2("Running several tasks together"),
    p("""Awaiting tasks one after another runs them one after another. To run several waits **at the same time**, start them all first (calling the method returns a running task) and then `await Task.WhenAll(...)`. If each takes a second, the total is about one second, not three. `WhenAll` on `Task<T>` tasks gives back an array of results **in the same order you passed the tasks**, regardless of which finished first, so your output stays predictable."""),
    code(r'''
async Task<string> LoadAsync(string name, int delayMs)
{
    await Task.Delay(delayMs);
    return name.ToUpper();
}

Task<string> a = LoadAsync("slow", 200);    // starts running immediately
Task<string> b = LoadAsync("fast", 10);
string[] results = await Task.WhenAll(a, b);
Console.WriteLine(string.Join(", ", results));   // Output: SLOW, FAST  (argument order)
'''),
    tip("""When you want deterministic output from concurrent work, do not print from inside the tasks (the order would depend on timing). Collect the results and print them after the `await`, in a fixed order."""),
    h2("Errors and CPU work"),
    p("""If an async method throws, the exception is stored in the task and re-thrown at the `await`, so an ordinary `try/catch` around the `await` handles it. For CPU-heavy work, `Task.Run` runs a lambda on a thread-pool thread and gives you a task to await."""),
    code(r'''
async Task<int> FailAsync()
{
    await Task.Delay(10);
    throw new InvalidOperationException("boom");
}

try
{
    await FailAsync();
}
catch (InvalidOperationException ex)
{
    Console.WriteLine($"Caught: {ex.Message}");   // Output: Caught: boom
}

int sum = await Task.Run(() => Enumerable.Range(1, 100).Sum());
Console.WriteLine(sum);                            // Output: 5050
'''),
    warn("""**Common mistake: `async void`.** An `async void` method cannot be awaited, and its exceptions cannot be caught by the caller; they can crash the whole program. Always return `Task` or `Task<T>`. The only legitimate use of `async void` is an event handler."""),
    warn("""**Common mistake: blocking with `.Result` or `.Wait()`.** Writing `GetNumberAsync().Result` freezes the current thread until the task finishes. In apps with a UI or request context, that can **deadlock**: the task needs the blocked thread to continue, and the thread is waiting for the task. Use `await` all the way up instead. It is also easy to forget `await` on a call, which leaves the work running unobserved and loses its exceptions."""),
    link("Read more on Microsoft Learn: Asynchronous programming", "https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/"),
]

ASYNC_CODEALONG = codealong(
    "Code Along: async and await",
    "Type each step into one Program.cs in order. Top-level statements can use `await` directly.",
    [
        step(
            "Your first async method",
            "Write a `Task<int>` method that waits and then returns a value. `await` pauses the method without blocking the thread.",
            r'''
async Task<int> GetPriceAsync(string item)
{
    await Task.Delay(50);      // pretend to call a slow service
    return item switch
    {
        "apple" => 3,
        "bread" => 5,
        _ => 1,
    };
}

int applePrice = await GetPriceAsync("apple");
Console.WriteLine($"apple costs {applePrice}");
''',
        ),
        step(
            "Await in sequence",
            "Each `await` finishes before the next line runs, so this output is always in the same order.",
            r'''
int bread = await GetPriceAsync("bread");
int milk = await GetPriceAsync("milk");
Console.WriteLine($"bread costs {bread}, milk costs {milk}");
''',
        ),
        step(
            "Run tasks together with Task.WhenAll",
            "Calling an async method starts it. Collect the tasks, then await them all at once. The results come back in the order you gave the tasks.",
            r'''
Task<int> t1 = GetPriceAsync("apple");
Task<int> t2 = GetPriceAsync("bread");
Task<int> t3 = GetPriceAsync("milk");
int[] prices = await Task.WhenAll(t1, t2, t3);
Console.WriteLine($"Prices: {string.Join(", ", prices)}");
Console.WriteLine($"Total: {prices.Sum()}");
''',
        ),
        step(
            "Handle an exception from an await",
            "A failure inside an async method surfaces at the `await`, where an ordinary try/catch can handle it.",
            r'''
async Task CheckAsync(int quantity)
{
    await Task.Delay(10);
    if (quantity <= 0) throw new InvalidOperationException("Quantity must be positive");
    Console.WriteLine($"Quantity {quantity} is fine");
}

await CheckAsync(2);
try
{
    await CheckAsync(0);
}
catch (InvalidOperationException ex)
{
    Console.WriteLine($"Caught: {ex.Message}");
}
''',
        ),
        step(
            "Offload CPU work with Task.Run",
            "Use `Task.Run` for a heavy calculation so it runs on another thread, and `await` its result.",
            r'''
long bigSum = await Task.Run(() =>
{
    long total = 0;
    for (int i = 1; i <= 1_000_000; i++) total += i;
    return total;
});
Console.WriteLine($"Sum of 1..1,000,000 = {bigSum}");
''',
        ),
    ],
)

ASYNC_LAB = lab(
    "Lab: Async Price Lookup",
    "Intermediate",
    "Write async methods, await them in sequence and together, handle a failure, and offload a calculation. Print only after awaiting so the output is deterministic.",
    [
        "Write a local method `async Task<int> GetPriceAsync(string item)` that does `await Task.Delay(10)`, then returns 3 for `apple`, 5 for `bread`, 4 for `milk`, and for anything else throws `new InvalidOperationException($\"Unknown item: {item}\")`",
        "Sequentially `await` the price of `apple` and `bread` and print `apple: 3` and `bread: 5` (using the awaited values)",
        "Start tasks for `apple`, `bread`, and `milk`, then use `await Task.WhenAll(...)` to get an `int[]`. Print `Total via WhenAll: ` with the sum, then `Prices: ` with the array joined by `, `",
        "Call `GetPriceAsync(\"cheese\")` inside `try`/`catch (InvalidOperationException ex)` and print `Error: ` followed by `ex.Message`",
        "Use `await Task.Run(...)` to add the integers 1 to 1000 with a `for` loop and print `Task.Run sum: ` with the result",
    ],
    """
apple: 3
bread: 5
Total via WhenAll: 12
Prices: 3, 5, 4
Error: Unknown item: cheese
Task.Run sum: 500500
""",
    "A switch expression keeps the price lookup short: `item switch { \"apple\" => 3, ..., _ => throw new InvalidOperationException(...) }`. Remember the `await` before `Task.WhenAll`; without it you get the task, not the array. Print after the awaits, not from inside the tasks.",
)

ASYNC_SOLUTION = r'''
async Task<int> GetPriceAsync(string item)
{
    await Task.Delay(10);
    return item switch
    {
        "apple" => 3,
        "bread" => 5,
        "milk" => 4,
        _ => throw new InvalidOperationException($"Unknown item: {item}"),
    };
}

int apple = await GetPriceAsync("apple");
int bread = await GetPriceAsync("bread");
Console.WriteLine($"apple: {apple}");
Console.WriteLine($"bread: {bread}");

Task<int> a = GetPriceAsync("apple");
Task<int> b = GetPriceAsync("bread");
Task<int> c = GetPriceAsync("milk");
int[] prices = await Task.WhenAll(a, b, c);
Console.WriteLine($"Total via WhenAll: {prices.Sum()}");
Console.WriteLine($"Prices: {string.Join(", ", prices)}");

try
{
    await GetPriceAsync("cheese");
}
catch (InvalidOperationException ex)
{
    Console.WriteLine($"Error: {ex.Message}");
}

int sum = await Task.Run(() =>
{
    int total = 0;
    for (int i = 1; i <= 1000; i++) total += i;
    return total;
});
Console.WriteLine($"Task.Run sum: {sum}");
'''

# ─── 7.3 File I/O ───

FILEIO_READING = [
    h2("Persisting data"),
    p("""Variables vanish when your program ends. **Files** are how data survives: settings, logs, saved games, exported reports. C# reads and writes files through the `System.IO` namespace, which is already imported for you. Two ideas cover most needs: quick one-call helpers on the `File` class, and **streams** (`StreamReader` / `StreamWriter`) for working line by line."""),
    h2("Building paths safely"),
    p("""Windows writes paths with `\\`, Linux and macOS with `/`. Never glue them together with string concatenation. `Path.Combine` joins pieces using the right separator for the current system, and other `Path` methods pick paths apart. `Path.GetTempPath()` returns the operating system's temporary folder, a safe place to experiment."""),
    code(r'''
string dir = Path.Combine(Path.GetTempPath(), "csharp_demo");
string file = Path.Combine(dir, "notes.txt");

Console.WriteLine(Path.GetFileName(file));        // Output: notes.txt
Console.WriteLine(Path.GetExtension(file));       // Output: .txt
Console.WriteLine(Path.GetFileNameWithoutExtension(file)); // Output: notes

Directory.CreateDirectory(dir);        // creates it (does nothing if it already exists)
Console.WriteLine(Directory.Exists(dir));   // Output: True
'''),
    h2("One-call file helpers"),
    p("""The `File` class has helpers that open, read or write, and close the file in one call. `WriteAllText` creates the file or **replaces** it if it exists. `AppendAllText` adds to the end. `ReadAllText` returns everything as one string, and `ReadAllLines` returns a `string[]` with one entry per line. Files are written as UTF-8 text by default."""),
    code(r'''
File.WriteAllText(file, "first line\nsecond line\n");
File.AppendAllText(file, "third line\n");

string all = File.ReadAllText(file);
string[] lines = File.ReadAllLines(file);
Console.WriteLine(lines.Length);          // Output: 3
Console.WriteLine(lines[2]);              // Output: third line
Console.WriteLine(File.Exists(file));     // Output: True

File.WriteAllLines(file, ["a", "b", "c"]);   // one entry per line
'''),
    p("""`File.ReadLines` looks like `ReadAllLines` but returns a lazy sequence that reads the file as you loop. That makes it the better choice for large files, or when you only want the first few lines. It also means you can chain LINQ onto it."""),
    code(r'''
foreach (string line in File.ReadLines(file))
{
    Console.WriteLine(line);              // streams one line at a time
}
int count = File.ReadLines(file).Count(l => l.StartsWith("a"));
'''),
    warn("""**Common mistake:** hard-coding a path like `"C:\\temp\\data.txt"`. It fails on Linux and macOS, and the folder may not exist or be writable. Build paths with `Path.Combine` from a known base such as `Path.GetTempPath()`. Also remember `WriteAllText` silently **overwrites** an existing file; use `AppendAllText` when you mean to add."""),
    h2("StreamWriter and StreamReader with using"),
    p("""For incremental work (writing many lines in a loop, reading a line at a time) open a `StreamWriter` or `StreamReader`. These hold an open file handle, which is a limited operating-system resource, so you must **close** them. The `using` keyword does that automatically: when the variable goes out of scope, it is disposed, which flushes buffered text and releases the file."""),
    code(r'''
using (var writer = new StreamWriter(file))
{
    writer.WriteLine("alpha");
    writer.WriteLine("beta");
}   // closed and flushed here

using var reader = new StreamReader(file);   // 'using' declaration: closes at end of scope
string? line;
while ((line = reader.ReadLine()) is not null)
{
    Console.WriteLine(line);                 // Output: alpha, then beta
}
'''),
    note("""`reader.ReadLine()` returns `null` at the end of the file, which is why the variable is `string?` and the loop tests `is not null`. The short form `using var x = ...;` (no braces) disposes the object at the end of the enclosing block."""),
    h2("Directories and cleanup"),
    p("""`Directory.GetFiles(dir)` lists files in a folder. The order is not guaranteed, so sort the result when output matters. Because tests and examples should leave no mess behind, finish by deleting what you created. `Directory.Delete(dir, true)` removes a folder **and everything in it**; `File.Delete(path)` removes one file."""),
    code(r'''
string[] files = Directory.GetFiles(dir);
Array.Sort(files);
foreach (string f in files) Console.WriteLine(Path.GetFileName(f));

try
{
    string text = File.ReadAllText(Path.Combine(dir, "missing.txt"));
}
catch (FileNotFoundException)
{
    Console.WriteLine("That file does not exist");
}

Directory.Delete(dir, true);               // clean up
'''),
    tip("""Wrap the file work in `try { ... } finally { Directory.Delete(dir, true); }` so cleanup still happens if something fails halfway. Be very careful with the recursive `true` flag: double-check the path before deleting."""),
    link("Read more on Microsoft Learn: File and stream I/O", "https://learn.microsoft.com/en-us/dotnet/standard/io/"),
]

FILEIO_CODEALONG = codealong(
    "Code Along: Reading and Writing Files",
    "Type each step into one Program.cs in order. Everything happens in a unique folder under the system temp directory, and the last step deletes it.",
    [
        step(
            "Make a working folder",
            "Build a unique folder path under the temp directory with `Path.Combine`, create it, and inspect a file path with the `Path` helpers.",
            r'''
string dir = Path.Combine(Path.GetTempPath(), "csj_fileio_" + Guid.NewGuid().ToString("N"));
Directory.CreateDirectory(dir);
string notes = Path.Combine(dir, "notes.txt");
Console.WriteLine($"File name: {Path.GetFileName(notes)}");
Console.WriteLine($"Extension: {Path.GetExtension(notes)}");
Console.WriteLine($"Folder exists: {Directory.Exists(dir)}");
''',
        ),
        step(
            "Write, append, and read back",
            "`WriteAllText` creates or replaces the file, `AppendAllText` adds to it, and `ReadAllLines` reads it back as an array.",
            r'''
File.WriteAllText(notes, "first line\nsecond line\n");
File.AppendAllText(notes, "third line\n");
string[] lines = File.ReadAllLines(notes);
Console.WriteLine($"Line count: {lines.Length}");
Console.WriteLine($"Last line: {lines[^1]}");
Console.WriteLine($"File exists: {File.Exists(notes)}");
''',
        ),
        step(
            "Stream lines lazily with ReadLines",
            "`File.ReadLines` yields one line at a time, so it pairs nicely with LINQ and with big files.",
            r'''
foreach (string line in File.ReadLines(notes).Where(l => l.Contains("line") && !l.StartsWith("second")))
{
    Console.WriteLine($"Kept: {line}");
}
''',
        ),
        step(
            "StreamWriter and StreamReader",
            "Write a second file line by line, then read it back. The `using` blocks guarantee the file is closed and flushed.",
            r'''
string report = Path.Combine(dir, "report.csv");
using (var writer = new StreamWriter(report))
{
    writer.WriteLine("name,score");
    writer.WriteLine("Ava,92");
    writer.WriteLine("Ben,78");
}

using (var reader = new StreamReader(report))
{
    string? row;
    while ((row = reader.ReadLine()) is not null)
    {
        Console.WriteLine($"Row: {row}");
    }
}
''',
        ),
        step(
            "List files and clean up",
            "List the folder's files (sorted, because the order is not guaranteed), then delete the whole folder so nothing is left behind.",
            r'''
string[] files = Directory.GetFiles(dir);
Array.Sort(files);
foreach (string f in files)
{
    Console.WriteLine($"Found: {Path.GetFileName(f)}");
}

Directory.Delete(dir, true);
Console.WriteLine($"Folder exists after cleanup: {Directory.Exists(dir)}");
''',
        ),
    ],
)

FILEIO_LAB = lab(
    "Lab: Log File Report",
    "Intermediate",
    "Write a log file, read it back, filter it into a second file with a StreamWriter, and clean up. All files live in a temp folder that you delete at the end.",
    [
        "Create a folder with `Path.Combine(Path.GetTempPath(), \"csj_lab_\" + Guid.NewGuid().ToString(\"N\"))` and `Directory.CreateDirectory`",
        "Write `all.log` (in that folder, built with `Path.Combine`) using `File.WriteAllLines` with these five lines in order: `INFO started`, `WARN disk low`, `ERROR failed to save`, `INFO saved`, `ERROR timeout`. Then add the line `INFO done` with `File.AppendAllLines`",
        "Read `all.log` back with `File.ReadLines`. Print `Total lines: ` and the count, and `Errors: ` and the number of lines that start with `ERROR`",
        "Using a `StreamWriter` inside a `using` block, write only the ERROR lines to `errors.log`. Then read `errors.log` with a `StreamReader` and print each line",
        "Print `Files: ` followed by the file names in the folder (`Path.GetFileName`), sorted alphabetically and joined by `, `. Finally delete the folder recursively and print `Exists after cleanup: ` with `Directory.Exists`",
    ],
    """
Total lines: 6
Errors: 2
ERROR failed to save
ERROR timeout
Files: all.log, errors.log
Exists after cleanup: False
""",
    "`File.ReadLines(path)` supports LINQ: `.Count(l => l.StartsWith(\"ERROR\"))` and `.Where(...)`. Close the writer (end the `using` block) **before** reading `errors.log`, so everything is flushed. For sorting names: `Directory.GetFiles(dir).Select(Path.GetFileName).Order()` works, or use `Array.Sort` on the full paths.",
)

FILEIO_SOLUTION = r'''
string dir = Path.Combine(Path.GetTempPath(), "csj_lab_" + Guid.NewGuid().ToString("N"));
Directory.CreateDirectory(dir);
try
{
    string all = Path.Combine(dir, "all.log");
    File.WriteAllLines(all, ["INFO started", "WARN disk low", "ERROR failed to save", "INFO saved", "ERROR timeout"]);
    File.AppendAllLines(all, ["INFO done"]);

    Console.WriteLine($"Total lines: {File.ReadLines(all).Count()}");
    Console.WriteLine($"Errors: {File.ReadLines(all).Count(l => l.StartsWith("ERROR"))}");

    string errors = Path.Combine(dir, "errors.log");
    using (var writer = new StreamWriter(errors))
    {
        foreach (string line in File.ReadLines(all).Where(l => l.StartsWith("ERROR")))
        {
            writer.WriteLine(line);
        }
    }

    using (var reader = new StreamReader(errors))
    {
        string? row;
        while ((row = reader.ReadLine()) is not null)
        {
            Console.WriteLine(row);
        }
    }

    var names = Directory.GetFiles(dir).Select(f => Path.GetFileName(f)).OrderBy(n => n);
    Console.WriteLine($"Files: {string.Join(", ", names)}");
}
finally
{
    Directory.Delete(dir, true);
}
Console.WriteLine($"Exists after cleanup: {Directory.Exists(dir)}");
'''

# ─── 7.4 JSON Serialization ───

JSON_READING = [
    h2("What JSON is for"),
    p("""**JSON** is a plain-text format for structured data: objects in curly braces, lists in square brackets, and values that are strings, numbers, booleans, or `null`. It is how web APIs talk, how many config files are written, and a handy way to save your own data. **Serializing** turns a C# object into JSON text; **deserializing** turns JSON text back into an object."""),
    p("""Use the `System.Text.Json` namespace, part of .NET itself with no packages needed. It is **not** in the implicit usings, so add `using System.Text.Json;` at the very top of your file. Use `using System.Text.Json.Serialization;` too if you need attributes like `[JsonPropertyName]`."""),
    code(r'''
using System.Text.Json;

var person = new Person("Ada", 36);
string json = JsonSerializer.Serialize(person);
Console.WriteLine(json);                        // Output: {"Name":"Ada","Age":36}

Person? back = JsonSerializer.Deserialize<Person>(json);
Console.WriteLine(back);                        // Output: Person { Name = Ada, Age = 36 }

record Person(string Name, int Age);
'''),
    p("""Records work well because their positional properties are public and they have a constructor the serializer can use. Classes work too, as long as they have a public parameterless constructor (or you give them a matching constructor) and **public properties** with setters."""),
    warn("""**Common mistake:** expecting public **fields** to be saved. By default only public **properties** are serialized. A class with `public string Name;` (a field, no `{ get; set; }`) serializes to an empty `{}`. Write `public string Name { get; set; }` instead."""),
    h2("JsonSerializerOptions"),
    p("""Behavior is tuned with a `JsonSerializerOptions` object that you pass as the last argument. Two options you will use constantly: `WriteIndented = true` for human-readable output, and `PropertyNamingPolicy = JsonNamingPolicy.CamelCase`, because most web JSON uses names like `firstName` rather than C#'s `FirstName`."""),
    code(r'''
var options = new JsonSerializerOptions
{
    WriteIndented = true,
    PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
};
Console.WriteLine(JsonSerializer.Serialize(new Person("Ada", 36), options));
// Output:
// {
//   "name": "Ada",
//   "age": 36
// }
'''),
    tip("""Create one options object and reuse it; do not build a new one for every call. .NET caches work per options instance, so a shared instance is faster. Property names are **case-sensitive** when reading by default; set `PropertyNameCaseInsensitive = true` when you receive JSON whose casing you do not control."""),
    h2("Renaming and ignoring with attributes"),
    p("""When the JSON name must differ from your C# name, put `[JsonPropertyName("...")]` on the property. It wins over any naming policy. `[JsonIgnore]` keeps a property out of the JSON entirely."""),
    code(r'''
using System.Text.Json.Serialization;

class Settings
{
    public string Theme { get; set; } = "light";

    [JsonPropertyName("font_size")]
    public int FontSize { get; set; } = 12;

    [JsonIgnore]
    public string Secret { get; set; } = "hidden";
}
// Serialize(new Settings()) => {"Theme":"light","font_size":12}
'''),
    h2("Collections round trip"),
    p("""Lists, arrays, and dictionaries serialize as JSON arrays and objects, and you ask for the same shape when reading back by giving the full generic type."""),
    code(r'''
var people = new List<Person> { new("Ada", 36), new("Alan", 41) };
string listJson = JsonSerializer.Serialize(people);
Console.WriteLine(listJson);
// Output: [{"Name":"Ada","Age":36},{"Name":"Alan","Age":41}]

List<Person>? loaded = JsonSerializer.Deserialize<List<Person>>(listJson);
Console.WriteLine(loaded!.Count);               // Output: 2
Console.WriteLine(loaded[1].Name);              // Output: Alan
'''),
    note("""By default, characters such as `<`, `>`, `&`, `+`, and anything outside basic ASCII (like `é`) are escaped as `\\uXXXX` in the output. That is valid JSON and reads back to the same string, so you do not need to fix it."""),
    h2("Handling invalid JSON"),
    p("""Text that arrives from a user, a file, or the network may not be valid JSON. `Deserialize` then throws a `JsonException`. Catch it and report the problem in **your own words** rather than showing the library's technical message to your users. Remember too that valid JSON can still deserialize to `null` (the text `null`), and that missing properties just keep their default values."""),
    code(r'''
string bad = "{ \"Name\": \"Ada\", ";      // truncated, invalid JSON
try
{
    Person? p = JsonSerializer.Deserialize<Person>(bad);
}
catch (JsonException)
{
    Console.WriteLine("Sorry, that data is not valid JSON.");
}
'''),
    warn("""**Common mistake:** assuming `Deserialize` always returns an object. Its return type is nullable (`Person?`), so check for `null` before using it. And do not catch `Exception` broadly: catching `JsonException` handles exactly the malformed-data case."""),
    link("Read more on Microsoft Learn: System.Text.Json overview", "https://learn.microsoft.com/en-us/dotnet/standard/serialization/system-text-json/overview"),
]

JSON_CODEALONG = codealong(
    "Code Along: Serializing and Deserializing JSON",
    "Type each step into one Program.cs in order. The `using` lines must be the very first lines of the file.",
    [
        step(
            "Serialize an object to JSON",
            "Start the file with the two `using` lines, then turn a `Person` into JSON text and back into an object.",
            r'''
using System.Text.Json;
using System.Text.Json.Serialization;

var person = new Person("Ada", 36);
string json = JsonSerializer.Serialize(person);
Console.WriteLine(json);

Person? back = JsonSerializer.Deserialize<Person>(json);
Console.WriteLine($"Back: {back?.Name}, {back?.Age}");
''',
        ),
        step(
            "Declare the types",
            "Add a record and a class at the **bottom** of the file. `Settings` renames one property with `[JsonPropertyName]`.",
            r'''
record Person(string Name, int Age);

class Settings
{
    public string Theme { get; set; } = "light";

    [JsonPropertyName("font_size")]
    public int FontSize { get; set; } = 12;
}
''',
            at="bottom",
        ),
        step(
            "Options: indentation and camelCase",
            "Create a `JsonSerializerOptions` with `WriteIndented` and a camelCase naming policy. Then serialize a `Settings` object to see the attribute win over the policy.",
            r'''
var options = new JsonSerializerOptions
{
    WriteIndented = true,
    PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
};
Console.WriteLine(JsonSerializer.Serialize(new Person("Grace", 45), options));
Console.WriteLine(JsonSerializer.Serialize(new Settings(), options));
''',
        ),
        step(
            "Round-trip a list",
            "Collections serialize as JSON arrays. Ask for the full generic type when reading them back.",
            r'''
var people = new List<Person> { new("Ada", 36), new("Alan", 41) };
string listJson = JsonSerializer.Serialize(people);
Console.WriteLine(listJson);

List<Person>? loaded = JsonSerializer.Deserialize<List<Person>>(listJson);
Console.WriteLine($"Loaded {loaded?.Count} people, second is {loaded?[1].Name}");

Settings? settings = JsonSerializer.Deserialize<Settings>("{\"Theme\":\"dark\",\"font_size\":18}");
Console.WriteLine($"Theme: {settings?.Theme}, font: {settings?.FontSize}");
''',
        ),
        step(
            "Handle invalid JSON",
            "Catch `JsonException` and print your own friendly message instead of the library's.",
            r'''
string[] inputs = ["{\"Name\":\"Ada\",\"Age\":36}", "{ \"Name\": \"Ada\", ", "not json at all"];
foreach (string input in inputs)
{
    try
    {
        Person? parsed = JsonSerializer.Deserialize<Person>(input);
        Console.WriteLine($"Parsed: {parsed?.Name}");
    }
    catch (JsonException)
    {
        Console.WriteLine("Sorry, that data is not valid JSON.");
    }
}
''',
        ),
    ],
)

JSON_LAB = lab(
    "Lab: Library Catalog",
    "Intermediate",
    "Save and load a small catalog as JSON. You will use a naming policy, a property rename, a list round trip, and error handling. Remember the `using System.Text.Json;` and `using System.Text.Json.Serialization;` lines at the very top.",
    [
        "Declare a class `Book` at the bottom of the file with properties `string Title` (default `\"\"`), `string Author` (default `\"\"`, marked `[JsonPropertyName(\"writer\")]`), and `int Year`, all with `{ get; set; }`",
        "Create a `List<Book>` with two books in order: `Dune` by `Frank Herbert` (1965), then `Emma` by `Jane Austen` (1815)",
        "Serialize the list using a `JsonSerializerOptions` with `PropertyNamingPolicy = JsonNamingPolicy.CamelCase` (no indentation) and print the JSON text exactly as produced",
        "Deserialize that JSON back to `List<Book>`; print `Round trip count: ` with the count, then one line per book as `<Title> (<Year>) by <Author>`",
        "Deserialize `{\"title\":\"Solo\"}` with the same options and print the result as `<Title>|<Author>|<Year>` to show defaults for missing properties",
        "Deserialize the text `{ not json` inside `try`/`catch (JsonException)` and print your own message `Could not parse input.` when it fails",
    ],
    """
[{"title":"Dune","writer":"Frank Herbert","year":1965},{"title":"Emma","writer":"Jane Austen","year":1815}]
Round trip count: 2
Dune (1965) by Frank Herbert
Emma (1815) by Jane Austen
Solo||0
Could not parse input.
""",
    "`JsonPropertyName` wins over the naming policy, so the Author property appears as `writer` while the others become camelCase. Use the same options object for serializing and deserializing so `title` maps back to `Title`. `Deserialize<Book>` returns `Book?`, so use `?.` or `!` when reading its properties.",
)

JSON_SOLUTION = r'''
using System.Text.Json;
using System.Text.Json.Serialization;

var books = new List<Book>
{
    new() { Title = "Dune", Author = "Frank Herbert", Year = 1965 },
    new() { Title = "Emma", Author = "Jane Austen", Year = 1815 },
};
var options = new JsonSerializerOptions { PropertyNamingPolicy = JsonNamingPolicy.CamelCase };

string json = JsonSerializer.Serialize(books, options);
Console.WriteLine(json);

List<Book>? loaded = JsonSerializer.Deserialize<List<Book>>(json, options);
Console.WriteLine($"Round trip count: {loaded!.Count}");
foreach (Book b in loaded)
{
    Console.WriteLine($"{b.Title} ({b.Year}) by {b.Author}");
}

Book? solo = JsonSerializer.Deserialize<Book>("{\"title\":\"Solo\"}", options);
Console.WriteLine($"{solo!.Title}|{solo.Author}|{solo.Year}");

try
{
    JsonSerializer.Deserialize<Book>("{ not json", options);
}
catch (JsonException)
{
    Console.WriteLine("Could not parse input.");
}

class Book
{
    public string Title { get; set; } = "";

    [JsonPropertyName("writer")]
    public string Author { get; set; } = "";

    public int Year { get; set; }
}
'''

LESSONS = {
    (7, 1): lesson(
        subtitle="Pass behavior as data with delegates and lambdas, and build publisher/subscriber code with events.",
        reading=DELEGATES_READING,
        codealong=DELEGATES_CODEALONG,
        lab=DELEGATES_LAB,
    ),
    (7, 2): lesson(
        subtitle="Write non-blocking code with async and await, run tasks together with Task.WhenAll, and avoid the classic async pitfalls.",
        reading=ASYNC_READING,
        codealong=ASYNC_CODEALONG,
        lab=ASYNC_LAB,
    ),
    (7, 3): lesson(
        subtitle="Read and write text files with File, StreamReader, and StreamWriter, build portable paths, and clean up after yourself.",
        reading=FILEIO_READING,
        codealong=FILEIO_CODEALONG,
        lab=FILEIO_LAB,
    ),
    (7, 4): lesson(
        subtitle="Turn objects into JSON and back with System.Text.Json, customize the output, and handle bad input gracefully.",
        reading=JSON_READING,
        codealong=JSON_CODEALONG,
        lab=JSON_LAB,
    ),
}

# Reference solutions, used only by verify_content.py (never sent to the learner).
SOLUTIONS = {
    (7, 1): DELEGATES_SOLUTION,
    (7, 2): ASYNC_SOLUTION,
    (7, 3): FILEIO_SOLUTION,
    (7, 4): JSON_SOLUTION,
}
