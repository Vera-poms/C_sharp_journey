"""Module 8: Desktop App Development.

The in-app runner is a Linux console container, so WPF / .NET MAUI / XAML cannot run there.
The readings carry the real UI material (XAML and C# shown in code blocks, clearly labeled);
code-alongs and labs use console code built only on the BCL that teaches the same concepts.
"""
from .lesson_kit import *  # noqa: F401,F403

# ─────────────────────────── 8.1 Choosing WPF or .NET MAUI ───────────────────────────

L81_READING = [
    h2("Two ways to build a desktop app"),
    p("So far every program you wrote talks to the user through a text console. Real desktop applications have windows, buttons, text boxes, and lists. Microsoft offers several UI frameworks for C#, and the first decision you face is which one to learn. This lesson helps you choose, and explains why the rest of this module uses **WPF**."),
    note("**Read this first.** The in-app editor runs your code in a Linux console container, so it cannot open a window. In lessons 8.1 to 8.5 the UI parts (XAML and WPF code) are in the reading so you can study and copy them into a project on your own computer. The code-alongs and labs use console programs that practice the same ideas: property change notifications, commands, and view models. To run the real UI you need a Windows PC with Visual Studio and the .NET desktop workload."),
    h2("WPF: Windows Presentation Foundation"),
    p("WPF has existed since 2006 and was open-sourced and ported to modern .NET (it runs on .NET 10 today). It draws its own controls with DirectX, describes screens in a markup language called **XAML**, and has the most complete data binding system of any .NET UI framework. It runs on **Windows only**."),
    p("WPF is the sweet spot for line-of-business software: internal tools, dashboards, data entry apps, and admin consoles for Windows users. It is mature, well documented, and there are mountains of tutorials, controls, and Stack Overflow answers for it."),
    h2(".NET MAUI: one codebase, many platforms"),
    p("**.NET MAUI** (Multi-platform App UI) targets Windows, macOS (through Mac Catalyst), Android, and iOS from a single project. It also uses XAML and the same binding and MVVM ideas you will learn here. The trade-off is complexity: you need extra tooling per platform (an Android SDK and emulator, a Mac for iOS builds), and mobile and desktop screens often need different layouts anyway. MAUI does not officially target Linux."),
    p("Choose MAUI when you truly need the same app on phones and desktops. Choose WPF when your users are on Windows PCs and you want the shortest path to a polished desktop app."),
    h2("Other options worth knowing"),
    p("**WinUI 3** (part of the Windows App SDK) is Microsoft's modern native Windows UI layer, with newer visuals than WPF but a smaller ecosystem. **Windows Forms** is the older drag-and-drop framework, still fine for simple internal tools. **Avalonia** and **Uno Platform** are third-party, open-source frameworks that use XAML-style markup and run on Windows, macOS, and Linux (and more), which makes them the usual answer when you need Linux desktops. Everything you learn about XAML, binding, and MVVM transfers to all of them."),
    code("""
// Decision checklist (answer honestly, then read the result)
//
// 1. Do all my users run Windows?                     yes -> WPF
// 2. Do I need Android or iOS from the same code?     yes -> .NET MAUI
// 3. Do I need macOS or Linux desktops?               macOS -> MAUI or Avalonia, Linux -> Avalonia or Uno
// 4. Is this an internal or data-heavy business tool? yes -> WPF
// 5. Do I need the newest Windows 11 look and feel?   yes -> consider WinUI 3
// 6. Do I want the most tutorials and 3rd-party UI?   yes -> WPF
//
// No strong requirement either way? Pick WPF for learning.
"""),
    h2("Why this course uses WPF"),
    p("Because WPF is Windows-only, there are no emulators, no per-platform SDKs, and no workload juggling: install Visual Studio, create a project, press F5. That lets you focus on the ideas that matter in every XAML framework. XAML layout, data binding, and MVVM are what you are really learning; the framework is just where you practice them."),
    h2("Prerequisites and your first project"),
    p("On Windows, install **Visual Studio 2022 or later** (the free Community edition is fine) and tick the **.NET desktop development** workload in the installer. You already have the .NET SDK from module 1; the Windows desktop pieces (WPF) ship with it on Windows. You can also create and run a WPF project from the command line."),
    code("""
# PowerShell on Windows (this will not work in the Linux runner)
dotnet new wpf -n HelloWpf
cd HelloWpf
dotnet run

# For .NET MAUI you would first install the workload:
#   dotnet workload install maui
#   dotnet new maui -n HelloMaui
"""),
    p("The generated WPF project file shows what makes it special. The target framework ends in `-windows`, the output type is `WinExe` (a program that does not open a console window), and `UseWPF` pulls in the WPF libraries."),
    code("""
<!-- HelloWpf.csproj (XML project file; shown for reference) -->
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>WinExe</OutputType>
    <TargetFramework>net10.0-windows</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <UseWPF>true</UseWPF>
  </PropertyGroup>
</Project>
"""),
    warn("**Common mistake:** trying to build a WPF project on macOS or Linux, or in a console-only container. The `net10.0-windows` target framework only builds and runs on Windows, and you will get errors about the Windows desktop pack or about missing `-windows` support. If you are not on Windows, you can still follow this module: read the XAML, run the console code-alongs here, and look at Avalonia if you want to build a real window on your OS."),
    tip("You do not have to decide forever. A well-built MVVM app keeps its logic in plain C# classes that do not know about the UI. That code moves between WPF, MAUI, and Avalonia with little or no change, which is exactly what the later lessons teach."),
    link("Read more on Microsoft Learn: Desktop guide for WPF", "https://learn.microsoft.com/en-us/dotnet/desktop/wpf/"),
]

# ─────────────────────────── 8.2 XAML Layout ───────────────────────────

L82_READING = [
    h2("XAML is just objects"),
    p("**XAML** (eXtensible Application Markup Language) is an XML-based way of creating and wiring up .NET objects. Every XAML **element** is an object created with `new`. Every **attribute** sets a property on that object. Elements nested inside other elements become that object's children or content."),
    note("This lesson's UI code is XAML and WPF C#, shown in code blocks for you to study and try in a Windows WPF project. The highlighter in this app is tuned for C#, so XAML will look like plain text. The code-along at the end of the lesson builds a tree of objects in plain C# to prove that XAML is just object creation."),
    code("""
<!-- XAML -->
<Button Content="Save" Width="80" IsDefault="True" />

// The same thing in C# code:
var button = new Button();
button.Content = "Save";
button.Width = 80;
button.IsDefault = true;
"""),
    p("The XAML version is shorter and shows structure at a glance, which is why designers and developers both like it. At build time, WPF compiles the XAML so the object creation is fast."),
    h2("The anatomy of a window"),
    p("A WPF project's main screen is a `Window`. The root element declares **XML namespaces** (`xmlns`) that tell the parser where names like `Window` and `Button` come from, and `x:Class` links the markup to a C# partial class (the **code-behind**)."),
    code("""
<!-- MainWindow.xaml -->
<Window x:Class="HelloWpf.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Hello" Height="240" Width="360">
    <Grid>
        <TextBlock Text="Hello, XAML!" FontSize="24"
                   HorizontalAlignment="Center" VerticalAlignment="Center" />
    </Grid>
</Window>
"""),
    warn("**Common mistake:** a `Window` can hold exactly **one** child. If you place two controls directly inside `<Window>`, the compiler reports that the content property can only be set once. Always put a layout panel (like `Grid` or `StackPanel`) inside the window and put your controls in that."),
    h2("Layout panels: the three you need first"),
    p("WPF does not position controls with pixel coordinates by default. Instead, you put controls inside **panels** that decide where children go, so the window can resize gracefully. Learn these three panels and you can build most screens."),
    p("**StackPanel** lines children up one after another, vertically by default or horizontally with `Orientation=\"Horizontal\"`. **DockPanel** attaches children to the Top, Bottom, Left, or Right edge, and the last child fills what remains. **Grid** divides the space into rows and columns and is the workhorse for forms and whole-window layouts."),
    code("""
<!-- Grid with a header row, a content row, and a footer row -->
<Grid>
    <Grid.RowDefinitions>
        <RowDefinition Height="Auto" />   <!-- as tall as its content -->
        <RowDefinition Height="*" />      <!-- takes all remaining space -->
        <RowDefinition Height="40" />     <!-- fixed 40 units -->
    </Grid.RowDefinitions>
    <Grid.ColumnDefinitions>
        <ColumnDefinition Width="200" />
        <ColumnDefinition Width="*" />
    </Grid.ColumnDefinitions>

    <TextBlock Grid.Row="0" Grid.ColumnSpan="2" Text="Header" />
    <ListBox   Grid.Row="1" Grid.Column="0" />
    <TextBox   Grid.Row="1" Grid.Column="1" />
    <Button    Grid.Row="2" Grid.Column="1" Content="OK" HorizontalAlignment="Right" />
</Grid>
"""),
    p("`Grid.Row` and `Grid.Column` are **attached properties**: the child control stores a value that belongs to its parent panel. Rows and columns count from zero, and a missing value means zero. Sizes can be a fixed number, `Auto` (fit the content), or `*` (share the leftover space; `2*` gets twice as much as `*`)."),
    h2("Margin, padding, and alignment"),
    p("**Margin** is the space outside a control; **Padding** is the space inside it, between its border and its content. A single number applies to all sides; two numbers are horizontal and vertical; four numbers are left, top, right, and bottom, in that order. **HorizontalAlignment** and **VerticalAlignment** control where a control sits inside the space its parent gives it (`Left`, `Center`, `Right`, `Stretch`)."),
    code("""
<StackPanel Margin="16">
    <TextBlock Text="Your name" Margin="0,0,0,4" />
    <TextBox x:Name="NameBox" Padding="6" />
    <StackPanel Orientation="Horizontal" HorizontalAlignment="Right" Margin="0,12,0,0">
        <Button Content="Cancel" Margin="0,0,8,0" Padding="12,4" />
        <Button Content="Greet" Padding="12,4" IsDefault="True" Click="GreetButton_Click" />
    </StackPanel>
    <ListBox x:Name="HistoryList" Height="100" Margin="0,12,0,0" />
</StackPanel>
"""),
    tip("Use `Margin` for spacing between controls and `Padding` for breathing room inside one. If a button looks cramped, increase its `Padding`; if two controls touch, add `Margin` to one of them."),
    h2("Common controls"),
    p("**TextBlock** shows read-only text. **TextBox** lets the user type. **Button** raises a `Click` event. **ListBox** shows a scrollable list of items and exposes the chosen one through `SelectedItem`. Others you will meet soon include `CheckBox`, `ComboBox`, and `DataGrid`. Giving a control an `x:Name` creates a field with that name in the code-behind so you can touch it from C#."),
    h2("Code-behind and events"),
    p("The `Click=\"GreetButton_Click\"` attribute above connects the button's `Click` event (a normal C# event, just like the ones from module 7) to a method in the window's code-behind file. The constructor calls `InitializeComponent()`, which loads the compiled XAML and creates all the named controls."),
    code("""
// MainWindow.xaml.cs
using System.Windows;

namespace HelloWpf;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();   // builds the controls described in the XAML
    }

    private void GreetButton_Click(object sender, RoutedEventArgs e)
    {
        string name = NameBox.Text.Trim();
        if (name.Length == 0)
        {
            MessageBox.Show("Please type a name first.");
            return;
        }
        HistoryList.Items.Add($"Hello, {name}!");
        NameBox.Clear();
    }
}
"""),
    p("Code-behind is fine for small apps, but notice the problem: the logic reaches directly into controls (`NameBox.Text`, `HistoryList.Items`), so you cannot run or test it without a window. Lessons 8.3 and 8.4 show how data binding and MVVM remove that coupling."),
    link("Read more on Microsoft Learn: XAML overview (WPF)", "https://learn.microsoft.com/en-us/dotnet/desktop/wpf/xaml/"),
]

L82_CODEALONG = codealong(
    title="Code Along: XAML Is Just Objects",
    intro="You cannot open a window in this runner, but you can prove the key idea of XAML: markup describes a tree of objects with properties and events. You will build that tree in plain C#.",
    steps=[
        step(
            "Define a tiny element model",
            "Add these classes at the **bottom** of the file. `Element` stores properties by name and holds child elements, like a XAML element does. `Button` also has a `Click` event.",
            """
public class Element
{
    public SortedDictionary<string, string> Properties { get; } = new();
    public List<Element> Children { get; } = [];
    public string Kind => GetType().Name;

    public Element Set(string name, string value)
    {
        Properties[name] = value;
        return this;
    }

    public Element Add(Element child)
    {
        Children.Add(child);
        return this;
    }
}

public class StackPanel : Element { }
public class TextBlock : Element { }

public class Button : Element
{
    public event EventHandler? Click;
    public void PerformClick() => Click?.Invoke(this, EventArgs.Empty);
}
""",
            at="bottom",
        ),
        step(
            "Build the tree like XAML would",
            "Add this at the top of the file. Each `new` is an element, each `Set` is an attribute, and each `Add` nests a child.",
            """
var title = new TextBlock();
title.Set("Text", "Todo list").Set("FontSize", "20");

var saveButton = new Button();
saveButton.Set("Content", "Save").Set("Margin", "0,8,0,0");

var root = new StackPanel();
root.Set("Margin", "16").Add(title).Add(saveButton);
""",
        ),
        step(
            "Print it as XAML-style markup",
            "Add a recursive local function that prints each element with its attributes, indented by depth, then call it on the root.",
            """
void Print(Element element, int depth)
{
    string attributes = string.Join(" ", element.Properties.Select(kv => $"{kv.Key}=\\"{kv.Value}\\""));
    string open = attributes.Length > 0 ? $"{element.Kind} {attributes}" : element.Kind;
    Console.WriteLine($"{new string(' ', depth * 2)}<{open}>");
    foreach (var child in element.Children)
    {
        Print(child, depth + 1);
    }
}

Print(root, 0);
""",
        ),
        step(
            "Wire up an event",
            "In XAML you write `Click=\"Handler\"`. In C# you subscribe with `+=`. Add this at the end of the top section and run the program.",
            """
saveButton.Click += (sender, e) => Console.WriteLine("Save clicked");
saveButton.PerformClick();
Console.WriteLine($"Elements in tree: {1 + root.Children.Count}");
""",
        ),
    ],
)

# ─────────────────────────── 8.3 Data Binding ───────────────────────────

L83_READING = [
    h2("The problem binding solves"),
    p("In 8.2's code-behind you copied values into controls and read them back out by hand: `NameBox.Text`, `HistoryList.Items.Add(...)`. That works, but every change needs matching code on both sides, and it is easy to forget one. **Data binding** lets you declare once that a control property is connected to a property on a data object, and the framework keeps them in sync."),
    note("The XAML and WPF code in this lesson's reading needs a Windows WPF project to run. The code-along and lab below use the same underlying interfaces (`INotifyPropertyChanged`, `ObservableCollection<T>`) in a console program, so you can watch notifications flow without any window."),
    h2("Binding syntax and DataContext"),
    p("A binding is written in curly braces inside an attribute. `{Binding Name}` means: look up the property called `Name` on the control's **DataContext** and show it. The `DataContext` is simply an object that bindings read from; it is inherited by child controls, so you usually set it once on the window."),
    code("""
<!-- XAML: Text shows the Name property of whatever DataContext is -->
<StackPanel Margin="16">
    <TextBox  Text="{Binding Name, UpdateSourceTrigger=PropertyChanged}" />
    <TextBlock Text="{Binding Greeting}" FontSize="20" />
</StackPanel>

// C# code-behind: give the window its data object
public MainWindow()
{
    InitializeComponent();
    DataContext = new PersonViewModel { Name = "Ada" };
}
"""),
    h2("Binding modes"),
    p("The **mode** controls which direction values travel. `OneWay` flows from the data object to the control, ideal for labels. `TwoWay` flows both ways, which is what you want for a `TextBox` the user edits. `OneTime` reads once and never updates. `OneWayToSource` flows only from the control back to the data. Most properties have a sensible default (`TextBlock.Text` is one-way, `TextBox.Text` is two-way), and you override it with `Mode=`."),
    p("For a `TextBox`, the source is updated by default only when the box **loses focus**. Adding `UpdateSourceTrigger=PropertyChanged`, as above, updates the source on every keystroke, which is what you need for live previews and for enabling a button as the user types."),
    h2("INotifyPropertyChanged: how the UI hears about changes"),
    p("A binding reads a property once, so how does the screen know when the value later changes? The data object must tell it. The interface `INotifyPropertyChanged` has a single event, `PropertyChanged`. The binding subscribes to that event, and when it fires with the property name, the binding re-reads that property and updates the control. This is the events pattern from module 7 doing real work."),
    code("""
using System.ComponentModel;
using System.Runtime.CompilerServices;

public class PersonViewModel : INotifyPropertyChanged
{
    private string _name = "";

    public event PropertyChangedEventHandler? PropertyChanged;

    public string Name
    {
        get => _name;
        set
        {
            if (_name == value) return;          // nothing changed, stay quiet
            _name = value;
            OnPropertyChanged();                 // tells the UI 'Name' changed
            OnPropertyChanged(nameof(Greeting)); // Greeting depends on Name
        }
    }

    public string Greeting => $"Hello, {_name}!";

    private void OnPropertyChanged([CallerMemberName] string? propertyName = null)
        => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
}
"""),
    p("`[CallerMemberName]` makes the compiler fill in the name of the calling property for you, so you do not mistype strings. Notice that `Greeting` is read-only and computed from `Name`; it has no setter, so the only way the UI learns it changed is the extra `OnPropertyChanged(nameof(Greeting))` call."),
    warn("**Common mistake:** forgetting to raise `PropertyChanged`, or raising it with a misspelled name. The program compiles and runs, but the screen silently stays stale. Binding failures do not throw exceptions; WPF writes them to Visual Studio's **Output** window, so look there when a binding shows nothing."),
    h2("Collections: ObservableCollection<T>"),
    p("`INotifyPropertyChanged` covers single properties. For lists, the equivalent is `INotifyCollectionChanged`, whose `CollectionChanged` event fires when items are added, removed, or moved. You rarely implement it yourself: `ObservableCollection<T>` (in `System.Collections.ObjectModel`) is a ready-made list that raises it for you. A `ListBox` bound to one updates the instant you call `Add` or `Remove`."),
    code("""
<!-- XAML: a ListBox bound to a collection, with a template per item -->
<ListBox ItemsSource="{Binding Items}">
    <ListBox.ItemTemplate>
        <DataTemplate>
            <StackPanel Orientation="Horizontal">
                <CheckBox IsChecked="{Binding IsDone, Mode=TwoWay}" />
                <TextBlock Text="{Binding Title}" Margin="6,0,0,0" />
            </StackPanel>
        </DataTemplate>
    </ListBox.ItemTemplate>
</ListBox>

// ViewModel
public ObservableCollection<TodoItem> Items { get; } = [];
"""),
    p("A `DataTemplate` describes how to draw one item. Inside it, the `DataContext` is the individual item, so `{Binding Title}` reads `Title` from each `TodoItem`."),
    tip("Use `ObservableCollection<T>` for any collection a control displays. A plain `List<T>` also works for a one-time display, but changes to it never reach the screen. Also note that `ObservableCollection<T>` tells the UI when items are added or removed, not when a property **inside** an item changes; each item needs its own `INotifyPropertyChanged`."),
    link("Read more on Microsoft Learn: Data binding overview (WPF)", "https://learn.microsoft.com/en-us/dotnet/desktop/wpf/data/"),
]

L83_CODEALONG = codealong(
    title="Code Along: A Console Data Binding Simulator",
    intro="You will build the same machinery WPF uses: an object that raises `PropertyChanged`, a 'label' that subscribes and refreshes, and an `ObservableCollection<T>` that reports changes.",
    steps=[
        step(
            "Add the namespaces",
            "These `using` lines must be at the very top of `Program.cs`. `System.ComponentModel` holds `INotifyPropertyChanged`, `System.Collections.ObjectModel` holds `ObservableCollection<T>`, and `System.Collections.Specialized` holds the collection-changed types.",
            """
using System.Collections.ObjectModel;
using System.Collections.Specialized;
using System.ComponentModel;
using System.Runtime.CompilerServices;

Console.WriteLine("-- property binding --");
""",
        ),
        step(
            "Create a notifying data object",
            "Add these classes at the **bottom** of the file. `Person` raises `PropertyChanged` only when a value really changes. `BoundLabel` plays the role of a `TextBlock` binding: it subscribes, then refreshes when its property is announced.",
            """
public class Person : INotifyPropertyChanged
{
    private string _name = "";
    private int _age;

    public event PropertyChangedEventHandler? PropertyChanged;

    public string Name
    {
        get => _name;
        set { if (_name != value) { _name = value; Raise(); } }
    }

    public int Age
    {
        get => _age;
        set { if (_age != value) { _age = value; Raise(); } }
    }

    private void Raise([CallerMemberName] string? property = null)
        => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(property));
}

public class BoundLabel
{
    private readonly Func<string> _read;

    public BoundLabel(INotifyPropertyChanged source, string propertyName, Func<string> read)
    {
        _read = read;
        Refresh();
        source.PropertyChanged += (_, e) =>
        {
            if (e.PropertyName == propertyName) Refresh();
        };
    }

    public string Text { get; private set; } = "";

    private void Refresh()
    {
        Text = _read();
        Console.WriteLine($"  [label updated] {Text}");
    }
}
""",
            at="bottom",
        ),
        step(
            "Bind and change values",
            "Add this to the top section, after the `Console.WriteLine`. Watch which assignments cause a label update: only a real change to the property the label is bound to.",
            """
var person = new Person { Name = "Ada" };
var nameLabel = new BoundLabel(person, nameof(Person.Name), () => $"Name: {person.Name}");

person.Name = "Grace";   // changes -> label refreshes
person.Name = "Grace";   // same value -> no notification
person.Age = 36;         // different property -> label ignores it
Console.WriteLine($"Label text now: {nameLabel.Text}");
""",
        ),
        step(
            "Observe a collection",
            "Add this next. `ObservableCollection<T>` raises `CollectionChanged` with the kind of change in `e.Action`. Adding and removing report the affected items; `Clear` reports a `Reset`.",
            """
Console.WriteLine("-- collection binding --");
var items = new ObservableCollection<string>();
items.CollectionChanged += (_, e) =>
{
    string affected = e.NewItems?[0]?.ToString() ?? e.OldItems?[0]?.ToString() ?? "(all)";
    Console.WriteLine($"  collection {e.Action}: {affected}");
};

items.Add("Milk");
items.Add("Eggs");
items.Remove("Milk");
items.Clear();
Console.WriteLine($"Items left: {items.Count}");
""",
        ),
    ],
)

L83_LAB = lab(
    title="Lab: Thermostat Notifications",
    difficulty="Beginner",
    description="Build a small view-model-style class that notifies listeners when it changes, and record its changes in an `ObservableCollection<T>`. This is exactly the flow a bound WPF screen depends on.",
    requirements=[
        "Create a class `Thermostat` that implements `INotifyPropertyChanged`, with a `double Celsius` property that starts at `0`.",
        "When `Celsius` is set to a different value, store it, then raise `PropertyChanged` for `\"Celsius\"` and then for `\"Fahrenheit\"`. Setting the same value raises nothing.",
        "Add a read-only `double Fahrenheit` property computed as `Celsius * 9 / 5 + 32`.",
        "In top-level code create a `Thermostat t` and an `ObservableCollection<double> readings`. Subscribe to `readings.CollectionChanged` and print `Readings {e.Action}: {e.NewItems![0]}`.",
        "Subscribe to `t.PropertyChanged`: print `Changed: {e.PropertyName}`, and when the property name is `Celsius`, add `t.Celsius` to `readings`.",
        "Set `t.Celsius` to `20`, then `20` again, then `25`. Finally print `Fahrenheit: {t.Fahrenheit}` and `Total readings: {readings.Count}`.",
    ],
    expected_output="""
Changed: Celsius
Readings Add: 20
Changed: Fahrenheit
Changed: Celsius
Readings Add: 25
Changed: Fahrenheit
Fahrenheit: 77
Total readings: 2
""",
    hint="You need `using System.ComponentModel;` and `using System.Collections.ObjectModel;`. In the `Celsius` setter: `if (_celsius == value) return; _celsius = value;` then invoke `PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(\"Celsius\"))` and again for `\"Fahrenheit\"`. Put the class at the bottom of the file, below your top-level statements.",
)

L83_SOLUTION = """
using System.Collections.ObjectModel;
using System.ComponentModel;

var t = new Thermostat();
var readings = new ObservableCollection<double>();

readings.CollectionChanged += (_, e) => Console.WriteLine($"Readings {e.Action}: {e.NewItems![0]}");
t.PropertyChanged += (_, e) =>
{
    Console.WriteLine($"Changed: {e.PropertyName}");
    if (e.PropertyName == "Celsius") readings.Add(t.Celsius);
};

t.Celsius = 20;
t.Celsius = 20;
t.Celsius = 25;

Console.WriteLine($"Fahrenheit: {t.Fahrenheit}");
Console.WriteLine($"Total readings: {readings.Count}");

public class Thermostat : INotifyPropertyChanged
{
    private double _celsius;

    public event PropertyChangedEventHandler? PropertyChanged;

    public double Celsius
    {
        get => _celsius;
        set
        {
            if (_celsius == value) return;
            _celsius = value;
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs("Celsius"));
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs("Fahrenheit"));
        }
    }

    public double Fahrenheit => Celsius * 9 / 5 + 32;
}
"""

# ─────────────────────────── 8.4 The MVVM Pattern ───────────────────────────

L84_READING = [
    h2("Why separate the UI from the logic?"),
    p("The code-behind in 8.2 mixed screen handling with real logic, which makes it hard to test and hard to reuse. **MVVM** (Model-View-ViewModel) is the standard fix for XAML apps. It splits the program into three parts with clear jobs."),
    p("The **Model** is your data and business rules, plain C# classes with no UI knowledge (a `TodoItem`, a repository that loads data). The **View** is the XAML: how things look. The **ViewModel** sits between them. It exposes the model in a shape that is convenient for the screen (properties to bind to, commands to trigger) and holds the screen's state, but it never references a control."),
    note("The XAML and WPF parts here need a Windows project. The ViewModel classes themselves, plus `INotifyPropertyChanged` and `ICommand`, are plain .NET, so the code-along and lab run here in the console. The **CommunityToolkit.Mvvm** package shown later is a NuGet package, which this in-app runner cannot install, so you will practice the hand-written version here and use the toolkit in a real project."),
    h2("ICommand: actions the View can bind to"),
    p("A button needs to run some code when clicked, but binding to a **method** is not possible. The answer is `ICommand`, an interface in `System.Windows.Input` with three members: `Execute(object?)` does the work, `CanExecute(object?)` says whether the action is currently allowed, and the `CanExecuteChanged` event tells the button to re-ask. WPF disables a button automatically while `CanExecute` returns `false`."),
    p("`ICommand` is plain .NET, not WPF-specific, so you can implement and test it anywhere. Most apps write one reusable implementation that wraps delegates. It is conventionally called `RelayCommand`."),
    code("""
using System.Windows.Input;

public class RelayCommand : ICommand
{
    private readonly Action _execute;
    private readonly Func<bool>? _canExecute;

    public RelayCommand(Action execute, Func<bool>? canExecute = null)
    {
        _execute = execute;
        _canExecute = canExecute;
    }

    public event EventHandler? CanExecuteChanged;

    public bool CanExecute(object? parameter) => _canExecute?.Invoke() ?? true;

    public void Execute(object? parameter)
    {
        if (CanExecute(parameter)) _execute();
    }

    public void NotifyCanExecuteChanged() => CanExecuteChanged?.Invoke(this, EventArgs.Empty);
}
"""),
    h2("A ViewModel in practice"),
    p("A ViewModel inherits a small base class for notifications, exposes properties, and exposes commands. When `Name` changes, it asks the command to re-evaluate `CanExecute`, so the button enables itself as soon as the user types something."),
    code("""
public class GreetingViewModel : ObservableObject
{
    private string _name = "";
    private string _greeting = "";

    public GreetingViewModel()
    {
        GreetCommand = new RelayCommand(Greet, () => Name.Trim().Length > 0);
    }

    public string Name
    {
        get => _name;
        set
        {
            if (SetProperty(ref _name, value))
                GreetCommand.NotifyCanExecuteChanged();
        }
    }

    public string Greeting
    {
        get => _greeting;
        private set => SetProperty(ref _greeting, value);
    }

    public RelayCommand GreetCommand { get; }

    private void Greet() => Greeting = $"Hello, {Name.Trim()}!";
}
"""),
    code("""
<!-- The View: bindings only, no code-behind logic -->
<StackPanel Margin="16">
    <TextBox Text="{Binding Name, UpdateSourceTrigger=PropertyChanged}" />
    <Button Content="Greet" Command="{Binding GreetCommand}" Margin="0,8" />
    <TextBlock Text="{Binding Greeting}" FontSize="18" />
</StackPanel>
"""),
    h2("The production approach: CommunityToolkit.Mvvm"),
    p("Writing `SetProperty` boilerplate for every property gets tedious. Microsoft's **CommunityToolkit.Mvvm** NuGet package (`dotnet add package CommunityToolkit.Mvvm`) uses source generators to write it for you. You mark a private field with `[ObservableProperty]` and a method with `[RelayCommand]`, and the compiler generates the public `Name` property and the `GreetCommand`. The class must be `partial` and inherit `ObservableObject`. This is what most real WPF and MAUI apps use."),
    code("""
// Requires the NuGet package CommunityToolkit.Mvvm (not runnable in this app's console runner)
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

public partial class GreetingViewModel : ObservableObject
{
    [ObservableProperty]
    [NotifyCanExecuteChangedFor(nameof(GreetCommand))]
    private string _name = "";          // generates the public property Name

    [ObservableProperty]
    private string _greeting = "";      // generates Greeting

    [RelayCommand(CanExecute = nameof(CanGreet))]
    private void Greet() => Greeting = $"Hello, {Name.Trim()}!";   // generates GreetCommand

    private bool CanGreet() => Name.Trim().Length > 0;
}
"""),
    warn("**Common mistake:** binding to the generated name incorrectly. The field is `_name` but the property you bind to in XAML is `Name`, and the command is `GreetCommand` (the method name plus `Command`), not `Greet`. Another frequent one is forgetting the `partial` keyword on the class, which makes the generator fail."),
    h2("Testing a ViewModel without any UI"),
    p("Because a ViewModel has no controls, you can test it like any other class: create it, set properties, execute commands, and assert on the results. No window needs to open. This is the biggest practical payoff of MVVM, and it is exactly what the code-along does."),
    code("""
// A unit test (xUnit style) -- no window, no UI thread
[Fact]
public void Greet_is_disabled_until_a_name_is_entered()
{
    var vm = new GreetingViewModel();
    Assert.False(vm.GreetCommand.CanExecute(null));

    vm.Name = "Ada";
    Assert.True(vm.GreetCommand.CanExecute(null));

    vm.GreetCommand.Execute(null);
    Assert.Equal("Hello, Ada!", vm.Greeting);
}
"""),
    tip("A good rule: if your ViewModel file has `using System.Windows.Controls` (or touches `MessageBox`, a `Window`, or any control), the View has leaked into it. Keep ViewModels free of UI types and they stay testable and portable between WPF, MAUI, and Avalonia."),
    link("Read more on Microsoft Learn: MVVM Toolkit introduction", "https://learn.microsoft.com/en-us/dotnet/communitytoolkit/mvvm/"),
]

L84_CODEALONG = codealong(
    title="Code Along: A ViewModel You Can Test",
    intro="You will write the base class, the command, and a ViewModel, then drive them from `Main` exactly as a unit test would. No window needed.",
    steps=[
        step(
            "Add the namespaces",
            "Put these `using` lines at the very top of `Program.cs`. `System.Windows.Input` contains `ICommand`; it is part of regular .NET, so it works in a console app.",
            """
using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Windows.Input;

Console.WriteLine("-- ViewModel test --");
""",
        ),
        step(
            "Write ObservableObject and RelayCommand",
            "Add these two classes at the **bottom** of the file. `SetProperty` updates a backing field and raises `PropertyChanged` only if the value actually changed.",
            """
public abstract class ObservableObject : INotifyPropertyChanged
{
    public event PropertyChangedEventHandler? PropertyChanged;

    protected bool SetProperty<T>(ref T field, T value, [CallerMemberName] string? name = null)
    {
        if (EqualityComparer<T>.Default.Equals(field, value)) return false;
        field = value;
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
        return true;
    }
}

public class RelayCommand : ICommand
{
    private readonly Action _execute;
    private readonly Func<bool>? _canExecute;

    public RelayCommand(Action execute, Func<bool>? canExecute = null)
    {
        _execute = execute;
        _canExecute = canExecute;
    }

    public event EventHandler? CanExecuteChanged;

    public bool CanExecute(object? parameter) => _canExecute?.Invoke() ?? true;

    public void Execute(object? parameter)
    {
        if (CanExecute(parameter)) _execute();
    }

    public void NotifyCanExecuteChanged() => CanExecuteChanged?.Invoke(this, EventArgs.Empty);
}
""",
            at="bottom",
        ),
        step(
            "Write the ViewModel",
            "Add this class at the **bottom** of the file, below the other two. Its `SayHelloCommand` is only allowed when `Name` has some text, and changing `Name` asks the command to refresh.",
            """
public class GreetingViewModel : ObservableObject
{
    private string _name = "";
    private string _greeting = "Nobody greeted yet";

    public GreetingViewModel()
    {
        SayHelloCommand = new RelayCommand(SayHello, () => Name.Trim().Length > 0);
    }

    public string Name
    {
        get => _name;
        set
        {
            if (SetProperty(ref _name, value))
                SayHelloCommand.NotifyCanExecuteChanged();
        }
    }

    public string Greeting
    {
        get => _greeting;
        private set => SetProperty(ref _greeting, value);
    }

    public RelayCommand SayHelloCommand { get; }

    private void SayHello() => Greeting = $"Hello, {Name.Trim()}!";
}
""",
            at="bottom",
        ),
        step(
            "Test it like a unit test would",
            "Add this to the top section, below the `Console.WriteLine`. You subscribe to the events a real View would, then use only properties and commands.",
            """
var vm = new GreetingViewModel();
vm.PropertyChanged += (_, e) => Console.WriteLine($"  PropertyChanged: {e.PropertyName}");
vm.SayHelloCommand.CanExecuteChanged += (_, _) => Console.WriteLine("  CanExecuteChanged raised");

Console.WriteLine($"Can say hello? {vm.SayHelloCommand.CanExecute(null)}");
vm.SayHelloCommand.Execute(null);   // ignored: CanExecute is false
Console.WriteLine($"Greeting: {vm.Greeting}");

vm.Name = "  Ada ";
Console.WriteLine($"Can say hello? {vm.SayHelloCommand.CanExecute(null)}");
vm.SayHelloCommand.Execute(null);
Console.WriteLine($"Greeting: {vm.Greeting}");
""",
        ),
    ],
)

L84_LAB = lab(
    title="Lab: Counter ViewModel with Commands",
    difficulty="Intermediate",
    description="Write a complete MVVM trio from scratch: a notifying base class, a `RelayCommand`, and a `CounterViewModel` whose commands enable and disable themselves. Then drive it with no UI, like a unit test.",
    requirements=[
        "Write `abstract class ObservableObject : INotifyPropertyChanged` with a `protected bool SetProperty<T>(ref T field, T value, [CallerMemberName] string? name = null)` that raises `PropertyChanged` only when the value changes.",
        "Write `class RelayCommand : ICommand` with a constructor `(Action execute, Func<bool>? canExecute = null)`, a `NotifyCanExecuteChanged()` method that raises `CanExecuteChanged`, and an `Execute` that does nothing when `CanExecute` is false.",
        "Write `class CounterViewModel : ObservableObject` with a constructor `CounterViewModel(int max)`, an `int Count` property (public get, private set) starting at 0, and commands `IncrementCommand`, `DecrementCommand`, and `ResetCommand`, all of type `RelayCommand`.",
        "Increment is allowed while `Count < max`, decrement while `Count > 0`, and reset is always allowed (reset sets `Count` to 0). When `Count` changes, call `NotifyCanExecuteChanged()` on the increment and decrement commands after setting the value.",
        "In top-level code create `new CounterViewModel(3)`, print `Changed: {e.PropertyName}` on each `PropertyChanged`, and count how many times `IncrementCommand.CanExecuteChanged` fires.",
        "Use a local function `Show()` that prints `Count={Count} CanIncrement={...} CanDecrement={...}`. Call it, run Increment three times, call it, run Increment once more (it must be ignored), call it, run Reset, call it, then print `IncrementCommand.CanExecuteChanged raised {n} times`.",
    ],
    expected_output="""
Count=0 CanIncrement=True CanDecrement=False
Changed: Count
Changed: Count
Changed: Count
Count=3 CanIncrement=False CanDecrement=True
Count=3 CanIncrement=False CanDecrement=True
Changed: Count
Count=0 CanIncrement=True CanDecrement=False
IncrementCommand.CanExecuteChanged raised 4 times
""",
    hint="`using System.ComponentModel; using System.Runtime.CompilerServices; using System.Windows.Input;`. Give `Count` a setter like `private set { if (SetProperty(ref _count, value)) { IncrementCommand.NotifyCanExecuteChanged(); DecrementCommand.NotifyCanExecuteChanged(); } }`. Create the commands in the constructor with lambdas such as `() => Count++` and `() => Count < max`; the `max` parameter is captured by the lambda. Put all classes at the bottom of the file.",
)

L84_SOLUTION = """
using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Windows.Input;

var vm = new CounterViewModel(3);
int canExecuteChanged = 0;
vm.PropertyChanged += (_, e) => Console.WriteLine($"Changed: {e.PropertyName}");
vm.IncrementCommand.CanExecuteChanged += (_, _) => canExecuteChanged++;

void Show() => Console.WriteLine(
    $"Count={vm.Count} CanIncrement={vm.IncrementCommand.CanExecute(null)} CanDecrement={vm.DecrementCommand.CanExecute(null)}");

Show();
vm.IncrementCommand.Execute(null);
vm.IncrementCommand.Execute(null);
vm.IncrementCommand.Execute(null);
Show();
vm.IncrementCommand.Execute(null);
Show();
vm.ResetCommand.Execute(null);
Show();
Console.WriteLine($"IncrementCommand.CanExecuteChanged raised {canExecuteChanged} times");

public abstract class ObservableObject : INotifyPropertyChanged
{
    public event PropertyChangedEventHandler? PropertyChanged;

    protected bool SetProperty<T>(ref T field, T value, [CallerMemberName] string? name = null)
    {
        if (EqualityComparer<T>.Default.Equals(field, value)) return false;
        field = value;
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
        return true;
    }
}

public class RelayCommand : ICommand
{
    private readonly Action _execute;
    private readonly Func<bool>? _canExecute;

    public RelayCommand(Action execute, Func<bool>? canExecute = null)
    {
        _execute = execute;
        _canExecute = canExecute;
    }

    public event EventHandler? CanExecuteChanged;

    public bool CanExecute(object? parameter) => _canExecute?.Invoke() ?? true;

    public void Execute(object? parameter)
    {
        if (CanExecute(parameter)) _execute();
    }

    public void NotifyCanExecuteChanged() => CanExecuteChanged?.Invoke(this, EventArgs.Empty);
}

public class CounterViewModel : ObservableObject
{
    private int _count;

    public CounterViewModel(int max)
    {
        IncrementCommand = new RelayCommand(() => Count++, () => Count < max);
        DecrementCommand = new RelayCommand(() => Count--, () => Count > 0);
        ResetCommand = new RelayCommand(() => Count = 0);
    }

    public int Count
    {
        get => _count;
        private set
        {
            if (SetProperty(ref _count, value))
            {
                IncrementCommand.NotifyCanExecuteChanged();
                DecrementCommand.NotifyCanExecuteChanged();
            }
        }
    }

    public RelayCommand IncrementCommand { get; }
    public RelayCommand DecrementCommand { get; }
    public RelayCommand ResetCommand { get; }
}
"""

# ─────────────────────────── 8.5 Building a Full App ───────────────────────────

L85_READING = [
    h2("What we are building"),
    p("Time to put everything together: a **Todo list** desktop app where you type a task, press Enter or click Add, tick tasks off, remove them, and clear the completed ones, with a live count of what is left. It uses XAML layout (8.2), data binding (8.3), and MVVM with commands (8.4)."),
    note("**Where to do this part.** The real app is a WPF project, so you need a **Windows** PC with Visual Studio and the **.NET desktop development** workload (or the .NET SDK on Windows). Nothing here runs in this app's Linux console runner. The code-along and lab below build and exercise the Model and ViewModel logic from this lesson in the console, which is the part you can test without a window."),
    h2("Project layout"),
    p("Create the project with `dotnet new wpf -n TodoApp` (or Visual Studio's WPF App template). Then add folders so each piece of MVVM has a home. The default template already gives you `App.xaml`, `MainWindow.xaml`, and `MainWindow.xaml.cs`."),
    code("""
TodoApp/
  TodoApp.csproj
  App.xaml                 (application entry; StartupUri points at MainWindow.xaml)
  MainWindow.xaml          (View)
  MainWindow.xaml.cs       (only sets DataContext)
  Models/
    TodoItem.cs            (Model: title + done flag)
  ViewModels/
    ObservableObject.cs    (from lesson 8.4)
    RelayCommand.cs        (from lesson 8.4, with a parameter)
    MainViewModel.cs       (screen state and commands)
"""),
    h2("The Model and base classes"),
    p("`ObservableObject` is the same helper as 8.4. `RelayCommand` gains an optional command parameter, because the Remove button must say **which** item to remove. The `TodoItem` is both the data and observable, so ticking a checkbox can notify the ViewModel."),
    code("""
// ViewModels/ObservableObject.cs
using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace TodoApp.ViewModels;

public abstract class ObservableObject : INotifyPropertyChanged
{
    public event PropertyChangedEventHandler? PropertyChanged;

    protected void OnPropertyChanged([CallerMemberName] string? name = null)
        => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));

    protected bool SetProperty<T>(ref T field, T value, [CallerMemberName] string? name = null)
    {
        if (EqualityComparer<T>.Default.Equals(field, value)) return false;
        field = value;
        OnPropertyChanged(name);
        return true;
    }
}

// ViewModels/RelayCommand.cs
using System.Windows.Input;

namespace TodoApp.ViewModels;

public class RelayCommand : ICommand
{
    private readonly Action<object?> _execute;
    private readonly Predicate<object?>? _canExecute;

    public RelayCommand(Action<object?> execute, Predicate<object?>? canExecute = null)
    {
        _execute = execute;
        _canExecute = canExecute;
    }

    public event EventHandler? CanExecuteChanged;

    public bool CanExecute(object? parameter) => _canExecute?.Invoke(parameter) ?? true;

    public void Execute(object? parameter)
    {
        if (CanExecute(parameter)) _execute(parameter);
    }

    public void NotifyCanExecuteChanged() => CanExecuteChanged?.Invoke(this, EventArgs.Empty);
}

// Models/TodoItem.cs
using TodoApp.ViewModels;

namespace TodoApp.Models;

public class TodoItem : ObservableObject
{
    private bool _isDone;

    public TodoItem(string title) => Title = title;

    public string Title { get; }

    public bool IsDone
    {
        get => _isDone;
        set => SetProperty(ref _isDone, value);
    }
}
"""),
    h2("The ViewModel"),
    p("The `MainViewModel` owns the `ObservableCollection<TodoItem>` and the commands. It subscribes to each item's `PropertyChanged` so the remaining count updates when a checkbox is ticked, and it unsubscribes when an item is removed so nothing is kept alive by mistake."),
    code("""
// ViewModels/MainViewModel.cs
using System.Collections.ObjectModel;
using System.Collections.Specialized;
using System.ComponentModel;
using TodoApp.Models;

namespace TodoApp.ViewModels;

public class MainViewModel : ObservableObject
{
    private string _newTitle = "";

    public MainViewModel()
    {
        Items.CollectionChanged += OnItemsChanged;
        AddCommand = new RelayCommand(_ => Add(), _ => NewTitle.Trim().Length > 0);
        RemoveCommand = new RelayCommand(item => { if (item is TodoItem t) Items.Remove(t); });
        ClearCompletedCommand = new RelayCommand(_ => ClearCompleted(), _ => Items.Any(i => i.IsDone));
    }

    public ObservableCollection<TodoItem> Items { get; } = [];

    public string NewTitle
    {
        get => _newTitle;
        set
        {
            if (SetProperty(ref _newTitle, value))
                AddCommand.NotifyCanExecuteChanged();
        }
    }

    public int RemainingCount => Items.Count(i => !i.IsDone);
    public string StatusText => $"{RemainingCount} of {Items.Count} remaining";

    public RelayCommand AddCommand { get; }
    public RelayCommand RemoveCommand { get; }
    public RelayCommand ClearCompletedCommand { get; }

    private void Add()
    {
        Items.Add(new TodoItem(NewTitle.Trim()));
        NewTitle = "";
    }

    private void ClearCompleted()
    {
        foreach (var done in Items.Where(i => i.IsDone).ToList())
            Items.Remove(done);
    }

    private void OnItemsChanged(object? sender, NotifyCollectionChangedEventArgs e)
    {
        if (e.OldItems is not null)
            foreach (TodoItem item in e.OldItems) item.PropertyChanged -= OnItemChanged;
        if (e.NewItems is not null)
            foreach (TodoItem item in e.NewItems) item.PropertyChanged += OnItemChanged;
        Refresh();
    }

    private void OnItemChanged(object? sender, PropertyChangedEventArgs e)
    {
        if (e.PropertyName == nameof(TodoItem.IsDone)) Refresh();
    }

    private void Refresh()
    {
        OnPropertyChanged(nameof(RemainingCount));
        OnPropertyChanged(nameof(StatusText));
        ClearCompletedCommand.NotifyCanExecuteChanged();
    }
}
"""),
    h2("The View: MainWindow.xaml"),
    p("The window is a three-row `Grid`: the input row, the list (which takes the remaining space), and a footer. Everything dynamic is a binding. The remove button lives inside the item template, so its command must be found on the **window's** DataContext using `RelativeSource`, and `CommandParameter=\"{Binding}\"` passes the current item."),
    code("""
<!-- MainWindow.xaml -->
<Window x:Class="TodoApp.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Todo" Height="420" Width="360">
    <Grid Margin="12">
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto" />
            <RowDefinition Height="*" />
            <RowDefinition Height="Auto" />
        </Grid.RowDefinitions>

        <DockPanel Grid.Row="0" Margin="0,0,0,8">
            <Button DockPanel.Dock="Right" Content="Add" Padding="12,4" Margin="8,0,0,0"
                    Command="{Binding AddCommand}" />
            <TextBox Text="{Binding NewTitle, UpdateSourceTrigger=PropertyChanged}" Padding="6">
                <TextBox.InputBindings>
                    <KeyBinding Key="Enter" Command="{Binding AddCommand}" />
                </TextBox.InputBindings>
            </TextBox>
        </DockPanel>

        <ListBox Grid.Row="1" ItemsSource="{Binding Items}" HorizontalContentAlignment="Stretch">
            <ListBox.ItemTemplate>
                <DataTemplate>
                    <DockPanel>
                        <Button DockPanel.Dock="Right" Content="X" Padding="6,0"
                                Command="{Binding DataContext.RemoveCommand,
                                          RelativeSource={RelativeSource AncestorType=ListBox}}"
                                CommandParameter="{Binding}" />
                        <CheckBox IsChecked="{Binding IsDone, Mode=TwoWay}" VerticalAlignment="Center" />
                        <TextBlock Text="{Binding Title}" Margin="6,0" VerticalAlignment="Center">
                            <TextBlock.Style>
                                <Style TargetType="TextBlock">
                                    <Style.Triggers>
                                        <DataTrigger Binding="{Binding IsDone}" Value="True">
                                            <Setter Property="TextDecorations" Value="Strikethrough" />
                                            <Setter Property="Foreground" Value="Gray" />
                                        </DataTrigger>
                                    </Style.Triggers>
                                </Style>
                            </TextBlock.Style>
                        </TextBlock>
                    </DockPanel>
                </DataTemplate>
            </ListBox.ItemTemplate>
        </ListBox>

        <DockPanel Grid.Row="2" Margin="0,8,0,0">
            <Button DockPanel.Dock="Right" Content="Clear completed" Padding="8,2"
                    Command="{Binding ClearCompletedCommand}" />
            <TextBlock Text="{Binding StatusText}" VerticalAlignment="Center" />
        </DockPanel>
    </Grid>
</Window>

// MainWindow.xaml.cs -- the only code-behind in the whole app
using System.Windows;
using TodoApp.ViewModels;

namespace TodoApp;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
        DataContext = new MainViewModel();
    }
}
"""),
    warn("**Common mistake:** a binding that is correct in the XAML but points at the wrong object. Inside an item template the DataContext is the **item**, not the window's ViewModel, so `{Binding RemoveCommand}` would silently fail. That is why the Remove button uses `RelativeSource` to reach back up to the `ListBox`. When a button does nothing, check Visual Studio's Output window for binding errors."),
    h2("Run it, publish it, and keep going"),
    p("Press **F5** in Visual Studio, or run `dotnet run` in the project folder, to start the app with debugging. When you are ready to give it to someone, `dotnet publish` produces a folder of files to deliver. Without `--self-contained`, the user needs the matching .NET desktop runtime installed; with `--self-contained true` the runtime is bundled, so the folder is bigger but runs anywhere on Windows."),
    code("""
# PowerShell on Windows, from the TodoApp folder
dotnet run                                  # build and start (same as F5 without the debugger)

dotnet publish -c Release -r win-x64 --self-contained false -o publish
dotnet publish -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true -o publish-single
"""),
    tip("Good next steps: save the list to a JSON file using what you learned in module 7 (load it in the ViewModel's constructor), add an edit feature, or swap the hand-written classes for CommunityToolkit.Mvvm's `[ObservableProperty]` and `[RelayCommand]` to see how much boilerplate disappears. Then look at the MAUI or Avalonia project templates and notice that your Model and ViewModel code can be reused unchanged."),
    link("Read more on Microsoft Learn: Desktop guide for WPF", "https://learn.microsoft.com/en-us/dotnet/desktop/wpf/"),
]

L85_CODEALONG = codealong(
    title="Code Along: The Todo Model and ViewModel",
    intro="You will build the same Model and `MainViewModel` as in the reading and exercise it in the console. If these classes work here, the WPF View on top of them only needs bindings.",
    steps=[
        step(
            "Add the namespaces",
            "Put these at the very top of `Program.cs`.",
            """
using System.Collections.ObjectModel;
using System.Collections.Specialized;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Windows.Input;

Console.WriteLine("-- Todo ViewModel --");
""",
        ),
        step(
            "Add the base classes",
            "Add these at the **bottom** of the file. This `RelayCommand` takes an optional parameter so a Remove command can receive the item to remove.",
            """
public abstract class ObservableObject : INotifyPropertyChanged
{
    public event PropertyChangedEventHandler? PropertyChanged;

    protected void OnPropertyChanged([CallerMemberName] string? name = null)
        => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));

    protected bool SetProperty<T>(ref T field, T value, [CallerMemberName] string? name = null)
    {
        if (EqualityComparer<T>.Default.Equals(field, value)) return false;
        field = value;
        OnPropertyChanged(name);
        return true;
    }
}

public class RelayCommand : ICommand
{
    private readonly Action<object?> _execute;
    private readonly Predicate<object?>? _canExecute;

    public RelayCommand(Action<object?> execute, Predicate<object?>? canExecute = null)
    {
        _execute = execute;
        _canExecute = canExecute;
    }

    public event EventHandler? CanExecuteChanged;

    public bool CanExecute(object? parameter) => _canExecute?.Invoke(parameter) ?? true;

    public void Execute(object? parameter)
    {
        if (CanExecute(parameter)) _execute(parameter);
    }

    public void NotifyCanExecuteChanged() => CanExecuteChanged?.Invoke(this, EventArgs.Empty);
}
""",
            at="bottom",
        ),
        step(
            "Add the Model and ViewModel",
            "Add these at the **bottom** of the file, below the base classes. The ViewModel watches each item's `IsDone` so the counts stay correct.",
            """
public class TodoItem : ObservableObject
{
    private bool _isDone;

    public TodoItem(string title) => Title = title;

    public string Title { get; }

    public bool IsDone
    {
        get => _isDone;
        set => SetProperty(ref _isDone, value);
    }
}

public class MainViewModel : ObservableObject
{
    private string _newTitle = "";

    public MainViewModel()
    {
        Items.CollectionChanged += OnItemsChanged;
        AddCommand = new RelayCommand(_ => Add(), _ => NewTitle.Trim().Length > 0);
        RemoveCommand = new RelayCommand(item => { if (item is TodoItem t) Items.Remove(t); });
        ClearCompletedCommand = new RelayCommand(_ => ClearCompleted(), _ => Items.Any(i => i.IsDone));
    }

    public ObservableCollection<TodoItem> Items { get; } = [];

    public string NewTitle
    {
        get => _newTitle;
        set
        {
            if (SetProperty(ref _newTitle, value))
                AddCommand.NotifyCanExecuteChanged();
        }
    }

    public int RemainingCount => Items.Count(i => !i.IsDone);
    public string StatusText => $"{RemainingCount} of {Items.Count} remaining";

    public RelayCommand AddCommand { get; }
    public RelayCommand RemoveCommand { get; }
    public RelayCommand ClearCompletedCommand { get; }

    private void Add()
    {
        Items.Add(new TodoItem(NewTitle.Trim()));
        NewTitle = "";
    }

    private void ClearCompleted()
    {
        foreach (var done in Items.Where(i => i.IsDone).ToList())
            Items.Remove(done);
    }

    private void OnItemsChanged(object? sender, NotifyCollectionChangedEventArgs e)
    {
        if (e.OldItems is not null)
            foreach (TodoItem item in e.OldItems) item.PropertyChanged -= OnItemChanged;
        if (e.NewItems is not null)
            foreach (TodoItem item in e.NewItems) item.PropertyChanged += OnItemChanged;
        Refresh();
    }

    private void OnItemChanged(object? sender, PropertyChangedEventArgs e)
    {
        if (e.PropertyName == nameof(TodoItem.IsDone)) Refresh();
    }

    private void Refresh()
    {
        OnPropertyChanged(nameof(RemainingCount));
        OnPropertyChanged(nameof(StatusText));
        ClearCompletedCommand.NotifyCanExecuteChanged();
    }
}
""",
            at="bottom",
        ),
        step(
            "Add and complete items",
            "Add this to the top section. The status line is printed every time `StatusText` changes, just as a bound `TextBlock` would refresh.",
            """
var vm = new MainViewModel();
vm.PropertyChanged += (_, e) =>
{
    if (e.PropertyName == nameof(MainViewModel.StatusText))
        Console.WriteLine($"  status -> {vm.StatusText}");
};

Console.WriteLine($"Can add with empty title? {vm.AddCommand.CanExecute(null)}");
foreach (var title in new[] { "Buy milk", "Write lesson", "Walk dog" })
{
    vm.NewTitle = title;
    vm.AddCommand.Execute(null);
}

vm.Items[1].IsDone = true;
Console.WriteLine($"Can clear completed? {vm.ClearCompletedCommand.CanExecute(null)}");
""",
        ),
        step(
            "Remove and clear",
            "Finish by removing one item through its command (passing the item as the parameter) and clearing the completed ones. Then print what is left.",
            """
vm.RemoveCommand.Execute(vm.Items[0]);
vm.Items[0].IsDone = true;
vm.ClearCompletedCommand.Execute(null);

Console.WriteLine($"Final: {vm.StatusText}");
foreach (var item in vm.Items)
{
    Console.WriteLine($"- {item.Title} [{(item.IsDone ? "x" : " ")}]");
}
""",
        ),
    ],
)

L85_LAB = lab(
    title="Lab: Todo List ViewModel with a Live Summary",
    difficulty="Intermediate",
    description="Build a compact Todo ViewModel from an empty file. The summary text must notify listeners whenever items are added, removed, or ticked, and you will log every summary the way a bound label would see them.",
    requirements=[
        "Create `class TodoItem : INotifyPropertyChanged` with a get-only `string Title` set by the constructor and a `bool IsDone` property that raises `PropertyChanged` (with the name `\"IsDone\"`) only when its value changes.",
        "Create `class TodoListViewModel : INotifyPropertyChanged` with a public `ObservableCollection<TodoItem> Items` and a `string Summary` property computed as `{done}/{total} done`.",
        "Add `bool Add(string title)`: if the title is null, empty, or only whitespace return `false`; otherwise add a `TodoItem` with the trimmed title and return `true`.",
        "Add `int RemoveDone()`: remove every item whose `IsDone` is true (copy them to a list first) and return how many were removed.",
        "Raise `PropertyChanged` for `\"Summary\"` whenever the collection changes (add or remove) or any item's `IsDone` changes. Hook each added item's `PropertyChanged`, and unhook removed items.",
        "In top-level code, record each `Summary` notification into a `List<string>`, then: print `Add 'Plan': {result}`, print `Add blank: {result}` for `Add(\"   \")`, add `Build` and `Ship`, mark `Plan` and `Build` done, print `Removed: {n}`, print the log joined with ` | `, then print `Remaining: ` followed by each remaining title and ` [ ]` or ` [x]`.",
    ],
    expected_output="""
Add 'Plan': True
Add blank: False
Removed: 2
0/1 done | 0/2 done | 0/3 done | 1/3 done | 2/3 done | 1/2 done | 0/1 done
Remaining: Ship [ ]
""",
    hint="Wire items inside a `CollectionChanged` handler: loop `e.NewItems` and `e.OldItems` (cast with `foreach (TodoItem item in e.NewItems)` after a null check) to add and remove an `item.PropertyChanged` handler, then raise `Summary`. Summary is `$\"{Items.Count(i => i.IsDone)}/{Items.Count} done\"`. In `RemoveDone`, call `.ToList()` before removing so you do not modify the collection while looping over it. Put classes at the bottom.",
)

L85_SOLUTION = """
using System.Collections.ObjectModel;
using System.Collections.Specialized;
using System.ComponentModel;

var vm = new TodoListViewModel();
var log = new List<string>();
vm.PropertyChanged += (_, e) =>
{
    if (e.PropertyName == "Summary") log.Add(vm.Summary);
};

Console.WriteLine($"Add 'Plan': {vm.Add("Plan")}");
Console.WriteLine($"Add blank: {vm.Add("   ")}");
vm.Add("Build");
vm.Add("Ship");
vm.Items[0].IsDone = true;
vm.Items[1].IsDone = true;
Console.WriteLine($"Removed: {vm.RemoveDone()}");
Console.WriteLine(string.Join(" | ", log));
Console.Write("Remaining:");
foreach (var item in vm.Items)
{
    Console.Write($" {item.Title} [{(item.IsDone ? "x" : " ")}]");
}
Console.WriteLine();

public class TodoItem : INotifyPropertyChanged
{
    private bool _isDone;

    public TodoItem(string title) => Title = title;

    public event PropertyChangedEventHandler? PropertyChanged;

    public string Title { get; }

    public bool IsDone
    {
        get => _isDone;
        set
        {
            if (_isDone == value) return;
            _isDone = value;
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs("IsDone"));
        }
    }
}

public class TodoListViewModel : INotifyPropertyChanged
{
    public TodoListViewModel()
    {
        Items.CollectionChanged += OnItemsChanged;
    }

    public event PropertyChangedEventHandler? PropertyChanged;

    public ObservableCollection<TodoItem> Items { get; } = [];

    public string Summary => $"{Items.Count(i => i.IsDone)}/{Items.Count} done";

    public bool Add(string title)
    {
        if (string.IsNullOrWhiteSpace(title)) return false;
        Items.Add(new TodoItem(title.Trim()));
        return true;
    }

    public int RemoveDone()
    {
        var done = Items.Where(i => i.IsDone).ToList();
        foreach (var item in done) Items.Remove(item);
        return done.Count;
    }

    private void OnItemsChanged(object? sender, NotifyCollectionChangedEventArgs e)
    {
        if (e.OldItems is not null)
            foreach (TodoItem item in e.OldItems) item.PropertyChanged -= OnItemChanged;
        if (e.NewItems is not null)
            foreach (TodoItem item in e.NewItems) item.PropertyChanged += OnItemChanged;
        RaiseSummary();
    }

    private void OnItemChanged(object? sender, PropertyChangedEventArgs e) => RaiseSummary();

    private void RaiseSummary() => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs("Summary"));
}
"""

# ─────────────────────────── Registry ───────────────────────────

LESSONS = {
    (8, 1): lesson(
        subtitle="Compare WPF, .NET MAUI, WinUI 3, and Avalonia honestly, and learn why this course builds its desktop app with WPF.",
        reading=L81_READING,
        codealong=None,
        lab=None,
    ),
    (8, 2): lesson(
        subtitle="Read and write XAML: lay out windows with Grid, StackPanel, and DockPanel, use core controls, and connect events to code-behind.",
        reading=L82_READING,
        codealong=L82_CODEALONG,
        lab=None,
    ),
    (8, 3): lesson(
        subtitle="Connect UI to data with bindings, DataContext, INotifyPropertyChanged, and ObservableCollection, and watch change notifications flow.",
        reading=L83_READING,
        codealong=L83_CODEALONG,
        lab=L83_LAB,
    ),
    (8, 4): lesson(
        subtitle="Separate Model, View, and ViewModel, build commands with ICommand, and test a ViewModel without any UI.",
        reading=L84_READING,
        codealong=L84_CODEALONG,
        lab=L84_LAB,
    ),
    (8, 5): lesson(
        subtitle="Walk through a complete WPF Todo app, from project layout to publishing, and practice its Model and ViewModel logic.",
        reading=L85_READING,
        codealong=L85_CODEALONG,
        lab=L85_LAB,
    ),
}

# Reference solutions, used only by verify_content.py (never sent to the learner).
SOLUTIONS = {
    (8, 3): L83_SOLUTION,
    (8, 4): L84_SOLUTION,
    (8, 5): L85_SOLUTION,
}
