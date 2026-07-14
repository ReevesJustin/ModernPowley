# Units and Symbols

This dictionary preserves the terminology visible in the 1961 scan separately
from normalized repository names. `verified_visual_scan` means the printed scan
was inspected; it does not mean the complete calculator operation is available.

| printed symbol/term | repository symbol | definition | original unit | internal unit | conversion | manual page | confidence | ambiguity |
|---|---|---|---|---|---|---:|---|---|
| Case Capacity / powder space | `net_capacity_water_grains` | water weight filling space available behind the seated bullet | gr water | gr water | none | 3, 8-9 | high | Manual does not print a detailed weighing fixture procedure. |
| Density of loading | `loading_density` | powder weight divided by water weight filling powder space | gr/gr | dimensionless | none | 3 | high | Historical term, not modern bulk-density metadata. |
| Grains of Powder | `charge_weight_grains` | powder charge weight | gr | gr | none | 9-11 | high | Not inferred from gross capacity. |
| Bullet Weight | `bullet_weight_grains` | projectile weight | gr | gr | none | 9 | high | none |
| diameter | `bullet_diameter_inches` | diameter used in sectional-density arithmetic | in | in | none | 9 | high | Manual says bullet diameter. |
| Sectional Density | `sectional_density` | bullet grains divided by `7000*d^2` | lb/in2 convention | dimensionless numeric convention | divide grains by 7000 | 9 | high | Printed calculator table supplies common values. |
| Ratio of Charge to Bullet Weight | `mass_ratio` | charge weight divided by bullet weight | gr/gr | dimensionless | none | 5, 9 | high | Orientation is explicit on manual p. 9. |
| bore diameter | `bore_diameter_inches` | land diameter | in | in | none | 9 | medium | Not interchangeable with groove diameter. |
| groove diameter | `groove_diameter_inches` | groove diameter | in | in | none | 9 | medium | none |
| average between bore and groove | `effective_bore_diameter_inches` | arithmetic mean used when caliber slide lacks a caliber | in | in | `(bore+groove)/2` | 9 | high | Historical approximation. |
| effective barrel length / distance bullet travels | `projectile_travel_inches` | initial seated bullet-base position to muzzle | in | in | cleaning-rod tip distance plus bullet length | 9 | high | Not nominal barrel length and not barrel minus COAL. |
| bore capacity | `barrel_volume_water_grains` | swept bore volume over projectile travel | relative scale / volume | gr-water equivalent | cubic inches times 253 | 5, 9 | medium | Manual calculator assigns relative values; repository geometry follows printed definition. |
| Expansion Ratio | `total_expansion_ratio` | total gun volume divided by case powder-space volume | ratio | dimensionless | `1 + Vb/V0` | 5 | high | `Vb/V0` alone is named `barrel_volume_ratio`, not Expansion Ratio. |
| Powder Number | unresolved original scale | IMR designation or letter selected by Arrow 2 | graphical | unavailable | none | 3-5, 9-10 | high | Exact scale boundaries are absent. |
| Muzzle Velocity | unresolved original scale | value read from Expansion Ratio-Velocity Tables | f/s | ft/s | none | 5, 9-12 | high | Tables/scales are not present in the scan. |
| Maximum Pressure | unresolved historical pressure | copper-crusher result described with `psi` wording | printed psi | unavailable | none | 4, 8 | medium | Do not convert to modern transducer PSI or generic CUP. |
| Muzzle Pressure | unresolved original estimate | muzzle-pressure scale reading | psi | unavailable | none | 6 | medium | Only isolated readings are printed. |
| bullet energy | `bullet_energy_ft_lbf` | projectile kinetic energy in examples | ft lb | ft lbf | none | 4-5 | high | Not needed for reconstructed original operations. |
