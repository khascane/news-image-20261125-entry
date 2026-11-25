# THE WORLD TODAY — Wednesday, 25 November 2026

A one-page newspaper front page for the make.fun news-image bounty,
drawn entirely by hand in pure Python. No image library, no network,
no clock, no randomness: `main.py` builds the 1024×1024 PNG byte by
byte (PNG signature, IHDR, IDAT and IEND chunks with CRC32 checksums)
and every letter comes from a small 5×7 bitmap alphabet defined in
the program itself. Running it twice produces byte-identical output.

## How to run

```sh
MAKEFUN_OUTPUT_DIR=/some/dir python3 main.py
```

Without `MAKEFUN_OUTPUT_DIR` it writes `output/entry.png` next to the
program. It prints one line naming the file and its size.

## What is on the front page

**Lead story — "Pakistan's First Astronaut in Orbit".** This morning
at 05:18 Pakistan time, Pakistan Air Force pilot Muhammad Zeeshan
Ali, 40, lifted off aboard China's Shenzhou-24 spacecraft for the
Tiangong space station. He is the first Pakistani ever to orbit the
Earth, and the first foreign astronaut aboard Tiangong. He will spend
about a week in orbit running four Pakistani biotechnology
experiments. The hand-drawn illustration beside the story shows the
Shenzhou-24 rocket climbing on a tongue of flame, the Tiangong
station with its silver modules and blue solar wings, and the Earth
rising below them. A small fact box gives the launch time, the week
in orbit, and the four experiments.

**"CIA Hit by Cyber Attack".** CNN reports, citing people familiar
with the matter, that the CIA and the Office of the Director of
National Intelligence appear to have been hit by a cyber attack
touching classified information — the latest in a string of cyber
incidents against the US government, and, according to sources,
unrelated to the attack on the FBI criminal database.

**"Huawei Guilty on 10 of 12 Counts".** A US jury on 24 November
found Huawei guilty of 10 of 12 criminal charges — including bank
fraud, conspiracy to steal trade secrets and conspiracy to defraud
the US government — after a three-month trial in New York. Huawei
rejects the verdict.

**"30 Hostages Held in Cartagena".** Gunmen seized a supermarket in
Cartagena, Colombia, after a failed raid on an armoured truck. At
least 30 people are held hostage and five elderly women have been
freed, President Abelardo De La Espriella said.

**"AI Stocks Tumble".** The AI trade collapsed: the Nasdaq fell 1.5
percent, the S&P 500 0.5 percent, Nvidia about 6 percent and Micron
11 percent, while the Dow rose 0.8 percent. Selling worsened on
reports that the Trump administration is preparing higher tariffs on
China, the EU and 14 other economies. A day earlier Nvidia had
surged 31.5 percent after Jensen Huang returned as chief.

**In Brief.** President Zelenskiy confirmed Ukraine was behind
Saturday's drone attack on a Russian cargo ship in the Gulf of
Finland (Norway urged caution), and Kyiv claims it sank a Russian
warship off Libya on Monday. Houthi forces struck the tallest tower
in Riyadh, injuring eleven people. The WHO evacuated staff from a
hospital in Akwe, Ituri province, DR Congo, after three days
sheltering from heavy fighting amid the country's worst Ebola
outbreak on record — 5,775 deaths from 11,762 cases. South Korea's
Education Minister Choi Kyo-jin resigned over an exam-cheating
scandal. A 5.6-magnitude earthquake shook Koshi province in eastern
Nepal, near the Tibet border, on Tuesday at 07:17 local time. French
officials ordered the corruption case against former President
Nicolas Sarkozy and his wife Carla Bruni to court, with a first
hearing set for 1 April 2027. President Trump spared two turkeys,
Freedom and Feathers, from their Thanksgiving fate. Kim Yo-jong
threatened to close Switzerland's diplomatic office in Pyongyang in
retaliation for sanctions on a youth camp. And NATO pledged to defend
itself in space amid reports Russia is preparing to launch a
nuclear-armed satellite, possibly in December 2026.

**Markets strip (bottom).** Nasdaq −1.5%, S&P 500 −0.5%, Nvidia −6%,
Micron −11%, Dow +0.8%, Philadelphia semiconductor index −8%.

## Sources

Reuters, AP, CNN and other wire services, as credited in the footer
of the front page itself.
