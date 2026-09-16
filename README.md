# PHercParis4 absolute-winding reproduction bundle (villa #1626)

Everything needed to re-run the real-data before/after in
[villa #1626](https://github.com/ScrollPrize/villa/pull/1626): the two sealed seed-17 checkpoints,
the umbilicus, the two patches, and the three point-collection files the run actually loaded.
Assembled on request from @aviad12g.

## What it reproduces

`find_inconsistent_windings --pcl` on the frozen `[10500, 11500)` two-patch view, seed patch
`0000_mid_band_final`. At the single in-window absolute anchor (annotation winding 37, `col5`
point 97):

| arm | expected at anchor cell | native winding | difference |
|---|---:|---:|---:|
| baseline | 37 | 45 | **+8** |
| cap 0.75 | 37 | 43 | **+6** |

Before #1626 the explicit `--pcl` paths were silently filtered (`0 absolute`, `0 direct votes`)
because the diagnostic inherited the checkpoint's disabled-PCL toggle. After it, 6 absolute
collections load and the anchor is compared. `outputs/` carries the recorded baseline JSON and
stdout.

## Pinned inputs

| | value |
|---|---|
| villa commit | `1c124d53de222f882b389a1d7287eff5e48392ff` |
| scan frame | PHercParis4, `voxel_size_um 9.6`, umbilicus `coordinate_scale 1.0`, `lasagna_scale 4`, `spiral_outward_sense CW` |
| window | native z `[10500, 11500)` |
| seed (native zyx) | `[10936.452, 2740.049, 4185.588]`, grid ij `[55, 865]` |
| `max_hops` | `0` (no relative or cross-patch propagation) |
| input source | `https://dl.ash2txt.org/datasets/spiral_datasets/PHercParis4` (see `inputs/download_manifest.json`) |

**Checkpoints** — release assets on this repo, 474.7 MB each:

| file | SHA-256 |
|---|---|
| `sealed-baseline-seed17.ckpt` | `341048c2830d449e4a747a060f1c9b9817995054bf9548c8f2a7a22366d31e9c` |
| `sealed-cap075-seed17.ckpt` | `26bd5754642dc454857d9581f9006680fbda896323f84af44379d1190f360d68` |

**Inputs** — in this repo:

| file | SHA-256 |
|---|---|
| `inputs/umbilicus.json` | `c5f30b0d135c1d333f8170e592079a3d5a636e0071c0dcce560eecebb0ee2602` |
| `inputs/pcl/abs_winding.json` | `4e566731f7cbaf8f5ec843de687b3f72f4a784c40b587ebbaf544550902172c1` |
| `inputs/pcl/relative_windings.json` | `a3243511d4eb91387a9b32f4dbff11514b08c3ae36e9b2a2b8222607b4883ac1` |
| `inputs/pcl/same_windings.json` | `d9be52c5ebb42853f75f235241cbfd159738f6f34468bcd182523bc91dc91048` |

`inputs/patches/` holds `0000_mid_band_final` and `same_wrap002466_lasagna` as tifxyz.

## Two things to know

- **`inputs/spiral-scroll.json` is not served upstream.** Its own `provenance_note` says it was
  locally materialised from villa's historical production defaults for the sampler A/B. The
  values that matter are in the table above; if your loader derives them differently, that is
  the first place to look.
- **This is one anchor.** Both arms' patches were already native-strict-unsatisfied, so it
  validates the diagnostic path on real data but does not show a previously accepted false
  negative, and it cannot distinguish a global integer gauge offset from a local sheet switch.
  That limitation is in the PR too.

Full run outputs, failed attempts and hashes:
[gist bceb2ae8](https://gist.github.com/TAUIL-Abd-Elilah/bceb2ae8923aa07d309e81dabe55ec31) ·
replication protocol:
[gist 3c53376](https://gist.github.com/TAUIL-Abd-Elilah/3c53376761897c67695f75bfa663732e).

MIT · Codex assisted with the original #1626 implementation; this bundle was assembled with Claude.
