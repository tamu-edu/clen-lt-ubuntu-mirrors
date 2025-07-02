# lt-ubuntu-mirrors

Automatic mirror list generation using the official Ubuntu mirrors.  Filters the mirrors based on region, bandwidth, and latency

## Usage

To use the mirror list, modify the sources.list to look like the following:

    deb mirror+https://raw.githubusercontent.com/tamu-edu/clen-lt-ubuntu-mirrors/main/ubuntu.list focal main restricted universe multiverse
    deb mirror+https://raw.githubusercontent.com/tamu-edu/clen-lt-ubuntu-mirrors/main/ubuntu.list focal-updates main restricted universe multiverse
    deb mirror+https://raw.githubusercontent.com/tamu-edu/clen-lt-ubuntu-mirrors/main/ubuntu.list focal-backports main restricted universe multiverse
    deb mirror+https://raw.githubusercontent.com/tamu-edu/clen-lt-ubuntu-mirrors/main/ubuntu.list focal-security main restricted universe multiverse
