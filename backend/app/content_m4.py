"""Module 4: Methods and Program Structure."""
from .lesson_kit import *  # noqa: F401,F403

MS = "https://learn.microsoft.com/en-us/dotnet/csharp/"

# ─── 4.1 Defining and Calling Methods ───

L41_READING = [
    h2("Why methods exist"),
    p("A **method** is a named block of code that you can run whenever you want by writing its name. Methods let you stop repeating yourself, break a big problem into small pieces with good names, and test or change one piece without touching the rest. You have been calling methods since your first program: `Console.WriteLine(...)` is a method somebody else wrote."),
    p("Defining your own method takes four parts: a **return type**, a **name**, a **parameter list** in parentheses, and a **body** in braces. Here is the simplest kind, a method that does something but gives nothing back, which is marked with the return type `void`."),
    code("""
static void Greet(string person)
{
    Console.WriteLine($"Hello, {person}!");
}

Greet("Ada");    // Output: Hello, Ada!
Greet("Linus");  // Output: Hello, Linus!
"""),
    p("`person` is a **parameter**: a variable that exists only inside the method and receives its value from the caller. The value you pass in the call, like `\"Ada\"`, is called an **argument**. The `static` keyword is explained below; for now it is the right choice for every method in this module."),
    h2("Returning a value"),
    p("Most methods compute something. Replace `void` with a type and use `return` to hand a value back to the caller. The caller can store it, print it, or use it inside a bigger expression."),
    code("""
static int Square(int value)
{
    return value * value;
}

int area = Square(7);
Console.WriteLine(area);                // Output: 49
Console.WriteLine(Square(Square(2)));   // Output: 16
"""),
    p("The moment `return` runs, the method ends and control goes back to where it was called. That makes **early returns** a useful tool: check the easy or invalid cases first and return immediately, which avoids deep nesting."),
    code("""
static string Classify(int amount)
{
    if (amount < 0)
    {
        return "negative";
    }
    if (amount == 0)
    {
        return "zero";
    }
    return "positive";
}

Console.WriteLine(Classify(-3));  // Output: negative
Console.WriteLine(Classify(8));   // Output: positive
"""),
    warn("**Common mistake:** a non-`void` method must return a value on **every** path. If the `if` branches above did not end with a final `return`, the compiler would stop you with error CS0161: not all code paths return a value. Another classic: calling `Square(7);` and ignoring the result. It compiles, but the value is thrown away, so the line does nothing useful."),
    h2("Expression-bodied methods"),
    p("When a method is a single expression, you can skip the braces and `return` and use `=>` (read it as \"gives\"). This is only a shorter way to write the same method."),
    code("""
static int Cube(int value) => value * value * value;
static bool IsEven(int number) => number % 2 == 0;
static void Shout(string text) => Console.WriteLine(text.ToUpper());

Console.WriteLine(Cube(3));    // Output: 27
Console.WriteLine(IsEven(7));  // Output: False
Shout("hey");                  // Output: HEY
"""),
    h2("What does static mean here?"),
    p("In C#, methods normally live inside a type, such as a class, and `static` means \"this method belongs to the type itself, not to one particular object made from it\". You will learn what objects are in module 5. For now, remember that a program with top-level statements can call `static` methods directly by name, the same way you call `Console.WriteLine`."),
    note("When you write a method among your top-level statements like we do in this lesson, C# technically treats it as a **local function** inside the generated `Main` method. Local functions work the same for everyday use, but there are small differences: they cannot have `public` or `private`, they cannot be **overloaded** (two methods with the same name; see lesson 4.3), and they can be written anywhere in the file. Lesson 4.4 shows the full class form where methods are ordinary members."),
    h2("Local functions inside methods"),
    p("You can even declare a small helper **inside** another method. It is only visible to that method, which is handy for tiny pieces of logic that nothing else needs. Marking it `static` guarantees it does not secretly use the outer method's variables."),
    code("""
static string Summarize(int first, int second)
{
    return $"{Label(first)} and {Label(second)}";

    static string Label(int n) => n % 2 == 0 ? "even" : "odd";
}

Console.WriteLine(Summarize(4, 9));
// Output: even and odd
"""),
    tip("Name methods with a verb phrase in PascalCase (`PrintReport`, `CalculateTax`, `IsValid`). If you cannot name a method without using \"and\" (`ReadAndSave`), it probably does two jobs and should be two methods. Aim for methods short enough to read in one glance."),
    link("Read more on Microsoft Learn: Methods", MS + "programming-guide/classes-and-structs/methods"),
]

L41_CODEALONG = codealong(
    "Code Along: Your First Methods",
    "Type each method into Program.cs together with the lines that call it. Run after every step.",
    [
        step("A void method", "Define a method that prints a greeting, then call it twice with different arguments.",
             """
static void Greet(string person)
{
    Console.WriteLine($"Hello, {person}!");
}

Greet("Ada");
Greet("Linus");
"""),
        step("Return a value", "An expression-bodied method that returns an `int`. Calls can be nested, because a call is just an expression.",
             """
static int Square(int value) => value * value;

int area = Square(7);
Console.WriteLine($"Square(7) = {area}");
Console.WriteLine($"Square(Square(2)) = {Square(Square(2))}");
"""),
        step("Bool and loop methods", "A predicate (a method that answers yes or no) and a method with a loop that returns a `long`.",
             """
static bool IsEven(int candidate) => candidate % 2 == 0;

static long Factorial(int limit)
{
    long result = 1;
    for (int i = 2; i <= limit; i++)
    {
        result *= i;
    }
    return result;
}

Console.WriteLine($"IsEven(10): {IsEven(10)}");
Console.WriteLine($"IsEven(7): {IsEven(7)}");
Console.WriteLine($"Factorial(5): {Factorial(5)}");
"""),
        step("Early return and a local function", "Return early for the easy cases. The helper `Word` lives inside `Classify` and nowhere else.",
             """
static string Classify(int amount)
{
    if (amount < 0)
    {
        return "negative";
    }
    return Word(amount);

    static string Word(int n) => n == 0 ? "zero" : "positive";
}

Console.WriteLine($"Classify(-3): {Classify(-3)}");
Console.WriteLine($"Classify(0): {Classify(0)}");
Console.WriteLine($"Classify(8): {Classify(8)}");
"""),
    ],
)

L41_LAB = lab(
    "Lab: A Small Toolbox",
    "Beginner",
    "Write four small methods and call them to print a short report. Place your method definitions and the statements that call them in the same file.",
    [
        "Write `static void PrintBanner(string title)` that prints `=== ` + title + ` ===` (for example `=== Methods Lab ===`). Call it with `\"Methods Lab\"`.",
        "Write the expression-bodied method `static double CelsiusToFahrenheit(double celsius)` that returns `celsius * 9 / 5 + 32`. For each of the values 100, 0, and -40 (use a `foreach` over an `int[]`), print `<c>C = <f>F`, for example `100C = 212F`.",
        "Write `static bool IsEven(int number)` and print `7 is even: False` and `10 is even: True` by calling it (use the argument in the text).",
        "Write `static long Factorial(int n)` using a loop (`Factorial(0)` must be 1). Print `Factorial(10) = 3628800` and `Factorial(0) = 1`.",
        "Print all of the lines in the order of the requirements above.",
    ],
    """
=== Methods Lab ===
100C = 212F
0C = 32F
-40C = -40F
7 is even: False
10 is even: True
Factorial(10) = 3628800
Factorial(0) = 1
""",
    "Declare the array first: `int[] temps = [100, 0, -40];`. An `int` can be passed where a `double` is expected, because C# converts it automatically. Start the factorial with `long result = 1;` and multiply by every number from 2 up to `n`.",
)

L41_SOLUTION = """static void PrintBanner(string title)
{
    Console.WriteLine($"=== {title} ===");
}

static double CelsiusToFahrenheit(double celsius) => celsius * 9 / 5 + 32;

static bool IsEven(int number) => number % 2 == 0;

static long Factorial(int n)
{
    long result = 1;
    for (int i = 2; i <= n; i++)
    {
        result *= i;
    }
    return result;
}

PrintBanner("Methods Lab");

int[] temps = [100, 0, -40];
foreach (int c in temps)
{
    Console.WriteLine($"{c}C = {CelsiusToFahrenheit(c)}F");
}

Console.WriteLine($"7 is even: {IsEven(7)}");
Console.WriteLine($"10 is even: {IsEven(10)}");
Console.WriteLine($"Factorial(10) = {Factorial(10)}");
Console.WriteLine($"Factorial(0) = {Factorial(0)}");
"""

# ─── 4.2 Parameters and Return Values ───

L42_READING = [
    h2("Customizing how a method is called"),
    p("Plain parameters are enough for many methods, but C# gives you several tools to make calls shorter and safer, and to return more than one thing. In this lesson you will meet optional and named arguments, `params`, `out`, `ref`, `in`, and tuples."),
    h2("Optional parameters and named arguments"),
    p("Give a parameter a **default value** and callers may leave it out. Optional parameters must come after the required ones. At the call site you can also write the parameter's name with a colon, which lets you skip parameters or put arguments in any order and makes the call self-explanatory."),
    code("""
static string Pad(string text, int width = 8, char fill = '.')
{
    return text.PadLeft(width, fill);
}

Console.WriteLine(Pad("abc"));                  // Output: .....abc
Console.WriteLine(Pad("abc", 5));               // Output: ..abc
Console.WriteLine(Pad("abc", fill: '-'));       // Output: -----abc
Console.WriteLine(Pad(width: 6, text: "abc"));  // Output: ...abc
"""),
    tip("Named arguments shine when a call has several values of the same type, or a bare `true`. Compare `Save(data, true, false)` with `Save(data, overwrite: true, backup: false)`. The second reads like a sentence."),
    h2("params: any number of arguments"),
    p("A `params` parameter must be the **last** parameter and must be an array type. It lets callers pass any number of values separated by commas, including none, and the method receives them as an array. `Console.WriteLine(\"{0} {1}\", a, b)` uses the same idea."),
    code("""
static int Sum(params int[] numbers)
{
    int total = 0;
    foreach (int n in numbers)
    {
        total += n;
    }
    return total;
}

Console.WriteLine(Sum());           // Output: 0
Console.WriteLine(Sum(1, 2, 3));    // Output: 6
int[] data = [10, 20];
Console.WriteLine(Sum(data));       // Output: 30
"""),
    note("Recent versions of C# (starting with C# 13) allow `params` on other collection types as well, such as `params ReadOnlySpan<int>`, but `params int[]` still works the same and is the clearest form to learn."),
    h2("By value, by reference"),
    p("By default arguments are passed **by value**: the method gets its own copy of the value, so changing the parameter does not change the caller's variable."),
    code("""
static void AddTenCopy(int number)
{
    number += 10;                   // changes only the copy
}

int score = 5;
AddTenCopy(score);
Console.WriteLine(score);           // Output: 5
"""),
    p("Sometimes you want the method to change the caller's variable or hand extra results back. The modifiers `ref` and `out` pass a variable **by reference**, so the method works on the caller's actual variable. You must write the keyword at both the definition and the call."),
    code("""
static void Swap(ref int left, ref int right)
{
    int temp = left;
    left = right;
    right = temp;
}

int x = 3;
int y = 9;
Swap(ref x, ref y);
Console.WriteLine($"x={x} y={y}");   // Output: x=9 y=3
"""),
    p("`ref` requires the variable to already have a value before the call. `out` is for **extra results**: the variable does not need a value going in, and the method **must assign it** before returning. This is the pattern behind `int.TryParse`: the return value says whether it worked and the `out` value carries the result."),
    code("""
static bool TryDivide(int dividend, int divisor, out int quotient)
{
    if (divisor == 0)
    {
        quotient = 0;
        return false;
    }
    quotient = dividend / divisor;
    return true;
}

if (TryDivide(20, 4, out int answer))
{
    Console.WriteLine(answer);   // Output: 5
}
Console.WriteLine(TryDivide(1, 0, out int _));  // Output: False
"""),
    warn("**Common mistake:** forgetting to assign an `out` parameter on every path, which is compile error CS0177. Another one: reaching for `ref` or `out` when the method could simply return a value. `ref` and `out` make calls harder to read, so use them when you really need them, and prefer a tuple (below) when you just want to return a couple of values."),
    p("The `in` modifier passes a value by reference but **read-only**: the method cannot change it. It exists to avoid copying large values, and you will rarely need it for small types such as `int`. Just know it exists when you see `in` in someone else's code."),
    h2("Returning several values with a tuple"),
    p("A **tuple** groups a few values with names, in parentheses. A method can return one and the caller can unpack it into separate variables (called **deconstruction**). It is usually the cleanest way to return two or three related values."),
    code("""
static (int Min, int Max) FindRange(int[] values)
{
    int min = values[0];
    int max = values[0];
    foreach (int v in values)
    {
        if (v < min) { min = v; }
        if (v > max) { max = v; }
    }
    return (min, max);
}

var range = FindRange([4, 8, 15, 16, 23, 42]);
Console.WriteLine($"{range.Min} to {range.Max}");   // Output: 4 to 42

var (lowest, highest) = FindRange([7, 2, 9]);
Console.WriteLine($"{lowest}, {highest}");          // Output: 2, 9
"""),
    link("Read more on Microsoft Learn: Method parameters", MS + "language-reference/keywords/method-parameters"),
]

L42_CODEALONG = codealong(
    "Code Along: Parameters in Depth",
    "Each step defines a method and immediately uses it. Run after every step and compare the output with what you expected.",
    [
        step("Optional and named arguments", "Defaults let callers skip parameters; names let them pick which ones to set.",
             """
static string Pad(string text, int width = 8, char fill = '.')
{
    return text.PadLeft(width, fill);
}

Console.WriteLine(Pad("abc"));
Console.WriteLine(Pad("abc", 5));
Console.WriteLine(Pad("abc", fill: '-'));
Console.WriteLine(Pad(width: 6, text: "abc"));
"""),
        step("params", "Accept any number of integers, including none at all.",
             """
static int Sum(params int[] numbers)
{
    int total = 0;
    foreach (int n in numbers)
    {
        total += n;
    }
    return total;
}

Console.WriteLine($"Sum(): {Sum()}");
Console.WriteLine($"Sum(1, 2, 3): {Sum(1, 2, 3)}");
"""),
        step("out parameters", "Return a success flag from the method and the answer through `out`.",
             """
static bool TryDivide(int dividend, int divisor, out int quotient)
{
    if (divisor == 0)
    {
        quotient = 0;
        return false;
    }
    quotient = dividend / divisor;
    return true;
}

bool worked = TryDivide(20, 4, out int answer);
Console.WriteLine($"TryDivide(20, 4): {worked}, {answer}");
worked = TryDivide(1, 0, out answer);
Console.WriteLine($"TryDivide(1, 0): {worked}, {answer}");
"""),
        step("By value versus ref", "Compare a method that changes a copy with one that changes the caller's variable.",
             """
static void AddTenCopy(int number)
{
    number += 10;
}

static void AddTenRef(ref int number)
{
    number += 10;
}

int score = 5;
AddTenCopy(score);
Console.WriteLine($"After AddTenCopy: {score}");
AddTenRef(ref score);
Console.WriteLine($"After AddTenRef: {score}");
"""),
        step("Return a tuple", "Return two named values and deconstruct them into variables.",
             """
static (int Min, int Max) FindRange(int[] values)
{
    int min = values[0];
    int max = values[0];
    foreach (int v in values)
    {
        if (v < min) { min = v; }
        if (v > max) { max = v; }
    }
    return (min, max);
}

var range = FindRange([4, 8, 15, 16, 23, 42]);
Console.WriteLine($"Range: {range.Min} to {range.Max}");

var (lowest, highest) = FindRange([7, 2, 9]);
Console.WriteLine($"Lowest {lowest}, highest {highest}");
"""),
    ],
)

L42_LAB = lab(
    "Lab: Stats Helper",
    "Intermediate",
    "Write four methods that use different parameter styles, then call them in a fixed order to print a report.",
    [
        "Write `static (int Min, int Max, double Average) Summarize(params int[] values)` that uses a loop to compute the three results. Call it as `Summarize(4, 8, 15, 16, 23, 42)` and print `Min=4 Max=42 Average=18` using the tuple's named items.",
        "Write `static bool TryDivide(int a, int b, out int result)` that returns `false` and sets `result` to 0 when `b` is 0, otherwise sets `result` to `a / b` and returns `true`. Print `TryDivide(20, 4): True, 5` and `TryDivide(1, 0): False, 0` using the real returned values.",
        "Write `static void Swap(ref int first, ref int second)`. With `int x = 3; int y = 9;` print `Before: x=3 y=9`, call the method, then print `After: x=9 y=3`.",
        "Write `static string Pad(string text, int width = 8, char fill = '.')` returning `text.PadLeft(width, fill)`. Print `Pad(\"abc\")`, then `Pad(\"abc\", fill: '-')`, then `Pad(width: 5, text: \"abc\")`, each on its own line.",
    ],
    """
Min=4 Max=42 Average=18
TryDivide(20, 4): True, 5
TryDivide(1, 0): False, 0
Before: x=3 y=9
After: x=9 y=3
.....abc
-----abc
..abc
""",
    "Track `min`, `max`, and a running `sum` in one loop, then `return (min, max, (double)sum / values.Length);`. For `TryDivide`, declare each result variable inline with `out int q1`. Named arguments use a colon: `Pad(\"abc\", fill: '-')`.",
)

L42_SOLUTION = """static (int Min, int Max, double Average) Summarize(params int[] values)
{
    int min = values[0];
    int max = values[0];
    int sum = 0;
    foreach (int v in values)
    {
        if (v < min) { min = v; }
        if (v > max) { max = v; }
        sum += v;
    }
    return (min, max, (double)sum / values.Length);
}

static bool TryDivide(int a, int b, out int result)
{
    if (b == 0)
    {
        result = 0;
        return false;
    }
    result = a / b;
    return true;
}

static void Swap(ref int first, ref int second)
{
    int temp = first;
    first = second;
    second = temp;
}

static string Pad(string text, int width = 8, char fill = '.')
{
    return text.PadLeft(width, fill);
}

var stats = Summarize(4, 8, 15, 16, 23, 42);
Console.WriteLine($"Min={stats.Min} Max={stats.Max} Average={stats.Average}");

bool ok1 = TryDivide(20, 4, out int q1);
Console.WriteLine($"TryDivide(20, 4): {ok1}, {q1}");
bool ok2 = TryDivide(1, 0, out int q2);
Console.WriteLine($"TryDivide(1, 0): {ok2}, {q2}");

int x = 3;
int y = 9;
Console.WriteLine($"Before: x={x} y={y}");
Swap(ref x, ref y);
Console.WriteLine($"After: x={x} y={y}");

Console.WriteLine(Pad("abc"));
Console.WriteLine(Pad("abc", fill: '-'));
Console.WriteLine(Pad(width: 5, text: "abc"));
"""

# ─── 4.3 Method Overloading ───

L43_READING = [
    h2("One name, several versions"),
    p("**Overloading** means defining several methods with the **same name** but different parameter lists. The compiler looks at the arguments you pass and picks the version that fits. You already use this every day: `Console.WriteLine` has overloads for strings, ints, doubles, bools, and more, and `Math.Abs` works on `int`, `double`, and `decimal`."),
    p("Why bother? It lets callers use one natural name for \"the same idea on different inputs\", instead of forcing `AddInts`, `AddDoubles`, and `AddThree`. The versions should do the **same conceptual job**; if they do different things, give them different names."),
    note("Overloaded methods must be members of a type, for example a `static class`, because local functions (the kind we wrote at the top of a file in lessons 4.1 and 4.2) cannot be overloaded. In this lesson we put the methods in a `static class` at the bottom of the file and call them as `ClassName.Method(...)`. Module 5 explains classes in depth; for now treat a `static class` as a named container for static methods."),
    code("""
static class Calc
{
    public static int Add(int a, int b) => a + b;
    public static double Add(double a, double b) => a + b;
    public static int Add(int a, int b, int c) => a + b + c;
}

// Statements at the top of the file:
Console.WriteLine(Calc.Add(2, 3));       // Output: 5
Console.WriteLine(Calc.Add(2.5, 1.5));   // Output: 4
Console.WriteLine(Calc.Add(1, 2, 3));    // Output: 6
"""),
    p("Notice `public` on each method. Inside a class, members are private by default, so without `public` the statements at the top could not call them."),
    h2("What makes two overloads different"),
    p("Two methods can share a name only if their **signatures** differ. The signature is the name plus the number, types, and order of parameters (and whether they are `ref`, `out`, or `in`). The return type and parameter names are **not** part of the signature."),
    code("""
static class Shapes
{
    public static double Area(double radius) => Math.PI * radius * radius;   // OK
    public static double Area(double width, double height) => width * height; // OK: count differs

    // ERROR: same signature as Area(double radius), only the return type differs
    // public static int Area(double radius) => 0;
}
"""),
    warn("**Common mistake:** trying to overload on return type alone, or on parameter names alone. `int Parse(string s)` and `double Parse(string s)` cannot coexist, because at the call `Parse(\"5\")` the compiler has no way to choose. Give those methods different names, such as `ParseInt` and `ParseDouble`."),
    h2("How the compiler picks one"),
    p("When you call an overloaded method the compiler works in a simple order. First, it collects the overloads that **could** accept your arguments (count matches, and each argument can be implicitly converted to its parameter type). Second, among those, it picks the one that is the **best match**:"),
    p("An **exact type match** beats a conversion. A conversion to a **closer** type beats a conversion to a farther one (for example `int` to `long` is better than `int` to `double`, because `long` can be converted to `double` but not the other way). A normal call beats a call that must expand a `params` array. If no version is clearly better, you get an ambiguity error."),
    code("""
static class Show
{
    public static string Describe(int n) => $"int {n}";
    public static string Describe(long n) => $"long {n}";
    public static string Describe(double n) => $"double {n}";
    public static string Describe(string s) => $"string {s}";
    public static string Describe(int a, int b) => $"pair {a},{b}";
    public static string Describe(params int[] items) => $"params {items.Length} items";
}

// Statements at the top of the file:
Console.WriteLine(Show.Describe(5));        // Output: int 5      (exact match)
Console.WriteLine(Show.Describe(5L));       // Output: long 5     (exact match)
Console.WriteLine(Show.Describe(2.5f));     // Output: double 2.5 (float converts to double only)
Console.WriteLine(Show.Describe('A'));      // Output: int 65     (char converts to int, the closest)
Console.WriteLine(Show.Describe(1, 2));     // Output: pair 1,2   (normal form beats params)
Console.WriteLine(Show.Describe(1, 2, 3));  // Output: params 3 items
"""),
    p("In the `char` example, `char` converts implicitly to `int`, `long`, and `double`. `int` wins because it is the closest target. In the `Describe(1, 2)` call, both the fixed pair version and the `params` version are possible; the one without array expansion wins."),
    warn("Optional parameters and overloads together can confuse callers. If `Log(string message)` and `Log(string message, int level = 1)` both exist, `Log(\"hi\")` calls the first one, because the compiler prefers a candidate that does not need any default values filled in. Pick either optional parameters **or** overloads for a given variation, not both."),
    tip("Before adding another overload, ask whether an optional parameter would do the job (one method, one place to maintain). Use overloads when the **types** of the inputs differ, or when the logic really differs between the versions. When one overload can be written in terms of another, have it call the other so the real logic lives in one place."),
    link("Read more on Microsoft Learn: Methods and overloading", MS + "programming-guide/classes-and-structs/methods#overloaded-methods"),
]

L43_CODEALONG = codealong(
    "Code Along: Overloads and Overload Resolution",
    "This lesson uses two `static class` declarations. The class steps go at the bottom of Program.cs, and the calls go in the statements at the top.",
    [
        step("Declare the Calc overloads", "Add this class at the **bottom** of Program.cs, below all other code. Three methods share the name `Add` but differ in parameter types or count.",
             """
static class Calc
{
    public static int Add(int a, int b) => a + b;
    public static double Add(double a, double b) => a + b;
    public static int Add(int a, int b, int c) => a + b + c;
}
""", at="bottom"),
        step("Call Calc.Add", "Add these statements at the top of the file. Predict which overload each call uses before you run it.",
             """
Console.WriteLine($"Add(2, 3) = {Calc.Add(2, 3)}");
Console.WriteLine($"Add(2.5, 1.5) = {Calc.Add(2.5, 1.5)}");
Console.WriteLine($"Add(1, 2, 3) = {Calc.Add(1, 2, 3)}");
"""),
        step("Declare the Show overloads", "Add this second class at the **bottom** of the file, under `Calc`. Each overload names itself in its result so you can see which one ran.",
             """
static class Show
{
    public static string Describe(int n) => $"int {n}";
    public static string Describe(long n) => $"long {n}";
    public static string Describe(double n) => $"double {n}";
    public static string Describe(string s) => $"string {s}";
    public static string Describe(int a, int b) => $"pair {a},{b}";
    public static string Describe(params int[] items) => $"params {items.Length} items";
}
""", at="bottom"),
        step("Watch overload resolution", "Add these calls to the statements at the top. Each comment names the rule being demonstrated.",
             """
Console.WriteLine(Show.Describe(5));        // exact match: int
Console.WriteLine(Show.Describe(5L));       // exact match: long
Console.WriteLine(Show.Describe(2.5f));     // float converts to double
Console.WriteLine(Show.Describe('A'));      // char converts to int (closest)
Console.WriteLine(Show.Describe("hi"));     // string
Console.WriteLine(Show.Describe(1, 2));     // normal form beats params
Console.WriteLine(Show.Describe(1, 2, 3));  // only params fits
Console.WriteLine(Show.Describe());         // params with zero items
"""),
    ],
)

L43_LAB = lab(
    "Lab: Geometry Overloads",
    "Intermediate",
    "Write one overloaded method named `Area` in a static class, then call it with different argument types and watch the compiler pick the best match each time.",
    [
        "At the bottom of the file, declare `static class Geometry` containing four `public static string Area(...)` overloads.",
        "`Area(int side)` returns `Square {side}x{side} = {side * side}`. `Area(double radius)` returns `Circle r={radius} area={Math.PI * radius * radius:F2}`.",
        "`Area(int width, int height)` returns `Rectangle(int) {width}x{height} = {width * height}`. `Area(double width, double height)` returns `Rectangle(double) {width}x{height} = {width * height}`.",
        "At the top of the file print, one per line, the results of `Geometry.Area(5)`, `Geometry.Area(5.0)`, `Geometry.Area(5L)`, `Geometry.Area(3, 4)`, and `Geometry.Area(3, 4.5)`.",
    ],
    """
Square 5x5 = 25
Circle r=5 area=78.54
Circle r=5 area=78.54
Rectangle(int) 3x4 = 12
Rectangle(double) 3x4.5 = 13.5
""",
    "Compare the 3rd line with the 1st. `5L` is a `long`, which has no exact overload and cannot convert to `int`, so the compiler chooses the `double` version. For the last call `3` is converted to `double` because `4.5` cannot be an `int`.",
)

L43_SOLUTION = """Console.WriteLine(Geometry.Area(5));
Console.WriteLine(Geometry.Area(5.0));
Console.WriteLine(Geometry.Area(5L));
Console.WriteLine(Geometry.Area(3, 4));
Console.WriteLine(Geometry.Area(3, 4.5));

static class Geometry
{
    public static string Area(int side) => $"Square {side}x{side} = {side * side}";
    public static string Area(double radius) => $"Circle r={radius} area={Math.PI * radius * radius:F2}";
    public static string Area(int width, int height) => $"Rectangle(int) {width}x{height} = {width * height}";
    public static string Area(double width, double height) => $"Rectangle(double) {width}x{height} = {width * height}";
}
"""

# ─── 4.4 Namespaces and Top-level Statements ───

L44_READING = [
    h2("Putting code in the right place"),
    p("As programs grow you need a way to group related code and avoid name clashes. Two people can both write a class called `Logger`; a **namespace** lets them live side by side as `Acme.Logger` and `Contoso.Logger`. Namespaces also give the .NET library its structure: `System`, `System.IO`, `System.Text`, and so on."),
    h2("Namespaces and using directives"),
    p("You can always refer to something by its **fully qualified name**, such as `System.Text.StringBuilder`, but that is long. A `using` directive at the top of a file brings a namespace's types into scope so you can write just `StringBuilder`."),
    code("""
using System.Text;

StringBuilder sb = new();
sb.Append("Hello");
sb.Append(", world");
Console.WriteLine(sb.ToString());
// Output: Hello, world

// Without the using, you would write the full name:
System.Text.StringBuilder other = new();
"""),
    p("Where did `Console` come from, though, since there is no `using System;`? New projects turn on **implicit usings**: the build adds a hidden set of `global using` directives for common namespaces (`System`, `System.IO`, `System.Linq`, `System.Collections.Generic`, and a few more). A **global using** applies to every file in the project. You can add your own in any file or in the project file."),
    code("""
// GlobalUsings.cs, a file you add to your project:
global using System.Text;
global using System.Globalization;

// or in the .csproj file:
// <ItemGroup>
//   <Using Include="System.Text" />
// </ItemGroup>
"""),
    h2("using static and aliases"),
    p("Two more forms of `using` save typing. `using static` imports the **static members** of a type so you can call them without the type name. A `using` **alias** gives a long or conflicting name a short nickname."),
    code("""
using static System.Math;
using Money = decimal;
using Sb = System.Text.StringBuilder;

Money price = 19.99m;
Console.WriteLine(Max(3, 9));     // Output: 9   (Math.Max)
Console.WriteLine(Sqrt(144));     // Output: 12  (Math.Sqrt)
Sb builder = new();
"""),
    warn("**Common mistake:** putting `using` directives in the wrong place. In a file with top-level statements, all `using` directives must come **before** any statement, and all type and namespace declarations must come **after** the last statement. A `using` below a statement is a compile error. Also, importing too much with `using static` makes code harder to read, because readers cannot tell where `Max` comes from."),
    h2("Declaring your own namespace"),
    p("You put your own types in a namespace with the `namespace` keyword. The classic form wraps the types in braces. The modern **file-scoped** form is a single line that applies to the rest of the file, which saves one level of indentation."),
    code("""
// Classic, block-scoped:
namespace Acme.Billing
{
    public class Invoice { }
}

// File-scoped (C# 10): must be the first declaration in the file,
// and a file can have only one.
// namespace Acme.Billing;
//
// public class Invoice { }
"""),
    p("By convention a namespace mirrors your project and folder structure, for example `MyApp.Services`. A dot in the name only expresses grouping: `Acme.Billing` is just a namespace named `Billing` inside `Acme`."),
    h2("Top-level statements versus Main"),
    p("Every C# program starts executing at a method called `Main`. Older templates made you write it by hand, inside a class. Since C# 9 you can write **top-level statements**, and the compiler generates the class and `Main` for you. In a file with top-level statements, the command-line arguments are available as `args`."),
    code("""
// The traditional form:
namespace MyApp;

class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("Hello from Main");
    }
}

// The same program with top-level statements:
Console.WriteLine("Hello from top-level statements");
"""),
    p("Both are equally valid; top-level statements are simply less ceremony for small programs and scripts. Only **one** file in a project may contain top-level statements, and it becomes the entry point. Large applications often use the explicit `Main` or a similar structure, because they rely on classes and namespaces."),
    warn("File-scoped namespaces and top-level statements cannot be combined in the same file. A file-scoped `namespace X;` must come before every other member, but top-level statements must come before any type declarations, so the two rules conflict, and the compiler reports error CS8956. If you use top-level statements, declare your types in block-scoped `namespace X { ... }` at the bottom, or put them in other files."),
    h2("Organizing a single file"),
    p("When your program has top-level statements and its own types, the file order is always the same: **using directives, then statements, then type and namespace declarations at the bottom**. The statements can use the types below them just fine, since C# does not require declaration before use for types and members."),
    code("""
using System.Text;                          // 1. usings first

Console.WriteLine(Greetings.Greeter.Hello("Ada"));   // 2. statements

namespace Greetings                         // 3. types and namespaces last
{
    public static class Greeter
    {
        public static string Hello(string name) => $"Hello, {name}!";
    }
}
// Output: Hello, Ada!
"""),
    tip("As a rule, put each type in its own file once a program has more than a few, and name the file after the type. For this course's single-file exercises, keeping everything in one `Program.cs` with types at the bottom is the convention to follow."),
    link("Read more on Microsoft Learn: Top-level statements", MS + "fundamentals/program-structure/top-level-statements"),
    link("Read more on Microsoft Learn: Namespaces", MS + "fundamentals/types/namespaces"),
]

L44_CODEALONG = codealong(
    "Code Along: Namespaces and Usings",
    "You will use the three kinds of `using`, then declare two of your own namespaces at the bottom of the file.",
    [
        step("using static and an alias", "Put these `using` lines at the very top of Program.cs, above everything else, then add the statements below them.",
             """
using System.Text;
using static System.Math;
using Money = decimal;

Money price = 19.99m;
Console.WriteLine($"Price: {price}");
Console.WriteLine($"Max(3, 9) = {Max(3, 9)}");
Console.WriteLine($"Sqrt(144) = {Sqrt(144)}");
"""),
        step("StringBuilder from System.Text", "Thanks to `using System.Text;`, you can use `StringBuilder` by its short name.",
             """
StringBuilder builder = new();
builder.Append("Namespaces");
builder.Append(" keep code organized");
Console.WriteLine(builder.ToString());
Console.WriteLine(System.Math.Abs(-4));
"""),
        step("Declare two namespaces", "Add this code at the **bottom** of Program.cs. It declares a namespace and a nested one, each with its own `Greeter` class. Same class name, different namespaces, no conflict.",
             """
namespace Greetings
{
    public static class Greeter
    {
        public static string Hello(string name) => $"Hello, {name}!";
    }
}

namespace Greetings.Formal
{
    public static class Greeter
    {
        public static string Hello(string name) => $"Good day, {name}.";
    }
}
""", at="bottom"),
        step("Call by fully qualified name", "Back in the statements at the top, use the full names to say which `Greeter` you mean.",
             """
Console.WriteLine(Greetings.Greeter.Hello("Ada"));
Console.WriteLine(Greetings.Formal.Greeter.Hello("Ada"));
"""),
    ],
)

L44_LAB = lab(
    "Lab: A Tiny Shop in Two Namespaces",
    "Intermediate",
    "Organize a small program the way a real project would: usings first, statements next, and two namespaces with their own classes at the bottom of the file.",
    [
        "At the very top, add `using static System.Math;`, `using Report = Shop.Reports.Printer;`, and `using Sb = System.Text.StringBuilder;`.",
        "At the bottom, declare `namespace Shop` with `public static class Pricing` containing `public static decimal WithTax(decimal price) => price * 1.08m;`.",
        "Also at the bottom, declare `namespace Shop.Reports` with `public static class Printer` containing `public static string Line(string label, decimal amount) => $\"{label}: {amount:F2}\";`.",
        "In the statements, set `decimal subtotal = 100m;` and `decimal total = Shop.Pricing.WithTax(subtotal);`. Print three lines through the alias: `Report.Line(\"Subtotal\", subtotal)`, `Report.Line(\"Tax\", total - subtotal)`, and `Report.Line(\"Total\", total)`.",
        "Then print `Larger: ` followed by `Max(7, 12)` (from `using static`), and build the text `Done!` with a `Sb` by appending `\"Done\"` and then `'!'`, printing `sb.ToString()`.",
    ],
    """
Subtotal: 100.00
Tax: 8.00
Total: 108.00
Larger: 12
Done!
""",
    "The alias line must use the full path `Shop.Reports.Printer`. `Shop.Reports` is its own namespace, so its types are written `Shop.Reports.Printer`. Remember that types and namespaces go below all of your statements, while every `using` goes above them.",
)

L44_SOLUTION = """using static System.Math;
using Report = Shop.Reports.Printer;
using Sb = System.Text.StringBuilder;

decimal subtotal = 100m;
decimal total = Shop.Pricing.WithTax(subtotal);
Console.WriteLine(Report.Line("Subtotal", subtotal));
Console.WriteLine(Report.Line("Tax", total - subtotal));
Console.WriteLine(Report.Line("Total", total));
Console.WriteLine($"Larger: {Max(7, 12)}");
Sb sb = new();
sb.Append("Done");
sb.Append('!');
Console.WriteLine(sb.ToString());

namespace Shop
{
    public static class Pricing
    {
        public static decimal WithTax(decimal price) => price * 1.08m;
    }
}

namespace Shop.Reports
{
    public static class Printer
    {
        public static string Line(string label, decimal amount) => $"{label}: {amount:F2}";
    }
}
"""

LESSONS = {
    (4, 1): lesson(
        "Define your own methods with parameters and return values, shorten simple ones with expression bodies, and meet local functions.",
        L41_READING, L41_CODEALONG, L41_LAB),
    (4, 2): lesson(
        "Make method calls flexible and expressive with optional and named arguments, `params`, `out`, `ref`, and tuple return values.",
        L42_READING, L42_CODEALONG, L42_LAB),
    (4, 3): lesson(
        "Reuse one method name for different inputs, and predict which overload the compiler chooses.",
        L43_READING, L43_CODEALONG, L43_LAB),
    (4, 4): lesson(
        "Organize code with namespaces, `using` directives (including `global using` and `using static`), and the file layout rules for top-level statements versus `Main`.",
        L44_READING, L44_CODEALONG, L44_LAB),
}

# Reference solutions, used only by verify_content.py (never sent to the learner).
SOLUTIONS = {
    (4, 1): L41_SOLUTION,
    (4, 2): L42_SOLUTION,
    (4, 3): L43_SOLUTION,
    (4, 4): L44_SOLUTION,
}
