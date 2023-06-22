
## GNSS 周内秒

GNSS（全球导航卫星系统）周内秒（Second of Week, SOW）是一种在 GNSS 中常见的时间表示方式。

在 GNSS 中，时间通常使用 GPS 周和周内秒来表示。GPS 周是指**从1980年1月6日开始的周数**，
而周内秒则表示在当前 GPS 周中的秒数。这种表示方式非常适合 GNSS，
因为它可以在很小的数字中精确地表示时间，这对于 GNSS 的精确时间同步来说非常重要。

**一个 GPS 周有 604800 秒**（7天 * 24小时 * 60分钟 * 60秒）。
因此，周内秒是一个从 0 到 604799 的数字，表示当前 GPS 周的哪一秒。
例如，周内秒 0 表示 GPS 周的开始（即周日的 00:00:00），而周内秒 604799 则表示 GPS 周的结束（即下一个周六的 23:59:59）。

为了将周内秒转换为常规的日期和时间，你需要知道当前的 GPS 周。
然后，你可以将周内秒除以 86400（一天的秒数）来得到天数，然后再将余数转换为小时、分钟和秒。

    // 周内秒和绝对时间，日期的转换

    #include <iostream>
    #include <chrono>
    #include <ctime>
    
    // 计算1970年1月1日到1980年1月6日的秒数
    const int difference = 315964800;
    
    // 每周的秒数
    const int secondsPerWeek = 604800;
    
    long long weekToTime(int week, int secondOfWeek)
    {
        return week * secondsPerWeek + secondOfWeek + difference;
    }
    
    std::string timeToDate(long long time)
    {
        std::time_t time_t = static_cast<std::time_t>(time);
        std::string timeString = std::ctime(&time_t);
        return timeString;
    }
