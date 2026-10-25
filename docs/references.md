# External references

Sources used in this project that aren't stored in this repo.

## Ukrainian schematic of the original module

- **What:** a full schematic of the waffle plate. The title block gives the module number **CZ1525RPWR012** and the date **11.12.2023**. The file path in the title block reads *"We are from Ukraine … DCDC Leaf"*. Labels are partly in Ukrainian.
- **Where:** in Angel Monera Martinez's shared Google Drive folder, `docs/ukranian sch.jpg`, alongside two photos of a replacement board watermarked **"MASTER SERVICE"**.
- **Why it isn't copied here:** it is third-party work, and we don't have its authors' permission to redistribute it.

Information from it that bears on our schematic. All of it is **unverified** until checked against the module with a meter.

| Area | What the Ukrainian schematic shows | Our status |
|---|---|---|
| Input bridge | D1–D4 25V60 | Matches (verified) |
| Input shunt | R1 and R2 in series between pad 5 and pads 8/7 | Matches RS1 + RS2 (verified) |
| PFC driver | Q205 BCX53-16 (PNP), Q204 BCX56-16 (NPN), R3 10 k, R4 43 R, C204 1 µF | Q4/Q5 part numbers TBD in our schematic |
| PFC switches | Q1–Q3 with 39 R gate resistors (R5–R7). The IGBTs are labelled IRG4BC30K-S | We identified RJP6012, so their label may be a substitution |
| Boost diodes | D5, D6 20L60U | Our D5/D6 type TBD |
| Thermistors | TH201 100 k NTC on pads 10/9; TH202 100 k NTC on pads 17/18 | Not yet in our schematic. Explains pads J15 (10/9) and p31 (17/18) |
| Full bridge | 8 × RJP6012, each with a 10 R gate resistor; per switch a 1 k gate–emitter resistor and 1 nF capacitors; freewheel diodes D20–D23 labelled STTH5R06B | Our section C is unverified |
| Gate drive pads | 21/22, 23/24, 19/20, 25/26 | Unassigned in our schematic |
| Third "shunt" block | R16 **0 Ω** on pads 16/15 (N-N1) | Our RS3. Possibly a link rather than a shunt |
| Output rectifier | D7–D16 20L60U in two series-stacked bridges | Matches (verified) |
| Off-module | L1 460 µH PFC choke, 680 µF 450 V bulk capacitor, two transformers (350 µH marked), 470 µH output chokes | For context |

## Forum threads

- *Onboard charger failed 2012 but cannot find cause*: source of the community draft schematic used for our first pass. <https://mynissanleaf.com/threads/onboard-charger-failed-2012-but-cannot-find-cause.33140/>
- *Onboard charger capacitors failed*, page 4: photos of the charger wiring and connections. <https://mynissanleaf.com/threads/onboard-charger-capacitors-failed.28009/page-4>
