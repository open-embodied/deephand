## DeepHand Hand MuJoCo

This repo contains the MuJoCo-only DeepHand whole-hand simulation.

Primary assets:

- `assets/deephand_description/deephand_whole_hand.xml`
- `assets/deephand_description/deephand_hand_urdf.urdf`
- `assets/meshes/*.stl`
- `assets/simulate_whole_hand.py`

Run the interactive viewer:

```bash
python assets/simulate_whole_hand.py
```

Run a headless smoke test:

```bash
python assets/simulate_whole_hand.py --no-viewer --steps 1000
```

The three non-thumb fingers use MJCF `equality/connect` constraints to close
the PIP-DIP linkage loops. No lookup table is used in this MuJoCo model.
