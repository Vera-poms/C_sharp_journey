using System.Globalization;
using System.Runtime.CompilerServices;

// Lessons show US-formatted output ($1,250.75), so pin the culture regardless of the container locale.
internal static class __RunnerInit
{
    [ModuleInitializer]
    internal static void Init()
    {
        var us = CultureInfo.GetCultureInfo("en-US");
        CultureInfo.DefaultThreadCurrentCulture = us;
        CultureInfo.DefaultThreadCurrentUICulture = us;
        CultureInfo.CurrentCulture = us;
        CultureInfo.CurrentUICulture = us;
    }
}
