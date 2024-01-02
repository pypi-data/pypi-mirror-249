import datetime


def _release_schedule() -> tuple:
    """Chromium release schedule

    https://chromiumdash.appspot.com/schedule
    """
    schedule = (
        ('Jan 28, 2025', 133),
        ('Dec 17, 2024', 132),
        ('Nov 12, 2024', 131),
        ('Oct 15, 2024', 130),
        ('Sep 17, 2024', 129),
        ('Aug 20, 2024', 128),
        ('Jul 23, 2024', 127),
        ('Jun 11, 2024', 126),
        ('May 14, 2024', 125),
        ('Apr 16, 2024', 124),
        ('Mar 19, 2024', 123),
        ('Feb 20, 2024', 122),
        ('Jan 23, 2024', 121),
        ('Dec 5, 2023', 120)
    )

    return schedule


def _major_version(now: datetime.datetime | None = None) -> int:
    """Major version of Chrome Browser"""

    if now is None:
        now = datetime.datetime.now(datetime.timezone.utc)

    schedule = _release_schedule()
    version = schedule[len(schedule)-1][1] - 1

    for item in schedule:
        if now.date() > datetime.datetime.strptime(item[0], '%b %d, %Y').date():
            version = item[1]
            break

    return version


def _unified_platform() -> str:
    """platform part of user-agent

    macOS:   'Macintosh; Intel Mac OS X 10_15_7'
    windows: 'Windows NT 10.0; Win64; x64'
    linux:   'X11; Linux x86_64'

    https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/content/common/user_agent.cc
    """
    platform = 'Macintosh; Intel Mac OS X 10_15_7'

    return platform


def user_agent(major_ver: int | None = None) -> str:
    """Return the user-agent of Chrome Browser"""

    if major_ver is None:
        major_ver = _major_version()

    agent = 'Mozilla/5.0 ({}) AppleWebKit/537.36 (KHTML, like Gecko) ' \
            'Chrome/{}.0.0.0 Safari/537.36'

    return agent.format(_unified_platform(), major_ver)
