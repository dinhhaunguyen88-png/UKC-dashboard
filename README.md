# ⚓ UKC Analysis Dashboard

Interactive Under Keel Clearance (UKC) analysis tool for maritime operations at **Namdinhvu Port**.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45-red)
![Plotly](https://img.shields.io/badge/Plotly-6.3-purple)

## 🌐 Live Demo

👉 **[Open Dashboard](https://ukc-dashboard-3u4qmwbddhdugxo4miftbj.streamlit.app/)**

## ✨ Features

- **4 Interactive Charts** — UKC Area, Water Level Overview, UKC Bar Chart, Draft + UKC Combined
- **Dynamic Calculation Engine** — Change cargo, cranes, or any parameter → all charts update instantly
- **Dark Maritime Theme** — Professional navy/teal color scheme with glassmorphic cards
- **Safety Alerts** — Auto-detect UKC violations with visual warnings
- **Derived Calculations** — Cargo → Crane time → Draft changes → UKC (fully linked)

## 🚀 Run Locally

```bash
pip install streamlit plotly pandas numpy
streamlit run app.py
```

## 📊 Calculation Chain

```
Containers ÷ Crane throughput = Load/Unload time
  → Time × ΔDraft/h = Draft change
    → Draft → UKC = (Water level + |Bottom|) - Draft
      → 4 Charts update
```

## 📁 Project Structure

```
├── app.py                  # Main dashboard (UI + calculations + charts)
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml         # Dark maritime theme config
└── Test.py                 # Legacy static chart script
```

## 🔧 Parameters

| Group | Parameters |
|-------|-----------|
| 🚢 Vessel | Name, IMO, Draft (Tkt), LOA |
| 📦 Cargo | Import/Export containers |
| ⏱️ Operations | Crane rate, cranes, aux time, wait time, ΔTkt/h |
| 🌊 Port | Bottom elevation, water level, simulation hours |

## 📜 License

MIT
