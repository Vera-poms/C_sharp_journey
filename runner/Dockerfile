FROM mcr.microsoft.com/dotnet/sdk:10.0

ENV DOTNET_NOLOGO=1 \
    DOTNET_CLI_TELEMETRY_OPTOUT=1 \
    DOTNET_SKIP_FIRST_TIME_EXPERIENCE=1 \
    DOTNET_USE_POLLING_FILE_WATCHER=0 \
    MSBUILDDISABLENODEREUSE=1 \
    ASPNETCORE_URLS=http://+:8080

# Runner service (compiled once, at image build)
WORKDIR /src
COPY service/ ./service/
RUN dotnet publish service -c Release -o /opt/runner

# Template project each submission is compiled in
COPY template/ /opt/template/

# Offline NuGet feed. The running container has no internet, so `dotnet add package` and
# `dotnet new xunit` restore from this folder. It is filled once, here, at image build time:
# the xunit template's own package versions, plus the libraries the lessons mention.
# To offer another package, add its name to the loop below and rebuild the image.
RUN set -eux; mkdir -p /opt/offline-packages /tmp/seed; cd /tmp/seed; \
    dotnet new xunit -o xunit-proj; \
    dotnet restore xunit-proj --packages /opt/offline-packages; \
    dotnet new console -o libs; cd libs; \
    for p in Humanizer CommunityToolkit.Mvvm Newtonsoft.Json; do \
        dotnet add package "$p" --package-directory /opt/offline-packages; \
    done; \
    cd /; rm -rf /tmp/seed; chmod -R a+rX /opt/offline-packages

# Unprivileged user that executes learner code
RUN useradd --create-home --shell /usr/sbin/nologin runner \
    && mkdir /work /cache && chown runner /work /cache
USER runner
ENV HOME=/home/runner

# Only the offline feed is a package source. Restored packages are unpacked under /cache,
# which compose mounts as tmpfs (the root filesystem is read-only).
RUN mkdir -p /home/runner/.nuget/NuGet && printf '%s\n' \
    '<?xml version="1.0" encoding="utf-8"?>' \
    '<configuration>' \
    '  <packageSources>' \
    '    <clear />' \
    '    <add key="offline" value="/opt/offline-packages" />' \
    '  </packageSources>' \
    '</configuration>' > /home/runner/.nuget/NuGet/NuGet.Config
ENV NUGET_PACKAGES=/cache/packages \
    NUGET_HTTP_CACHE_PATH=/cache/http \
    NUGET_PLUGINS_CACHE_PATH=/cache/plugins

# Warm the NuGet/MSBuild caches so the first learner build isn't slow
RUN cp -r /opt/template /home/runner/warm \
    && dotnet build /home/runner/warm -o /home/runner/warm/out -nologo -v q \
    && rm -rf /home/runner/warm

EXPOSE 8080
WORKDIR /work
ENTRYPOINT ["dotnet", "/opt/runner/Runner.dll"]
