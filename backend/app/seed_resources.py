"""Per-lesson videos and external resources (Microsoft Learn + W3Schools).

Keyed by (module number, lesson number). Videos come from the official .NET
"C# for Beginners" series on YouTube and are embedded in the Video tab.
Resource entries are {source, text, href}.
"""

MS = "Microsoft Learn"
W3 = "W3Schools"
YT = "YouTube"

_MS = "https://learn.microsoft.com/en-us/dotnet/csharp"
_W3 = "https://www.w3schools.com/cs"


def ms(text: str, path: str) -> dict:
    return {"source": MS, "text": text, "href": f"{_MS}/{path}"}


def w3(text: str, page: str) -> dict:
    return {"source": W3, "text": text, "href": f"{_W3}/{page}.php"}


def video(youtube_id: str, title: str, duration: str) -> dict:
    return {
        "youtube_id": youtube_id,
        "title": title,
        "duration": duration,
        "provider": "dotnet on YouTube",
        "url": f"https://www.youtube.com/watch?v={youtube_id}",
    }


SERIES = {
    "source": YT,
    "text": "C# for Beginners — full playlist (Scott Hanselman & David Fowler)",
    "href": "https://www.youtube.com/watch?v=Z5JS36NlJiU",
}

RESOURCES = {
    (1, 1): [
        ms("A tour of C#", "tour-of-csharp/"),
        w3("C# Introduction", "cs_intro"),
        {"source": MS, "text": "What is .NET?", "href": "https://learn.microsoft.com/en-us/dotnet/core/introduction"},
    ],
    (1, 2): [
        {"source": MS, "text": "Install .NET on Windows", "href": "https://learn.microsoft.com/en-us/dotnet/core/install/windows"},
        w3("C# Get Started", "cs_getstarted"),
    ],
    (1, 3): [
        ms("Hello World — your first program", "tour-of-csharp/tutorials/hello-world"),
        w3("C# Syntax", "cs_syntax"),
        w3("C# Output", "cs_output"),
        w3("C# Comments", "cs_comments"),
    ],
    (1, 4): [
        {"source": MS, "text": ".NET CLI overview", "href": "https://learn.microsoft.com/en-us/dotnet/core/tools/"},
        {"source": MS, "text": "dotnet run", "href": "https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-run"},
    ],
    (2, 1): [
        ms("Declaring variables", "fundamentals/coding-style/identifier-names"),
        w3("C# Variables", "cs_variables"),
        w3("C# User Input", "cs_user_input"),
    ],
    (2, 2): [
        ms("Built-in types", "language-reference/builtin-types/built-in-types"),
        ms("The C# type system", "fundamentals/types/"),
        w3("C# Data Types", "cs_data_types"),
        w3("C# Booleans", "cs_booleans"),
    ],
    (2, 3): [
        ms("Casting and type conversions", "programming-guide/types/casting-and-type-conversions"),
        w3("C# Type Casting", "cs_type_casting"),
    ],
    (2, 4): [
        ms("String interpolation", "tutorials/string-interpolation"),
        w3("C# Strings", "cs_strings"),
        w3("C# String Interpolation", "cs_strings_interpol"),
    ],
    (2, 5): [
        ms("Arithmetic operators", "language-reference/operators/arithmetic-operators"),
        w3("C# Operators", "cs_operators"),
        w3("C# Math", "cs_math"),
    ],
    (3, 1): [
        ms("Selection statements: if and switch", "language-reference/statements/selection-statements"),
        w3("C# Conditions", "cs_conditions"),
        w3("C# Else If", "cs_conditions_elseif"),
    ],
    (3, 2): [
        ms("The switch expression", "language-reference/operators/switch-expression"),
        w3("C# Switch", "cs_switch"),
    ],
    (3, 3): [
        ms("Iteration statements", "language-reference/statements/iteration-statements"),
        w3("C# For Loop", "cs_for_loop"),
        w3("C# Foreach Loop", "cs_foreach_loop"),
        w3("C# Break/Continue", "cs_break"),
    ],
    (3, 4): [
        ms("Iteration statements", "language-reference/statements/iteration-statements"),
        w3("C# While and Do/While Loops", "cs_while_loop"),
    ],
    (3, 5): [
        ms("Exception handling", "fundamentals/exceptions/"),
        w3("C# Exceptions", "cs_exceptions"),
    ],
    (4, 1): [
        ms("Methods", "programming-guide/classes-and-structs/methods"),
        w3("C# Methods", "cs_methods"),
    ],
    (4, 2): [
        w3("C# Method Parameters", "cs_method_parameters"),
        ms("Passing parameters", "language-reference/keywords/method-parameters"),
    ],
    (4, 3): [
        w3("C# Method Overloading", "cs_method_overloading"),
    ],
    (4, 4): [
        ms("Top-level statements", "fundamentals/program-structure/top-level-statements"),
        ms("Namespaces", "fundamentals/types/namespaces"),
    ],
    (5, 1): [
        ms("Classes", "fundamentals/types/classes"),
        w3("C# OOP", "cs_oop"),
        w3("C# Classes and Objects", "cs_classes"),
    ],
    (5, 2): [
        ms("Properties", "programming-guide/classes-and-structs/properties"),
        w3("C# Constructors", "cs_constructors"),
        w3("C# Properties", "cs_properties"),
    ],
    (5, 3): [
        ms("Inheritance", "fundamentals/object-oriented/inheritance"),
        w3("C# Inheritance", "cs_inheritance"),
    ],
    (5, 4): [
        ms("Polymorphism", "fundamentals/object-oriented/polymorphism"),
        w3("C# Polymorphism", "cs_polymorphism"),
    ],
    (5, 5): [
        ms("Interfaces", "fundamentals/types/interfaces"),
        w3("C# Interface", "cs_interface"),
    ],
    (5, 6): [
        ms("Records", "fundamentals/types/records"),
    ],
    (6, 1): [
        {"source": MS, "text": "Collections in .NET", "href": "https://learn.microsoft.com/en-us/dotnet/standard/collections/"},
        w3("C# Arrays", "cs_arrays"),
        w3("C# Array Sorting", "cs_arrays_sort"),
    ],
    (6, 2): [
        {"source": MS, "text": "Dictionary<TKey,TValue>", "href": "https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.dictionary-2"},
        {"source": MS, "text": "HashSet<T>", "href": "https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.hashset-1"},
    ],
    (6, 3): [
        ms("Generics", "fundamentals/types/generics"),
    ],
    (6, 4): [
        ms("LINQ overview", "linq/"),
    ],
    (6, 5): [
        ms("LINQ query expressions", "linq/get-started/query-expression-basics"),
    ],
    (7, 1): [
        ms("Delegates", "programming-guide/delegates/"),
        ms("Events", "programming-guide/events/"),
    ],
    (7, 2): [
        ms("Asynchronous programming", "asynchronous-programming/"),
    ],
    (7, 3): [
        w3("C# Files", "cs_files"),
        {"source": MS, "text": "File and stream I/O", "href": "https://learn.microsoft.com/en-us/dotnet/standard/io/"},
    ],
    (7, 4): [
        {"source": MS, "text": "Serialize and deserialize JSON", "href": "https://learn.microsoft.com/en-us/dotnet/standard/serialization/system-text-json/overview"},
    ],
    (8, 1): [
        {"source": MS, "text": "Desktop guide for WPF", "href": "https://learn.microsoft.com/en-us/dotnet/desktop/wpf/"},
        {"source": MS, "text": ".NET MAUI documentation", "href": "https://learn.microsoft.com/en-us/dotnet/maui/"},
    ],
    (8, 2): [
        {"source": MS, "text": "XAML overview (WPF)", "href": "https://learn.microsoft.com/en-us/dotnet/desktop/wpf/xaml/"},
    ],
    (8, 3): [
        {"source": MS, "text": "Data binding overview (WPF)", "href": "https://learn.microsoft.com/en-us/dotnet/desktop/wpf/data/"},
    ],
    (8, 4): [
        {"source": MS, "text": "MVVM — Community Toolkit", "href": "https://learn.microsoft.com/en-us/dotnet/communitytoolkit/mvvm/"},
    ],
    (8, 5): [
        {"source": MS, "text": "Desktop guide for WPF", "href": "https://learn.microsoft.com/en-us/dotnet/desktop/wpf/"},
    ],
}

VIDEOS = {
    (1, 1): video("9THmGiSPjBQ", "What is C#? [Pt 1]", "2 min"),
    (1, 3): video("HFLALzkcjLM", "Hello World! [Pt 2]", "6 min"),
    (2, 1): video("lXheKhL6dDA", "Hello World, Introducing Strings! [Pt 4]", "5 min"),
    (2, 2): video("ZXCMBOxry8A", "Numbers, Integers, and Math [Pt 7]", "14 min"),
    (2, 3): video("Kg_k0vL0dD4", "Numbers, Precision, Casting, Doubles, and More [Pt 8]", "12 min"),
    (2, 4): video("nus5SP3AoHM", "The Basics of Strings! [Pt 5]", "10 min"),
    (3, 1): video("yH-ewL_u8w8", "Branching, Ifs, and Conditional Logic [Pt 9]", "14 min"),
    (3, 3): video("yuRdCZMuak0", "For Loops [Pt 11]", "11 min"),
    (3, 4): video("GLzAkJb0eoA", "Branching and While Loops [Pt 10]", "10 min"),
    (5, 1): video("Vp0vVzJgJ5g", "Object-oriented Programming (OOP) [Pt 18]", "17 min"),
    (6, 1): video("7PDNqmBdtrE", "Arrays, Lists, Indexing, and Foreach [Pt 13]", "11 min"),
    (6, 4): video("4ro5UCqU0P4", "Language Integrated Query (LINQ) and IEnumerable [Pt 15]", "11 min"),
}


def resources_for(key: tuple[int, int]) -> list[dict]:
    return [*RESOURCES.get(key, []), SERIES]
