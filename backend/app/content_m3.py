"""Module 3: Control Flow."""
from .lesson_kit import *  # noqa: F401,F403

MS = "https://learn.microsoft.com/en-us/dotnet/csharp/"

# ─── 3.1 if, else, and Conditions ───

L31_READING = [
    h2("Programs that make decisions"),
    p("So far your programs ran every line from top to bottom, exactly once. Real programs need to choose: show an error if the password is wrong, apply a discount if the cart is big enough, skip a step if there is nothing to do. **Control flow** is the set of statements that decide which lines run, and the `if` statement is the most basic one."),
    code("""
int temperature = 31;

if (temperature > 30)
{
    Console.WriteLine("Hot day. Drink water.");
}
// Output: Hot day. Drink water.
"""),
    p("The condition inside the parentheses must be a `bool` expression. If it is `true`, the block runs; if it is `false`, the block is skipped. Add an `else` to handle the other case, and `else if` to chain more questions. C# checks them from top to bottom and runs **only the first branch that matches**."),
    code("""
int score = 78;

if (score >= 90)
{
    Console.WriteLine("Grade A");
}
else if (score >= 80)
{
    Console.WriteLine("Grade B");
}
else if (score >= 70)
{
    Console.WriteLine("Grade C");
}
else
{
    Console.WriteLine("Needs work");
}
// Output: Grade C
"""),
    note("If you are coming from Python: C# uses `else if` (two words) instead of `elif`, wraps the condition in parentheses, and uses `{ }` braces instead of indentation. The indentation is only for humans, so the compiler does not care about it. Also, C# has no \"truthiness\": `if (count)` does not compile for an `int`. The condition must really be a `bool`, so you write `if (count > 0)`."),
    h2("Comparison and logical operators"),
    p("Conditions are built from comparison operators (`==`, `!=`, `<`, `>`, `<=`, `>=`), which each produce a `bool`. You combine bools with the logical operators: `&&` (and), `||` (or), and `!` (not)."),
    code("""
int age = 20;
bool hasTicket = true;
bool isBanned = false;

bool canEnter = age >= 18 && hasTicket && !isBanned;
Console.WriteLine(canEnter);
// Output: True

bool needsHelp = age < 12 || age > 65;
Console.WriteLine(needsHelp);
// Output: False
"""),
    p("`&&` and `||` use **short-circuit evaluation**: C# stops as soon as the answer is known. In `a && b`, if `a` is `false`, `b` is never evaluated. This is not just an optimization; you can rely on it to guard a risky check behind a safe one."),
    code("""
string? name = null;

// Safe: if name is null, the right side never runs.
if (name != null && name.Length > 3)
{
    Console.WriteLine("Long name");
}
else
{
    Console.WriteLine("No long name");
}
// Output: No long name
"""),
    warn("**Common mistake:** `=` assigns and `==` compares. Writing `if (isReady = true)` compiles for a `bool` (with a warning) and quietly sets `isReady` to `true` every time. Another classic is ordering an `else if` chain badly: with `if (score >= 70) ... else if (score >= 90)`, a score of 95 matches the first branch and the second one is never reached. Put the most specific condition first."),
    h2("The conditional (ternary) operator"),
    p("When you only need to pick one of two **values**, the conditional operator `condition ? valueIfTrue : valueIfFalse` is more compact than a full `if`/`else`. It is an expression, so you can assign or print its result directly."),
    code("""
int items = 1;
string label = items == 1 ? "item" : "items";
Console.WriteLine($"{items} {label}");
// Output: 1 item
"""),
    tip("Use `?:` for a simple either/or value. If you find yourself nesting one ternary inside another, or the branches do different things (not just produce a value), switch back to `if`/`else`. Readability wins."),
    h2("Pattern basics: `is`, `and`, `or`, `not`"),
    p("C# has a readable way to test a value against a **pattern**. The `is` operator checks a value, and you can combine patterns with `and`, `or`, and `not`. This lets you write a range check without repeating the variable name."),
    code("""
int hour = 14;

bool isOpen = hour is >= 9 and < 17;       // same as hour >= 9 && hour < 17
bool isEarlyHour = hour is 1 or 2 or 3;         // match any of several constants
string? nickname = null;

if (nickname is null)
{
    Console.WriteLine("No nickname");
}
if (nickname is not null)
{
    Console.WriteLine(nickname.ToUpper());
}
// Output: No nickname
"""),
    p("Prefer `is null` and `is not null` over `== null` for null checks. They read like English and cannot be fooled by a type that redefines `==`. You will meet many more patterns in the next lesson on `switch`."),
    link("Read more on Microsoft Learn: Selection statements (if and switch)", MS + "language-reference/statements/selection-statements"),
]

L31_CODEALONG = codealong(
    "Code Along: Making Decisions",
    "Type each step into Program.cs below the previous one, then run the program after each step.",
    [
        step("A basic if/else", "Start with one variable and a two-way decision. Try changing `temperature` to 31 and run it again.",
             """
int temperature = 22;

if (temperature > 25)
{
    Console.WriteLine("It's hot.");
}
else
{
    Console.WriteLine("It's comfortable.");
}
"""),
        step("An else-if chain", "Add a chain that turns a score into a letter grade. Only the first matching branch runs.",
             """
int score = 78;
string grade;

if (score >= 90)
{
    grade = "A";
}
else if (score >= 80)
{
    grade = "B";
}
else if (score >= 70)
{
    grade = "C";
}
else
{
    grade = "F";
}

Console.WriteLine($"Score {score} -> grade {grade}");
"""),
        step("Combine conditions", "Use `&&`, `||`, and `!` to build bigger conditions from smaller bools.",
             """
int age = 20;
bool hasTicket = true;
bool isWeekend = false;
bool isHoliday = true;

if (age >= 18 && hasTicket)
{
    Console.WriteLine("You may enter.");
}

if (isWeekend || isHoliday)
{
    Console.WriteLine("No school today.");
}

if (!hasTicket)
{
    Console.WriteLine("Buy a ticket first.");
}
"""),
        step("The ternary operator", "Choose between two values in a single expression.",
             """
string ageGroup = age >= 18 ? "adult" : "minor";
Console.WriteLine($"Age group: {ageGroup}");
"""),
        step("Patterns with is", "Finish with relational and logical patterns, plus `is null` and `is not null`.",
             """
int hour = 14;
bool isOpen = hour is >= 9 and < 17;
Console.WriteLine($"Open at {hour}:00? {isOpen}");

char letter = 'e';
bool isVowel = letter is 'a' or 'e' or 'i' or 'o' or 'u';
Console.WriteLine($"{letter} is a vowel: {isVowel}");

string? nickname = null;
Console.WriteLine(nickname is null ? "No nickname" : nickname);
"""),
    ],
)

L31_LAB = lab(
    "Lab: Shop Day Planner",
    "Beginner",
    "Use if/else chains, logical operators, the ternary operator, and patterns to make four decisions from a few starting values. The output is fully determined by the values given below.",
    [
        "Declare `int temperature = 18;` and classify it with an if/else if/else chain: below 10 is `Cold`, 10 to 19 is `Cool`, 20 to 29 is `Warm`, and 30 or more is `Hot`. Print `Temperature 18: Cool` (using the variable in the text).",
        "Declare `bool isRaining = true;` and use the ternary operator to print `Bring an umbrella` when it is raining, otherwise `No umbrella needed`.",
        "Declare `int hour = 14;` and use a pattern (`is >= 9 and < 17`) to store a bool named `isOpen`. Print `Shop is Open` or `Shop is Closed` accordingly (the word comes from `isOpen`).",
        "Declare `int year = 2024;` and decide if it is a leap year: divisible by 4 and not by 100, or divisible by 400. Print `2024 is a leap year` or `2024 is not a leap year` (using the variable).",
        "Print the four results in the order listed above, one per line.",
    ],
    "Temperature 18: Cool\nBring an umbrella\nShop is Open\n2024 is a leap year",
    "For the leap year, group with parentheses: `(year % 4 == 0 && year % 100 != 0) || year % 400 == 0`. For the shop line, `isOpen ? \"Open\" : \"Closed\"` can go right inside an interpolated string if you wrap it in parentheses.",
)

L31_SOLUTION = """int temperature = 18;
string kind;
if (temperature < 10)
{
    kind = "Cold";
}
else if (temperature < 20)
{
    kind = "Cool";
}
else if (temperature < 30)
{
    kind = "Warm";
}
else
{
    kind = "Hot";
}
Console.WriteLine($"Temperature {temperature}: {kind}");

bool isRaining = true;
Console.WriteLine(isRaining ? "Bring an umbrella" : "No umbrella needed");

int hour = 14;
bool isOpen = hour is >= 9 and < 17;
Console.WriteLine($"Shop is {(isOpen ? "Open" : "Closed")}");

int year = 2024;
bool leap = (year % 4 == 0 && year % 100 != 0) || year % 400 == 0;
Console.WriteLine(leap ? $"{year} is a leap year" : $"{year} is not a leap year");
"""

# ─── 3.2 switch Statements and Expressions ───

L32_READING = [
    h2("When an if/else chain gets long"),
    p("If you are comparing one value against many possibilities, a long `else if` chain repeats the variable over and over. The `switch` statement is built for this: it looks at one value and jumps to the matching `case`."),
    code("""
int day = 3;

switch (day)
{
    case 1:
        Console.WriteLine("Monday");
        break;
    case 2:
        Console.WriteLine("Tuesday");
        break;
    case 3:
        Console.WriteLine("Wednesday");
        break;
    default:
        Console.WriteLine("Another day");
        break;
}
// Output: Wednesday
"""),
    p("Each `case` ends with `break` (or `return`/`throw`, which you will meet later). The `default` case runs when nothing else matches. You can stack several labels on one block to share behavior."),
    code("""
char grade = 'B';

switch (grade)
{
    case 'A':
    case 'B':
        Console.WriteLine("Good job");
        break;
    case 'C':
        Console.WriteLine("Okay");
        break;
    default:
        Console.WriteLine("See your teacher");
        break;
}
// Output: Good job
"""),
    warn("**Common mistake:** forgetting `break`. In C, C++, and JavaScript a missing `break` makes execution \"fall through\" into the next case. C# refuses to compile it (error CS8120: control cannot fall through from one case label to another), which saves you from that bug. Stacked empty labels like `case 'A': case 'B':` are the only allowed form of sharing."),
    h2("The switch expression"),
    p("Most switches exist only to **produce a value**. The switch expression does that in far less code: no `case`, no `break`, and each arm uses `=>` to say \"if the value matches this pattern, the result is that\". The `_` is the **discard** pattern and matches anything, so it plays the role of `default`."),
    code("""
int day = 6;

string kind = day switch
{
    1 or 2 or 3 or 4 or 5 => "Weekday",
    6 or 7 => "Weekend",
    _ => "Not a valid day"
};
Console.WriteLine(kind);
// Output: Weekend
"""),
    p("The arms are separated by commas, the last one is optional-comma, and the whole thing ends with a semicolon because it is an expression. Arms are checked top to bottom and the first match wins."),
    h2("Relational patterns and `when` guards"),
    p("Arms can use the same patterns you saw with `is`: relational patterns (`<`, `>=`, and so on) and the combinators `and`, `or`, `not`. This replaces many `else if` ranges with a clean table."),
    code("""
int score = 85;

string grade = score switch
{
    >= 90 => "A",
    >= 80 => "B",
    >= 70 => "C",
    _ => "F"
};
Console.WriteLine(grade);
// Output: B
"""),
    p("When a pattern is not enough, add a `when` guard, which is any bool condition that must also be true for the arm to match."),
    code("""
int number = 12;

string description = number switch
{
    0 => "zero",
    < 0 => "negative",
    _ when number % 2 == 0 => "positive and even",
    _ => "positive and odd"
};
Console.WriteLine(description);
// Output: positive and even
"""),
    h2("Switching on more than one value"),
    p("To switch on two values at once, wrap them in a tuple (a pair in parentheses) and match both. You will learn more about tuples in module 4; here, think of `(a, b)` as \"look at a and b together\"."),
    code("""
bool isMember = true;
int items = 12;

string shipping = (isMember, items) switch
{
    (true, _) => "Free shipping",
    (false, >= 10) => "Discounted shipping",
    _ => "Standard shipping"
};
Console.WriteLine(shipping);
// Output: Free shipping
"""),
    warn("A switch expression must cover every possible input. If you forget a `_` arm for an `int`, the compiler warns that the expression is not exhaustive, and at runtime an unmatched value throws an exception (`SwitchExpressionException`). Always finish with a `_` arm unless the compiler can prove all cases are covered."),
    tip("Rule of thumb: use a **switch expression** when you are computing a value, a **switch statement** when each case needs to run several statements, and a plain `if` when you have one or two simple conditions."),
    link("Read more on Microsoft Learn: The switch expression", MS + "language-reference/operators/switch-expression"),
]

L32_CODEALONG = codealong(
    "Code Along: Switching on Values",
    "Add each step to Program.cs, run it, and then change the starting values to see other results.",
    [
        step("A switch statement", "Print the name of a weekday. Notice each case ends with `break`.",
             """
int dayNumber = 3;

switch (dayNumber)
{
    case 1:
        Console.WriteLine("Monday");
        break;
    case 2:
        Console.WriteLine("Tuesday");
        break;
    case 3:
        Console.WriteLine("Wednesday");
        break;
    default:
        Console.WriteLine("Another day");
        break;
}
"""),
        step("Share a block between cases", "Stack labels to treat several values the same way.",
             """
char letterGrade = 'B';

switch (letterGrade)
{
    case 'A':
    case 'B':
        Console.WriteLine("Good job");
        break;
    case 'C':
        Console.WriteLine("Okay");
        break;
    default:
        Console.WriteLine("See your teacher");
        break;
}
"""),
        step("A switch expression", "The same idea, but producing a value. Use `or` to match several constants.",
             """
int day = 6;

string dayKind = day switch
{
    1 or 2 or 3 or 4 or 5 => "Weekday",
    6 or 7 => "Weekend",
    _ => "Not a valid day"
};
Console.WriteLine($"Day {day} is a {dayKind}");
"""),
        step("Relational patterns", "Replace an else-if ladder with ranges.",
             """
int score = 85;

string grade = score switch
{
    >= 90 => "A",
    >= 80 => "B",
    >= 70 => "C",
    _ => "F"
};
Console.WriteLine($"Score {score} is a {grade}");
"""),
        step("Guards and tuples", "Use `when` for an extra condition, and a tuple to switch on two values at once.",
             """
int number = 12;

string description = number switch
{
    0 => "zero",
    < 0 => "negative",
    _ when number % 2 == 0 => "positive and even",
    _ => "positive and odd"
};
Console.WriteLine($"{number} is {description}");

bool isMember = false;
int itemCount = 12;

string shipping = (isMember, itemCount) switch
{
    (true, _) => "Free shipping",
    (false, >= 10) => "Discounted shipping",
    _ => "Standard shipping"
};
Console.WriteLine(shipping);
"""),
    ],
)

L32_LAB = lab(
    "Lab: Rock, Paper, Scissors Referee",
    "Beginner",
    "Build a tiny referee with a switch expression that matches a pair of choices using tuple patterns, then grade a score with relational patterns.",
    [
        "Declare three rounds as string variables: `a1 = \"rock\"`, `b1 = \"scissors\"`; `a2 = \"paper\"`, `b2 = \"paper\"`; `a3 = \"scissors\"`, `b3 = \"rock\"` (player A and player B).",
        "For each round, use a switch expression on the tuple `(a, b)` that returns `Player A wins` for rock beats scissors, scissors beats paper, and paper beats rock (A's choice first), `Draw` when both choices are equal (use a `_ when` guard), and `Player B wins` otherwise.",
        "Print each result as `Round 1: <result>`, `Round 2: <result>`, `Round 3: <result>`.",
        "Declare `int points = 85;` and use a switch expression with relational patterns to produce `A` for 90 or more, `B` for 80 to 89, `C` for 70 to 79, and `F` otherwise. Print `Grade: B`, using the variable for the letter.",
    ],
    "Round 1: Player A wins\nRound 2: Draw\nRound 3: Player B wins\nGrade: B",
    "Write the first arm like `(\"rock\", \"scissors\") or (\"scissors\", \"paper\") or (\"paper\", \"rock\") => ...`. Because you need the same expression three times, copy it and change the variable names. Order matters: put the draw guard `_ when a == b` after the winning arms and a final `_` arm last.",
)

L32_SOLUTION = """string a1 = "rock", b1 = "scissors";
string a2 = "paper", b2 = "paper";
string a3 = "scissors", b3 = "rock";

string r1 = (a1, b1) switch
{
    ("rock", "scissors") or ("scissors", "paper") or ("paper", "rock") => "Player A wins",
    _ when a1 == b1 => "Draw",
    _ => "Player B wins"
};
string r2 = (a2, b2) switch
{
    ("rock", "scissors") or ("scissors", "paper") or ("paper", "rock") => "Player A wins",
    _ when a2 == b2 => "Draw",
    _ => "Player B wins"
};
string r3 = (a3, b3) switch
{
    ("rock", "scissors") or ("scissors", "paper") or ("paper", "rock") => "Player A wins",
    _ when a3 == b3 => "Draw",
    _ => "Player B wins"
};
Console.WriteLine($"Round 1: {r1}");
Console.WriteLine($"Round 2: {r2}");
Console.WriteLine($"Round 3: {r3}");

int points = 85;
string letter = points switch
{
    >= 90 => "A",
    >= 80 => "B",
    >= 70 => "C",
    _ => "F"
};
Console.WriteLine($"Grade: {letter}");
"""

# ─── 3.3 for and foreach Loops ───

L33_READING = [
    h2("Doing something many times"),
    p("A **loop** repeats a block of code. Instead of copying `Console.WriteLine` ten times you write it once and tell C# how many times to run it. C# has four loops; in this lesson you will learn the two you use most often: `for` and `foreach`. The `while` loops come in the next lesson."),
    h2("The for loop"),
    p("A `for` loop packs three parts into its header: an **initializer** (runs once), a **condition** (checked before every pass), and an **iterator** (runs after every pass). It is the right tool when you know how many times to repeat or you need the counter."),
    code("""
for (int i = 1; i <= 5; i++)
{
    Console.WriteLine($"Pass {i}");
}
// Output:
// Pass 1
// Pass 2
// Pass 3
// Pass 4
// Pass 5
"""),
    p("Read the header aloud: \"start `i` at 1, keep going while `i` is at most 5, and add 1 after each pass.\" `i++` is shorthand for `i = i + 1`. The variable `i` only exists inside the loop. You can also count down or by steps, such as `i -= 2`."),
    h2("A first look at arrays"),
    p("To loop over a group of values you need a collection. Full collections such as `List<T>` come in module 6. For now, all you need is an **array**, a fixed-size, ordered group of values of one type. You write the type with `[]`, create it with square brackets, read an element with an index that starts at **0**, and get the size from `.Length`."),
    code("""
int[] scores = [90, 72, 85];
string[] names = ["Ada", "Linus", "Grace"];

Console.WriteLine(scores[0]);      // Output: 90
Console.WriteLine(names.Length);   // Output: 3
"""),
    warn("**Common mistake:** off-by-one errors. Array indexes run from `0` to `Length - 1`. A loop like `for (int i = 0; i <= scores.Length; i++)` goes one step too far, and reading `scores[3]` throws an `IndexOutOfRangeException` and crashes your program. Use `i < scores.Length`."),
    h2("The foreach loop"),
    p("When you just need every item and do not care about its position, `foreach` is simpler and safer: there is no counter to get wrong."),
    code("""
string[] names = ["Ada", "Linus", "Grace"];

foreach (string name in names)
{
    Console.WriteLine($"Hello, {name}!");
}
// Output:
// Hello, Ada!
// Hello, Linus!
// Hello, Grace!
"""),
    p("The loop variable (`name`) is read-only: you cannot assign to it inside the loop. If you need the index or you need to change items, use a `for` loop instead. Later you will use the same `foreach` on lists and many other collections."),
    h2("break and continue"),
    p("Two keywords change how a loop runs. `continue` skips the rest of the current pass and moves to the next one. `break` leaves the loop entirely."),
    code("""
int[] numbers = [4, -2, 9, 0, 15];
int sum = 0;

foreach (int n in numbers)
{
    if (n < 0)
    {
        continue;      // skip negatives, go to next item
    }
    if (n == 0)
    {
        break;         // stop at the first zero
    }
    sum += n;
}
Console.WriteLine(sum);
// Output: 13
"""),
    p("Trace that carefully: 4 is added, -2 is skipped, 9 is added, then 0 triggers `break`, so 15 is never reached. The sum is **13**. Tracing a loop by hand on a small example is the best way to understand what it does."),
    h2("Nested loops"),
    p("A loop inside another loop is a **nested loop**. The inner loop runs completely for every single pass of the outer loop. This is how you build grids and tables."),
    code("""
for (int row = 1; row <= 3; row++)
{
    for (int col = 1; col <= 3; col++)
    {
        Console.Write($"{row * col} ");
    }
    Console.WriteLine();
}
// Output:
// 1 2 3
// 2 4 6
// 3 6 9
"""),
    tip("`Console.Write` prints without a line break and `Console.WriteLine()` with no argument ends the line. A `break` inside the inner loop only leaves the inner loop, not the outer one."),
    link("Read more on Microsoft Learn: Iteration statements", MS + "language-reference/statements/iteration-statements"),
]

L33_CODEALONG = codealong(
    "Code Along: Loops",
    "Build up one program with a loop of each kind. Run it after every step and read the output carefully.",
    [
        step("A counting for loop", "Print the numbers 1 to 5, then count down from 3.",
             """
for (int i = 1; i <= 5; i++)
{
    Console.WriteLine($"Pass {i}");
}

for (int countdown = 3; countdown >= 1; countdown--)
{
    Console.WriteLine($"{countdown}...");
}
Console.WriteLine("Liftoff!");
"""),
        step("Loop over an array", "Create an array and use `for` with `Length`, then `foreach`. Arrays are covered fully later; for now, `int[]` is just a fixed list of ints.",
             """
int[] numbers = [4, -2, 9, 0, 15];

for (int i = 0; i < numbers.Length; i++)
{
    Console.WriteLine($"numbers[{i}] = {numbers[i]}");
}

string[] names = ["Ada", "Linus", "Grace"];
foreach (string name in names)
{
    Console.WriteLine($"Hello, {name}!");
}
"""),
        step("continue and break", "Skip negatives with `continue` and stop at the first zero with `break`. Predict the sum before you run it.",
             """
int sum = 0;
foreach (int n in numbers)
{
    if (n < 0)
    {
        continue;
    }
    if (n == 0)
    {
        break;
    }
    sum += n;
}
Console.WriteLine($"Sum before the first zero: {sum}");
"""),
        step("Nested loops", "Print a small multiplication table. The inner loop runs fully for each row.",
             """
for (int row = 1; row <= 3; row++)
{
    for (int col = 1; col <= 3; col++)
    {
        Console.Write($"{row * col} ");
    }
    Console.WriteLine();
}
"""),
    ],
)

L33_LAB = lab(
    "Lab: Number Cruncher",
    "Beginner",
    "Use foreach, for, continue, break, and nested loops on a small array to produce three pieces of output.",
    [
        "Declare `int[] data = [4, -2, 9, 0, 15, -7, 8, 23, 6];`.",
        "Use `foreach` and `continue` to add up every value that is not negative. Print `Sum of non-negatives: 65`, using the variable for the number.",
        "Use a `for` loop with an index and `break` to find the first value greater than 20. Print `First value over 20 is 23 at index 7`, using variables for the value and the index.",
        "Use nested `for` loops (an outer loop for rows 1 to 4, an inner loop for the stars) with `Console.Write(\"*\")` and `Console.WriteLine()` to print a right triangle of stars: one star on the first line, two on the second, up to four.",
        "Print the three results in the order listed: the sum line, the first-over-20 line, then the four star lines.",
    ],
    "Sum of non-negatives: 65\nFirst value over 20 is 23 at index 7\n*\n**\n***\n****",
    "For the search, declare `int foundIndex = -1;` before the loop; when you find a match, set it and `break`. For the triangle, the inner loop should run from 1 up to the current row number.",
)

L33_SOLUTION = """int[] data = [4, -2, 9, 0, 15, -7, 8, 23, 6];

int sum = 0;
foreach (int value in data)
{
    if (value < 0)
    {
        continue;
    }
    sum += value;
}
Console.WriteLine($"Sum of non-negatives: {sum}");

int foundIndex = -1;
for (int i = 0; i < data.Length; i++)
{
    if (data[i] > 20)
    {
        foundIndex = i;
        break;
    }
}
Console.WriteLine($"First value over 20 is {data[foundIndex]} at index {foundIndex}");

for (int row = 1; row <= 4; row++)
{
    for (int star = 1; star <= row; star++)
    {
        Console.Write("*");
    }
    Console.WriteLine();
}
"""

# ─── 3.4 while and do-while Loops ───

L34_READING = [
    h2("Looping until something happens"),
    p("A `for` loop is great when you know how many passes you need. Often you do not: you want to keep going **until** something becomes true, such as a user typing \"quit\", a balance reaching a goal, or a number shrinking to zero. That is the job of `while` and `do`/`while`."),
    h2("The while loop"),
    p("A `while` loop checks its condition **before** each pass. If the condition is false the very first time, the body never runs."),
    code("""
int fuel = 3;

while (fuel > 0)
{
    Console.WriteLine($"Burning fuel, {fuel} left");
    fuel--;
}
Console.WriteLine("Out of fuel");
// Output:
// Burning fuel, 3 left
// Burning fuel, 2 left
// Burning fuel, 1 left
// Out of fuel
"""),
    p("Every `while` loop needs three things: a starting state (`fuel = 3`), a condition that uses that state (`fuel > 0`), and a change inside the body that eventually makes the condition false (`fuel--`). Missing any one of them is the usual source of bugs."),
    warn("**Common mistake:** the infinite loop. If you forget `fuel--`, the condition stays true forever and the program hangs, burning CPU until you stop it (Ctrl+C in a terminal). Another variant is changing the wrong variable, or a condition that can never become false such as `while (x >= 0)` while `x` only grows. When a loop seems stuck, add a `Console.WriteLine` of the variable in the condition and watch it."),
    h2("The do-while loop"),
    p("A `do`/`while` loop checks its condition **after** the body, so the body always runs at least once. It fits cases like \"show a menu, then ask whether to show it again\". Note the semicolon after the condition."),
    code("""
int attempts = 0;

do
{
    attempts++;
    Console.WriteLine($"Attempt {attempts}");
}
while (attempts < 3);
// Output:
// Attempt 1
// Attempt 2
// Attempt 3
"""),
    code("""
int count = 10;

while (count < 5)
{
    Console.WriteLine("while: never printed");
}

do
{
    Console.WriteLine("do-while: printed once");
}
while (count < 5);
// Output: do-while: printed once
"""),
    h2("Sentinel loops"),
    p("A **sentinel** is a special value that means \"stop\". The pattern is: read an item, and keep looping until you see the sentinel. In real programs the items usually come from the keyboard or a file. In this course your programs run without a keyboard, so we simulate the input with an array and an index. The loop logic is identical."),
    code("""
int[] inputs = [5, 12, 7, -1, 99];   // -1 is the sentinel; 99 is never reached
int index = 0;
int total = 0;

while (inputs[index] != -1)
{
    total += inputs[index];
    index++;
}
Console.WriteLine($"Total: {total}");
// Output: Total: 24
"""),
    p("If the sentinel were missing from the array, `index` would run past the end and throw an `IndexOutOfRangeException`. In real code you would also check `index < inputs.Length`."),
    h2("while (true) with break"),
    p("Sometimes the natural place to decide to stop is in the middle of the body, not at the top. A deliberate infinite loop `while (true)` combined with `break` handles that cleanly."),
    code("""
int n = 1;

while (true)
{
    n *= 2;
    if (n > 100)
    {
        break;
    }
}
Console.WriteLine(n);
// Output: 128
"""),
    tip("Use `for` when you count, `foreach` when you visit every item, `while` when you repeat until a condition changes, `do`/`while` when the body must run at least once, and `while (true)` plus `break` when the exit test belongs in the middle. `continue` and `break` work in all of them."),
    link("Read more on Microsoft Learn: Iteration statements (while and do)", MS + "language-reference/statements/iteration-statements"),
]

L34_CODEALONG = codealong(
    "Code Along: Looping Until Done",
    "Add each step to Program.cs. For every loop, predict the output before you run it.",
    [
        step("A while loop", "A countdown that changes its own state each pass.",
             """
int fuel = 3;

while (fuel > 0)
{
    Console.WriteLine($"Burning fuel, {fuel} left");
    fuel--;
}
Console.WriteLine("Out of fuel");
"""),
        step("while versus do-while", "Start the counter past the limit. The `while` body is skipped but the `do` body runs once.",
             """
int level = 10;

while (level < 5)
{
    Console.WriteLine("while: never printed");
}

do
{
    Console.WriteLine("do-while: printed once");
}
while (level < 5);
"""),
        step("A sentinel loop", "Total up values until the sentinel `-1` shows up. The array simulates user input.",
             """
int[] inputs = [5, 12, 7, -1, 99];
int index = 0;
int total = 0;

while (inputs[index] != -1)
{
    total += inputs[index];
    index++;
}
Console.WriteLine($"Total: {total}");
"""),
        step("while (true) with break", "Double a number until it passes 100, deciding to stop in the middle of the body.",
             """
int doubled = 1;

while (true)
{
    doubled *= 2;
    if (doubled > 100)
    {
        break;
    }
}
Console.WriteLine($"First power of two above 100: {doubled}");
"""),
        step("Loop on a changing number", "Peel digits off a number with `%` and `/`. This loop runs until the number reaches 0.",
             """
int number = 4721;
int digitSum = 0;

while (number > 0)
{
    digitSum += number % 10;
    number /= 10;
}
Console.WriteLine($"Digit sum: {digitSum}");
"""),
    ],
)

L34_LAB = lab(
    "Lab: Collatz and Compound Growth",
    "Intermediate",
    "Use while loops where the number of passes is not known in advance: the Collatz sequence, a digit sum, and compound growth until a goal is reached.",
    [
        "Collatz: start with `long value = 27;` and `int steps = 0;` and `long peak = value;`. While `value != 1`: if `value` is even divide it by 2, otherwise set it to `3 * value + 1`; add 1 to `steps`; and update `peak` if `value` is larger. Print `Collatz 27: 111 steps, peak 9232` using your variables.",
        "Digit sum: start with `int n = 9875;` and use a `while (n > 0)` loop with `% 10` and `/ 10` to add up the digits. Print `Digit sum: 29` using the variable.",
        "Compound growth: start with `decimal balance = 1000m;` and `int years = 0;`. Use a `while` loop that runs while `balance < 2000m`, multiplying the balance by `1.05m` and adding 1 to `years` each pass. Print `Years to double: 15` and then `Final balance: 2078.93` (format the balance with `:F2`).",
        "Use a `do`/`while` loop that runs at least once to print `Tries: 1` when its condition `tries < 1` starts out false (declare `int tries = 0;` and increment it inside the body, then print it after the loop).",
        "Print the results in the order given: Collatz, digit sum, years, final balance, tries.",
    ],
    "Collatz 27: 111 steps, peak 9232\nDigit sum: 29\nYears to double: 15\nFinal balance: 2078.93\nTries: 1",
    "Use `value % 2 == 0` to test for even. The loop conditions for each part are `value != 1`, `n > 0`, and `balance < 2000m`. For the do/while, the body is `tries++;` and the condition is `tries < 1`.",
)

L34_SOLUTION = """long value = 27;
int steps = 0;
long peak = value;
while (value != 1)
{
    if (value % 2 == 0)
    {
        value /= 2;
    }
    else
    {
        value = 3 * value + 1;
    }
    steps++;
    if (value > peak)
    {
        peak = value;
    }
}
Console.WriteLine($"Collatz 27: {steps} steps, peak {peak}");

int n = 9875;
int digitSum = 0;
while (n > 0)
{
    digitSum += n % 10;
    n /= 10;
}
Console.WriteLine($"Digit sum: {digitSum}");

decimal balance = 1000m;
int years = 0;
while (balance < 2000m)
{
    balance *= 1.05m;
    years++;
}
Console.WriteLine($"Years to double: {years}");
Console.WriteLine($"Final balance: {balance:F2}");

int tries = 0;
do
{
    tries++;
}
while (tries < 1);
Console.WriteLine($"Tries: {tries}");
"""

# ─── 3.5 Exceptions and try/catch ───

L35_READING = [
    h2("When things go wrong"),
    p("Sometimes a program is asked to do something impossible: divide by zero, read item 10 of a 3-item array, or turn the text \"abc\" into a number. When that happens .NET creates an **exception**, an object that describes the problem, and **throws** it. If nothing catches it, the program crashes with an error message."),
    code("""
int[] values = [1, 2, 3];
int position = 10;

Console.WriteLine(values[position]);   // throws IndexOutOfRangeException
Console.WriteLine("never reached");
"""),
    p("Exceptions are for **unexpected problems**. You deal with them using a `try`/`catch` statement: put the risky code in the `try` block, and put the recovery code in a `catch` block. If nothing goes wrong, the `catch` is skipped. If something goes wrong, execution jumps straight to the `catch`."),
    code("""
int top = 10;
int bottom = 0;

try
{
    int result = top / bottom;
    Console.WriteLine(result);
}
catch (DivideByZeroException)
{
    Console.WriteLine("Cannot divide by zero.");
}
Console.WriteLine("Program continues.");
// Output:
// Cannot divide by zero.
// Program continues.
"""),
    h2("Catch specific exceptions"),
    p("Every exception has a type, such as `DivideByZeroException`, `FormatException`, or `ArgumentException`. You can write several `catch` blocks, each for a different type. C# uses the first one that matches, so list the **most specific types first**. The general `Exception` type matches everything and belongs last, if you use it at all."),
    code("""
string text = "abc";

try
{
    int number = int.Parse(text);
    Console.WriteLine(number);
}
catch (FormatException)
{
    Console.WriteLine("That is not a number.");
}
catch (OverflowException)
{
    Console.WriteLine("That number is too big.");
}
// Output: That is not a number.
"""),
    p("Inside a catch you can name the exception to inspect it: `catch (FormatException ex)`. `ex.GetType().Name` gives the type name and `ex.Message` gives a description. Messages for built-in exceptions are written for developers and can differ between .NET versions, so do not build program logic on their exact text."),
    warn("**Common mistake:** `catch (Exception) { }` with an empty body. It swallows every problem, including bugs you never expected, and leaves you with a program that silently does the wrong thing. Catch only the exceptions you know how to handle, and do something useful when you do."),
    h2("finally: code that always runs"),
    p("A `finally` block runs whether the `try` succeeded, a `catch` handled an error, or an exception escaped. It is for cleanup you must never skip, such as closing a file or releasing a resource. (Later you will see the `using` statement, which does this cleanup for you.)"),
    code("""
try
{
    Console.WriteLine("Working...");
    throw new InvalidOperationException("Something broke");
}
catch (InvalidOperationException ex)
{
    Console.WriteLine($"Caught: {ex.Message}");
}
finally
{
    Console.WriteLine("Cleanup done.");
}
// Output:
// Working...
// Caught: Something broke
// Cleanup done.
"""),
    h2("Throwing your own exceptions"),
    p("You can raise an exception yourself with `throw new SomeException(\"message\")`. Do this when your code detects input it cannot work with. Pick the built-in type that best describes the problem: `ArgumentException` for a bad argument, `InvalidOperationException` for an action that is not valid right now, and so on. The message you pass in is what `ex.Message` returns."),
    code("""
int age = -5;

try
{
    if (age < 0)
    {
        throw new ArgumentException("Age cannot be negative.");
    }
}
catch (ArgumentException ex)
{
    Console.WriteLine(ex.Message);
}
// Output: Age cannot be negative.
"""),
    note("If you catch an exception just to log it and want it to keep travelling up, write `throw;` (alone). Writing `throw ex;` instead resets the exception's stack trace and hides where the error really started."),
    h2("TryParse versus exceptions"),
    p("Bad user input is not really exceptional: it happens all the time. `int.Parse` throws when the text is wrong, but `int.TryParse` returns a `bool` and hands the number back through an `out` parameter (you will learn `out` properly in the next module). It is faster and clearer for input you expect to be bad."),
    code("""
if (int.TryParse("42", out int good))
{
    Console.WriteLine($"Parsed {good}");
}
if (!int.TryParse("forty-two", out int bad))
{
    Console.WriteLine($"Could not parse, bad is {bad}");
}
// Output:
// Parsed 42
// Could not parse, bad is 0
"""),
    tip("Rule of thumb: if the failure is **common and expected** (typed input, optional data), check with `TryParse` or an `if`. If it means **something is truly broken** or a caller broke the rules, throw an exception. Exceptions are slow compared to normal code, and using them for everyday flow control makes programs harder to read."),
    link("Read more on Microsoft Learn: Exception handling", MS + "fundamentals/exceptions/"),
]

L35_CODEALONG = codealong(
    "Code Along: Catching Exceptions",
    "These steps print exception type names and your own messages. Those are stable, unlike the wording of built-in messages.",
    [
        step("Catch a divide-by-zero", "Put the risky division in `try` and recover in `catch`. The last line proves the program kept going.",
             """
int top = 10;
int bottom = 0;

try
{
    int result = top / bottom;
    Console.WriteLine(result);
}
catch (DivideByZeroException)
{
    Console.WriteLine("Cannot divide by zero.");
}
Console.WriteLine("Program continues.");
"""),
        step("Several catch blocks", "Parse three strings. Each failure lands in the catch that matches its exception type.",
             """
string[] inputs = ["42", "abc", "99999999999"];

foreach (string text in inputs)
{
    try
    {
        int number = int.Parse(text);
        Console.WriteLine($"Parsed {number}");
    }
    catch (FormatException)
    {
        Console.WriteLine($"'{text}' is not a number");
    }
    catch (OverflowException)
    {
        Console.WriteLine($"'{text}' is too big for an int");
    }
}
"""),
        step("finally and throw", "Throw your own exception, catch it by type, and see that `finally` runs regardless.",
             """
try
{
    Console.WriteLine("Working...");
    throw new InvalidOperationException("Something broke");
}
catch (InvalidOperationException ex)
{
    Console.WriteLine($"Caught {ex.GetType().Name}: {ex.Message}");
}
finally
{
    Console.WriteLine("Cleanup done.");
}
"""),
        step("Validate with throw", "Throw `ArgumentException` for an invalid value and catch it just a few lines later.",
             """
int age = -5;

try
{
    if (age < 0)
    {
        throw new ArgumentException("Age cannot be negative.");
    }
    Console.WriteLine("Age is fine.");
}
catch (ArgumentException ex)
{
    Console.WriteLine(ex.Message);
}
"""),
        step("TryParse instead", "For expected bad input, ask `TryParse` rather than catching an exception.",
             """
if (int.TryParse("42", out int good))
{
    Console.WriteLine($"Parsed {good}");
}
if (!int.TryParse("forty-two", out int bad))
{
    Console.WriteLine($"Could not parse, bad is {bad}");
}
"""),
    ],
)

L35_LAB = lab(
    "Lab: Safe Calculator",
    "Intermediate",
    "Process a list of text inputs, converting each to a number and dividing 100 by it. Handle three different kinds of failure with separate catch blocks, always run a finally block, and then count valid inputs with TryParse.",
    [
        "Declare `string[] inputs = [\"10\", \"abc\", \"0\", \"25\", \"-5\"];` and loop over it with `foreach` (call the loop variable `s`).",
        "Inside a `try`, parse with `int.Parse(s)` into `n`. If `n < 0`, `throw new ArgumentException($\"Negative not allowed: {n}\");`. Otherwise compute `100 / n` and print `100 / <n> = <result>`.",
        "Add `catch (FormatException)` printing `'<s>' is not a number`, `catch (DivideByZeroException)` printing `Cannot divide by zero`, and `catch (ArgumentException ex)` printing `Error: ` followed by `ex.Message`.",
        "Add a `finally` block that prints `Done with '<s>'` for every input, success or failure.",
        "After the loop, use `int.TryParse(s, out _)` in a second `foreach` to count how many inputs are valid integers, and print `Valid numbers: 4`, using your counter.",
    ],
    """
100 / 10 = 10
Done with '10'
'abc' is not a number
Done with 'abc'
Cannot divide by zero
Done with '0'
100 / 25 = 4
Done with '25'
Error: Negative not allowed: -5
Done with '-5'
Valid numbers: 4
""",
    "Order the catch blocks however you like since the three types are unrelated. `ArgumentException` and `FormatException` are separate types here. The `_` in `out _` means \"I do not need the value\".",
)

L35_SOLUTION = """string[] inputs = ["10", "abc", "0", "25", "-5"];

foreach (string s in inputs)
{
    try
    {
        int n = int.Parse(s);
        if (n < 0)
        {
            throw new ArgumentException($"Negative not allowed: {n}");
        }
        Console.WriteLine($"100 / {n} = {100 / n}");
    }
    catch (FormatException)
    {
        Console.WriteLine($"'{s}' is not a number");
    }
    catch (DivideByZeroException)
    {
        Console.WriteLine("Cannot divide by zero");
    }
    catch (ArgumentException ex)
    {
        Console.WriteLine($"Error: {ex.Message}");
    }
    finally
    {
        Console.WriteLine($"Done with '{s}'");
    }
}

int valid = 0;
foreach (string s in inputs)
{
    if (int.TryParse(s, out _))
    {
        valid++;
    }
}
Console.WriteLine($"Valid numbers: {valid}");
"""

LESSONS = {
    (3, 1): lesson(
        "Make your programs choose. You will write if/else if/else chains, combine conditions with logical operators, pick values with the ternary operator, and use simple patterns with `is`.",
        L31_READING, L31_CODEALONG, L31_LAB),
    (3, 2): lesson(
        "Replace long else-if ladders with `switch`. You will use the classic switch statement, the modern switch expression, and relational, `when`, and tuple patterns.",
        L32_READING, L32_CODEALONG, L32_LAB),
    (3, 3): lesson(
        "Repeat work with `for` and `foreach`, control loops with `break` and `continue`, and nest loops to build grids. Includes a first look at `int[]` and `string[]` arrays.",
        L33_READING, L33_CODEALONG, L33_LAB),
    (3, 4): lesson(
        "Repeat until a condition changes using `while` and `do`/`while`, build sentinel loops, and learn to spot and avoid infinite loops.",
        L34_READING, L34_CODEALONG, L34_LAB),
    (3, 5): lesson(
        "Handle failure gracefully with try/catch/finally, throw your own exceptions, and choose between exceptions and `int.TryParse`.",
        L35_READING, L35_CODEALONG, L35_LAB),
}

# Reference solutions, used only by verify_content.py (never sent to the learner).
SOLUTIONS = {
    (3, 1): L31_SOLUTION,
    (3, 2): L32_SOLUTION,
    (3, 3): L33_SOLUTION,
    (3, 4): L34_SOLUTION,
    (3, 5): L35_SOLUTION,
}
