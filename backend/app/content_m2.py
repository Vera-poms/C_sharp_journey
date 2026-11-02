"""Module 2: Variables, Types, and Operators."""
from .lesson_kit import *  # noqa: F401,F403

# ─── Module 2, lesson 2: Built-in Data Types ───

BUILTIN_TYPES_READING = [
    {"type": "h2", "text": "What is a data type?"},
    {
        "type": "p",
        "text": "A data type tells the compiler two things: how much memory to reserve for a value, and what operations are valid on it. When you write `int age = 25;`, the compiler knows to allocate 4 bytes and allow arithmetic operations like addition and multiplication. If you tried to add a number to a `bool`, the compiler would stop you — that operation doesn't make sense for a true/false value.",
    },
    {
        "type": "p",
        "text": "C# is a **statically typed** language. This means every variable's type is known at compile time, before your program ever runs. This is different from Python or JavaScript, where a variable can hold any type and errors only surface at runtime. Static typing catches entire categories of bugs before your code ships.",
    },
    {
        "type": "callout",
        "kind": "note",
        "text": "If you're coming from Python, think of C# types as making your type hints mandatory and enforced. Python's `age: int = 25` is a suggestion; C#'s `int age = 25;` is a contract the compiler enforces.",
    },
    {"type": "h2", "text": "Integer types"},
    {
        "type": "p",
        "text": "C# provides several integer types that differ in size (how much memory they use) and range (how large a number they can hold). The most common one is `int`, which uses 4 bytes and can store values from roughly −2.1 billion to +2.1 billion. For most everyday counting, `int` is the right choice.",
    },
    {
        "type": "code",
        "code": "int age = 25;              // 4 bytes, range: −2.1B to +2.1B\nlong population = 8_000_000_000; // 8 bytes, for very large numbers\nshort temperature = -15;        // 2 bytes, range: −32,768 to +32,767\nbyte level = 255;              // 1 byte, range: 0 to 255",
    },
    {
        "type": "p",
        "text": "Notice the underscore in `8_000_000_000` — C# lets you use underscores as digit separators to make large numbers easier to read. The compiler ignores them entirely.",
    },
    {
        "type": "callout",
        "kind": "tip",
        "text": "**When to choose what:** Use `int` for almost everything. Use `long` when values might exceed 2 billion (file sizes, timestamps, population counts). Use `byte` for raw binary data or when optimizing memory in large arrays. You'll rarely need `short` in modern code.",
    },
    {"type": "h2", "text": "Floating-point types"},
    {
        "type": "p",
        "text": "For numbers with decimal points, C# gives you three options. The most common is `double`, which provides about 15 digits of precision. For financial calculations where rounding errors are unacceptable, use `decimal` — it's slower but accurate to 28 digits.",
    },
    {
        "type": "code",
        "code": "double pi = 3.14159265358979;    // 8 bytes, ~15 digits precision\nfloat speed = 88.5f;              // 4 bytes, ~7 digits (note the 'f' suffix)\ndecimal price = 29.99m;           // 16 bytes, ~28 digits (note the 'm' suffix)",
    },
    {
        "type": "p",
        "text": "Pay attention to the suffixes: `float` literals need an `f` and `decimal` literals need an `m`. Without a suffix, C# treats a decimal number as a `double` by default.",
    },
    {
        "type": "callout",
        "kind": "warn",
        "text": "**Common mistake:** Using `double` for money. `0.1 + 0.2` in floating-point math doesn't equal `0.3` — it equals `0.30000000000000004`. Always use `decimal` for currency, pricing, and financial calculations.",
    },
    {"type": "h2", "text": "Text and characters"},
    {
        "type": "p",
        "text": "A `string` holds a sequence of characters — text of any length. A `char` holds exactly one Unicode character. Strings use double quotes; chars use single quotes.",
    },
    {
        "type": "code",
        "code": "string name = \"Verap\";\nstring greeting = \"Hello, \" + name;  // Concatenation: \"Hello, Verap\"\nchar grade = 'A';                  // Single character\nchar newline = '\\n';               // Escape sequence",
    },
    {
        "type": "p",
        "text": "Strings in C# are **immutable** — once created, they can't be changed. When you \"modify\" a string, C# actually creates a new string in memory. This is important for performance when building strings in loops; you'll learn about `StringBuilder` later for those cases.",
    },
    {"type": "h2", "text": "Boolean type"},
    {
        "type": "p",
        "text": "A `bool` holds exactly one of two values: `true` or `false`. Booleans are the foundation of every decision your program makes — every `if` statement, every loop condition, every comparison.",
    },
    {
        "type": "code",
        "code": "bool isLoggedIn = true;\nbool hasPermission = false;\nbool isAdult = age >= 18;  // Comparison produces a bool",
    },
    {"type": "h2", "text": "The `var` keyword"},
    {
        "type": "p",
        "text": "C# can often figure out the type for you. When you use `var`, the compiler infers the type from the value you assign. The variable is still statically typed — `var` is just shorthand.",
    },
    {
        "type": "code",
        "code": "var count = 10;           // Compiler infers: int\nvar name = \"Claude\";      // Compiler infers: string\nvar price = 9.99m;        // Compiler infers: decimal\n\n// var mystery;  ← ERROR: must assign a value so the compiler knows the type",
    },
    {
        "type": "p",
        "text": "Use `var` when the type is obvious from the right side of the assignment. Use explicit types when it makes code clearer — especially when the type isn't immediately obvious from the value or method call.",
    },
    {
        "type": "link",
        "text": "Read more on Microsoft Learn: Built-in types",
        "href": "https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/built-in-types",
    },
]

BUILTIN_TYPES_CODEALONG = {
    "title": "Code Along: Working with Data Types",
    "intro": "Follow each step in order. Type the code yourself — don't copy-paste — to build muscle memory.",
    "filename": "Program.cs",
    "steps": [
        {
            "title": "Declare integer variables",
            "body": "Start by declaring a few integer variables. Use `int` for everyday numbers and `long` when you need a bigger range.",
            "code": "int currentYear = 2026;\nint birthYear = 1998;\nint age = currentYear - birthYear;\nConsole.WriteLine($\"Age: {age}\");",
        },
        {
            "title": "Try floating-point types",
            "body": "Add these below your integer code. Notice the `f` and `m` suffixes — they tell the compiler which type you want.",
            "code": "double gravity = 9.81;\nfloat temp = 36.6f;\ndecimal balance = 1250.75m;\nConsole.WriteLine($\"Balance: {balance:C}\");",
        },
        {
            "title": "Work with strings and booleans",
            "body": "Combine strings using interpolation (`$\"...\"`) and create a boolean from a comparison.",
            "code": "string firstName = \"Verap\";\nstring language = \"C#\";\nbool isLearning = true;\n\nConsole.WriteLine(\n  $\"{firstName} is learning {language}: {isLearning}\"\n);",
        },
        {
            "title": "Explore var and type inference",
            "body": "Use `var` and then call `.GetType().Name` to see what the compiler inferred.",
            "code": "var count = 42;\nvar pi = 3.14159;\nvar message = \"Hello\";\n\nConsole.WriteLine($\"count: {count.GetType().Name}\");\nConsole.WriteLine($\"pi:    {pi.GetType().Name}\");\nConsole.WriteLine($\"msg:   {message.GetType().Name}\");",
        },
    ],
}

BUILTIN_TYPES_LAB = {
    "title": "Lab: Type Detective",
    "difficulty": "Beginner",
    "description": "Write a program that declares variables of different types, performs operations on them, and prints the results. This lab tests your understanding of when to use each data type and how they behave.",
    "filename": "Lab.cs",
    "requirements": [
        "Declare a `decimal` variable for a product price of `49.99`",
        "Declare an `int` for quantity with value `3`",
        "Calculate the total cost (price × quantity) and store it as `decimal`",
        "Declare a `bool` that checks if the total exceeds `100.00`",
        "Print the total formatted as currency and whether it exceeds the threshold",
    ],
    "expected_output": "Total: $149.97\nExceeds $100: True",
    "hint": "Start with\n  decimal price = 49.99m;\n  int quantity = 3;\nThen multiply them and use > to compare.",
}

# ─── Module 2, lesson 1: Understanding Variables ───

VARIABLES_READING = [
    h2("What is a variable?"),
    p("A variable is a named place in memory that holds a value your program can use and change. Picture a labeled box: the label is the variable's **name**, the kind of thing the box is allowed to hold is its **type**, and what is inside right now is its **value**. Almost every program you will ever write is a series of steps that read from boxes, compute something, and put results into other boxes."),
    h2("Declaring and assigning"),
    p("In C# you must **declare** a variable before you use it, which means stating its type and name. You **assign** a value with a single equals sign, which in programming means \"store the value on the right into the variable on the left\", not \"is equal to\". Doing both at once is called **initializing**."),
    code(r'''
int score;              // declaration only
score = 10;             // assignment
string player = "Ada";  // declaration + initialization
int level = 1, lives = 3;   // several of the same type at once

score = 25;             // later, change the value
Console.WriteLine($"{player}: {score}");
// Output: Ada: 25
'''),
    p("Once a variable has a type, it keeps that type forever. A box made for `int` can never hold text. This is the static typing you saw in the last lesson, and it is why C# can catch mistakes before your program runs."),
    code(r'''
int count = 5;
// count = "five";   // ERROR CS0029: Cannot implicitly convert type 'string' to 'int'
'''),
    h2("Use before you assign"),
    p("C# also refuses to let you read a local variable that has never been given a value. This rule is called **definite assignment**, and it prevents a whole class of bugs that exist in languages that silently hand you garbage or zero."),
    code(r'''
int total;
// Console.WriteLine(total);   // ERROR CS0165: Use of unassigned local variable 'total'
total = 0;
Console.WriteLine(total);      // fine now
// Output: 0
'''),
    h2("Naming rules and conventions"),
    p("The **rules** are enforced by the compiler. A name may contain letters, digits, and underscores, but it cannot start with a digit, cannot contain spaces or symbols like `-`, and cannot be a reserved keyword such as `int` or `class`. Names are **case-sensitive**, so `score` and `Score` are two different variables. (If you truly need a keyword as a name, you can prefix it with `@`, but avoid that.)"),
    p("The **conventions** are not enforced, but every C# team follows them, and your code will look professional if you do too. Local variables and parameters use **camelCase** (`playerName`, `totalPrice`). Types, methods, and properties use **PascalCase**, which you will see from module 4 onward. Choose descriptive names: `elapsedSeconds` beats `e`, and `isValid` beats `flag`."),
    code(r'''
int playerAge = 30;      // good: camelCase and descriptive
int PlayerAge2 = 30;     // legal, but PascalCase is for types and methods
// int 2players = 2;     // ERROR: a name cannot start with a digit
// int my-score = 5;     // ERROR: hyphens are not allowed
// int class = 1;        // ERROR: 'class' is a keyword
int @class = 1;          // legal with @, but avoid it
'''),
    warn("Because names are case-sensitive, `playerName` and `PlayerName` are different variables. A typo in capitalization gives you `CS0103: The name does not exist`, not a silent bug. If you see that error, compare the spelling and capitalization letter by letter."),
    h2("const: values that never change"),
    p("Some values must never change while the program runs, such as the number of days in a week or a tax rate. Declare them with `const`. A constant must be given its value right where it is declared, and the compiler will reject any attempt to change it later. By convention, constants use PascalCase."),
    code(r'''
const int DaysInWeek = 7;
const string AppName = "Journey";
// DaysInWeek = 8;   // ERROR CS0131: The left-hand side of an assignment must be a variable
Console.WriteLine($"{AppName} has {DaysInWeek} days per week");
// Output: Journey has 7 days per week
'''),
    tip("Reach for `const` whenever a value has a meaning that you would otherwise have to remember, like `const int MaxPlayers = 4;`. A named constant is easier to read than the bare number 4, and to change you edit it in exactly one place."),
    h2("Scope: where a variable lives"),
    p("A variable exists only inside the pair of curly braces in which it is declared, from the declaration to the closing brace. This is its **scope**. Code outside that block cannot see it, and C# does not let an inner block declare a name that is already in use in the surrounding block, which avoids confusing accidental overlap."),
    code(r'''
int outer = 1;
{
    int inner = 2;
    Console.WriteLine(outer + inner);   // both visible here
    // Output: 3
}
// Console.WriteLine(inner);   // ERROR CS0103: 'inner' does not exist in this context
'''),
    note("You will use scope constantly once you meet `if` statements, loops, and methods in the next modules, because each of them has its own curly-brace block. For now remember the rule of thumb: declare a variable as close as possible to where you first use it."),
    h2("Nullable value types: int?"),
    p("A normal `int` always holds a number, so there is no way to say \"we do not know\" or \"no value was given\". Adding a question mark makes a **nullable value type**: `int?` can hold any int, or the special value `null`, which means \"no value\". The same works for `double?`, `bool?`, `DateTime?`, and any other value type."),
    code(r'''
int? discount = null;                 // no discount specified
Console.WriteLine(discount.HasValue); // Output: False

discount = 15;
Console.WriteLine(discount.HasValue); // Output: True
Console.WriteLine(discount.Value);    // Output: 15

int safe = discount ?? 0;             // use 0 if null
Console.WriteLine(safe);              // Output: 15
'''),
    p("`HasValue` tells you whether a value is present, `Value` gets it, and the `??` operator supplies a fallback when the variable is `null`. Reading `.Value` while the variable is `null` throws an `InvalidOperationException`, so check first or use `??` (or `GetValueOrDefault()`, which returns the default such as 0). Nullable reference types, such as `string?`, are a related idea you will meet when working with objects."),
    link("Read more on Microsoft Learn: Identifier names", "https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/identifier-names"),
]

VARIABLES_CODEALONG = codealong(
    "Code Along: Declaring and Using Variables",
    "Type each step into one Program.cs file, in order. Every step keeps the variables from the earlier ones.",
    [
        step(
            "Declare and initialize",
            "Declare a string and an int, give them values, and print them with an interpolated string. You will study the `$\"...\"` syntax in lesson 2.4; for now each `{name}` is replaced by the variable's value.",
            r'''
string playerName = "Ada";
int score = 0;
Console.WriteLine($"{playerName} has {score} points");
''',
        ),
        step(
            "Reassign a variable",
            "A variable can change as often as you like. The right side is calculated first, using the current value, and then stored back in the variable.",
            r'''
score = 10;
score = score + 5;
Console.WriteLine($"{playerName} now has {score} points");
''',
        ),
        step(
            "Use a constant",
            "A `const` is fixed forever. Try uncommenting the last line after you run the program to see the compiler complain, then comment it out again.",
            r'''
const int MaxScore = 100;
int remaining = MaxScore - score;
Console.WriteLine($"Points left to win: {remaining}");
// MaxScore = 200;   // ERROR: cannot assign to a constant
''',
        ),
        step(
            "Explore scope",
            "Variables declared inside a pair of braces disappear at the closing brace. `bonus` exists only in the block, but `score` was declared outside, so the block can change it.",
            r'''
{
    int bonus = 5;
    score = score + bonus;
    Console.WriteLine($"Inside the block: bonus = {bonus}");
}
Console.WriteLine($"Outside the block: score = {score}");
''',
        ),
        step(
            "Try a nullable int",
            "Declare an `int?`, check `HasValue`, then give it a value and use `??` to provide a fallback for the null case.",
            r'''
int? bonusLevel = null;
Console.WriteLine($"Has level: {bonusLevel.HasValue}");
Console.WriteLine($"Level or default: {bonusLevel ?? 1}");

bonusLevel = 3;
Console.WriteLine($"Has level: {bonusLevel.HasValue}");
Console.WriteLine($"Level or default: {bonusLevel ?? 1}");
''',
        ),
    ],
)

VARIABLES_LAB = lab(
    "Lab: Stock Counter",
    "Beginner",
    "Model a tiny shop's stock with a constant, a changing variable, and a nullable discount, and print the state at each point.",
    [
        "Declare a constant `const string StoreName = \"Byte Shop\";` and print `Store: Byte Shop` using string interpolation.",
        "Declare an `int stock = 12;` and an `int sold = 5;`. Subtract `sold` from `stock` by assigning the result back to `stock`, then print `Stock after sale: 7`.",
        "Declare `int? discountPercent = null;`. Print `Has discount: ` followed by the value of `discountPercent.HasValue`.",
        "On the next line print `Discount used: ` followed by `discountPercent ?? 0`.",
        "Assign `15` to `discountPercent` and print the same two lines again (`Has discount: ...` and `Discount used: ...`).",
    ],
    "Store: Byte Shop\nStock after sale: 7\nHas discount: False\nDiscount used: 0\nHas discount: True\nDiscount used: 15",
    "Interpolated strings put an expression inside braces, like $\"Stock after sale: {stock}\". Because bool values print as True or False, you can place discountPercent.HasValue straight into the braces.",
)

VARIABLES_SOLUTION = r'''const string StoreName = "Byte Shop";
Console.WriteLine($"Store: {StoreName}");

int stock = 12;
int sold = 5;
stock = stock - sold;
Console.WriteLine($"Stock after sale: {stock}");

int? discountPercent = null;
Console.WriteLine($"Has discount: {discountPercent.HasValue}");
Console.WriteLine($"Discount used: {discountPercent ?? 0}");

discountPercent = 15;
Console.WriteLine($"Has discount: {discountPercent.HasValue}");
Console.WriteLine($"Discount used: {discountPercent ?? 0}");
'''

# ─── Module 2, lesson 3: Type Conversion & Casting ───

CONVERSION_READING = [
    h2("Why conversion matters"),
    p("Real programs constantly move values between types: text typed by a user must become a number before you can add it, a `double` result sometimes needs to be stored as an `int`, and a number often has to become text for display. C# is strict about this. It will convert automatically only when no information can be lost, and it makes you say so explicitly everywhere else."),
    h2("Implicit conversions: safe and automatic"),
    p("When the destination type can hold every possible value of the source type, C# converts for you. This is a **widening** conversion. An `int` fits inside a `long`, and an `int` fits inside a `double`, so no cast is needed."),
    code(r'''
int small = 42;
long big = small;        // int -> long, implicit
double precise = small;  // int -> double, implicit
Console.WriteLine($"{big} {precise}");
// Output: 42 42
'''),
    h2("Explicit casts: you take responsibility"),
    p("Going the other way, from a bigger type to a smaller one, can lose data, so the compiler requires an **explicit cast**: the target type in parentheses in front of the value. This is a **narrowing** conversion. Casting a `double` to an `int` does not round; it **truncates**, dropping everything after the decimal point."),
    code(r'''
double price = 9.99;
// int whole = price;      // ERROR CS0266: Cannot implicitly convert type 'double' to 'int'
int whole = (int)price;    // explicit cast
Console.WriteLine(whole);
// Output: 9

Console.WriteLine((int)-9.99);   // Output: -9  (truncates toward zero)
Console.WriteLine((char)65);     // Output: A
Console.WriteLine((int)'A');     // Output: 65
'''),
    warn("`(int)9.99` gives 9, not 10. If you want rounding, call `Math.Round(9.99)` first or use `Convert.ToInt32`, which rounds. Truncating prices or averages by accident is one of the most common data bugs in beginner programs."),
    h2("Overflow: when the value does not fit"),
    p("A cast to a smaller integer type keeps only the bits that fit. By default C# does **not** warn you at runtime. The number silently wraps around, which can turn a large positive number into something surprising. If you would rather get an error, wrap the code in a `checked` context, which throws an `OverflowException` instead."),
    code(r'''
int number = 300;
byte wrapped = (byte)number;     // a byte holds 0-255
Console.WriteLine(wrapped);
// Output: 44   (300 - 256)

int max = int.MaxValue;
Console.WriteLine(max + 1);      // wraps around
// Output: -2147483648

// int boom = checked(max + 1);  // throws System.OverflowException
'''),
    h2("Turning text into numbers: Parse and TryParse"),
    p("Text such as `\"42\"` is not a number to C#, even though it looks like one. Every numeric type has a `Parse` method that converts a string, and a safer `TryParse`. `Parse` throws a `FormatException` when the text is not a valid number, which crashes the program if nothing catches it. `TryParse` never throws. It returns a `bool` that says whether it worked and gives you the number through an `out` parameter, a special argument the method fills in for you."),
    code(r'''
int a = int.Parse("42");
Console.WriteLine(a + 1);            // Output: 43

bool ok = int.TryParse("12abc", out int parsed);
Console.WriteLine($"{ok}, {parsed}");
// Output: False, 0

bool ok2 = double.TryParse("3.14", out double pi);
Console.WriteLine($"{ok2}, {pi}");
// Output: True, 3.14
'''),
    note("`out int parsed` declares the variable right in the call. When `TryParse` fails, the variable still exists but holds the default value (0). In module 3 you will combine `TryParse` with an `if` statement to react to bad input, which is the standard way to handle anything a user types."),
    tip("Use `TryParse` for anything that comes from outside your program (user input, files, web requests), because you cannot trust it. Use `Parse` only when a bad value would be a bug in your own code. Parsing also depends on the culture: `\"3,14\"` is a valid decimal in some European cultures but not in en-US."),
    h2("The Convert class"),
    p("The `Convert` class offers methods like `Convert.ToInt32`, `Convert.ToDouble`, and `Convert.ToString` that accept many source types. Unlike a cast, `Convert.ToInt32` **rounds** a `double`, and it uses banker's rounding (halfway values go to the nearest even number). `Convert.ToInt32` on a `null` string returns 0, while `int.Parse(null)` throws."),
    code(r'''
Console.WriteLine(Convert.ToInt32(2.5));    // Output: 2  (rounds to even)
Console.WriteLine(Convert.ToInt32(3.5));    // Output: 4
Console.WriteLine(Convert.ToInt32(9.99));   // Output: 10
Console.WriteLine(Convert.ToInt32("123"));  // Output: 123
Console.WriteLine(Convert.ToString(99) + "!");  // Output: 99!
'''),
    p("Every object also has a `ToString()` method, so `42.ToString()` is the usual way to get text from a number. And when you use a number inside an interpolated string, C# calls it for you."),
    link("Read more on Microsoft Learn: Casting and type conversions", "https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/types/casting-and-type-conversions"),
]

CONVERSION_CODEALONG = codealong(
    "Code Along: Converting Between Types",
    "Type each step into one Program.cs file. Predict each output before you run the program.",
    [
        step(
            "Implicit widening",
            "An `int` fits into a `long` or a `double`, so C# converts it for you.",
            r'''
int apples = 7;
long applesLong = apples;
double applesDouble = apples;
Console.WriteLine($"{applesLong} {applesDouble}");
''',
        ),
        step(
            "Explicit narrowing",
            "Going from `double` to `int` needs a cast, and the decimal part is dropped, not rounded. Casting between `char` and `int` shows the character code.",
            r'''
double temperature = 36.9;
int truncated = (int)temperature;
Console.WriteLine($"Truncated: {truncated}");
Console.WriteLine($"Letter: {(char)66}, code: {(int)'C'}");
''',
        ),
        step(
            "Watch a value wrap around",
            "A `byte` holds only 0 to 255, so 300 wraps to 44. No error is raised by default.",
            r'''
int tooBig = 300;
byte wrapped = (byte)tooBig;
Console.WriteLine($"300 as a byte: {wrapped}");
''',
        ),
        step(
            "Parse text",
            "`int.Parse` converts valid text into a number. After that you can do arithmetic on it.",
            r'''
string quantityText = "12";
int quantity = int.Parse(quantityText);
Console.WriteLine($"Double the quantity: {quantity * 2}");
''',
        ),
        step(
            "Use TryParse safely",
            "`TryParse` returns whether it worked and gives you the value through `out`. Bad text yields `False` and 0 instead of crashing.",
            r'''
bool goodOk = int.TryParse("250", out int goodValue);
bool badOk = int.TryParse("two hundred", out int badValue);
Console.WriteLine($"Good: {goodOk}, {goodValue}");
Console.WriteLine($"Bad: {badOk}, {badValue}");
''',
        ),
        step(
            "Compare Convert with a cast",
            "`Convert.ToInt32` rounds where a cast truncates. Notice that 2.5 rounds to 2 and 3.5 to 4 (banker's rounding).",
            r'''
double ratingA = 4.7;
Console.WriteLine($"Cast: {(int)ratingA}, Convert: {Convert.ToInt32(ratingA)}");
Console.WriteLine($"2.5 -> {Convert.ToInt32(2.5)}, 3.5 -> {Convert.ToInt32(3.5)}");
''',
        ),
    ],
)

CONVERSION_LAB = lab(
    "Lab: Order Parser",
    "Beginner",
    "An order arrives as text. Convert the pieces to real numbers, compute with them, and demonstrate the difference between casting and converting.",
    [
        "Create `string priceText = \"19.99\";` and `string quantityText = \"3\";`. Convert the price with `decimal.Parse` and the quantity with `int.TryParse`, using `out int quantity`. Both text values are valid.",
        "Compute `decimal total = price * quantity;` and print `Total: ` followed by the total (it should show `59.97`).",
        "Print `Quantity valid: ` followed by the bool result of the `TryParse` for the quantity.",
        "Call `int.TryParse(\"x7\", out int badNumber)`. Print `Bad input valid: ` followed by its bool result, then `Bad input value: ` followed by `badNumber`.",
        "Declare `double rating = 9.99;`. Print `Cast: ` followed by `(int)rating`, then `Convert: ` followed by `Convert.ToInt32(rating)`.",
        "Declare `int big = 258;`, cast it to a `byte` named `wrapped` with `(byte)big`, and print `Wrapped: ` followed by `wrapped`.",
    ],
    "Total: 59.97\nQuantity valid: True\nBad input valid: False\nBad input value: 0\nCast: 9\nConvert: 10\nWrapped: 2",
    "TryParse returns a bool and fills the variable you pass after `out`. Keep that bool in a variable such as `bool quantityOk` so you can print it later. A decimal literal needs the m suffix, but here the value comes from text, so decimal.Parse handles it.",
)

CONVERSION_SOLUTION = r'''string priceText = "19.99";
string quantityText = "3";
decimal price = decimal.Parse(priceText);
bool quantityOk = int.TryParse(quantityText, out int quantity);

decimal total = price * quantity;
Console.WriteLine($"Total: {total}");
Console.WriteLine($"Quantity valid: {quantityOk}");

bool badOk = int.TryParse("x7", out int badNumber);
Console.WriteLine($"Bad input valid: {badOk}");
Console.WriteLine($"Bad input value: {badNumber}");

double rating = 9.99;
Console.WriteLine($"Cast: {(int)rating}");
Console.WriteLine($"Convert: {Convert.ToInt32(rating)}");

int big = 258;
byte wrapped = (byte)big;
Console.WriteLine($"Wrapped: {wrapped}");
'''

# ─── Module 2, lesson 4: String Interpolation ───

INTERPOLATION_READING = [
    h2("Building strings from values"),
    p("Programs constantly need to mix text and values: \"Hello, Ada, you have 3 messages\". One way is concatenation with `+`, which works but gets messy fast. **String interpolation** is the modern way: put a `$` in front of the opening quote and write any expression inside `{curly braces}`, and C# replaces it with the value."),
    code(r'''
string name = "Ada";
int messages = 3;

string old = "Hello, " + name + ", you have " + messages + " messages";
string modern = $"Hello, {name}, you have {messages} messages";
Console.WriteLine(modern);
// Output: Hello, Ada, you have 3 messages
'''),
    p("The braces can hold more than a variable name. Any expression works, such as arithmetic or a method call."),
    code(r'''
int width = 4, height = 5;
Console.WriteLine($"Area: {width * height}");        // Output: Area: 20
Console.WriteLine($"Shout: {name.ToUpper()}!");      // Output: Shout: ADA!
'''),
    h2("Format specifiers"),
    p("After the expression, add a colon and a **format specifier** to control how the value is shown. The most useful ones for numbers are `C` (currency), `N` (number with thousands separators), `F` (fixed decimals), `P` (percent), `D` (integer padded with zeros), and `X` (hexadecimal). A digit after the letter sets the number of decimals or digits. Results depend on the culture; this course uses en-US."),
    code(r'''
double price = 1234.5;
Console.WriteLine($"{price:C}");        // Output: $1,234.50
Console.WriteLine($"{price:N0}");       // Output: 1,235
Console.WriteLine($"{3.14159:F2}");     // Output: 3.14
Console.WriteLine($"{0.256:P1}");       // Output: 25.6%
Console.WriteLine($"{42:D5}");          // Output: 00042
Console.WriteLine($"{255:X}");          // Output: FF
'''),
    p("Dates have their own custom patterns, such as `yyyy-MM-dd` for 2026-03-14. Notice that `MM` means month and lowercase `mm` means minutes, a classic mix-up."),
    code(r'''
var launch = new DateTime(2026, 3, 14);
Console.WriteLine($"{launch:yyyy-MM-dd}");   // Output: 2026-03-14
Console.WriteLine($"{launch:MMMM d, yyyy}"); // Output: March 14, 2026
'''),
    h2("Alignment"),
    p("A comma and a number after the expression set a minimum **width**. A positive number right-aligns the value, and a negative number left-aligns it. You can combine it with a format specifier by putting the alignment first: `{value,10:C}`. This is how you make neat columns in console output."),
    code(r'''
string item = "Tea";
decimal cost = 2.5m;
Console.WriteLine($"|{item,-8}|{cost,8:C}|");
// Output: |Tea     |   $2.50|
Console.WriteLine($"|{"Total",-8}|{cost * 2,8:C}|");
// Output: |Total   |   $5.00|
'''),
    warn("To print a literal brace inside an interpolated string, double it: `$\"{{name}}\"` prints `{name}`, not the variable's value. Forgetting this is the usual cause of the confusing error `CS1013` or of values appearing that you did not expect."),
    h2("Verbatim strings and raw string literals"),
    p("Backslashes in normal strings start escape sequences, which is annoying for file paths. A **verbatim string** starts with `@` and treats backslashes literally (type `\"\"` for a quote inside it). Verbatim strings can also span lines. They can be combined with interpolation as `$@\"...\"` or `@$\"...\"`."),
    code(r'''
string path = @"C:\Users\Ada\notes.txt";
Console.WriteLine(path);
// Output: C:\Users\Ada\notes.txt

string quote = @"She said ""hello""";
Console.WriteLine(quote);
// Output: She said "hello"
'''),
    p('A **raw string literal**, added in C# 11, goes further. It starts and ends with three (or more) double quotes, so you can include quotes and backslashes freely with no escaping at all. It is ideal for JSON, SQL, and other pieces of text. The closing quotes decide how much leading whitespace is trimmed, so everything is aligned relative to them.'),
    code(r'''
string json = """
    {
      "name": "Ada",
      "path": "C:\temp"
    }
    """;
Console.WriteLine(json);
// Output:
// {
//   "name": "Ada",
//   "path": "C:\temp"
// }
'''),
    h2("A quick tour of string methods"),
    p("Strings come with many built-in methods. Remember that strings are **immutable**: these methods never change the original, they return a new string that you must keep or print."),
    code(r'''
string text = "  Hello, C# World  ";
Console.WriteLine(text.Trim());                 // Output: Hello, C# World
Console.WriteLine(text.Trim().ToUpper());       // Output: HELLO, C# WORLD
Console.WriteLine(text.Trim().Length);          // Output: 14
Console.WriteLine(text.Contains("C#"));         // Output: True
Console.WriteLine(text.Trim().StartsWith("Hello")); // Output: True
Console.WriteLine(text.Trim().Replace("World", "Journey")); // Output: Hello, C# Journey
Console.WriteLine(text.Trim().Substring(7, 2)); // Output: C#
Console.WriteLine(text.Trim().IndexOf("C#"));   // Output: 7
Console.WriteLine("7".PadLeft(3, '0'));         // Output: 007
Console.WriteLine(string.IsNullOrEmpty(""));    // Output: True
'''),
    tip("Calling `text.ToUpper()` on its own line does nothing useful, because the new string is thrown away. Write `text = text.ToUpper();` to keep the result. Also prefer interpolation over `+` once there are more than two pieces; it is shorter and much easier to read."),
    link("Read more on Microsoft Learn: String interpolation", "https://learn.microsoft.com/en-us/dotnet/csharp/tutorials/string-interpolation"),
]

INTERPOLATION_CODEALONG = codealong(
    "Code Along: Formatting Text",
    "Type each step into one Program.cs file. Run after each step and compare your output with what you expect.",
    [
        step(
            "Interpolate values",
            "Put `$` before the string and expressions inside braces. Any expression works, not just variable names.",
            r'''
string name = "Ada";
int apples = 3;
int pricePerApple = 2;
Console.WriteLine($"{name} bought {apples} apples for {apples * pricePerApple} dollars.");
''',
        ),
        step(
            "Format numbers",
            "Add a colon and a specifier after the value: currency, thousands separators, fixed decimals, and percent.",
            r'''
double amount = 1234.5;
double ratio = 0.256;
Console.WriteLine($"Currency: {amount:C}");
Console.WriteLine($"Number:   {amount:N0}");
Console.WriteLine($"Fixed:    {amount:F3}");
Console.WriteLine($"Percent:  {ratio:P1}");
''',
        ),
        step(
            "Align columns",
            "A comma and a width right-align; a negative width left-aligns. This builds a neat little table.",
            r'''
string header1 = "Item";
string header2 = "Price";
Console.WriteLine($"{header1,-10}{header2,8}");
Console.WriteLine($"{"Coffee",-10}{3.5m,8:C}");
Console.WriteLine($"{"Bagel",-10}{2.25m,8:C}");
''',
        ),
        step(
            "Verbatim and escaped braces",
            "A verbatim string keeps backslashes as they are, and doubled braces print literal braces in an interpolated string.",
            r'''
string folder = @"C:\Users\Ada\Documents";
Console.WriteLine(folder);
Console.WriteLine($"Use {{name}} to insert {name}");
''',
        ),
        step(
            "Write a raw string",
            "A raw string starts and ends with three quotes, and you can use quotes freely inside. The closing quotes set the indentation that gets removed.",
            r'''
string json = """
    {
      "user": "Ada",
      "active": true
    }
    """;
Console.WriteLine(json);
''',
        ),
        step(
            "Call string methods",
            "Methods return new strings, so chain them or store the result. Count positions from zero.",
            r'''
string title = "  learning C# strings  ";
string clean = title.Trim();
Console.WriteLine(clean.ToUpper());
Console.WriteLine($"Length: {clean.Length}");
Console.WriteLine(clean.Replace("learning", "mastering"));
Console.WriteLine($"Starts with 'learn': {clean.StartsWith("learn")}");
Console.WriteLine($"Index of C#: {clean.IndexOf("C#")}");
''',
        ),
    ],
)

INTERPOLATION_LAB = lab(
    "Lab: Cafe Receipt",
    "Beginner",
    "Format a small receipt with currency, alignment, a percent, and a few string methods. Every width and symbol matters, so match the requirements exactly.",
    [
        "Declare `string cafe = \"blue bean cafe\";` and print it converted to upper case with `ToUpper()`.",
        "Print a separator line of exactly 20 hyphens (`--------------------`).",
        "Declare `decimal latte = 4.50m;` and `decimal bagel = 3.25m;`. Print two lines in the form `$\"{name,-8}{quantity,3}{lineTotal,10:C}\"`: first `Latte` with quantity `2` and a line total of `latte * 2`, then `Bagel` with quantity `1` and a line total of `bagel * 1`.",
        "Print the separator again, then compute `decimal subtotal` (the two line totals added together) and print `Subtotal: ` followed by the value formatted with `:C`.",
        "Declare `decimal taxRate = 0.08m;`. Print `Tax rate: ` followed by `taxRate` formatted with `:P0`, then `Tax: ` followed by `subtotal * taxRate` formatted with `:C`.",
        "Print `Thanks, ` followed by `cafe.Substring(0, 4).ToUpper()` and an exclamation mark, with no space before the `!`.",
    ],
    "BLUE BEAN CAFE\n--------------------\nLatte     2     $9.00\nBagel     1     $3.25\n--------------------\nSubtotal: $12.25\nTax rate: 8%\nTax: $0.98\nThanks, BLUE!",
    "In an interpolated string the alignment goes right after the expression, before the colon: {value,10:C}. A negative number such as -8 pads on the right. You can store the line totals in their own decimal variables to keep the interpolated strings short.",
)

INTERPOLATION_SOLUTION = r'''string cafe = "blue bean cafe";
Console.WriteLine(cafe.ToUpper());
Console.WriteLine("--------------------");

decimal latte = 4.50m;
decimal bagel = 3.25m;
decimal latteTotal = latte * 2;
decimal bagelTotal = bagel * 1;
Console.WriteLine($"{"Latte",-8}{2,3}{latteTotal,10:C}");
Console.WriteLine($"{"Bagel",-8}{1,3}{bagelTotal,10:C}");
Console.WriteLine("--------------------");

decimal subtotal = latteTotal + bagelTotal;
Console.WriteLine($"Subtotal: {subtotal:C}");

decimal taxRate = 0.08m;
Console.WriteLine($"Tax rate: {taxRate:P0}");
Console.WriteLine($"Tax: {subtotal * taxRate:C}");

Console.WriteLine($"Thanks, {cafe.Substring(0, 4).ToUpper()}!");
'''

# ─── Module 2, lesson 5: Operators & Expressions ───

OPERATORS_READING = [
    h2("Operators and expressions"),
    p("An **operator** is a symbol that does something to values, and an **expression** is any piece of code that produces a value, like `2 + 3` or `price * quantity`. The values the operator works on are called **operands**. Expressions can be nested inside each other, and the result can be stored in a variable or printed."),
    h2("Arithmetic operators"),
    p("C# has the five arithmetic operators you expect: `+`, `-`, `*`, `/`, and `%` (remainder, also called modulo). Multiplication and division happen before addition and subtraction, just like in math class."),
    code(r'''
Console.WriteLine(7 + 3);    // Output: 10
Console.WriteLine(7 - 3);    // Output: 4
Console.WriteLine(7 * 3);    // Output: 21
Console.WriteLine(7.0 / 2);  // Output: 3.5
Console.WriteLine(2 + 3 * 4); // Output: 14
'''),
    h2("Integer division"),
    p("When **both** operands are integers, `/` is integer division: it throws away the fractional part. `7 / 2` is `3`, not `3.5`. To get a fractional result, at least one operand must be a `double` or `decimal`, either by writing it that way or by casting."),
    code(r'''
Console.WriteLine(7 / 2);          // Output: 3
Console.WriteLine(7 / 2.0);        // Output: 3.5
int total = 7, count = 2;
Console.WriteLine((double)total / count);   // Output: 3.5
Console.WriteLine((double)(total / count)); // Output: 3   (cast too late!)
'''),
    warn("This is one of the most common surprises for new C# programmers, especially those from Python where `7 / 2` gives `3.5`. Compute averages and percentages with at least one `double` or `decimal` operand, and remember the cast must be applied **before** the division. Dividing an integer by zero throws a `DivideByZeroException`, while dividing a `double` by zero gives `Infinity`."),
    h2("Remainder (modulo)"),
    p("The `%` operator gives what is left over after division. It is the standard tool for checking whether a number is even or odd, wrapping around a range (like hours on a clock), and splitting a total into units. Notice that the sign of the result follows the left operand."),
    code(r'''
Console.WriteLine(17 % 5);    // Output: 2   (17 = 3*5 + 2)
Console.WriteLine(10 % 2);    // Output: 0   (even)
Console.WriteLine(-7 % 3);    // Output: -1
int seconds = 3725;
Console.WriteLine($"{seconds / 60} minutes {seconds % 60} seconds");
// Output: 62 minutes 5 seconds
'''),
    h2("Compound assignment, ++ and --"),
    p("Updating a variable from its own value is so common that C# has shortcuts: `+=`, `-=`, `*=`, `/=`, and `%=`. So `score += 5` means `score = score + 5`. Adding or subtracting exactly 1 has its own shorter forms, `++` and `--`. Placed after the variable (**postfix**), the expression yields the old value and then updates the variable. Placed before (**prefix**), it updates first and then yields the new value."),
    code(r'''
int score = 10;
score += 5;       // 15
score *= 2;       // 30
score -= 1;       // 29
Console.WriteLine(score);   // Output: 29

int i = 5;
int a = i++;      // a gets 5, then i becomes 6
int b = ++i;      // i becomes 7, then b gets 7
Console.WriteLine($"{a} {b} {i}");   // Output: 5 7 7
'''),
    tip("When `++` is on a line by itself, prefix and postfix behave identically. Only use the value of `i++` inside a bigger expression when you are sure of the order, because it is easy to misread. Clarity beats cleverness."),
    h2("Comparison operators"),
    p("Comparison operators compare two values and produce a `bool`: `==` (equal), `!=` (not equal), `<`, `>`, `<=`, and `>=`. Beware: a single `=` assigns, and a double `==` compares. For strings, `==` compares the actual characters, so `\"abc\" == \"abc\"` is `true`."),
    code(r'''
int age = 20;
Console.WriteLine(age >= 18);    // Output: True
Console.WriteLine(age == 21);    // Output: False
Console.WriteLine(age != 21);    // Output: True
Console.WriteLine("abc" == "abc"); // Output: True
Console.WriteLine(0.1 + 0.2 == 0.3);  // Output: False  (binary floating point)
'''),
    h2("Logical operators"),
    p("Logical operators combine bools. `&&` (and) is true only if both sides are true, `||` (or) is true if at least one side is, and `!` (not) flips a value. Both `&&` and `||` are **short-circuit** operators: the right side is not even evaluated when the left side already decides the answer."),
    code(r'''
bool hasTicket = true;
bool isMember = false;
Console.WriteLine(hasTicket && isMember);   // Output: False
Console.WriteLine(hasTicket || isMember);   // Output: True
Console.WriteLine(!hasTicket);              // Output: False

int year = 2100;
bool leap = (year % 4 == 0 && year % 100 != 0) || year % 400 == 0;
Console.WriteLine(leap);                    // Output: False
'''),
    h2("Precedence and parentheses"),
    p("When an expression has several operators, **precedence** decides which runs first. In general: `++`/`--` and `!` come first, then `* / %`, then `+ -`, then comparisons (`< > <= >=`), then `== !=`, then `&&`, then `||`, and assignment is last. Operators on the same level run left to right. You do not need to memorize the table. Use parentheses to say what you mean, since they cost nothing and make code self-documenting."),
    code(r'''
Console.WriteLine(2 + 3 * 4);       // Output: 14
Console.WriteLine((2 + 3) * 4);     // Output: 20
Console.WriteLine(10 - 4 - 3);      // Output: 3   (left to right)
bool result = true || false && false;  // && binds tighter than ||
Console.WriteLine(result);          // Output: True
'''),
    h2("Two handy operators: ?: and ??"),
    p("The **conditional operator** `condition ? whenTrue : whenFalse` picks between two values in a single expression. The **null-coalescing operator** `??` gives a fallback when its left side is `null`, and `??=` assigns only when the variable is currently `null`. Both appear in everyday C# code."),
    code(r'''
int temperature = 28;
string label = temperature > 25 ? "warm" : "cool";
Console.WriteLine(label);                // Output: warm

string? nickname = null;
Console.WriteLine(nickname ?? "guest");  // Output: guest
nickname ??= "Ada";                      // assigns because it was null
Console.WriteLine(nickname);             // Output: Ada
'''),
    note("The `string?` above is a nullable reference type, meaning \"this string is allowed to be null\". The compiler uses it to warn you when you might use a null by mistake. Module 3 shows how `if` statements make the same decisions as `?:` with more room for several lines of code."),
    link("Read more on Microsoft Learn: Arithmetic operators", "https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/arithmetic-operators"),
]

OPERATORS_CODEALONG = codealong(
    "Code Along: Expressions in Action",
    "Type each step into one Program.cs file, in order, and run it to check your predictions.",
    [
        step(
            "Arithmetic and integer division",
            "Notice that dividing two ints discards the fraction, but a `double` operand keeps it.",
            r'''
int apples = 17;
int people = 5;
Console.WriteLine($"Each person gets {apples / people} apples");
Console.WriteLine($"{apples % people} apples are left over");
Console.WriteLine($"Exact share: {(double)apples / people}");
''',
        ),
        step(
            "Compound assignment",
            "Each shortcut updates the variable from its own value.",
            r'''
int points = 10;
points += 5;
points *= 2;
points -= 3;
Console.WriteLine($"Points: {points}");
''',
        ),
        step(
            "Increment and decrement",
            "Postfix returns the old value; prefix returns the new one. Predict the three numbers before you run.",
            r'''
int counter = 5;
int before = counter++;
int after = ++counter;
Console.WriteLine($"before={before}, after={after}, counter={counter}");
''',
        ),
        step(
            "Comparison and logical operators",
            "Combine comparisons with `&&`, `||`, and `!`. The result of each expression is a `bool`.",
            r'''
int age = 20;
bool hasId = true;
bool canEnter = age >= 18 && hasId;
bool needsCheck = !hasId || age < 21;
Console.WriteLine($"Can enter: {canEnter}");
Console.WriteLine($"Needs check: {needsCheck}");
''',
        ),
        step(
            "Precedence",
            "Multiplication runs before addition, and parentheses override the order.",
            r'''
Console.WriteLine(2 + 3 * 4);
Console.WriteLine((2 + 3) * 4);
Console.WriteLine(100 - 20 - 5);
''',
        ),
        step(
            "Conditional and null-coalescing",
            "`?:` chooses between two values and `??` supplies a fallback for `null`.",
            r'''
string size = points > 20 ? "big" : "small";
string? nickname = null;
Console.WriteLine($"Size: {size}");
Console.WriteLine($"Hello, {nickname ?? "guest"}");
''',
        ),
    ],
)

OPERATORS_LAB = lab(
    "Lab: Clock and Calendar Calculator",
    "Beginner",
    "Use division, remainder, compound assignment, and logical operators to break a duration into parts and check years for leap-year status.",
    [
        "Declare `int totalSeconds = 7384;`. Calculate `hours` as `totalSeconds / 3600`, then `remaining` as `totalSeconds % 3600`, then `minutes` as `remaining / 60` and `seconds` as `remaining % 60`. Print `Duration: 2h 3m 4s` using the variables (the numbers must come from your calculations).",
        "Declare `int totalPoints = 7;` and `int players = 2;`. Print `Average (integer): ` followed by `totalPoints / players`, then `Average (exact): ` followed by `(double)totalPoints / players`.",
        "Declare `int bonus = 10;`, then use `bonus += 5;` and `bonus *= 2;`. Print `Bonus: ` followed by `bonus`.",
        "For each year 2024, 2100, and 2000, evaluate `(year % 4 == 0 && year % 100 != 0) || year % 400 == 0`, and print `Is <year> a leap year: <result>` (for example `Is 2024 a leap year: True`).",
        "Declare `string? nickname = null;` and print `Welcome, ` followed by `nickname ?? \"guest\"`.",
    ],
    "Duration: 2h 3m 4s\nAverage (integer): 3\nAverage (exact): 3.5\nBonus: 30\nIs 2024 a leap year: True\nIs 2100 a leap year: False\nIs 2000 a leap year: True\nWelcome, guest",
    "Hours come from integer division by 3600, and the % operator gives the leftover seconds to feed the next step. For the leap years, declare each year as an int variable and reuse the same expression, wrapping the && part in parentheses so || is applied afterwards.",
)

OPERATORS_SOLUTION = r'''int totalSeconds = 7384;
int hours = totalSeconds / 3600;
int remaining = totalSeconds % 3600;
int minutes = remaining / 60;
int seconds = remaining % 60;
Console.WriteLine($"Duration: {hours}h {minutes}m {seconds}s");

int totalPoints = 7;
int players = 2;
Console.WriteLine($"Average (integer): {totalPoints / players}");
Console.WriteLine($"Average (exact): {(double)totalPoints / players}");

int bonus = 10;
bonus += 5;
bonus *= 2;
Console.WriteLine($"Bonus: {bonus}");

int year1 = 2024;
int year2 = 2100;
int year3 = 2000;
bool leap1 = (year1 % 4 == 0 && year1 % 100 != 0) || year1 % 400 == 0;
bool leap2 = (year2 % 4 == 0 && year2 % 100 != 0) || year2 % 400 == 0;
bool leap3 = (year3 % 4 == 0 && year3 % 100 != 0) || year3 % 400 == 0;
Console.WriteLine($"Is {year1} a leap year: {leap1}");
Console.WriteLine($"Is {year2} a leap year: {leap2}");
Console.WriteLine($"Is {year3} a leap year: {leap3}");

string? nickname = null;
Console.WriteLine($"Welcome, {nickname ?? "guest"}");
'''

NEW_LESSONS = {
    (2, 1): lesson(
        subtitle="Declare, name, and assign variables, use constants, understand scope, and represent missing values with nullable types.",
        reading=VARIABLES_READING,
        codealong=VARIABLES_CODEALONG,
        lab=VARIABLES_LAB,
    ),
    (2, 3): lesson(
        subtitle="Convert between types safely using implicit conversions, explicit casts, Parse, TryParse, and the Convert class, and understand overflow.",
        reading=CONVERSION_READING,
        codealong=CONVERSION_CODEALONG,
        lab=CONVERSION_LAB,
    ),
    (2, 4): lesson(
        subtitle="Build and format text with interpolated strings, format specifiers, alignment, verbatim and raw strings, and common string methods.",
        reading=INTERPOLATION_READING,
        codealong=INTERPOLATION_CODEALONG,
        lab=INTERPOLATION_LAB,
    ),
    (2, 5): lesson(
        subtitle="Combine values with arithmetic, comparison, and logical operators, and predict how expressions are evaluated.",
        reading=OPERATORS_READING,
        codealong=OPERATORS_CODEALONG,
        lab=OPERATORS_LAB,
    ),
}

NEW_SOLUTIONS = {
    (2, 1): VARIABLES_SOLUTION,
    (2, 3): CONVERSION_SOLUTION,
    (2, 4): INTERPOLATION_SOLUTION,
    (2, 5): OPERATORS_SOLUTION,
}

LESSONS = {
    **NEW_LESSONS,
    (2, 2): {
        "subtitle": "Every value in C# has a type. Understanding data types is the foundation of writing correct, efficient programs. In this lesson, you'll learn the types C# gives you out of the box and when to use each one.",
        "reading": BUILTIN_TYPES_READING,
        "codealong": BUILTIN_TYPES_CODEALONG,
        "lab": BUILTIN_TYPES_LAB,
    },
}

# Reference solutions, used only by verify_content.py (never sent to the learner).
SOLUTIONS = {
    **NEW_SOLUTIONS,
    (2, 2): """decimal price = 49.99m;
int quantity = 3;
decimal total = price * quantity;
bool exceeds = total > 100.00m;
Console.WriteLine($"Total: {total:C}");
Console.WriteLine($"Exceeds $100: {exceeds}");
""",
}
