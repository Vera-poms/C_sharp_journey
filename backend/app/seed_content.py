"""Course content loaded into Postgres on first start.

Reading blocks:   {type: p|h2|code|callout|link, ...}. Inline `code` and **bold**
                  are allowed in text fields and rendered by the frontend.
Code-along:       steps (title, body, code, at); learner code is run for real by the runner.
Lab:              requirements and expected_output; a submission passes when the
                  program's real output matches.
"""

import importlib

MODULES = [
    {
        "title": "C# and .NET Foundations",
        "description": "What C# is, the .NET ecosystem, Hello World, and the dotnet CLI",
        "lessons": [
            "What is C# and .NET?",
            "Installing the .NET SDK",
            "Your First Program",
            "The dotnet CLI",
        ],
    },
    {
        "title": "Variables, Types, and Operators",
        "description": "Built-in types, type conversion, string interpolation, nullable types",
        "lessons": [
            "Understanding Variables",
            "Built-in Data Types",
            "Type Conversion & Casting",
            "String Interpolation",
            "Operators & Expressions",
        ],
    },
    {
        "title": "Control Flow",
        "description": "Conditionals, loops, switch expressions, and basic error handling",
        "lessons": [
            "if, else, and Conditions",
            "switch Statements and Expressions",
            "for and foreach Loops",
            "while and do-while Loops",
            "Exceptions and try/catch",
        ],
    },
    {
        "title": "Methods and Program Structure",
        "description": "Defining methods, parameters, return types, overloading, namespaces",
        "lessons": [
            "Defining and Calling Methods",
            "Parameters and Return Values",
            "Method Overloading",
            "Namespaces and Top-level Statements",
        ],
    },
    {
        "title": "Object-Oriented Programming",
        "description": "Classes, inheritance, polymorphism, interfaces, records",
        "lessons": [
            "Classes and Objects",
            "Properties and Constructors",
            "Inheritance",
            "Polymorphism",
            "Interfaces",
            "Records",
        ],
    },
    {
        "title": "Collections, Generics, and LINQ",
        "description": "Lists, dictionaries, generic types, LINQ queries",
        "lessons": [
            "Arrays and Lists",
            "Dictionaries and Sets",
            "Generics",
            "LINQ Basics",
            "LINQ in Practice",
        ],
    },
    {
        "title": "Intermediate C# Patterns",
        "description": "Delegates, events, async/await, file I/O, JSON serialization",
        "lessons": [
            "Delegates and Events",
            "async and await",
            "File I/O",
            "JSON Serialization",
        ],
    },
    {
        "title": "Desktop App Development",
        "description": "WPF or .NET MAUI, XAML, data binding, MVVM, building a full app",
        "lessons": [
            "Choosing WPF or .NET MAUI",
            "XAML Layout",
            "Data Binding",
            "The MVVM Pattern",
            "Building a Full App",
        ],
    },
]

COMING_SOON = [{"type": "p", "text": "This lesson's content is coming soon."}]

# (module number, lesson number) -> content overrides. Lessons are written per module in
# content_m<N>.py and checked by backend/verify_content.py.
RICH_LESSONS: dict = {}
for _n in range(1, 9):
    try:
        RICH_LESSONS.update(importlib.import_module(f".content_m{_n}", __package__).LESSONS)
    except ModuleNotFoundError:
        pass
