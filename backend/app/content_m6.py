"""Module 6: Collections, Generics, and LINQ."""
from .lesson_kit import *  # noqa: F401,F403

# ─── 6.1 Arrays and Lists ───

ARRAYS_LISTS_READING = [
    h2("Why collections?"),
    p("""So far every value you have stored lived in its own variable. That works for three scores, but not for three hundred, and not when you do not know the count until the program runs. A **collection** is one variable that holds many values, and C# gives you two everyday choices: arrays and `List<T>`."""),
    h2("Arrays: fixed size, fast, simple"),
    p("""An array is a numbered row of boxes, all holding the same type. You choose the length when you create it, and it can never grow or shrink. Positions start at **0**, so an array of 3 items has valid positions 0, 1, and 2."""),
    code(r'''
int[] scores = new int[3];          // three slots, each starts at 0
scores[0] = 90;
scores[1] = 75;
scores[2] = 82;

string[] days = ["Mon", "Tue", "Wed"];   // create and fill in one step
Console.WriteLine(days.Length);          // Output: 3
Console.WriteLine(days[1]);              // Output: Tue

foreach (int s in scores)
{
    Console.WriteLine(s);                // Output: 90, then 75, then 82
}
'''),
    warn("""**Common mistake:** asking for a position that does not exist. `scores[3]` on a 3-item array compiles fine but throws `IndexOutOfRangeException` when it runs. The last valid position is always `Length - 1`. If you are coming from Python, note that C# does not accept negative numbers like `-1` here (you will meet a C# alternative, `^1`, below)."""),
    h2("List<T>: the growable collection"),
    p("""A `List<T>` is like an array that resizes itself. The `<T>` means 'a list of some type': `List<string>` holds strings, `List<int>` holds integers. You will learn exactly how that works in the Generics lesson. For now, read `List<string>` as 'list of strings'. Most day-to-day C# code uses `List<T>` instead of raw arrays because you can add and remove items freely."""),
    code(r'''
var names = new List<string> { "Ada", "Grace" };
names.Add("Linus");            // add to the end
names.Insert(1, "Alan");       // insert at position 1, shifting the rest right
bool removed = names.Remove("Grace");   // removes the first match, returns true
names.RemoveAt(0);             // remove by position

Console.WriteLine(names.Count);           // Output: 2  (Count, not Length)
Console.WriteLine(names.Contains("Alan"));// Output: True
Console.WriteLine(names.IndexOf("Linus"));// Output: 1  (-1 if not found)
Console.WriteLine(string.Join(", ", names)); // Output: Alan, Linus
'''),
    p("""Notice the naming: arrays use `.Length`, lists use `.Count`. Both are properties (no parentheses). `string.Join(", ", collection)` is the quickest way to print a whole collection on one line."""),
    warn("""**Do not change a list while a `foreach` is looping over it.** Calling `Add` or `Remove` inside the loop makes the next iteration throw `InvalidOperationException` ('Collection was modified'). Loop over a copy, or collect what to remove and do it after the loop."""),
    h2("Indices and ranges"),
    p("""C# has two handy pieces of syntax for picking out positions. The **hat** operator `^` counts from the end: `^1` is the last item, `^2` the second to last. The **range** operator `..` slices: `1..4` means 'from position 1 up to, but not including, position 4'. Either side may be left off."""),
    code(r'''
int[] nums = [10, 20, 30, 40, 50];

Console.WriteLine(nums[^1]);                  // Output: 50
Console.WriteLine(nums[^2]);                  // Output: 40
Console.WriteLine(string.Join(", ", nums[1..4])); // Output: 20, 30, 40
Console.WriteLine(string.Join(", ", nums[..2]));  // Output: 10, 20
Console.WriteLine(string.Join(", ", nums[^2..])); // Output: 40, 50

var list = new List<int>(nums);
Console.WriteLine(list[^1]);                  // Output: 50
'''),
    note("""A range on an array (or a string) gives you a **new copy** of that slice. Changing the slice does not change the original. The `^` index works on `List<T>` too, but the `..` range syntax does not apply to a `List<T>` directly. Use `list.GetRange(start, count)` or convert with `list.ToArray()` first."""),
    h2("Collection expressions and sorting"),
    p("""You have already seen `[10, 20, 30]` above. That is a **collection expression**: square brackets create whatever collection the target type asks for, whether an array, a `List<T>`, or something else. Use `[]` for an empty one. Sorting is built in: `list.Sort()` and `Array.Sort(array)` reorder in place from smallest to largest, and `Reverse()` flips the current order."""),
    code(r'''
List<int> values = [42, 7, 19, 3];
values.Sort();                          // now 3, 7, 19, 42
Console.WriteLine(string.Join(", ", values));   // Output: 3, 7, 19, 42
values.Reverse();                       // now 42, 19, 7, 3
Console.WriteLine(string.Join(", ", values));   // Output: 42, 19, 7, 3

string[] fruits = ["pear", "apple", "fig"];
Array.Sort(fruits);
Console.WriteLine(string.Join(", ", fruits));   // Output: apple, fig, pear
List<string> empty = [];
Console.WriteLine(empty.Count);                 // Output: 0
'''),
    tip("""Reach for `List<T>` by default. Use an array when the size is truly fixed or an API hands you one. Sorting in place **changes** the collection. If you need the original order later, copy it first with `new List<int>(values)`."""),
    link("Read more on Microsoft Learn: Collections", "https://learn.microsoft.com/en-us/dotnet/standard/collections/"),
]

ARRAYS_LISTS_CODEALONG = codealong(
    "Code Along: Arrays and Lists",
    "Type each step into one Program.cs, in order. Each step adds to the same file.",
    [
        step(
            "Create and loop over an array",
            "An array has a fixed length and zero-based positions. Create one with `new int[3]`, fill the slots, and add a second array with a collection expression.",
            r'''
int[] scores = new int[3];
scores[0] = 90;
scores[1] = 75;
scores[2] = 82;
string[] days = ["Mon", "Tue", "Wed"];
Console.WriteLine($"Length: {scores.Length}, first day: {days[0]}");
foreach (int s in scores)
{
    Console.WriteLine($"Score: {s}");
}
''',
        ),
        step(
            "Grow a List",
            "A `List<string>` can change size. Add, insert, and remove items, then print the result with `string.Join`.",
            r'''
var names = new List<string> { "Ada", "Grace" };
names.Add("Linus");
names.Insert(1, "Alan");
names.Remove("Grace");
Console.WriteLine($"Count: {names.Count}");
Console.WriteLine(string.Join(", ", names));
Console.WriteLine($"Has Ada: {names.Contains("Ada")}, index of Linus: {names.IndexOf("Linus")}");
''',
        ),
        step(
            "Use ^ and ..",
            "Pick items from the end with `^` and slice with `..`. Remember the end of a range is excluded.",
            r'''
int[] nums = [10, 20, 30, 40, 50];
Console.WriteLine($"Last: {nums[^1]}, second to last: {nums[^2]}");
Console.WriteLine($"nums[1..4]: {string.Join(", ", nums[1..4])}");
Console.WriteLine($"nums[..2]: {string.Join(", ", nums[..2])}");
Console.WriteLine($"nums[^2..]: {string.Join(", ", nums[^2..])}");
Console.WriteLine($"Last name: {names[^1]}");
''',
        ),
        step(
            "Sort and reverse",
            "Build a list with a collection expression, sort it in place, then reverse it. Do the same for a string array with `Array.Sort`.",
            r'''
List<int> values = [42, 7, 19, 3];
values.Sort();
Console.WriteLine($"Ascending: {string.Join(", ", values)}");
values.Reverse();
Console.WriteLine($"Descending: {string.Join(", ", values)}");

string[] fruits = ["pear", "apple", "fig"];
Array.Sort(fruits);
Console.WriteLine($"Fruits: {string.Join(", ", fruits)}");
''',
        ),
    ],
)

ARRAYS_LISTS_LAB = lab(
    "Lab: Leaderboard",
    "Beginner",
    "Build a small game leaderboard. You will add and remove scores in a List, sort it, and use indices and ranges to report results.",
    [
        "Start with `List<int> scores = [72, 95, 88, 61, 95, 70];` then add `83` with `Add` and remove the value `61` with `Remove`",
        "Sort the list ascending with `Sort()`, then call `Reverse()` so it is highest-first",
        "Create an `int[]` named `top3` containing the first three scores by calling `scores.ToArray()` and slicing it with a range",
        "Use a `foreach` loop (no LINQ) to add up all scores into an `int` total, then compute the average as a `double` (`total / count`)",
        "Print exactly five lines: `Scores: ...` (all scores joined with `, `), `Top 3: ...`, `Lowest: ` (use `scores[^1]`), `Count: ` (the list's count), and `Average: ` formatted with one decimal place (`:F1`)",
    ],
    """
Scores: 95, 95, 88, 83, 72, 70
Top 3: 95, 95, 88
Lowest: 70
Count: 6
Average: 83.8
""",
    "After `Sort()` and `Reverse()` the highest score is at position 0 and the lowest at `^1`. For the average, cast one side to double: `(double)total / scores.Count`. `ToArray()` gives you an array, and arrays can be sliced with `[..3]`.",
)

ARRAYS_LISTS_SOLUTION = r'''
List<int> scores = [72, 95, 88, 61, 95, 70];
scores.Add(83);
scores.Remove(61);
scores.Sort();
scores.Reverse();
int[] top3 = scores.ToArray()[..3];
int total = 0;
foreach (int s in scores)
{
    total += s;
}
double average = (double)total / scores.Count;
Console.WriteLine($"Scores: {string.Join(", ", scores)}");
Console.WriteLine($"Top 3: {string.Join(", ", top3)}");
Console.WriteLine($"Lowest: {scores[^1]}");
Console.WriteLine($"Count: {scores.Count}");
Console.WriteLine($"Average: {average:F1}");
'''

# ─── 6.2 Dictionaries and Sets ───

DICT_SETS_READING = [
    h2("Looking things up by key"),
    p("""A list finds things by position. But often you want to find a value by something meaningful: a product by its name, a user by their id. A `Dictionary<TKey, TValue>` stores **pairs**: each unique key maps to one value. If you know Python, this is a `dict`. Looking up a key is very fast no matter how many entries there are."""),
    code(r'''
var stock = new Dictionary<string, int>
{
    ["apples"] = 5,
    ["pears"] = 0,
};
stock["bananas"] = 12;      // adds a new key
stock["apples"] += 3;       // updates an existing key

Console.WriteLine(stock["apples"]);   // Output: 8
Console.WriteLine(stock.Count);       // Output: 3
stock.Remove("pears");
Console.WriteLine(stock.ContainsKey("pears"));  // Output: False
'''),
    warn("""**Common mistake:** reading a key that is not there. `stock["kiwis"]` throws `KeyNotFoundException`. Also, `stock.Add("apples", 1)` throws if the key already exists, while `stock["apples"] = 1` quietly overwrites. Use the indexer to 'add or update' and `Add` when a duplicate would be a bug."""),
    h2("TryGetValue: the safe lookup"),
    p("""`TryGetValue` asks 'is this key here?' and hands back the value in one step. It returns `true` or `false`, and the value comes out through an `out` parameter, a variable that the method fills in for you."""),
    code(r'''
if (stock.TryGetValue("apples", out int count))
{
    Console.WriteLine($"We have {count} apples");   // Output: We have 8 apples
}
else
{
    Console.WriteLine("No apples tracked");
}

// Shortcut when a missing key can simply mean zero:
int kiwis = stock.GetValueOrDefault("kiwis");       // 0
'''),
    h2("Iterating and the order caveat"),
    p("""You can loop over a dictionary with `foreach`, and each item is a key/value pair that you can unpack right in the loop header. The catch: a dictionary makes **no promise about the order** of its entries. It often looks like insertion order, but removing and adding items can change that, and you should never depend on it."""),
    code(r'''
foreach (var (key, value) in stock)
{
    Console.WriteLine($"{key} = {value}");   // order not guaranteed!
}

// Deterministic output: sort the keys first.
var keys = new List<string>(stock.Keys);
keys.Sort();
foreach (string key in keys)
{
    Console.WriteLine($"{key} = {stock[key]}");
}
'''),
    tip("""Whenever a dictionary's contents are printed or compared in a test, copy the keys into a `List<string>`, `Sort()` it, and loop over that. Your output then looks the same on every run and every machine."""),
    h2("HashSet<T>: unique items and set math"),
    p("""A `HashSet<T>` holds each value **at most once** and answers 'is this in the set?' very quickly. `Add` returns `true` if the item was new and `false` if it was already there. Sets also support the operations you may remember from math class: union, intersection, and difference."""),
    code(r'''
HashSet<int> a = [1, 2, 3, 4];
HashSet<int> b = [3, 4, 5];
Console.WriteLine(a.Add(4));          // Output: False (already present)
Console.WriteLine(a.Contains(2));     // Output: True

var union = new HashSet<int>(a);  union.UnionWith(b);       // 1,2,3,4,5
var common = new HashSet<int>(a); common.IntersectWith(b);  // 3,4
var onlyA = new HashSet<int>(a);  onlyA.ExceptWith(b);      // 1,2
Console.WriteLine(a.IsSubsetOf(union));   // Output: True
'''),
    note("""`UnionWith`, `IntersectWith`, and `ExceptWith` **modify the set they are called on**. That is why the example copies `a` first with `new HashSet<int>(a)`. Like dictionaries, sets have no guaranteed order, so copy to a list and sort before printing."""),
    h2("Queue and Stack in brief"),
    p("""Two small collections are worth knowing. A `Queue<T>` is first in, first out, like a line at a shop: `Enqueue` joins the back, `Dequeue` serves the front, `Peek` looks without removing. A `Stack<T>` is last in, first out, like a pile of plates: `Push` adds on top, `Pop` removes the top. Calling `Dequeue` or `Pop` on an empty one throws `InvalidOperationException`, so check `Count` first."""),
    code(r'''
var line = new Queue<string>();
line.Enqueue("Ann");
line.Enqueue("Bo");
Console.WriteLine(line.Dequeue());   // Output: Ann
Console.WriteLine(line.Peek());      // Output: Bo

var pile = new Stack<string>();
pile.Push("page1");
pile.Push("page2");
Console.WriteLine(pile.Pop());       // Output: page2
'''),
    link("Read more on Microsoft Learn: Dictionary<TKey,TValue>", "https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.dictionary-2"),
]

DICT_SETS_CODEALONG = codealong(
    "Code Along: Dictionaries, Sets, Queues",
    "Type each step into one Program.cs in order. We sort before printing anything whose order is not guaranteed.",
    [
        step(
            "Create and update a dictionary",
            "Build a dictionary with the indexer syntax, add a key, and update an existing one with `+=`.",
            r'''
var stock = new Dictionary<string, int>
{
    ["apples"] = 5,
    ["pears"] = 0,
};
stock["bananas"] = 12;
stock["apples"] += 3;
Console.WriteLine($"Apples: {stock["apples"]}");
Console.WriteLine($"Kinds: {stock.Count}");
''',
        ),
        step(
            "Look up safely",
            "Use `TryGetValue` so a missing key does not crash the program. `GetValueOrDefault` is a shortcut that returns 0 for a missing int.",
            r'''
if (stock.TryGetValue("pears", out int pears))
{
    Console.WriteLine($"Pears in stock: {pears}");
}
if (!stock.TryGetValue("kiwis", out int kiwis))
{
    Console.WriteLine("No kiwis tracked");
}
Console.WriteLine($"Contains bananas: {stock.ContainsKey("bananas")}");
Console.WriteLine($"Kiwis (default): {stock.GetValueOrDefault("kiwis")}");
''',
        ),
        step(
            "Count words, print in sorted order",
            "A classic dictionary job: count how often each word appears. Copy the keys to a list and sort it so the output is the same every run.",
            r'''
string sentence = "to be or not to be";
var counts = new Dictionary<string, int>();
foreach (string word in sentence.Split(' '))
{
    counts[word] = counts.GetValueOrDefault(word) + 1;
}
var keys = new List<string>(counts.Keys);
keys.Sort();
foreach (string key in keys)
{
    Console.WriteLine($"{key}: {counts[key]}");
}
''',
        ),
        step(
            "Set operations",
            "Create two sets, then copy before applying union, intersection, and difference. The small `Show` helper sorts a set so it prints predictably.",
            r'''
HashSet<int> a = [1, 2, 3, 4];
HashSet<int> b = [3, 4, 5];
Console.WriteLine($"Add 4 again: {a.Add(4)}");

var union = new HashSet<int>(a);
union.UnionWith(b);
var common = new HashSet<int>(a);
common.IntersectWith(b);
var onlyA = new HashSet<int>(a);
onlyA.ExceptWith(b);
Console.WriteLine($"Union: {Show(union)}");
Console.WriteLine($"Common: {Show(common)}");
Console.WriteLine($"Only A: {Show(onlyA)}");

string Show(HashSet<int> set)
{
    var items = new List<int>(set);
    items.Sort();
    return string.Join(", ", items);
}
''',
        ),
        step(
            "Queue and Stack",
            "A queue serves the oldest item first; a stack hands back the newest.",
            r'''
var line = new Queue<string>();
line.Enqueue("Ann");
line.Enqueue("Bo");
line.Enqueue("Cy");
Console.WriteLine($"Serving {line.Dequeue()}, next is {line.Peek()}, waiting: {line.Count}");

var history = new Stack<string>();
history.Push("page1");
history.Push("page2");
Console.WriteLine($"Leaving {history.Pop()}, now on {history.Peek()}");
''',
        ),
    ],
)

DICT_SETS_LAB = lab(
    "Lab: Word Counter and Set Toolkit",
    "Beginner",
    "Count words with a dictionary, query it safely, compare two sets, and reverse text with a stack. Every printed collection must be in a predictable order.",
    [
        "Split the text `the cat and the hat and the bat` on spaces and count each word in a `Dictionary<string, int>`",
        "Copy the dictionary's keys into a `List<string>`, sort it, and print one line per word in the form `word: count`",
        "Print `Unique words: ` followed by the number of entries in the dictionary",
        "Use `TryGetValue` to look up `dog`; print `dog: not found` when missing (or `dog: <count>` if it were found)",
        "Create `HashSet<int>` sets A = 1,2,3,4 and B = 3,4,5. Print three lines: `Both: ` (intersection), `Either: ` (union), and `Only A: ` (A without B), each with numbers sorted ascending and joined by `, `",
        "Push the characters of `abc` onto a `Stack<char>`, pop them all into a string, and print `Reversed: ` followed by the result",
    ],
    """
and: 2
bat: 1
cat: 1
hat: 1
the: 3
Unique words: 5
dog: not found
Both: 3, 4
Either: 1, 2, 3, 4, 5
Only A: 1, 2
Reversed: cba
""",
    "Counting: `counts[w] = counts.GetValueOrDefault(w) + 1;`. For each set operation, copy first (`new HashSet<int>(a)`), then call `IntersectWith`, `UnionWith`, or `ExceptWith`. A set has no order, so copy it into a `List<int>` and `Sort()` before `string.Join`. A stack gives characters back in reverse order.",
)

DICT_SETS_SOLUTION = r'''
string text = "the cat and the hat and the bat";
var counts = new Dictionary<string, int>();
foreach (string w in text.Split(' '))
{
    counts[w] = counts.GetValueOrDefault(w) + 1;
}
var keys = new List<string>(counts.Keys);
keys.Sort();
foreach (string k in keys)
{
    Console.WriteLine($"{k}: {counts[k]}");
}
Console.WriteLine($"Unique words: {counts.Count}");
if (counts.TryGetValue("dog", out int dog))
{
    Console.WriteLine($"dog: {dog}");
}
else
{
    Console.WriteLine("dog: not found");
}

HashSet<int> setA = [1, 2, 3, 4];
HashSet<int> setB = [3, 4, 5];
var both = new HashSet<int>(setA);
both.IntersectWith(setB);
var either = new HashSet<int>(setA);
either.UnionWith(setB);
var onlyA = new HashSet<int>(setA);
onlyA.ExceptWith(setB);
Console.WriteLine($"Both: {Sorted(both)}");
Console.WriteLine($"Either: {Sorted(either)}");
Console.WriteLine($"Only A: {Sorted(onlyA)}");

var stack = new Stack<char>();
foreach (char c in "abc")
{
    stack.Push(c);
}
string reversed = "";
while (stack.Count > 0)
{
    reversed += stack.Pop();
}
Console.WriteLine($"Reversed: {reversed}");

string Sorted(HashSet<int> set)
{
    var items = new List<int>(set);
    items.Sort();
    return string.Join(", ", items);
}
'''

# ─── 6.3 Generics ───

GENERICS_READING = [
    h2("The problem generics solve"),
    p("""Imagine a collection class that must work for numbers, strings, and customers. One option is to store everything as `object`, the base type of all values. It works, but you lose two things: the compiler can no longer tell you what is inside, and value types like `int` get **boxed** (wrapped in a heap object) every time you store them."""),
    code(r'''
List<object> things = new List<object>();
things.Add(42);                 // boxed: the int is wrapped in an object
things.Add("oops");
int first = (int)things[0];     // a cast is required to get the int back
int second = (int)things[1];    // compiles! but crashes: InvalidCastException
'''),
    p("""**Generics** fix this. A generic type or method has one or more **type parameters**, placeholders like `T` that the caller fills in. `List<int>` is a list that can only hold ints. The compiler checks it for you, no casts are needed, and ints are stored directly without boxing."""),
    h2("Generic methods"),
    p("""Put the type parameter in angle brackets after the method name, then use it anywhere a type could appear. Usually the compiler works out `T` from the arguments, so you rarely have to write it."""),
    code(r'''
static T FirstOr<T>(List<T> items, T fallback)
{
    return items.Count > 0 ? items[0] : fallback;
}

var numbers = new List<int> { 5, 6 };
Console.WriteLine(FirstOr(numbers, -1));              // Output: 5   (T inferred as int)
Console.WriteLine(FirstOr(new List<string>(), "none"));// Output: none (T inferred as string)
Console.WriteLine(FirstOr<double>(new List<double>(), 1.5)); // Output: 1.5 (T written out)
'''),
    h2("Generic classes and records"),
    p("""Types can be generic too. By convention a single parameter is named `T`; with several, use descriptive names that start with `T`, like `TKey` and `TValue`. `Dictionary<TKey, TValue>` is exactly that."""),
    code(r'''
class Box<T>
{
    public T Value { get; }
    public Box(T value) => Value = value;
}

record Pair<TFirst, TSecond>(TFirst First, TSecond Second);

var b = new Box<string>("hi");
var pair = new Pair<string, int>("age", 30);
Console.WriteLine(b.Value);                       // Output: hi
Console.WriteLine($"{pair.First} = {pair.Second}");// Output: age = 30
'''),
    h2("Constraints: telling the compiler what T can do"),
    p("""Inside a generic method, `T` could be anything, so the compiler only lets you do things that work for everything. You cannot compare two `T` values with `>`, because plenty of types have no ordering. A **constraint** with `where` promises that `T` has certain abilities, and unlocks them."""),
    code(r'''
static T Largest<T>(List<T> items) where T : IComparable<T>
{
    T best = items[0];
    foreach (T item in items)
    {
        if (item.CompareTo(best) > 0) best = item;   // allowed thanks to the constraint
    }
    return best;
}

Console.WriteLine(Largest(new List<int> { 3, 9, 4 }));            // Output: 9
Console.WriteLine(Largest(new List<string> { "pear", "fig" }));   // Output: pear
'''),
    warn("""**Common mistake:** forgetting the constraint. Without `where T : IComparable<T>`, the line `item.CompareTo(best)` fails to compile (and so does `item > best`). Calling `Largest` with a type that does not meet the constraint, such as a class that is not comparable, is also a compile error, which is exactly the point."""),
    p("""Common constraints: `where T : class` (a reference type), `where T : struct` (a value type such as `int`), `where T : new()` (has a public parameterless constructor, so you can write `new T()`), and `where T : SomeInterface` or `SomeBaseClass`. You can combine them with commas, for example `where T : class, new()`."""),
    h2("default(T)"),
    p("""Sometimes a generic method needs 'the empty value of T' without knowing what T is. `default(T)`, or just `default` when the type is clear, gives `0` for numbers, `false` for `bool`, and `null` for reference types such as `string`."""),
    code(r'''
Console.WriteLine(default(int));            // Output: 0
Console.WriteLine(default(bool));           // Output: False
Console.WriteLine(default(string) is null); // Output: True

static T Last<T>(List<T> items) => items.Count > 0 ? items[^1] : default!;
Console.WriteLine(Last(new List<int>()));   // Output: 0
'''),
    note("""The `!` in `default!` quiets a nullable warning: the compiler worries that `default` might be `null` for a `T` that is not allowed to be null. It does not change behavior. Another approach is declaring the return type as `T?`, which tells callers 'might be empty'."""),
    tip("""You have been using generics all along: `List<T>`, `Dictionary<TKey, TValue>`, `HashSet<T>`. Reach for writing your own generic type or method when you catch yourself copy-pasting the same code for different types. Do not make things generic just in case."""),
    link("Read more on Microsoft Learn: Generics", "https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/generics"),
]

GENERICS_CODEALONG = codealong(
    "Code Along: Writing Generic Code",
    "Type each step into one Program.cs in order. Steps that declare a type go at the bottom of the file.",
    [
        step(
            "A generic method",
            "Write a small generic method as a local function. The compiler infers `T` from the arguments.",
            r'''
T FirstOr<T>(List<T> items, T fallback) => items.Count > 0 ? items[0] : fallback;

Console.WriteLine(FirstOr(new List<int> { 5, 6 }, -1));
Console.WriteLine(FirstOr(new List<string>(), "none"));
''',
        ),
        step(
            "Add a constraint",
            "To compare items, `T` must promise it can compare itself to another `T`. That is what `where T : IComparable<T>` does.",
            r'''
T Largest<T>(IEnumerable<T> items) where T : IComparable<T>
{
    bool first = true;
    T best = default!;
    foreach (T item in items)
    {
        if (first || item.CompareTo(best) > 0)
        {
            best = item;
            first = false;
        }
    }
    return best;
}

Console.WriteLine($"Largest int: {Largest(new[] { 3, 9, 4 })}");
Console.WriteLine($"Largest string: {Largest(new[] { "pear", "apple", "fig" })}");
''',
        ),
        step(
            "Declare a generic class and record",
            "Add these two declarations at the **bottom** of the file, below all your other code.",
            r'''
class Box<T>
{
    public T Value { get; }
    public Box(T value) => Value = value;
    public override string ToString() => $"Box<{typeof(T).Name}>({Value})";
}

record Pair<TFirst, TSecond>(TFirst First, TSecond Second);
''',
            at="bottom",
        ),
        step(
            "Use them, and meet default(T)",
            "Create boxes of different types, build a pair, and print the default values of a few types.",
            r'''
var intBox = new Box<int>(7);
var textBox = new Box<string>("hi");
Console.WriteLine(intBox);
Console.WriteLine(textBox);

var pair = new Pair<string, int>("age", 30);
Console.WriteLine($"{pair.First} = {pair.Second}");

Console.WriteLine($"default int: {default(int)}");
Console.WriteLine($"default bool: {default(bool)}");
Console.WriteLine($"default string is null: {default(string) is null}");
''',
        ),
    ],
)

GENERICS_LAB = lab(
    "Lab: A Generic Toolkit",
    "Intermediate",
    "Write one generic method with a constraint and one generic class, then use both with different types.",
    [
        "Write a generic method `T Largest<T>(List<T> items) where T : IComparable<T>` that returns the biggest item, or `default` if the list is empty (a local function at the top of the file is fine)",
        "Print `Largest int: ` for the list 7, 42, 13; `Largest string: ` for the list apple, pear, fig; and `Largest of empty: ` for an empty `List<int>`",
        "Declare a generic class `SimpleStack<T>` at the bottom of the file. It keeps its items in a private `List<T>`, has a `Count` property, a `Push(T item)` method, and a `T Pop()` method that removes and returns the newest item, or returns `default` when empty",
        "With a `SimpleStack<int>`, push 10, 20, 30. Then print `Popped: ` twice, then `Count: `, then `Popped: ` once more, then `Pop on empty: ` for one more `Pop()`",
        "With a new empty `SimpleStack<string>`, print `Empty string stack: ` followed by the popped value, or `<null>` when it is null (use `??`)",
    ],
    """
Largest int: 42
Largest string: pear
Largest of empty: 0
Popped: 30
Popped: 20
Count: 1
Popped: 10
Pop on empty: 0
Empty string stack: <null>
""",
    "Inside `Largest`, start with `items[0]` as the best so far and compare with `item.CompareTo(best) > 0`. For the empty case use `return default!;` (the `!` silences a warning). In the stack, the newest item is at `_items[^1]`; remove it with `RemoveAt(_items.Count - 1)`.",
)

GENERICS_SOLUTION = r'''
T Largest<T>(List<T> items) where T : IComparable<T>
{
    if (items.Count == 0) return default!;
    T best = items[0];
    foreach (T item in items)
    {
        if (item.CompareTo(best) > 0) best = item;
    }
    return best;
}

Console.WriteLine($"Largest int: {Largest(new List<int> { 7, 42, 13 })}");
Console.WriteLine($"Largest string: {Largest(new List<string> { "apple", "pear", "fig" })}");
Console.WriteLine($"Largest of empty: {Largest(new List<int>())}");

var ints = new SimpleStack<int>();
ints.Push(10);
ints.Push(20);
ints.Push(30);
Console.WriteLine($"Popped: {ints.Pop()}");
Console.WriteLine($"Popped: {ints.Pop()}");
Console.WriteLine($"Count: {ints.Count}");
Console.WriteLine($"Popped: {ints.Pop()}");
Console.WriteLine($"Pop on empty: {ints.Pop()}");

var words = new SimpleStack<string>();
Console.WriteLine($"Empty string stack: {words.Pop() ?? "<null>"}");

class SimpleStack<T>
{
    private readonly List<T> _items = new();

    public int Count => _items.Count;

    public void Push(T item) => _items.Add(item);

    public T Pop()
    {
        if (_items.Count == 0) return default!;
        T top = _items[^1];
        _items.RemoveAt(_items.Count - 1);
        return top;
    }
}
'''

# ─── 6.4 LINQ Basics ───

LINQ_BASICS_READING = [
    h2("Asking questions of a collection"),
    p("""Think about the loops you write over collections: 'keep the ones that match', 'turn each into something else', 'find the biggest', 'add them up'. These patterns are so common that C# has a built-in toolbox for them called **LINQ** (Language Integrated Query). Instead of writing the loop, you describe **what** you want, and LINQ does the looping."""),
    p("""LINQ lives in the `System.Linq` namespace, which your projects already import automatically. Its methods work on arrays, lists, dictionaries, sets, and anything else you can `foreach` over."""),
    h2("A first look at lambdas"),
    p("""Most LINQ methods take a tiny inline function called a **lambda**. The arrow `=>` reads 'goes to': `n => n > 10` means 'given n, answer whether n is greater than 10'. The name before the arrow is just a parameter name you choose. You will study lambdas properly in the Delegates lesson; for now, read them as 'for each item'."""),
    h2("The core methods"),
    code(r'''
int[] numbers = [5, 12, 8, 21, 3, 16];

var big = numbers.Where(n => n > 10);          // keep matching items: 12, 21, 16
var doubled = numbers.Select(n => n * 2);      // transform each: 10, 24, 16, 42, 6, 32
var ascending = numbers.OrderBy(n => n);       // 3, 5, 8, 12, 16, 21
var descending = numbers.OrderByDescending(n => n);

Console.WriteLine(string.Join(", ", big));         // Output: 12, 21, 16
Console.WriteLine(string.Join(", ", doubled));     // Output: 10, 24, 16, 42, 6, 32
Console.WriteLine(string.Join(", ", ascending));   // Output: 3, 5, 8, 12, 16, 21
'''),
    h2("Answering single questions"),
    code(r'''
Console.WriteLine(numbers.First());              // Output: 5
Console.WriteLine(numbers.First(n => n > 10));   // Output: 12
Console.WriteLine(numbers.FirstOrDefault(n => n > 100)); // Output: 0 (nothing matched)
Console.WriteLine(numbers.Any(n => n > 20));     // Output: True
Console.WriteLine(numbers.Count(n => n % 2 == 0));// Output: 3  (12, 8, 16)
Console.WriteLine(numbers.Sum());                // Output: 65
Console.WriteLine(numbers.Max());                // Output: 21
Console.WriteLine(numbers.Average());            // Output: 10.833333333333334
'''),
    warn("""**Common mistake:** using `First` when nothing might match. `First` throws `InvalidOperationException` ('Sequence contains no matching element') on an empty result. Use `FirstOrDefault` (returns `0`, `null`, or another default) or check with `Any` first when a match is not guaranteed."""),
    h2("Chaining and method vs query syntax"),
    p("""Each method returns a new sequence, so you can chain them into a pipeline: filter, then sort, then transform. This **method syntax** is what most C# developers write. LINQ also has **query syntax**, which reads like SQL. The compiler turns it into the same method calls, so they are interchangeable."""),
    code(r'''
// Method syntax
var a = numbers.Where(n => n > 5).OrderBy(n => n).Select(n => $"#{n}");

// Query syntax: same result
var b = from n in numbers
        where n > 5
        orderby n
        select $"#{n}";

Console.WriteLine(string.Join(" ", a));   // Output: #8 #12 #16 #21
Console.WriteLine(string.Join(" ", b));   // Output: #8 #12 #16 #21
'''),
    note("""Query syntax is pleasant for filter-sort-select, but it cannot express every operation (there is no keyword for `Count` or `First`), so you will see the two mixed. Learn method syntax first. It covers everything."""),
    h2("Lazy execution"),
    p("""Here is the idea that surprises most beginners: `Where`, `Select`, and `OrderBy` do **not** run when you call them. They build a *recipe*. The work happens only when something asks for the results, such as a `foreach`, `string.Join`, `First()`, `Count()`, or `ToList()`. This is called **deferred** (or lazy) execution."""),
    code(r'''
var checkedItems = numbers.Where(n =>
{
    Console.WriteLine($"  checking {n}");
    return n > 10;
});
Console.WriteLine("Query created");     // nothing has been checked yet
Console.WriteLine(checkedItems.First());
// Output:
// Query created
//   checking 5
//   checking 12
// 12
'''),
    p("""Notice `First()` stopped as soon as it found 12; items after it were never checked. Because the recipe runs fresh each time you ask, the results also reflect whatever is in the source **at that moment**. Call `ToList()` or `ToArray()` when you want to run the query once and keep a snapshot."""),
    tip("""Working with records or classes? The same methods apply: `people.Where(p => p.Age >= 18).Select(p => p.Name)`. The lambda parameter is simply one `Person`."""),
    link("Read more on Microsoft Learn: LINQ", "https://learn.microsoft.com/en-us/dotnet/csharp/linq/"),
]

LINQ_BASICS_CODEALONG = codealong(
    "Code Along: Your First LINQ Queries",
    "Type each step into one Program.cs in order. Take note of when each query actually runs.",
    [
        step(
            "Filter, transform, and sort",
            "`Where` keeps items, `Select` transforms them, and `OrderBy` sorts them. Print each result with `string.Join`.",
            r'''
int[] numbers = [5, 12, 8, 21, 3, 16];
Console.WriteLine($"Big: {string.Join(", ", numbers.Where(n => n > 10))}");
Console.WriteLine($"Doubled: {string.Join(", ", numbers.Select(n => n * 2))}");
Console.WriteLine($"Sorted: {string.Join(", ", numbers.OrderBy(n => n))}");
Console.WriteLine($"Descending: {string.Join(", ", numbers.OrderByDescending(n => n))}");
''',
        ),
        step(
            "Ask single questions",
            "These methods return one value instead of a sequence: first match, yes/no, a count, or a total.",
            r'''
Console.WriteLine($"First big: {numbers.First(n => n > 10)}");
Console.WriteLine($"First over 100 (default): {numbers.FirstOrDefault(n => n > 100)}");
Console.WriteLine($"Any over 20: {numbers.Any(n => n > 20)}");
Console.WriteLine($"Even count: {numbers.Count(n => n % 2 == 0)}");
Console.WriteLine($"Sum: {numbers.Sum()}, Max: {numbers.Max()}, Min: {numbers.Min()}");
''',
        ),
        step(
            "Declare a record to query",
            "Add this record at the **bottom** of the file. Next we will run LINQ over a list of them.",
            r'''
record Product(string Name, decimal Price, string Category);
''',
            at="bottom",
        ),
        step(
            "Query a list of records",
            "The same methods work on your own types. Here is one question written in method syntax and again in query syntax.",
            r'''
var products = new List<Product>
{
    new("Laptop", 999.99m, "Electronics"),
    new("Mouse", 19.99m, "Electronics"),
    new("Desk", 249.50m, "Furniture"),
    new("Pen", 1.50m, "Office"),
};

var cheapNames = products.Where(p => p.Price < 100m).OrderBy(p => p.Price).Select(p => p.Name);
Console.WriteLine($"Cheap (method): {string.Join(", ", cheapNames)}");

var cheapQuery = from p in products
                 where p.Price < 100m
                 orderby p.Price
                 select p.Name;
Console.WriteLine($"Cheap (query):  {string.Join(", ", cheapQuery)}");
Console.WriteLine($"Electronics total: {products.Where(p => p.Category == "Electronics").Sum(p => p.Price):C}");
''',
        ),
        step(
            "See lazy execution happen",
            "The query below prints a message each time it checks an item. Watch when those messages appear. Then see how a later change to the source shows up in an unfinished query but not in a `ToList()` snapshot.",
            r'''
var lazy = numbers.Where(n =>
{
    Console.WriteLine($"  checking {n}");
    return n > 10;
});
Console.WriteLine("Query created, nothing checked yet");
Console.WriteLine($"First match: {lazy.First()}");

var data = new List<int> { 1, 2, 3 };
var evens = data.Where(n => n % 2 == 0);
var snapshot = data.Where(n => n % 2 == 0).ToList();
data.Add(4);
Console.WriteLine($"Lazy evens: {string.Join(", ", evens)}");
Console.WriteLine($"Snapshot evens: {string.Join(", ", snapshot)}");
''',
        ),
    ],
)

LINQ_BASICS_LAB = lab(
    "Lab: Product Report",
    "Beginner",
    "Use LINQ to answer questions about a catalog of products. Declare the record and the list exactly as described so your output matches.",
    [
        "Declare `record Product(string Name, decimal Price, string Category);` at the bottom of the file. In the program, create a `List<Product>` with these six items in this order: Laptop 999.99 Electronics, Mouse 19.99 Electronics, Desk 249.50 Furniture, Chair 129.00 Furniture, Pen 1.50 Office, Notebook 4.25 Office",
        "Print `Under $50: ` followed by the names of products priced under 50, cheapest first, joined by `, `",
        "Print `Furniture count: ` with the number of Furniture products",
        "Print `Electronics total: ` with the sum of Electronics prices formatted as currency (`:C`)",
        "Print `Any over $1000: ` with the boolean result, and `Most expensive: ` with the name of the priciest product (use `OrderByDescending` and `First`)",
        "Using **query syntax** (`from ... where ... select`), print `Office items: ` followed by the Office product names in upper case, in list order, joined by `, `",
    ],
    """
Under $50: Pen, Notebook, Mouse
Furniture count: 2
Electronics total: $1,019.98
Any over $1000: False
Most expensive: Laptop
Office items: PEN, NOTEBOOK
""",
    "Sum a decimal property with `.Sum(p => p.Price)`. For the pricey one: `products.OrderByDescending(p => p.Price).First().Name`. Query syntax pattern: `from p in products where p.Category == \"Office\" select p.Name.ToUpper()`.",
)

LINQ_BASICS_SOLUTION = r'''
var products = new List<Product>
{
    new("Laptop", 999.99m, "Electronics"),
    new("Mouse", 19.99m, "Electronics"),
    new("Desk", 249.50m, "Furniture"),
    new("Chair", 129.00m, "Furniture"),
    new("Pen", 1.50m, "Office"),
    new("Notebook", 4.25m, "Office"),
};

var cheap = products.Where(p => p.Price < 50m).OrderBy(p => p.Price).Select(p => p.Name);
Console.WriteLine($"Under $50: {string.Join(", ", cheap)}");
Console.WriteLine($"Furniture count: {products.Count(p => p.Category == "Furniture")}");
decimal electronics = products.Where(p => p.Category == "Electronics").Sum(p => p.Price);
Console.WriteLine($"Electronics total: {electronics:C}");
Console.WriteLine($"Any over $1000: {products.Any(p => p.Price > 1000m)}");
Console.WriteLine($"Most expensive: {products.OrderByDescending(p => p.Price).First().Name}");

var office = from p in products
             where p.Category == "Office"
             select p.Name.ToUpper();
Console.WriteLine($"Office items: {string.Join(", ", office)}");

record Product(string Name, decimal Price, string Category);
'''

# ─── 6.5 LINQ in Practice ───

LINQ_PRACTICE_READING = [
    h2("From basics to real queries"),
    p("""Real data usually comes as a list of records or objects, and the interesting questions are about **groups** and **relationships**: 'average score per course', 'which student belongs to which course', 'the top three'. This lesson adds the LINQ methods that answer them. The examples use these two records:"""),
    code(r'''
record Student(string Name, string Course, int Score);
record Course(string Code, string Title);

var students = new List<Student>
{
    new("Ava", "CS", 92), new("Ben", "CS", 78), new("Cara", "MATH", 85),
    new("Dan", "MATH", 64), new("Eli", "CS", 88), new("Fay", "HIST", 71),
};
'''),
    h2("GroupBy"),
    p("""`GroupBy` splits a sequence into buckets that share a key. Each bucket is a group object with a `Key` property, and it is itself a sequence of the items inside, so you can call `Count()`, `Average(...)`, and so on on it."""),
    code(r'''
foreach (var group in students.GroupBy(s => s.Course).OrderBy(g => g.Key))
{
    Console.WriteLine($"{group.Key}: {group.Count()} students, average {group.Average(s => s.Score):F1}");
}
// Output:
// CS: 3 students, average 86.0
// HIST: 1 students, average 71.0
// MATH: 2 students, average 74.5
'''),
    h2("ToDictionary"),
    p("""`ToDictionary` turns a sequence into a dictionary by telling it how to compute each key and (optionally) each value. It is the quick way to build a lookup table from a list."""),
    code(r'''
Dictionary<string, int> scoreByName = students.ToDictionary(s => s.Name, s => s.Score);
Console.WriteLine(scoreByName["Cara"]);   // Output: 85
'''),
    warn("""**Common mistake:** a duplicate key. `ToDictionary` throws `ArgumentException` if two items produce the same key (for instance two students named Ava). Choose a key that is truly unique, or use `GroupBy` when duplicates are expected. Remember too that a dictionary's enumeration order is not guaranteed, so sort keys before printing."""),
    h2("Join"),
    p("""`Join` matches items from two lists on a shared value, like a SQL join or a lookup between two spreadsheets. You give it the other list, a key selector for each side, and a function that builds one result from a matching pair. Items with no match are left out."""),
    code(r'''
var courses = new List<Course> { new("CS", "Computer Science"), new("MATH", "Mathematics"), new("HIST", "History") };

var lines = students.Join(courses,
    s => s.Course,            // key from a student
    c => c.Code,              // key from a course
    (s, c) => $"{s.Name} studies {c.Title}");
Console.WriteLine(lines.First());   // Output: Ava studies Computer Science
'''),
    h2("Aggregate, Zip, Take, Skip, Distinct"),
    p("""`Aggregate` folds a whole sequence into a single value by repeatedly combining an accumulator with the next item. `Zip` pairs up two sequences item by item. `Take(n)` keeps the first n, `Skip(n)` drops the first n (together they make paging), and `Distinct` removes duplicates."""),
    code(r'''
int[] scores = students.Select(s => s.Score).ToArray();      // 92, 78, 85, 64, 88, 71
int total = scores.Aggregate(0, (sum, score) => sum + score);// 478
string names = students.Select(s => s.Name).Aggregate((acc, n) => acc + ", " + n);
// names: Ava, Ben, Cara, Dan, Eli, Fay

var pairs = students.Select(s => s.Name).Zip(scores, (n, sc) => $"{n}={sc}");
Console.WriteLine(string.Join(" ", pairs.Skip(2).Take(2)));  // Output: Cara=85 Dan=64
Console.WriteLine(string.Join(", ", students.Select(s => s.Course).Distinct())); // Output: CS, MATH, HIST
'''),
    note("""For the simple cases you do not need `Aggregate`: `Sum`, `Max`, and `string.Join` cover most of them. Reach for `Aggregate` when no ready-made method fits. Also look for `OrderBy(...).ThenBy(...)` for multi-level sorting and `MaxBy`/`MinBy` to find the whole item with the biggest or smallest property."""),
    h2("Deferred execution gotchas"),
    p("""Because queries are recipes that run when you enumerate them, three surprises catch people. First, a query sees the **current** value of any variable it captured, not the value when you wrote it. Second, a query that is enumerated twice does its work twice (expensive if it hits a file or database). Third, changing the source collection while looping over a query on it throws."""),
    code(r'''
int passMark = 80;
var passing = students.Where(s => s.Score >= passMark);
passMark = 90;                                   // changed AFTER the query was written
Console.WriteLine(passing.Count());              // Output: 1  (uses 90, not 80)

passMark = 80;
var frozen = students.Where(s => s.Score >= passMark).ToList();
passMark = 90;
Console.WriteLine(frozen.Count);                 // Output: 3  (ToList ran it at 80)
'''),
    tip("""Call `ToList()` or `ToArray()` when you want the results **now** and will use them more than once. `Count()`, `Sum()`, `First()`, `ToDictionary()`, and `Any()` also run immediately. Methods that return another sequence (`Where`, `Select`, `OrderBy`, `Take`, `Skip`, `Distinct`, `Zip`, `Join`, `GroupBy`) are the deferred ones."""),
    link("Read more on Microsoft Learn: Standard query operators", "https://learn.microsoft.com/en-us/dotnet/csharp/linq/standard-query-operators/"),
]

LINQ_PRACTICE_CODEALONG = codealong(
    "Code Along: Grouping, Joining, and Aggregating",
    "Type each step into one Program.cs in order. We use two small records and a list of students.",
    [
        step(
            "Declare the records",
            "Add these two records at the **bottom** of the file.",
            r'''
record Student(string Name, string Course, int Score);
record Course(string Code, string Title);
''',
            at="bottom",
        ),
        step(
            "Create data and group it",
            "Build the lists, then group students by course. Each group has a `Key` and can be counted and averaged. We sort groups by key for stable output.",
            r'''
var students = new List<Student>
{
    new("Ava", "CS", 92), new("Ben", "CS", 78), new("Cara", "MATH", 85),
    new("Dan", "MATH", 64), new("Eli", "CS", 88), new("Fay", "HIST", 71),
};
var courses = new List<Course>
{
    new("CS", "Computer Science"), new("MATH", "Mathematics"), new("HIST", "History"),
};

foreach (var grp in students.GroupBy(s => s.Course).OrderBy(g => g.Key))
{
    Console.WriteLine($"{grp.Key}: {grp.Count()} students, average {grp.Average(s => s.Score):F1}");
}
''',
        ),
        step(
            "ToDictionary and Join",
            "Build a lookup table from names to scores, then join students with their course titles.",
            r'''
Dictionary<string, int> scoreByName = students.ToDictionary(s => s.Name, s => s.Score);
Console.WriteLine($"Cara scored {scoreByName["Cara"]}");

var joined = students.Join(courses, s => s.Course, c => c.Code,
    (s, c) => $"{s.Name} studies {c.Title}");
foreach (string line in joined.Take(3))
{
    Console.WriteLine(line);
}
''',
        ),
        step(
            "Aggregate, Zip, Skip, Take, Distinct",
            "Fold the scores into one total, zip names with scores, page through the pairs, and list the distinct courses in first-seen order.",
            r'''
int[] scores = students.Select(s => s.Score).ToArray();
int total = scores.Aggregate(0, (sum, score) => sum + score);
string allNames = students.Select(s => s.Name).Aggregate((acc, n) => acc + ", " + n);
Console.WriteLine($"Total: {total}");
Console.WriteLine($"Names: {allNames}");

var pairs = students.Select(s => s.Name).Zip(scores, (n, sc) => $"{n}={sc}");
Console.WriteLine($"Skip 2, take 2: {string.Join(" ", pairs.Skip(2).Take(2))}");
Console.WriteLine($"Courses: {string.Join(", ", students.Select(s => s.Course).Distinct())}");
''',
        ),
        step(
            "Watch a deferred-execution gotcha",
            "The first query reads `passMark` when it runs, not when it was written. `ToList()` freezes the answer at that moment.",
            r'''
int passMark = 80;
var passing = students.Where(s => s.Score >= passMark);
passMark = 90;
Console.WriteLine($"Passing at 90: {passing.Count()}");

passMark = 80;
var frozen = students.Where(s => s.Score >= passMark).ToList();
passMark = 90;
Console.WriteLine($"Frozen at 80: {frozen.Count}");
''',
        ),
    ],
)

LINQ_PRACTICE_LAB = lab(
    "Lab: Sales Analysis",
    "Intermediate",
    "Analyze a list of sales records with GroupBy, ToDictionary, Join, Distinct, Take, and Aggregate. Use the exact data below.",
    [
        "Declare `record Sale(string Rep, string Region, decimal Amount);` and `record Manager(string Region, string Name);` at the bottom of the file",
        "Create `List<Sale>` in this order: (Ana, North, 120.00m), (Raj, South, 80.50m), (Ana, North, 45.25m), (Mei, East, 200.00m), (Raj, South, 19.50m), (Mei, East, 50.00m), (Tom, North, 10.00m). Create managers: (North, Lee), (South, Kim), (East, Ori)",
        "Group sales by Region, order the groups by key, and print `Region: total` for each with the total formatted with `:F2` (for example `East: 250.00`)",
        "Print `Reps: ` followed by the distinct rep names in first-seen order, joined by `, `. Then print `Top 2: ` followed by the two largest sale amounts (largest first, each formatted with `F2`), joined by `, `",
        "Use `GroupBy` + `ToDictionary` to build a `Dictionary<string, decimal>` of total amount per rep, and print `Raj total: ` with Raj's total formatted `F2`",
        "Join sales to managers on Region. For each result build the text `<Rep> reports to <Manager>`, remove duplicates with `Distinct`, and print each on its own line. Finally use `Aggregate` (starting from `0m`) to compute the grand total and print `Grand total: ` formatted `F2`",
    ],
    """
East: 250.00
North: 175.25
South: 100.00
Reps: Ana, Raj, Mei, Tom
Top 2: 200.00, 120.00
Raj total: 100.00
Ana reports to Lee
Raj reports to Kim
Mei reports to Ori
Tom reports to Lee
Grand total: 525.25
""",
    "For totals per rep: `sales.GroupBy(s => s.Rep).ToDictionary(g => g.Key, g => g.Sum(s => s.Amount))`. `Join` keeps the order of the first list, and `Distinct` keeps first occurrences. For the grand total: `sales.Aggregate(0m, (sum, s) => sum + s.Amount)`.",
)

LINQ_PRACTICE_SOLUTION = r'''
var sales = new List<Sale>
{
    new("Ana", "North", 120.00m),
    new("Raj", "South", 80.50m),
    new("Ana", "North", 45.25m),
    new("Mei", "East", 200.00m),
    new("Raj", "South", 19.50m),
    new("Mei", "East", 50.00m),
    new("Tom", "North", 10.00m),
};
var managers = new List<Manager>
{
    new("North", "Lee"),
    new("South", "Kim"),
    new("East", "Ori"),
};

foreach (var grp in sales.GroupBy(s => s.Region).OrderBy(g => g.Key))
{
    Console.WriteLine($"{grp.Key}: {grp.Sum(s => s.Amount):F2}");
}

Console.WriteLine($"Reps: {string.Join(", ", sales.Select(s => s.Rep).Distinct())}");
var top = sales.OrderByDescending(s => s.Amount).Take(2).Select(s => s.Amount.ToString("F2"));
Console.WriteLine($"Top 2: {string.Join(", ", top)}");

Dictionary<string, decimal> totals = sales.GroupBy(s => s.Rep).ToDictionary(g => g.Key, g => g.Sum(s => s.Amount));
Console.WriteLine($"Raj total: {totals["Raj"]:F2}");

var reports = sales.Join(managers, s => s.Region, m => m.Region, (s, m) => $"{s.Rep} reports to {m.Name}").Distinct();
foreach (string line in reports)
{
    Console.WriteLine(line);
}

decimal grand = sales.Aggregate(0m, (sum, s) => sum + s.Amount);
Console.WriteLine($"Grand total: {grand:F2}");

record Sale(string Rep, string Region, decimal Amount);
record Manager(string Region, string Name);
'''

LESSONS = {
    (6, 1): lesson(
        subtitle="Store many values in one variable. You will create arrays and lists, pick items with indices and ranges, and sort and modify collections.",
        reading=ARRAYS_LISTS_READING,
        codealong=ARRAYS_LISTS_CODEALONG,
        lab=ARRAYS_LISTS_LAB,
    ),
    (6, 2): lesson(
        subtitle="Look things up by key with dictionaries, keep unique items with sets, and process items in order with queues and stacks, all with deterministic output.",
        reading=DICT_SETS_READING,
        codealong=DICT_SETS_CODEALONG,
        lab=DICT_SETS_LAB,
    ),
    (6, 3): lesson(
        subtitle="Write code once that works for many types. You will build generic methods and classes, constrain them with `where`, and understand why generics beat `object`.",
        reading=GENERICS_READING,
        codealong=GENERICS_CODEALONG,
        lab=GENERICS_LAB,
    ),
    (6, 4): lesson(
        subtitle="Query collections with LINQ: filter, transform, sort, and summarize in a few readable lines, and understand why queries run lazily.",
        reading=LINQ_BASICS_READING,
        codealong=LINQ_BASICS_CODEALONG,
        lab=LINQ_BASICS_LAB,
    ),
    (6, 5): lesson(
        subtitle="Group, join, and aggregate lists of records with LINQ, and avoid the classic deferred-execution surprises.",
        reading=LINQ_PRACTICE_READING,
        codealong=LINQ_PRACTICE_CODEALONG,
        lab=LINQ_PRACTICE_LAB,
    ),
}

# Reference solutions, used only by verify_content.py (never sent to the learner).
SOLUTIONS = {
    (6, 1): ARRAYS_LISTS_SOLUTION,
    (6, 2): DICT_SETS_SOLUTION,
    (6, 3): GENERICS_SOLUTION,
    (6, 4): LINQ_BASICS_SOLUTION,
    (6, 5): LINQ_PRACTICE_SOLUTION,
}
