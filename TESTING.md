# Verification

The game was verified in **WebMSX 6.0.8**, using an **NTSC MSX1 at the original
3.58 MHz CPU clock**. A separate boot check used a **32 KB RAM configuration**.
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
| Gameplay CPU returns to its original clock | Passed |
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

GitHub repository creation and GitHub Pages deployment have not yet occurred.
The complete `docs/` site and deployment instructions are ready for that step.
