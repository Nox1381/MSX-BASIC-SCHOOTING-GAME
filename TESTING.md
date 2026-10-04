# Verification

The turbo build was verified in **WebMSX 6.0.8**, using an **NTSC MSX1 with an
8× CPU clock and 1000% simulation speed**. All 18 gameplay checks below passed
again after the turbo changes. The original build also passed at the native
3.58 MHz clock and with a **32 KB RAM configuration** before turbo tuning.
Browser playback was also checked with the actual pinned jsDelivr dependency,
not only a locally cached emulator. No physical MSX hardware was available.

The browser checks exercised the BASIC interpreter and MSX hardware emulation.
Startup, movement, and initial enemy spawning used ordinary gameplay. For
repeatable collision, healing, wave, and score-limit checks, controlled fixtures
placed enemies and set game state while the BASIC game was paused. The checks
then resumed the same BASIC code and used the MSX keyboard inputs.

| Check | Result |
| --- | --- |
| Disk BASIC loads AUTOEXEC.BAS and the full game | Passed |
| Gameplay CPU keeps its 8× turbo clock | Passed |
| Sprite 0 contains the exact requested eight bytes | Passed |
| Start screen, initial wave, five-point health display | Passed |
| Natural enemy spawning from the arena edges | Passed |
| Arrow-key movement | Passed |
| Crates block player movement | Passed |
| Pause freezes movement, counters, score, and spawning | Passed |
| Bullets kill a walker and add 10 points | Passed |
| Armored zombies survive two hits and die on the third | Passed |
| Clearing a wave awards the bonus and increases difficulty | Passed |
| Medkits heal two points and disappear | Passed |
| Contact damage grants temporary invulnerability | Passed |
| Maximum wave and score values preserve the arena border | Passed |
| Fatal contact produces the game-over menu | Passed |
| Restart resets the game and preserves the best score | Passed |
| Launcher fits a 390-pixel viewport without horizontal overflow | Passed |
| Quit restores the BASIC prompt | Passed |
| Browser runs without JavaScript exceptions | Passed |

The source validator and disk checks also passed. These checked BASIC line
numbers, line lengths, jump targets, FAT12 cluster chains, both FAT copies,
and byte-for-byte agreement between the disk's BASIC file and its source.

The faster rectangle collision tests were checked against the original tile
checks at all 43,621 integer positions in a 241 × 181 area. Every result matched.
Enemy movement first tests its combined move, then falls back to sliding along
each axis when blocked. Fire cooldown, spawning, invulnerability and medkit
lifetime were adjusted for faster play.

Five-second headless-browser benchmarks measured the following BASIC update
rates. The busy fixture used six zombies, invulnerability and held fire. These
measurements are specific to the test host; actual speed varies by browser and
device. The BASIC timer targets about 30 updates per second when the emulator
can keep up; this is not a promise of a fixed frame rate.

| Scene | Original native clock | Turbo build |
| --- | ---: | ---: |
| Empty arena | 3.0 updates/s | 12.0 updates/s |
| Six zombies and held fire | 0.4 updates/s | 10.0 updates/s |

All project files were published to `Nox1381/MSX-BASIC-SCHOOTING-GAME`.
The uploaded Git blob hashes were checked against the local files, including
the disk image and screenshot. The README's direct WebMSX link was checked
against the live GitHub-hosted disk: the title screen and first wave loaded at
the original MSX1 CPU clock, with no JavaScript exceptions.

GitHub Pages deployment is pending because secure browser sign-in was
unavailable. The complete `docs/` launcher is ready to enable from the
repository's `main` branch and `/docs` folder. The direct play link works
independently of Pages.
