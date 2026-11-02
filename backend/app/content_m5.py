"""Module 5: Object-Oriented Programming."""
from .lesson_kit import *  # noqa: F401,F403

# ─── 5.1 Classes and Objects ───

M51_READING = [
    h2("Why classes exist"),
    p("So far your programs have used separate variables and methods. That works for small programs, but imagine tracking a hundred players in a game: each one has a name, a score, and some health, and there are rules for changing those values. Keeping `name1`, `score1`, `name2`, `score2` and so on would be a mess. A **class** lets you bundle data and the behavior that works on that data into one named unit."),
    p("Think of a class as a **blueprint**. A blueprint for a house describes rooms and doors, but you can't live in a blueprint. An **object** (also called an **instance**) is a real house built from it. You can build many houses from one blueprint, and each has its own paint color."),
    h2("Declaring a class"),
    p("A class contains **fields** (variables that store data) and **methods** (code that acts on that data). Members declared inside a class are written once and shared by every object of that class, but each object gets its own copy of the field values."),
    code(r"""
class Car
{
    public string Model = "Unknown";   // a field
    public int Speed;                  // a field (defaults to 0)

    public void Accelerate(int amount) // a method
    {
        Speed += amount;
    }

    public string Describe()
    {
        return $"{Model} at {Speed} km/h";
    }
}
"""),
    note("By convention a class name is **PascalCase** (`Car`, `BankAccount`). A class declaration is a type declaration, so in a file that also uses top-level statements it must go **below** the statements, never above them."),
    h2("Creating objects with new"),
    p("Declaring a class creates no objects. You build one with the `new` keyword, which allocates memory for the object and gives you a **reference** to it. You then reach its members with the dot operator."),
    code(r"""
Car roadster = new Car();
roadster.Model = "Roadster";
roadster.Accelerate(30);
Console.WriteLine(roadster.Describe());
// Output: Roadster at 30 km/h

Car truck = new Car();          // a second, independent object
truck.Model = "Truck";
Console.WriteLine(truck.Describe());
// Output: Truck at 0 km/h

var coupe = new Car();          // var works fine when the type is obvious
Car sedan = new();              // target-typed new: the type comes from the left side
"""),
    p("Notice that `roadster` and `truck` are separate. Calling `Accelerate` on one never changes the other, because each object owns its own `Speed` field."),
    h2("References versus values"),
    p("This is the most important idea in the lesson. Built-in types like `int`, `double`, and `bool` are **value types**: the variable holds the value itself. A class is a **reference type**: the variable holds a *reference* (think of it as an address or a remote control), and the object lives elsewhere in memory."),
    code(r"""
int a = 1;
int b = a;      // copies the value
b = 99;
Console.WriteLine($"{a} {b}");
// Output: 1 99

Car first = new Car();
Car second = first;   // copies the REFERENCE, not the object
second.Model = "Shared";
Console.WriteLine(first.Model);
// Output: Shared   (both variables point to the same object)

Console.WriteLine(first == second);
// Output: True    (for plain classes == asks: are these the same object?)
"""),
    warn("**Common mistake:** assuming that `Car second = first;` makes a copy. It doesn't; it gives you a second remote control for the same television. If you want an independent object, create one with `new` and copy the fields you need."),
    p("A reference variable can also hold the special value `null`, meaning it points at nothing. Calling a member on `null` crashes with a `NullReferenceException`. Because Nullable reference types are enabled in this course, the compiler warns you when you try to assign `null` to a type that isn't declared nullable (`Car?`)."),
    h2("Access modifiers"),
    p("Access modifiers decide who may touch a member. `public` means anyone can use it. `private` means only code inside the same class can. Members without a modifier are **private by default**, but writing the modifier explicitly makes your intent clear. (You'll meet `protected` in the inheritance lesson.)"),
    code(r"""
class Wallet
{
    private int _coins;                 // hidden from the outside

    public void Add(int amount)         // the only way to change it
    {
        if (amount > 0)
        {
            _coins += amount;
        }
    }

    public int GetCoins()
    {
        return _coins;
    }
}

// Wallet w = new Wallet();
// w._coins = 1_000_000;   // ERROR: '_coins' is inaccessible due to its protection level
"""),
    tip("Make fields `private` by default and expose behavior through public methods. That way the class controls its own rules (here: you can never add a negative amount). This idea is called **encapsulation**, and the next lesson shows the idiomatic C# way to do it with properties. A common style is to name private fields with a leading underscore, like `_coins`."),
    h2("Static members: belonging to the class itself"),
    p("Normally each object has its own fields. A `static` member instead belongs to the **class**, so there is exactly one copy no matter how many objects exist, and you reach it through the class name. You have already used static members: `Console.WriteLine` and `Math.Max` are static methods."),
    code(r"""
class Wallet
{
    public static int MaxCoins = 100;   // one copy shared by everything

    public static bool IsValidAmount(int amount)
    {
        return amount > 0 && amount <= MaxCoins;
    }
}

Console.WriteLine(Wallet.MaxCoins);            // Output: 100
Console.WriteLine(Wallet.IsValidAmount(250));  // Output: False
"""),
    note("A static method cannot use instance fields, because there is no particular object for it to look at. An instance method can use static members freely."),
    link("Read more on Microsoft Learn: Classes", "https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/classes"),
]

M51_CODEALONG = codealong(
    "Code Along: Your First Classes",
    "You'll build a small `Player` class and watch references behave. C# needs your top-level statements first and type declarations last, so some steps add code at the top of Program.cs and some at the bottom.",
    [
        step(
            "Declare the Player class",
            "Add this class at the **bottom** of Program.cs, below any other code. It has two fields and two methods.",
            r"""
class Player
{
    public string Name = "Unknown";
    public int Score;

    public void AddScore(int points)
    {
        Score += points;
    }

    public string Describe()
    {
        return $"{Name} has {Score} points";
    }
}
""",
            at="bottom",
        ),
        step(
            "Create two objects",
            "Go to the **top** of Program.cs and build two `Player` objects with `new`. Each one has its own `Name` and `Score`.",
            r"""
Player hero = new Player();
hero.Name = "Ada";
hero.AddScore(10);

Player rival = new Player();
rival.Name = "Linus";
rival.AddScore(7);

Console.WriteLine(hero.Describe());
Console.WriteLine(rival.Describe());
""",
        ),
        step(
            "References versus values",
            "Add this below your top-level code. Changing the object through `alias` also changes what `hero` sees, but copying an `int` does not link the two variables.",
            r"""
Player alias = hero;
alias.AddScore(5);
Console.WriteLine(hero.Describe());
Console.WriteLine($"alias is hero? {alias == hero}");
Console.WriteLine($"alias is rival? {alias == rival}");

int a = 1;
int b = a;
b = 99;
Console.WriteLine($"a = {a}, b = {b}");
""",
        ),
        step(
            "Add a class with a private field and a static member",
            "Add this class at the **bottom** of Program.cs, below `Player`. Outside code can only change `_coins` through `Add`.",
            r"""
class Wallet
{
    public static int MaxCoins = 100;
    private int _coins;

    public void Add(int amount)
    {
        if (amount > 0 && _coins + amount <= MaxCoins)
        {
            _coins += amount;
        }
    }

    public int GetCoins()
    {
        return _coins;
    }
}
""",
            at="bottom",
        ),
        step(
            "Use the Wallet",
            "Add this at the **top** level, below the rest of your statements. The commented line shows what the compiler would reject.",
            r"""
Wallet wallet = new Wallet();
wallet.Add(60);
wallet.Add(60);   // rejected: it would pass MaxCoins
wallet.Add(-5);   // rejected: negative
Console.WriteLine($"Coins: {wallet.GetCoins()} of {Wallet.MaxCoins}");
// wallet._coins = 999;   // ERROR: _coins is private
""",
        ),
    ],
)

M51_LAB = lab(
    "Lab: Inventory Item",
    "Beginner",
    "Model a stock item with a class. The class guards its own data: stock can never exceed a shared maximum, and you can't remove more than you have. Put your top-level statements first and your class at the bottom of the file.",
    [
        "Declare a class `Item` with a public string field `Name` (initialized to an empty string) and a **private** int field `_quantity`.",
        "Add a public static int field `MaxQuantity` set to `50`.",
        "Add `public void AddStock(int amount)` that increases `_quantity` by `amount` but never lets it go above `Item.MaxQuantity` (cap it at the maximum).",
        "Add `public bool Remove(int amount)`: if `amount` is greater than `_quantity` return `false` and change nothing; otherwise subtract it and return `true`.",
        "Add `public string Describe()` returning `Name: quantity`, for example `Widget: 40`.",
        "In your top-level code: create `widget` (Name `Widget`), call `AddStock(30)` twice, and print `Describe()`. Print `Remove(10)`, then `Describe()`. Print `Remove(100)`, then `Describe()`. Then do `Item same = widget;`, call `same.Remove(5)`, and print `widget.Describe()`. Finally create `gadget` (Name `Gadget`) and print its `Describe()`.",
    ],
    "Widget: 50\nTrue\nWidget: 40\nFalse\nWidget: 40\nWidget: 35\nGadget: 0",
    "For the cap, think about `if (_quantity > MaxQuantity) _quantity = MaxQuantity;` after adding (or use `Math.Min`). Printing a bool with `Console.WriteLine(widget.Remove(10))` prints `True` or `False`. The `same` variable is a second reference to the same object, so `widget` sees the change.",
)

# ─── 5.2 Properties and Constructors ───

M52_READING = [
    h2("Why not just use public fields?"),
    p("In the last lesson you saw that public fields let anyone put any value into an object, including nonsense like a negative price. You could hide the field and write `GetPrice()` and `SetPrice()` methods, and plenty of languages do. C# has a nicer built-in feature for this: the **property**."),
    p("A property looks like a field to the code that uses it (`product.Price = 5;`), but behind the scenes it runs code, so the class stays in control. That control is called **encapsulation**: an object protects its own state and exposes a small, safe surface."),
    h2("Auto-implemented properties"),
    p("The simplest property is **auto-implemented**: you write `get` and `set` and the compiler creates a hidden field for you. It's the right choice whenever you don't need extra logic."),
    code(r"""
class Person
{
    public string Name { get; set; } = "";   // read and write, with a default value
    public int Age { get; set; }
}

var person = new Person();
person.Name = "Grace";
person.Age = 36;
Console.WriteLine($"{person.Name}, {person.Age}");
// Output: Grace, 36
"""),
    p("You can leave out `set` to get a **read-only** property (it can only be assigned in a constructor or initializer), or restrict it with `{ get; private set; }` so that only the class itself can change it."),
    h2("Properties with logic"),
    p("When you need validation, write the accessors yourself with a **backing field**. The `value` keyword inside `set` is whatever the caller assigned."),
    code(r"""
class Product
{
    private decimal _price;

    public decimal Price
    {
        get { return _price; }
        set
        {
            if (value < 0)
            {
                throw new ArgumentException("Price cannot be negative.");
            }
            _price = value;
        }
    }
}

var p = new Product();
p.Price = 19.99m;     // runs the set accessor
// p.Price = -1m;     // would throw ArgumentException
"""),
    note("Recent versions of C# add a `field` keyword (C# 14) so you can write `set { field = value.Trim(); }` without declaring the backing field yourself. The explicit backing field above works in every version and is worth understanding first."),
    h2("Computed properties, init, and required"),
    p("A property doesn't need to store anything. A **computed property** has only a getter that calculates its result from other data each time. The `=>` form is a short way to write a getter that returns one expression."),
    code(r"""
class Rectangle
{
    public double Width { get; set; }
    public double Height { get; set; }

    public double Area => Width * Height;     // computed, read-only
}

var r = new Rectangle { Width = 3, Height = 4 };
Console.WriteLine(r.Area);
// Output: 12
"""),
    p("Two modifiers make objects safer to create. An **init** accessor can be set only while the object is being created (in a constructor or object initializer) and never afterward. A **required** property must be set by the code that creates the object, or it won't compile."),
    code(r"""
class Book
{
    public required string Title { get; init; }   // must be supplied, then fixed
    public int Pages { get; init; } = 100;        // optional, defaults to 100
}

var book = new Book { Title = "C# Basics", Pages = 320 };
// book.Title = "Other";      // ERROR: init-only property
// var empty = new Book();    // ERROR: required member 'Title' must be set
"""),
    h2("Constructors"),
    p("A **constructor** is a special method that runs when you write `new`. It has the same name as the class and no return type. Its job is to put the new object into a valid state. If you write no constructor at all, C# gives you an empty one, which is why `new Player()` worked last lesson."),
    code(r"""
class Account
{
    public string Owner { get; }
    public decimal Balance { get; private set; }

    public Account(string owner, decimal openingBalance)
    {
        this.Owner = owner;
        this.Balance = openingBalance;
    }

    public Account(string owner) : this(owner, 0m)   // overload that reuses the first one
    {
    }
}

var a = new Account("Ada", 50m);
var b = new Account("Linus");
Console.WriteLine($"{a.Owner}: {a.Balance}, {b.Owner}: {b.Balance}");
// Output: Ada: 50, Linus: 0
"""),
    p("Constructors can be **overloaded**, just like methods: same name, different parameters. The `: this(owner, 0m)` after the second constructor makes it call the first one, so the setup logic lives in one place."),
    h2("The this keyword"),
    p("Inside an instance member, `this` means the object the code is running on. You usually don't need it, but it is required when a parameter has the same name as a member and you want to tell them apart, as in `this.name = name;`. It also lets you pass the current object to something else."),
    h2("Primary constructors and object initializers"),
    p("C# 12 added **primary constructors** for classes: put the parameters right after the class name and they are available throughout the class body. They're a compact way to capture values."),
    code(r"""
class Circle(double radius)
{
    public double Radius { get; } = radius;           // initialize a property from the parameter
    public double Area => Math.PI * Radius * Radius;
}

var c = new Circle(2);
Console.WriteLine($"{c.Area:F2}");
// Output: 12.57
"""),
    p("An **object initializer** lets you set accessible properties right after `new`, inside braces: `new Person { Name = \"Grace\", Age = 36 }`. It's tidy when a class has many optional settings, and it works together with `init` and `required`."),
    warn("**Common mistake:** with a primary constructor, the parameter is not automatically a property. `class Circle(double radius)` does not give you `circle.radius`. You must write something like `public double Radius { get; } = radius;` to expose it."),
    tip("Choose the lightest tool that works: auto property for plain data, `init`/`required` for data that shouldn't change after creation, a full property only when you must validate or transform, and a constructor when an object can't be valid without certain values."),
    link("Read more on Microsoft Learn: Properties", "https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/properties"),
]

M52_CODEALONG = codealong(
    "Code Along: Properties and Constructors",
    "You'll build a `Product` with a validated property and two constructors, then try primary constructors and `required`/`init`. Class declarations go at the **bottom** of the file; the code that uses them goes at the top.",
    [
        step(
            "Declare Product",
            "Add this class at the **bottom** of Program.cs. It has a read-only-after-creation name, a validated price, a computed property, and two constructors.",
            r"""
class Product
{
    private decimal _price;

    public string Name { get; init; }

    public decimal Price
    {
        get { return _price; }
        set
        {
            if (value < 0)
            {
                throw new ArgumentException("Price cannot be negative.");
            }
            _price = value;
        }
    }

    public decimal PriceWithTax => Price * 1.10m;

    public Product(string name, decimal price)
    {
        this.Name = name;
        this.Price = price;
    }

    public Product(string name) : this(name, 0m)
    {
    }
}
""",
            at="bottom",
        ),
        step(
            "Create products with both constructors",
            "At the **top** of Program.cs, create one product with each constructor and print the properties, including the computed one.",
            r"""
var laptop = new Product("Laptop", 1000m);
Console.WriteLine($"{laptop.Name}: {laptop.Price:C} (with tax {laptop.PriceWithTax:C})");

var sticker = new Product("Sticker");
Console.WriteLine($"{sticker.Name}: {sticker.Price:C}");
""",
        ),
        step(
            "Watch validation work",
            "Add this below your earlier top-level code. The setter throws for a negative price, so wrap the assignment in `try/catch` and confirm the old value survives.",
            r"""
try
{
    laptop.Price = -5m;
}
catch (ArgumentException ex)
{
    Console.WriteLine($"Rejected: {ex.Message}");
}
Console.WriteLine($"Still {laptop.Price:C}");
""",
        ),
        step(
            "Primary constructor, required and init",
            "Add these two classes at the **bottom** of Program.cs, under `Product`.",
            r"""
class Circle(double radius)
{
    public double Radius { get; } = radius;
    public double Area => Math.PI * Radius * Radius;
}

class Book
{
    public required string Title { get; init; }
    public int Pages { get; init; } = 100;
}
""",
            at="bottom",
        ),
        step(
            "Use object initializers",
            "Add this at the **top** level, below your other statements. Try uncommenting the two ERROR lines to see the compiler messages, then comment them out again.",
            r"""
var circle = new Circle(2);
Console.WriteLine($"Radius {circle.Radius}, area {circle.Area:F2}");

var book = new Book { Title = "C# Basics", Pages = 320 };
var draft = new Book { Title = "Draft" };
Console.WriteLine($"{book.Title}: {book.Pages} pages");
Console.WriteLine($"{draft.Title}: {draft.Pages} pages");
// book.Title = "Other";     // ERROR: init-only property
// var empty = new Book();   // ERROR: required member 'Title' must be set
""",
        ),
    ],
)

M52_LAB = lab(
    "Lab: Thermostat",
    "Beginner",
    "Build a `Thermostat` class that protects its own temperature range, offers two constructors, and exposes a computed Fahrenheit value. Remember: top-level statements first, class at the bottom.",
    [
        "Declare class `Thermostat` with a read-only property `public string Room { get; }` and a private int backing field `_target`.",
        "Add a property `public int Target` whose setter clamps the value into the range 10 to 30 (use `Math.Clamp(value, 10, 30)`), storing the result in `_target`; the getter returns `_target`.",
        "Add a computed read-only property `public int Fahrenheit => Target * 9 / 5 + 32;`.",
        "Add constructor `Thermostat(string room)` that sets `Room` and sets `Target` to `20`, and constructor `Thermostat(string room, int target)` that chains to the first one with `: this(room)` and then assigns `Target = target`.",
        "Add `public string Describe()` returning `Room: TargetC / FahrenheitF`, for example `Lobby: 20C / 68F`.",
        "In top-level code: create `lobby` as `new Thermostat(\"Lobby\")` and `office` as `new Thermostat(\"Office\", 25)` and print both `Describe()` results. Then set `lobby.Target = 5` and print `lobby.Describe()`, then set `lobby.Target = 99` and print `lobby.Describe()` again.",
    ],
    "Lobby: 20C / 68F\nOffice: 25C / 77F\nLobby: 10C / 50F\nLobby: 30C / 86F",
    "The setter body is one line: `_target = Math.Clamp(value, 10, 30);`. Because the second constructor starts with `: this(room)`, the target is 20 first and is then overwritten by your `target` argument, and that assignment goes through the setter, so it is clamped too.",
)

# ─── 5.3 Inheritance ───

M53_READING = [
    h2("Sharing code between related types"),
    p("Suppose you model a `Dog` and a `Cat`. Both have a name, both can eat, both can make a sound. Copying that code into each class means every bug fix has to be made twice. **Inheritance** lets one class (the **derived** or child class) automatically receive everything from another (the **base** or parent class) and then add or change what makes it special."),
    p("Use inheritance when the relationship reads naturally as **is-a**: a dog *is an* animal. If it reads as *has-a* (a car *has an* engine), you want an ordinary field or property instead, not inheritance."),
    h2("Base and derived classes"),
    p("You write the base class after a colon. The derived class gets all the base class's accessible members for free."),
    code(r"""
class Animal
{
    public string Name { get; }

    public Animal(string name)
    {
        Name = name;
    }

    public void Eat()
    {
        Console.WriteLine($"{Name} is eating.");
    }
}

class Dog : Animal          // Dog IS an Animal
{
    public Dog(string name) : base(name)   // pass the name up to Animal's constructor
    {
    }

    public void Fetch()
    {
        Console.WriteLine($"{Name} fetches the ball.");
    }
}

var rex = new Dog("Rex");
rex.Eat();     // inherited from Animal
rex.Fetch();   // defined in Dog
// Output: Rex is eating.
// Output: Rex fetches the ball.
"""),
    p("A derived class must make sure its base part is built first. That's what `: base(name)` does: it calls a constructor of the base class. If the base class has no parameterless constructor and you forget this call, the compiler stops you."),
    warn("**Common mistake:** forgetting `: base(...)`. If `Animal` only has a constructor that takes a name, then `public Dog(string name) { }` fails to compile with an error saying there is no argument that corresponds to the required parameter of `Animal`. Pass the arguments up explicitly."),
    h2("protected: visible to the family"),
    p("`private` members are hidden even from derived classes. `protected` sits in between: visible inside the class and in classes derived from it, but not to the outside world."),
    code(r"""
class Animal
{
    protected int Energy = 10;       // derived classes may use it
}

class Dog : Animal
{
    public void Run()
    {
        Energy -= 3;                 // OK: inside a derived class
    }
}

// var d = new Dog();
// d.Energy = 100;                   // ERROR: protected, not accessible from outside
"""),
    h2("Changing inherited behavior: virtual and override"),
    p("Sometimes a derived class wants its own version of an inherited method. The base class opts in by marking the method `virtual`, and the derived class replaces it with `override`. Inside the override, `base.Method()` still calls the original version."),
    code(r"""
class Animal
{
    public virtual string Speak()
    {
        return "Some generic sound";
    }
}

class Dog : Animal
{
    public override string Speak()
    {
        return "Woof!";
    }
}

class Puppy : Dog
{
    public override string Speak()
    {
        return base.Speak() + " (squeaky)";   // reuse the parent's version
    }
}

Console.WriteLine(new Animal().Speak());   // Output: Some generic sound
Console.WriteLine(new Dog().Speak());      // Output: Woof!
Console.WriteLine(new Puppy().Speak());    // Output: Woof! (squeaky)
"""),
    warn("**Common mistake:** writing a method with the same name in a derived class but leaving out `override` (or leaving out `virtual` in the base). The compiler warns that you are *hiding* the inherited member. Hiding behaves differently from overriding and almost never does what you wanted, so treat that warning as an error."),
    h2("sealed: closing the family"),
    p("Put `sealed` on a class to forbid anyone from deriving from it, or on an override to stop further overriding. Use it when a class wasn't designed to be extended. Many built-in classes, including `string`, are sealed."),
    code(r"""
sealed class Puppy : Dog
{
    public override string Speak() { return "Yip!"; }
}

// class TinyPuppy : Puppy { }   // ERROR: cannot derive from sealed type 'Puppy'
"""),
    h2("object: the root of everything"),
    p("In C#, every type ultimately derives from `System.Object`, written `object`. If you declare a class with no base class, it inherits from `object`. That is why every value you create has methods like `ToString()`, `Equals()`, `GetHashCode()`, and `GetType()`. C# allows only **one** base class, but the chain can be as long as you like (Puppy, then Dog, then Animal, then object)."),
    h2("Checking types: is and as"),
    p("A `Dog` variable can hold a `Dog` or anything derived from `Dog`. A variable of type `Animal` can hold any animal, but then you can only call `Animal` members on it. To find out what an object really is, use `is`. The pattern form `is Dog d` tests and gives you a correctly typed variable in one go. The `as` operator tries a conversion and gives `null` instead of throwing when it doesn't fit."),
    code(r"""
Animal pet = new Dog("Rex");

Console.WriteLine(pet is Dog);        // Output: True
Console.WriteLine(pet is Animal);     // Output: True   (a Dog is an Animal)

if (pet is Dog dog)
{
    dog.Fetch();                      // now typed as Dog
}

Dog? maybe = pet as Dog;              // Dog or null
Console.WriteLine(maybe is not null); // Output: True
Console.WriteLine(pet.GetType().Name);// Output: Dog  (the real type, not Animal)
"""),
    tip("Prefer composition over inheritance when in doubt. Deep inheritance trees are hard to change because each level depends on the ones above it. Inherit when there is a true is-a relationship and real shared behavior."),
    link("Read more on Microsoft Learn: Inheritance", "https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/object-oriented/inheritance"),
]

M53_CODEALONG = codealong(
    "Code Along: An Animal Hierarchy",
    "You'll build `Animal`, `Dog`, and a sealed `Puppy`, and test them with `is` and `as`. The classes all go at the **bottom** of Program.cs and the code that uses them goes at the top.",
    [
        step(
            "The base class",
            "Add `Animal` at the **bottom** of Program.cs. Note the `protected` field and the `virtual` method.",
            r"""
class Animal
{
    protected int Energy = 10;

    public string Name { get; }

    public int EnergyLevel => Energy;

    public Animal(string name)
    {
        Name = name;
    }

    public virtual string Speak()
    {
        return $"{Name} makes a sound.";
    }

    public void Eat()
    {
        Energy += 5;
    }
}
""",
            at="bottom",
        ),
        step(
            "Derived classes",
            "Add `Dog` and `Puppy` at the **bottom** of Program.cs, below `Animal`. They call `base(name)` and override `Speak`.",
            r"""
class Dog : Animal
{
    public Dog(string name) : base(name)
    {
    }

    public override string Speak()
    {
        return $"{Name} says Woof!";
    }

    public void Fetch()
    {
        Energy -= 3;
    }
}

sealed class Puppy : Dog
{
    public Puppy(string name) : base(name)
    {
    }

    public override string Speak()
    {
        return base.Speak() + " (squeaky)";
    }
}
""",
            at="bottom",
        ),
        step(
            "Create and compare",
            "At the **top** of Program.cs, create a plain `Animal` and a `Dog` and see how `Speak` differs.",
            r"""
var generic = new Animal("Creature");
var dog = new Dog("Rex");
Console.WriteLine(generic.Speak());
Console.WriteLine(dog.Speak());
""",
        ),
        step(
            "Use inherited and protected members",
            "Add this below your other top-level code. `Eat` is inherited, `Fetch` changes the protected `Energy`, and outside code can only read it through `EnergyLevel`.",
            r"""
dog.Eat();
dog.Fetch();
Console.WriteLine($"Energy: {dog.EnergyLevel}");
// dog.Energy = 100;   // ERROR: 'Animal.Energy' is inaccessible (protected)
""",
        ),
        step(
            "Test types with is and as",
            "Add this below the rest of your top-level code. The variable's declared type is `Animal`, but the object is a `Puppy`.",
            r"""
Animal pet = new Puppy("Bit");
Console.WriteLine(pet.Speak());
Console.WriteLine(pet is Dog);
Console.WriteLine(generic is Dog);

Dog? asDog = pet as Dog;
Console.WriteLine(asDog is not null);

if (pet is Dog d)
{
    d.Fetch();
    Console.WriteLine($"Energy: {d.EnergyLevel}");
}

object root = pet;
Console.WriteLine(root.GetType().Name);
""",
        ),
    ],
)

M53_LAB = lab(
    "Lab: Vehicle Fleet",
    "Intermediate",
    "Build a small vehicle hierarchy that uses constructors with `base(...)`, a protected field, `virtual`/`override`, `sealed`, and type tests. Remember: top-level statements first, classes at the bottom.",
    [
        "Class `Vehicle` with a read-only property `public string Name { get; }`, a constructor `Vehicle(string name)`, a method `public virtual int WheelCount()` returning `4`, and a **non-virtual** method `public string Describe()` returning `Name has N wheels` (call `WheelCount()` for N), e.g. `Sedan has 4 wheels`.",
        "Class `Motorcycle : Vehicle` whose constructor passes the name to the base and which overrides `WheelCount()` to return `2`.",
        "Class `Truck : Vehicle` with a `protected int Axles` field, constructor `Truck(string name, int axles)` that calls `base(name)` and stores the axles, and an override of `WheelCount()` returning `Axles * 4`.",
        "A `sealed` class `DumpTruck : Truck` with constructor `DumpTruck(string name)` calling `base(name, 3)` and an override of `WheelCount()` returning `base.WheelCount() + 2`.",
        "In top-level code create `Vehicle[] fleet = [new Vehicle(\"Sedan\"), new Motorcycle(\"Ducati\"), new Truck(\"Hauler\", 2), new DumpTruck(\"Dumper\")];` and print each vehicle's `Describe()` with a `foreach`.",
        "Then with `Vehicle v = fleet[2];` print, each on its own line: `v is Truck`, `v is DumpTruck`, `(v as Motorcycle) is null`, `fleet[3] is Truck`, and `fleet[3].GetType().Name`.",
    ],
    "Sedan has 4 wheels\nDucati has 2 wheels\nHauler has 8 wheels\nDumper has 14 wheels\nTrue\nFalse\nTrue\nTrue\nDumpTruck",
    "`Describe()` calls `WheelCount()`, and because `WheelCount` is virtual, the version that runs depends on the real object type. For `DumpTruck`, `base.WheelCount()` runs `Truck`'s version: 3 axles times 4 is 12, plus 2 is 14. An array of `Vehicle` can hold every one of these classes.",
)

# ─── 5.4 Polymorphism ───

M54_READING = [
    h2("One call, many behaviors"),
    p("**Polymorphism** is a Greek word meaning many forms. In practice it means you can write code against a general type, such as `Shape`, and that code automatically does the right thing for every specific type, such as a circle or a rectangle. You don't write an `if` for every kind of shape; each shape knows how to do its own work."),
    p("It builds directly on the last lesson: a derived object can be used anywhere its base type is expected, and calls to `virtual` methods are resolved by the **real** type of the object at runtime, not by the type of the variable."),
    h2("Virtual and override in action"),
    code(r"""
class Animal
{
    public virtual string Speak()
    {
        return "...";
    }
}

class Dog : Animal
{
    public override string Speak()
    {
        return "Woof!";
    }
}

class Cat : Animal
{
    public override string Speak()
    {
        return "Meow!";
    }
}

Animal a = new Dog();   // variable type: Animal, real type: Dog
Console.WriteLine(a.Speak());
// Output: Woof!        (the Dog version runs)

a = new Cat();
Console.WriteLine(a.Speak());
// Output: Meow!
"""),
    p("The variable's declared type decides which members you are allowed to *call*. The object's real type decides which *version* runs. Keep those two ideas separate and polymorphism stops feeling magical."),
    h2("Collections of a base type"),
    p("The real payoff appears when you hold different objects in one collection. Here we use an **array**, which is a fixed-size, ordered group of values of one type, written `Animal[]`. (Module 6 covers arrays and the resizable `List<T>` in depth. A `List<Animal>` works the same way for this purpose.)"),
    code(r"""
Animal[] zoo = [new Dog(), new Cat(), new Dog()];

foreach (Animal animal in zoo)
{
    Console.WriteLine(animal.Speak());   // each object answers for itself
}
// Output: Woof!
// Output: Meow!
// Output: Woof!
"""),
    p("If you invent a `Cow` class tomorrow, this loop doesn't change at all. Code that is open to new types without being edited is a major reason object-oriented design is popular."),
    h2("Abstract classes and members"),
    p("Sometimes a base class is only an idea, not something you'd create on its own. What does a generic `Shape` look like? You can't draw one. Mark such a class `abstract` and the compiler forbids `new Shape()`. Inside it you may declare **abstract members**: methods or properties with no body that every concrete derived class **must** implement."),
    code(r"""
abstract class Shape
{
    public string Name { get; }

    protected Shape(string name)       // abstract classes can have constructors
    {
        Name = name;
    }

    public abstract double Area();     // no body: derived classes must supply one

    public string Describe()           // abstract classes can also have real, shared code
    {
        return $"{Name}: {Area():F1}";
    }
}

class Square : Shape
{
    private double _side;

    public Square(double side) : base("Square")
    {
        _side = side;
    }

    public override double Area()      // required
    {
        return _side * _side;
    }
}

// Shape s = new Shape("x");           // ERROR: cannot create an instance of an abstract class
Shape shape = new Square(3);
Console.WriteLine(shape.Describe());
// Output: Square: 9.0
"""),
    warn("**Common mistake:** deriving from an abstract class and forgetting to implement one of its abstract members. The compiler reports that your class does not implement the inherited abstract member, and you can't create objects of it until you do (or you mark your own class `abstract` too)."),
    h2("Overriding ToString"),
    p("Every object inherits `ToString()` from `object`. By default it returns just the type's name, which is rarely useful. Override it to give your class a readable text form. `Console.WriteLine(obj)` and string interpolation call `ToString()` for you, and debuggers use it too."),
    code(r"""
class Point
{
    public int X { get; }
    public int Y { get; }

    public Point(int x, int y)
    {
        X = x;
        Y = y;
    }

    public override string ToString()
    {
        return $"({X}, {Y})";
    }
}

var pt = new Point(3, 4);
Console.WriteLine(pt);               // Output: (3, 4)
Console.WriteLine($"Point is {pt}"); // Output: Point is (3, 4)
"""),
    note("If you leave `ToString()` alone on a class you wrote, printing it shows only the class name. That's the first sign you should add an override."),
    tip("Design question to ask: does this base class make sense on its own? If yes, make it a normal class with `virtual` methods that have sensible defaults. If no, make it `abstract` and let the compiler enforce that every subtype fills in the missing pieces."),
    link("Read more on Microsoft Learn: Polymorphism", "https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/object-oriented/polymorphism"),
]

M54_CODEALONG = codealong(
    "Code Along: Shapes",
    "You'll build an abstract `Shape` with concrete shapes and treat them all through the base type. As always, classes go at the **bottom** of Program.cs and the code that uses them goes at the top.",
    [
        step(
            "The abstract base class",
            "Add `Shape` at the **bottom** of Program.cs. `Area()` is abstract, and `ToString()` is overridden once for all shapes.",
            r"""
abstract class Shape
{
    public string Name { get; }

    protected Shape(string name)
    {
        Name = name;
    }

    public abstract double Area();

    public override string ToString()
    {
        return $"{Name} with area {Area():F2}";
    }
}
""",
            at="bottom",
        ),
        step(
            "Two concrete shapes",
            "Add these at the **bottom** of Program.cs, under `Shape`. Each one must override `Area()`.",
            r"""
class Circle : Shape
{
    private double _radius;

    public Circle(double radius) : base("Circle")
    {
        _radius = radius;
    }

    public override double Area()
    {
        return Math.PI * _radius * _radius;
    }
}

class Rectangle : Shape
{
    private double _width;
    private double _height;

    public Rectangle(double width, double height) : base("Rectangle")
    {
        _width = width;
        _height = height;
    }

    public override double Area()
    {
        return _width * _height;
    }
}
""",
            at="bottom",
        ),
        step(
            "Treat derived objects as the base type",
            "At the **top** of Program.cs, put different shapes in one `Shape[]` array and loop over it. `Console.WriteLine(shape)` calls your `ToString()` override.",
            r"""
Shape[] shapes = [new Circle(1.5), new Rectangle(3, 4)];

foreach (Shape shape in shapes)
{
    Console.WriteLine(shape);
}
// var oops = new Shape("x");   // ERROR: cannot create an instance of an abstract class
""",
        ),
        step(
            "Add a new shape without touching old code",
            "Add `Triangle` at the **bottom** of Program.cs.",
            r"""
class Triangle : Shape
{
    private double _width;
    private double _height;

    public Triangle(double width, double height) : base("Triangle")
    {
        _width = width;
        _height = height;
    }

    public override double Area()
    {
        return 0.5 * _width * _height;
    }
}
""",
            at="bottom",
        ),
        step(
            "Total the areas polymorphically",
            "Add this below your other top-level code. The loop only knows about `Shape`, yet it works with all three kinds.",
            r"""
Shape[] more = [new Circle(1.5), new Rectangle(3, 4), new Triangle(6, 5)];

double total = 0;
foreach (Shape s in more)
{
    total += s.Area();
}

Console.WriteLine($"Total area: {total:F2}");
Console.WriteLine(more[2]);
""",
        ),
    ],
)

M54_LAB = lab(
    "Lab: Payroll",
    "Intermediate",
    "Model different kinds of employees behind an abstract base class, then compute payroll by looping over one array of the base type. Remember: top-level statements first, classes at the bottom.",
    [
        "Declare `abstract class Employee` with a read-only `string Name` property, a protected constructor taking the name, `public abstract decimal MonthlyPay();`, and an override of `ToString()` returning `Name: pay` where pay is `MonthlyPay()` formatted with `:C`, e.g. `Alice: $5,000.00`.",
        "`SalariedEmployee : Employee` with constructor `(string name, decimal annualSalary)`; its `MonthlyPay()` returns the annual salary divided by `12`.",
        "`HourlyEmployee : Employee` with constructor `(string name, decimal rate, int hours)`; its `MonthlyPay()` returns `rate * hours`.",
        "`Manager : SalariedEmployee` with constructor `(string name, decimal annualSalary, decimal bonus)`; it overrides `MonthlyPay()` to return `base.MonthlyPay() + bonus`.",
        "In top-level code create `Employee[] staff = [new SalariedEmployee(\"Alice\", 60000m), new HourlyEmployee(\"Bob\", 25m, 160), new Manager(\"Carol\", 96000m, 500m)];`.",
        "Loop with `foreach`, printing each employee (`Console.WriteLine(e)`) and adding `e.MonthlyPay()` to a `decimal total`. After the loop print `Total payroll: ` followed by the total formatted with `:C`.",
    ],
    "Alice: $5,000.00\nBob: $4,000.00\nCarol: $8,500.00\nTotal payroll: $17,500.00",
    "`Manager` must be able to override `MonthlyPay`, which means `SalariedEmployee.MonthlyPay` is an `override` that is not `sealed`. Store the bonus in a private field. The abstract `Employee` can't be created with `new`, but the array's element type can still be `Employee`.",
)

# ─── 5.5 Interfaces ───

M55_READING = [
    h2("A contract without code"),
    p("An **interface** is a contract: a list of members that a type promises to provide, with no (or very little) implementation. It answers the question *what can this thing do?* without caring *what is it?* A `Duck`, a `Plane`, and a `Superhero` have nothing in common as a family, yet all of them can `Fly()`. An interface captures exactly that shared ability."),
    p("By convention, interface names start with a capital **I**, such as `IFlyable`, `IComparable`, or `IDisposable`. You'll recognize them instantly in the standard library."),
    h2("Declaring and implementing an interface"),
    code(r"""
interface IFlyable
{
    string Fly();                 // no body, no access modifier needed
}

class Duck : IFlyable             // the colon means 'implements'
{
    public string Fly()           // must be public and match the signature
    {
        return "Duck flaps and takes off";
    }
}

class Plane : IFlyable
{
    public string Fly()
    {
        return "Plane roars down the runway";
    }
}
"""),
    p("A class that lists an interface must implement **every** member of it, or the compiler reports an error. Members of an interface can be methods, properties, and a few other kinds, but not ordinary instance fields."),
    h2("Polymorphism through interfaces"),
    p("Because both classes promise `Fly()`, you can treat them uniformly through the interface type, exactly as you did with a base class."),
    code(r"""
IFlyable[] flyers = [new Duck(), new Plane()];

foreach (IFlyable f in flyers)
{
    Console.WriteLine(f.Fly());
}
// Output: Duck flaps and takes off
// Output: Plane roars down the runway
"""),
    p("A method that accepts `IFlyable` will work with any class written now or in the future, as long as it implements the interface. This is how large programs stay flexible: code depends on **contracts**, not on specific classes."),
    h2("Implementing several interfaces"),
    p("A class can inherit from only one base class, but it can implement **as many interfaces as it likes**. This is why interfaces are the tool for combining abilities."),
    code(r"""
interface ISwimmable
{
    string Swim();
}

class Duck : IFlyable, ISwimmable    // two contracts
{
    public string Fly()  { return "Duck flaps and takes off"; }
    public string Swim() { return "Duck paddles"; }
}

class Fish : ISwimmable              // only one
{
    public string Swim() { return "Fish glides"; }
}

object thing = new Duck();
if (thing is ISwimmable swimmer)     // ask: does it support this ability?
{
    Console.WriteLine(swimmer.Swim());
}
// Output: Duck paddles
"""),
    p("The `is` check works with interfaces just as it does with classes: it asks whether the object's real type implements that interface."),
    h2("Interface or abstract class?"),
    p("Both let you write code against something general. Choose with these rules of thumb. An **abstract class** models what something *is*, can hold fields and shared implementation, and a class can have only one. An **interface** models what something *can do*, is mostly a pure contract, and a class can implement many. If unrelated types need the same ability, use an interface. If related types share real code and state, use an abstract base class. Many designs use both."),
    h2("Default interface members"),
    p("Since C# 8 an interface member may include a **default implementation**. Implementing classes get that behavior for free and may skip it. This lets library authors add a member to an interface without breaking every existing class."),
    code(r"""
interface INotifier
{
    string Send(string message);

    string SendTwice(string message)        // default implementation
    {
        return Send(message) + " | " + Send(message);
    }
}

class Email : INotifier
{
    public string Send(string message)      // SendTwice is inherited from the interface
    {
        return $"[Email] {message}";
    }
}

INotifier notifier = new Email();
Console.WriteLine(notifier.SendTwice("Hi"));
// Output: [Email] Hi | [Email] Hi

// var e = new Email();
// e.SendTwice("Hi");   // ERROR: Email does not contain a definition for 'SendTwice'
"""),
    warn("**Common mistake:** calling a default interface member through the class type. The default implementation is reachable only through a variable of the **interface** type, as in `INotifier notifier = new Email();`. Use default members sparingly; they are meant for evolving an interface, not for replacing abstract classes."),
    tip("Name interfaces for the capability: `IComparable`, `IEnumerable`, `IDisposable`. Keep them small. An interface with two or three related members is far easier to implement and reuse than one with twenty."),
    link("Read more on Microsoft Learn: Interfaces", "https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/interfaces"),
]

M55_CODEALONG = codealong(
    "Code Along: Abilities as Interfaces",
    "You'll define two interfaces, implement them in three unrelated classes, and treat the objects through the interface types. Interfaces and classes go at the **bottom** of Program.cs; the code that uses them goes at the top.",
    [
        step(
            "Declare the interfaces",
            "Add these at the **bottom** of Program.cs. `ISwimmable` includes a default implementation of `Describe()`.",
            r"""
interface IFlyable
{
    string Fly();
}

interface ISwimmable
{
    string Swim();

    string Describe()
    {
        return "Can swim";
    }
}
""",
            at="bottom",
        ),
        step(
            "Implement them in classes",
            "Add these classes at the **bottom** of Program.cs, below the interfaces. `Duck` implements both contracts.",
            r"""
class Duck : IFlyable, ISwimmable
{
    public string Fly()
    {
        return "Duck flaps and takes off";
    }

    public string Swim()
    {
        return "Duck paddles";
    }
}

class Fish : ISwimmable
{
    public string Swim()
    {
        return "Fish glides";
    }
}

class Plane : IFlyable
{
    public string Fly()
    {
        return "Plane roars down the runway";
    }
}
""",
            at="bottom",
        ),
        step(
            "Use objects through an interface",
            "At the **top** of Program.cs, put a `Duck` and a `Plane` in one `IFlyable[]` array. The loop doesn't care what each object is.",
            r"""
IFlyable[] flyers = [new Duck(), new Plane()];

foreach (IFlyable f in flyers)
{
    Console.WriteLine(f.Fly());
}
""",
        ),
        step(
            "Ask what an object can do",
            "Add this below your other top-level code. A `Plane` doesn't implement `ISwimmable`, so it takes the `else` branch.",
            r"""
object[] things = [new Duck(), new Fish(), new Plane()];

foreach (object thing in things)
{
    if (thing is ISwimmable swimmer)
    {
        Console.WriteLine($"{swimmer.Swim()} ({swimmer.Describe()})");
    }
    else
    {
        Console.WriteLine($"{thing.GetType().Name} cannot swim");
    }
}
""",
        ),
        step(
            "Reach a default member",
            "Add this below the rest of your top-level code. `Describe` is only available through the interface type.",
            r"""
Fish fish = new Fish();
// Console.WriteLine(fish.Describe());   // ERROR: Fish has no 'Describe' member

ISwimmable asSwimmer = fish;
Console.WriteLine(asSwimmer.Describe());
""",
        ),
    ],
)

M55_LAB = lab(
    "Lab: Notifiers",
    "Intermediate",
    "Design two interfaces and two classes. One class implements both interfaces, the other only one, and you query the objects through the interface types. Remember: top-level statements first, types at the bottom.",
    [
        "Declare `interface INotifier` with a property `string Channel { get; }`, a method `string Send(string message);`, and a default method `string SendTwice(string message)` that returns `Send(message) + \" | \" + Send(message)`.",
        "Declare `interface IAuditable` with a property `int SentCount { get; }`.",
        "`EmailNotifier : INotifier, IAuditable`: `Channel` is `\"Email\"`; every call to `Send` increments a private counter and returns `[Email] ` followed by the message; `SentCount` returns the counter.",
        "`SmsNotifier : INotifier`: `Channel` is `\"SMS\"`; `Send` returns `[SMS] ` followed by `message.ToUpperInvariant()`. It is not auditable.",
        "In top-level code create `INotifier[] notifiers = [new EmailNotifier(), new SmsNotifier()];`. Loop and print `n.Send(\"Server restarted\")` for each. Then loop again: if `n is IAuditable a` print `Channel is audited: N sent`, otherwise print `Channel is not audited`.",
        "Finally print `notifiers[0].SendTwice(\"Ping\")`, then use `if (notifiers[0] is IAuditable total)` to print `Email total: ` followed by `total.SentCount`.",
    ],
    "[Email] Server restarted\n[SMS] SERVER RESTARTED\nEmail is audited: 1 sent\nSMS is not audited\n[Email] Ping | [Email] Ping\nEmail total: 3",
    "Properties on an interface are declared `string Channel { get; }`; in the class you can implement it with `public string Channel => \"Email\";`. `SendTwice` calls `Send` twice, so the email counter goes from 1 to 3. The default method is reachable because `notifiers` is typed as `INotifier[]`.",
)

# ─── 5.6 Records ───

M56_READING = [
    h2("Classes that are really just data"),
    p("A lot of the types you write simply carry data around: a point, an address, a customer's name and email. For plain classes, comparing two objects with `==` asks if they're the same object in memory, not whether they contain the same data. Printing one shows only the type name. You end up writing constructors, properties, `Equals`, and `ToString` by hand every time."),
    p("A **record** is a class (reference type) designed for data. You describe the data in one line, and the compiler generates the boilerplate: properties, a constructor, value-based equality, a readable `ToString()`, and more."),
    h2("Positional records"),
    code(r"""
record Point(int X, int Y);          // one line replaces a whole class

var p = new Point(1, 2);
Console.WriteLine(p.X);              // Output: 1
Console.WriteLine(p);                // Output: Point { X = 1, Y = 2 }
// p.X = 10;                         // ERROR: positional properties are init-only
"""),
    p("The parameters in parentheses become **init-only properties**, so a record created this way is immutable by default: you can read `X` and `Y`, but you can't change them afterward. As with every type declaration, the record goes at the **bottom** of a file that uses top-level statements."),
    h2("Value equality"),
    p("Two records are **equal** when they are the same type and all their properties are equal. This is called **value equality**, and `==` and `Equals` both use it."),
    code(r"""
var a = new Point(1, 2);
var b = new Point(1, 2);

Console.WriteLine(a == b);                      // Output: True   (same values)
Console.WriteLine(object.ReferenceEquals(a, b));// Output: False  (still two objects)

// Compare with an ordinary class, where == checks identity:
// class PlainPoint { public int X; public int Y; }
// new PlainPoint() == new PlainPoint()         // False
"""),
    h2("Non-destructive mutation with with"),
    p("Since records are immutable, how do you get a modified version? With a **with expression**. It copies the record and lets you change some properties in the copy. The original is untouched."),
    code(r"""
var moved = a with { X = 10 };

Console.WriteLine(a);       // Output: Point { X = 1, Y = 2 }
Console.WriteLine(moved);   // Output: Point { X = 10, Y = 2 }
"""),
    warn("**Common mistake:** assuming a record is deeply immutable. `with` makes a **shallow** copy, and an init-only property that holds a mutable object (like an array or a list) still points at the same object in both copies. Only the record's own properties are protected."),
    h2("Deconstruction"),
    p("Positional records can be **deconstructed**: split into separate variables in a single statement, in the order the parameters were declared. Use `_` when you don't care about a value."),
    code(r"""
var (x, y) = moved;
Console.WriteLine($"x={x}, y={y}");
// Output: x=10, y=2

var (onlyX, _) = moved;      // _ discards the second value
"""),
    h2("Adding members to a record"),
    p("A record is still a class, so you can add methods, computed properties, and extra properties with braces instead of the semicolon."),
    code(r"""
record Rectangle(double Width, double Height)
{
    public double Area => Width * Height;

    public bool IsSquare()
    {
        return Width == Height;
    }
}

var r = new Rectangle(3, 4);
Console.WriteLine($"{r.Area} {r.IsSquare()}");
// Output: 12 False
"""),
    h2("Record structs"),
    p("Plain `record` creates a reference type. If you want value-type semantics (stored directly in the variable, copied on assignment), you can write `record struct`, or `readonly record struct` to make it immutable, as in `readonly record struct Coordinate(int Row, int Col);`. Structs are an advanced topic; just know the option exists and that the syntax mirrors what you've seen here."),
    h2("Record or class?"),
    p("Choose a **record** when the type's identity *is* its data: coordinates, money amounts, DTOs, results returned from a method, configuration snapshots. You get immutability, equality, and printing without effort. Choose a **class** when objects have identity and changing state over time, such as a `BankAccount` whose balance changes, or when the type is mostly behavior. Two bank accounts with the same balance are still different accounts, but two points at (1, 2) are the same point."),
    tip("Records can also inherit from other records, and the generated equality accounts for the derived type. Reach for that only after you're comfortable with the basics."),
    link("Read more on Microsoft Learn: Records", "https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/records"),
]

M56_CODEALONG = codealong(
    "Code Along: Records",
    "You'll define a positional record and explore equality, `with`, and deconstruction, and compare it to a plain class. Type declarations go at the **bottom** of Program.cs; the code that uses them goes at the top.",
    [
        step(
            "Declare a record",
            "Add this one-line record at the **bottom** of Program.cs.",
            r"""
record Point(int X, int Y);
""",
            at="bottom",
        ),
        step(
            "Create and print records",
            "At the **top** of Program.cs, create two points with the same values. Printing shows the generated `ToString()`, and `==` compares their values.",
            r"""
var a = new Point(1, 2);
var b = new Point(1, 2);

Console.WriteLine(a);
Console.WriteLine($"a == b: {a == b}");
Console.WriteLine($"Same object: {object.ReferenceEquals(a, b)}");
""",
        ),
        step(
            "Copy with changes, then deconstruct",
            "Add this below your top-level code. `moved` is a modified copy and `a` doesn't change; the last two lines split `moved` into variables in parameter order.",
            r"""
var moved = a with { X = 10 };
Console.WriteLine(a);
Console.WriteLine(moved);
Console.WriteLine($"a == moved: {a == moved}");

var (x, y) = moved;
Console.WriteLine($"x={x}, y={y}");
""",
        ),
        step(
            "Contrast with a class",
            "Add this plain class at the **bottom** of Program.cs, then add the comparison lines at the top level. Same data, but `==` on a class checks identity.",
            r"""
class PlainPoint
{
    public int X;
    public int Y;
}
""",
            at="bottom",
        ),
        step(
            "Compare two class objects",
            "Add this at the **top** level, below your other statements.",
            r"""
var c = new PlainPoint { X = 1, Y = 2 };
var d = new PlainPoint { X = 1, Y = 2 };
Console.WriteLine($"c == d: {c == d}");
""",
        ),
    ],
)

M56_LAB = lab(
    "Lab: Product Snapshots",
    "Beginner",
    "Use a record to model a product, make a discounted copy with `with`, compare values, and deconstruct. Remember: top-level statements first, the record at the bottom.",
    [
        "Declare `record Product(string Name, decimal Price, int Stock)` with a body that adds a computed property `public decimal Value => Price * Stock;`.",
        "Create `a` as `new Product(\"Pen\", 2.50m, 10)` and `b` as the same values, and print `a == b`, then `object.ReferenceEquals(a, b)`.",
        "Create `sale` with `a with { Price = 1.75m }`. Print `a`, then print `sale` (use `Console.WriteLine` directly on the records), then print `a == sale`.",
        "Deconstruct `sale` with `var (name, price, stock) = sale;` and print `Pen costs $1.75 with 10 left` using interpolation: `{name} costs {price:C} with {stock} left`.",
        "Print `Value before: ` and `a.Value`, then `, after: ` and `sale.Value`, both formatted with `:C`, on one line.",
    ],
    "True\nFalse\nProduct { Name = Pen, Price = 2.50, Stock = 10, Value = 25.00 }\nProduct { Name = Pen, Price = 1.75, Stock = 10, Value = 17.50 }\nFalse\nPen costs $1.75 with 10 left\nValue before: $25.00, after: $17.50",
    "A record with a body looks like `record Product(string Name, decimal Price, int Stock) { public decimal Value => Price * Stock; }`. The generated `ToString()` prints the public properties in the order they are declared, including your computed `Value` property at the end. The `with` copy leaves `a` unchanged, which is why printing `a` after creating `sale` still shows the original price.",
)

LESSONS = {
    (5, 1): lesson(
        subtitle="Define your own types with classes, create objects with `new`, understand how references differ from values, and control access with `public`, `private`, and `static`.",
        reading=M51_READING,
        codealong=M51_CODEALONG,
        lab=M51_LAB,
    ),
    (5, 2): lesson(
        subtitle="Protect your objects' data with properties, build them correctly with constructors, and use `init`, `required`, and object initializers.",
        reading=M52_READING,
        codealong=M52_CODEALONG,
        lab=M52_LAB,
    ),
    (5, 3): lesson(
        subtitle="Reuse and specialize code with base and derived classes, `virtual`/`override`, `protected`, `sealed`, and the `is` and `as` operators.",
        reading=M53_READING,
        codealong=M53_CODEALONG,
        lab=M53_LAB,
    ),
    (5, 4): lesson(
        subtitle="Write code against a general type and let each object do the right thing, using abstract classes, overrides, and collections of a base type.",
        reading=M54_READING,
        codealong=M54_CODEALONG,
        lab=M54_LAB,
    ),
    (5, 5): lesson(
        subtitle="Define contracts with interfaces, implement several in one class, decide between interfaces and abstract classes, and use default interface members.",
        reading=M55_READING,
        codealong=M55_CODEALONG,
        lab=M55_LAB,
    ),
    (5, 6): lesson(
        subtitle="Model data with records: get value equality, readable printing, `with` copies, and deconstruction, and know when a class is the better choice.",
        reading=M56_READING,
        codealong=M56_CODEALONG,
        lab=M56_LAB,
    ),
}

# Reference solutions, used only by verify_content.py (never sent to the learner).
SOLUTIONS = {
    (5, 1): r"""
Item widget = new Item();
widget.Name = "Widget";
widget.AddStock(30);
widget.AddStock(30);
Console.WriteLine(widget.Describe());
Console.WriteLine(widget.Remove(10));
Console.WriteLine(widget.Describe());
Console.WriteLine(widget.Remove(100));
Console.WriteLine(widget.Describe());
Item same = widget;
same.Remove(5);
Console.WriteLine(widget.Describe());
Item gadget = new Item();
gadget.Name = "Gadget";
Console.WriteLine(gadget.Describe());

class Item
{
    public string Name = "";
    private int _quantity;
    public static int MaxQuantity = 50;

    public void AddStock(int amount)
    {
        _quantity += amount;
        if (_quantity > MaxQuantity)
        {
            _quantity = MaxQuantity;
        }
    }

    public bool Remove(int amount)
    {
        if (amount > _quantity)
        {
            return false;
        }
        _quantity -= amount;
        return true;
    }

    public string Describe()
    {
        return $"{Name}: {_quantity}";
    }
}
""",
    (5, 2): r"""
var lobby = new Thermostat("Lobby");
var office = new Thermostat("Office", 25);
Console.WriteLine(lobby.Describe());
Console.WriteLine(office.Describe());
lobby.Target = 5;
Console.WriteLine(lobby.Describe());
lobby.Target = 99;
Console.WriteLine(lobby.Describe());

class Thermostat
{
    private int _target;

    public string Room { get; }

    public int Target
    {
        get { return _target; }
        set { _target = Math.Clamp(value, 10, 30); }
    }

    public int Fahrenheit => Target * 9 / 5 + 32;

    public Thermostat(string room)
    {
        Room = room;
        Target = 20;
    }

    public Thermostat(string room, int target) : this(room)
    {
        Target = target;
    }

    public string Describe()
    {
        return $"{Room}: {Target}C / {Fahrenheit}F";
    }
}
""",
    (5, 3): r"""
Vehicle[] fleet = [new Vehicle("Sedan"), new Motorcycle("Ducati"), new Truck("Hauler", 2), new DumpTruck("Dumper")];
foreach (Vehicle item in fleet)
{
    Console.WriteLine(item.Describe());
}
Vehicle v = fleet[2];
Console.WriteLine(v is Truck);
Console.WriteLine(v is DumpTruck);
Console.WriteLine((v as Motorcycle) is null);
Console.WriteLine(fleet[3] is Truck);
Console.WriteLine(fleet[3].GetType().Name);

class Vehicle
{
    public string Name { get; }

    public Vehicle(string name)
    {
        Name = name;
    }

    public virtual int WheelCount()
    {
        return 4;
    }

    public string Describe()
    {
        return $"{Name} has {WheelCount()} wheels";
    }
}

class Motorcycle : Vehicle
{
    public Motorcycle(string name) : base(name)
    {
    }

    public override int WheelCount()
    {
        return 2;
    }
}

class Truck : Vehicle
{
    protected int Axles;

    public Truck(string name, int axles) : base(name)
    {
        Axles = axles;
    }

    public override int WheelCount()
    {
        return Axles * 4;
    }
}

sealed class DumpTruck : Truck
{
    public DumpTruck(string name) : base(name, 3)
    {
    }

    public override int WheelCount()
    {
        return base.WheelCount() + 2;
    }
}
""",
    (5, 4): r"""
Employee[] staff = [new SalariedEmployee("Alice", 60000m), new HourlyEmployee("Bob", 25m, 160), new Manager("Carol", 96000m, 500m)];
decimal total = 0m;
foreach (Employee e in staff)
{
    Console.WriteLine(e);
    total += e.MonthlyPay();
}
Console.WriteLine($"Total payroll: {total:C}");

abstract class Employee
{
    public string Name { get; }

    protected Employee(string name)
    {
        Name = name;
    }

    public abstract decimal MonthlyPay();

    public override string ToString()
    {
        return $"{Name}: {MonthlyPay():C}";
    }
}

class SalariedEmployee : Employee
{
    private decimal _annual;

    public SalariedEmployee(string name, decimal annualSalary) : base(name)
    {
        _annual = annualSalary;
    }

    public override decimal MonthlyPay()
    {
        return _annual / 12;
    }
}

class HourlyEmployee : Employee
{
    private decimal _rate;
    private int _hours;

    public HourlyEmployee(string name, decimal rate, int hours) : base(name)
    {
        _rate = rate;
        _hours = hours;
    }

    public override decimal MonthlyPay()
    {
        return _rate * _hours;
    }
}

class Manager : SalariedEmployee
{
    private decimal _bonus;

    public Manager(string name, decimal annualSalary, decimal bonus) : base(name, annualSalary)
    {
        _bonus = bonus;
    }

    public override decimal MonthlyPay()
    {
        return base.MonthlyPay() + _bonus;
    }
}
""",
    (5, 5): r"""
INotifier[] notifiers = [new EmailNotifier(), new SmsNotifier()];
foreach (INotifier n in notifiers)
{
    Console.WriteLine(n.Send("Server restarted"));
}
foreach (INotifier n in notifiers)
{
    if (n is IAuditable a)
    {
        Console.WriteLine($"{n.Channel} is audited: {a.SentCount} sent");
    }
    else
    {
        Console.WriteLine($"{n.Channel} is not audited");
    }
}
Console.WriteLine(notifiers[0].SendTwice("Ping"));
if (notifiers[0] is IAuditable total)
{
    Console.WriteLine("Email total: " + total.SentCount);
}

interface INotifier
{
    string Channel { get; }
    string Send(string message);

    string SendTwice(string message)
    {
        return Send(message) + " | " + Send(message);
    }
}

interface IAuditable
{
    int SentCount { get; }
}

class EmailNotifier : INotifier, IAuditable
{
    private int _sent;

    public string Channel => "Email";

    public int SentCount => _sent;

    public string Send(string message)
    {
        _sent++;
        return "[Email] " + message;
    }
}

class SmsNotifier : INotifier
{
    public string Channel => "SMS";

    public string Send(string message)
    {
        return "[SMS] " + message.ToUpperInvariant();
    }
}
""",
    (5, 6): r"""
var a = new Product("Pen", 2.50m, 10);
var b = new Product("Pen", 2.50m, 10);
Console.WriteLine(a == b);
Console.WriteLine(object.ReferenceEquals(a, b));
var sale = a with { Price = 1.75m };
Console.WriteLine(a);
Console.WriteLine(sale);
Console.WriteLine(a == sale);
var (name, price, stock) = sale;
Console.WriteLine($"{name} costs {price:C} with {stock} left");
Console.WriteLine($"Value before: {a.Value:C}, after: {sale.Value:C}");

record Product(string Name, decimal Price, int Stock)
{
    public decimal Value => Price * Stock;
}
""",
}
