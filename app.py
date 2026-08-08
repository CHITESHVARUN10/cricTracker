"""
IPL Match Insights Dashboard — Streamlit App
Pixel-for-pixel port of the 9 Stitch HTML screens.

Design tokens extracted DIRECTLY from stitch_screens/*.html:
  primary:              #a33d23
  primary-container:    #e76f51
  secondary:            #006a60
  secondary-container:  #8cf5e4
  tertiary:             #436370
  tertiary-container:   #7797a6
  surface:              #f9f9ff
  surface-container-lowest: #ffffff
  surface-container-low:    #f0f3ff
  surface-container:        #e7eefe
  surface-container-high:   #e2e8f8
  surface-variant:      #dce2f3
  background:           #f9f9ff  (body: radial-gradient(circle,#fff9f0 0%,#ffecdb 100%))
  on-background:        #151c27
  on-surface:           #151c27
  on-surface-variant:   #57423d
  on-primary:           #ffffff
  on-primary-container: #590f00
  outline-variant:      #dec0b9
  outline:              #8a716c
  primary-fixed:        #ffdad2
  primary-fixed-dim:    #ffb4a2

  shadow-soft / shadow-ambient: box-shadow: 0px 4px 20px rgba(231,111,81,0.08)

  Fonts:
    Headlines: Archivo Narrow (32px/700, 24px/600)
    Body:      Plus Jakarta Sans (16px/400, 14px/400)
    Labels:    JetBrains Mono (14px/500 tracking 0.05em, 12px/500)
    Display:   Archivo Narrow 48px/700

  Spacing:
    gutter: 24px  md: 24px  sm: 12px  lg: 40px  xl: 64px  xs: 4px

  Border-radius:
    DEFAULT: 0.25rem  lg: 0.5rem  xl: 0.75rem

  Table: bg-surface-variant header, zebra odd:bg-surface-bright/50,
         hover: rgba(163,61,35,0.05), JetBrains Mono, right-aligned numbers
         border border-outline-variant rounded-lg
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from data_loader import load_matches, load_balls, load_players, load_teams

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IPL Match Insights",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Auto-recover sidebar if user hit the invisible collapse trap ──
# Streamlit persists collapsed state in localStorage, so a restart alone
# doesn't bring it back. This component forces it open on every load.
components.html("""
<script>
(function(){
  try{
    var pdoc = window.parent.document;
    var plocal = window.parent.localStorage;
    try{
      plocal.setItem('streamlitSidebarCollapsed','false');
      plocal.removeItem('st.sidebarCollapsed');
      // brute-force: any key that looks like sidebar collapsed -> reset
      for(var i=0;i<plocal.length;i++){
        var k=plocal.key(i);
        if(k && k.toLowerCase().indexOf('sidebar')!==-1 && plocal.getItem(k)==='true'){
          plocal.setItem(k,'false');
        }
      }
    }catch(e){}
    function forceOpen(){
      var sb = pdoc.querySelector('[data-testid="stSidebar"]');
      if(sb){
        sb.style.transform='none';
        sb.style.visibility='visible';
        sb.style.display='flex';
        sb.style.marginLeft='0';
        sb.style.width='21rem';
        sb.setAttribute('aria-expanded','true');
      }
      var expand = pdoc.querySelector('[data-testid="collapsedControl"]')
                 || pdoc.querySelector('[data-testid="stSidebarCollapsedControl"]');
      if(expand && expand.offsetParent!==null){
        expand.click();
        // after click, hide the toggle so it can't trap again
        setTimeout(function(){ expand.style.display='none'; }, 100);
      }
    }
    forceOpen();
    setTimeout(forceOpen,100);
    setTimeout(forceOpen,500);
    setTimeout(forceOpen,1500);
  }catch(e){}
})();
</script>
""", height=0, width=0)

# ─── GLOBAL CSS (extracted from stitch_screens HTML verbatim) ─────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Archivo+Narrow:ital,wght@0,400..700;1,400..700&family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&family=Plus+Jakarta+Sans:ital,wght@0,200..800;1,200..800&display=swap');

/* ── Design tokens ── */
:root {
  --primary:             #a33d23;
  --primary-container:   #e76f51;
  --secondary:           #006a60;
  --secondary-container: #8cf5e4;
  --tertiary:            #436370;
  --tertiary-container:  #7797a6;
  --surface:             #f9f9ff;
  --surface-lowest:      #ffffff;
  --surface-low:         #f0f3ff;
  --surface-container:   #e7eefe;
  --surface-high:        #e2e8f8;
  --surface-variant:     #dce2f3;
  --on-background:       #151c27;
  --on-surface:          #151c27;
  --on-surface-variant:  #57423d;
  --on-primary:          #ffffff;
  --on-primary-container:#590f00;
  --outline-variant:     #dec0b9;
  --outline:             #8a716c;
  --primary-fixed:       #ffdad2;
  --primary-fixed-dim:   #ffb4a2;
  --shadow-ambient: 0px 4px 20px rgba(231,111,81,0.08);
  --shadow-hover:   0px 8px 30px rgba(231,111,81,0.12);
}

/* ── Base resets ── */
html, body, [data-testid="stAppViewContainer"] {
  background: radial-gradient(circle, #fff9f0 0%, #ffecdb 100%) !important;
  color: #151c27 !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Hide Streamlit's black top toolbar (Deploy/Menu bar) without creating an invisible click-trap */
[data-testid="stHeader"] {
  background: transparent !important;
  pointer-events: none !important;
}
[data-testid="stHeader"] * {
  pointer-events: auto !important;
}
[data-testid="stDecoration"] {
  display: none !important;
}
[data-testid="stToolbar"] {
  display: none !important;
}
/* ── Sidebar must never be collapsible via an invisible button ── */
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"] {
  display: none !important;
  pointer-events: none !important;
}
[data-testid="stSidebar"][aria-expanded="false"] {
  transform: none !important;
  visibility: visible !important;
  display: flex !important;
  margin-left: 0 !important;
  width: 21rem !important;
}

[data-testid="stSidebar"] {
  background: #f9f9ff !important;
  border-right: 1px solid #dec0b9;
  box-shadow: var(--shadow-ambient);
}
[data-testid="stSidebar"] > div { padding: 24px 20px; }
[data-testid="stMainBlockContainer"] { padding: 16px 24px 40px 24px; }

/* ── Header / navigation ── */
.ipl-header {
  background: #f9f9ff;
  border-bottom: 1px solid #dec0b9;
  box-shadow: var(--shadow-ambient);
  padding: 0 24px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  border-radius: 0 0 0.75rem 0.75rem;
}
.ipl-logo {
  font-family: 'Archivo Narrow', sans-serif;
  font-size: 24px;
  font-weight: 700;
  color: #a33d23;
  letter-spacing: -0.01em;
}
.ipl-nav {
  display: flex;
  align-items: center;
  gap: 24px;
}
.ipl-nav a {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.05em;
  color: #436370;
  text-decoration: none;
  transition: color 0.2s ease;
}
.ipl-nav a:hover { color: #e76f51; }

/* ── Sidebar brand (from 04_venue.html sidebar) ── */
.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 4px 16px 4px;
  margin-bottom: 16px;
  border-bottom: 1px solid #dec0b9;
}
.brand-logo {
  width: 40px; height: 40px;
  border-radius: 9999px;
  background: linear-gradient(135deg, #a33d23, #e76f51);
  color: #ffffff;
  display: flex; align-items: center; justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}
.brand-text {
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-width: 0;
}
.brand-title {
  font-family: 'Archivo Narrow', sans-serif;
  font-size: 18px;
  font-weight: 700;
  color: #a33d23;
  line-height: 1.15;
}
.brand-tagline {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #57423d;
  margin-top: 3px;
  line-height: 1.2;
}

/* ── Header extras (search + icons, from 04_venue.html) ── */
.ipl-header-left {
  display: flex;
  align-items: center;
  gap: 32px;
}
.ipl-header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
.ipl-search {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #fff9f0;
  border: 1px solid #dec0b9;
  border-radius: 9999px;
  padding: 8px 16px;
  min-width: 240px;
}
.ipl-search input {
  border: none;
  outline: none;
  background: transparent;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 14px;
  color: #151c27;
  width: 100%;
}
.ipl-search input::placeholder { color: #8a716c; }
.search-icon { color: #57423d; font-size: 14px; }
.header-icon {
  font-size: 18px;
  color: #436370;
  cursor: pointer;
  transition: color 0.2s ease;
}
.header-icon:hover { color: #e76f51; }
.header-avatar {
  width: 32px; height: 32px;
  border-radius: 9999px;
  border: 2px solid transparent;
  background: #f0f3ff;
  color: #436370;
  display: flex; align-items: center; justify-content: center;
  font-size: 16px;
  transition: border-color 0.2s ease;
}
.header-avatar:hover { border-color: #e76f51; }

/* ── Page title ── */
.page-title {
  font-family: 'Archivo Narrow', sans-serif;
  font-size: 32px;
  font-weight: 700;
  line-height: 1.2;
  color: #151c27;
  margin-bottom: 4px;
}
.page-subtitle {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 18px;
  font-weight: 400;
  line-height: 1.6;
  color: #57423d;
  margin-bottom: 24px;
}

/* ── Section title ── */
.section-title {
  font-family: 'Archivo Narrow', sans-serif;
  font-size: 24px;
  font-weight: 600;
  line-height: 1.3;
  color: #151c27;
  margin-bottom: 12px;
}

/* ── Hero banner card (shell screen) ── */
.hero-card {
  background: #f9f9ff;
  border-radius: 0.75rem;
  box-shadow: var(--shadow-ambient);
  padding: 40px;
  position: relative;
  overflow: hidden;
  margin-bottom: 24px;
}
.hero-card::after {
  content: '';
  position: absolute;
  top: 0; right: 0;
  width: 256px; height: 256px;
  background: #e76f51;
  opacity: 0.05;
  border-radius: 0 0 0 100%;
}
.hero-title {
  font-family: 'Archivo Narrow', sans-serif;
  font-size: 32px;
  font-weight: 700;
  line-height: 1.2;
  color: #a33d23;
  margin-bottom: 12px;
}
.hero-subtitle {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 18px;
  font-weight: 400;
  line-height: 1.6;
  color: #57423d;
  max-width: 600px;
}

/* ── KPI card (shell screen) ── */
.kpi-card {
  background: #f9f9ff;
  border-radius: 0.75rem;
  box-shadow: var(--shadow-ambient);
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  transition: transform 0.2s ease;
}
.kpi-card:hover { transform: translateY(-4px); }
.kpi-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: #436370;
}
.kpi-value {
  font-family: 'Archivo Narrow', sans-serif;
  font-size: 48px;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.02em;
  color: #a33d23;
}
.kpi-bar-track {
  width: 100%;
  height: 4px;
  background: #dce2f3;
  border-radius: 9999px;
  overflow: hidden;
  margin-top: auto;
}
.kpi-bar-fill {
  height: 100%;
  border-radius: 9999px;
}

/* ── Content card ── */
.content-card {
  background: #f9f9ff;
  border-radius: 0.75rem;
  box-shadow: var(--shadow-ambient);
  padding: 24px;
  border: 1px solid #F1F1F1;
  margin-bottom: 24px;
}
.content-card:hover {
  box-shadow: var(--shadow-hover);
  transition: box-shadow 0.3s ease;
}
.card-title {
  font-family: 'Archivo Narrow', sans-serif;
  font-size: 24px;
  font-weight: 600;
  line-height: 1.3;
  color: #151c27;
  margin-bottom: 20px;
}
.card-section-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: #57423d;
  margin-bottom: 16px;
}

/* ── Metric card (toss/venue style) ── */
.metric-card {
  background: #ffffff;
  border: 1px solid rgba(220,226,243,0.5);
  border-radius: 0.5rem;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  box-shadow: var(--shadow-ambient);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-hover);
}
.metric-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: #57423d;
}
.metric-value {
  font-family: 'Archivo Narrow', sans-serif;
  font-size: 48px;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.02em;
  color: #151c27;
}
.metric-value .unit {
  font-size: 24px;
  font-weight: 600;
  line-height: 1.3;
  color: #57423d;
  margin-left: 4px;
}
.metric-mini-bar {
  width: 100%;
  height: 4px;
  background: #dce2f3;
  border-radius: 9999px;
  overflow: hidden;
  margin-top: 8px;
}
.metric-mini-bar .fill {
  height: 100%;
  border-radius: 9999px;
}
.metric-info {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 12px;
  color: #57423d;
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 4px;
}

/* ── Table styling (from 04_venue / 06_players / 07_insights_lab) ── */
.ipl-table-wrap {
  overflow-x: auto;
  border: 1px solid #dec0b9;
  border-radius: 0.5rem;
  background: #f9f9ff;
  margin-bottom: 16px;
}
.ipl-table {
  width: 100%;
  border-collapse: collapse;
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  font-weight: 500;
}
.ipl-table thead tr {
  background: #dce2f3;
}
.ipl-table thead th {
  padding: 12px 16px;
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: #436370;
  border-bottom: 1px solid #dec0b9;
  white-space: nowrap;
}
.ipl-table thead th.right { text-align: right; }
.ipl-table thead th.primary { color: #a33d23; }
.ipl-table tbody tr { border-bottom: 1px solid #e7eefe; }
.ipl-table tbody tr:nth-child(even) { background: rgba(249,249,255,0.5); }
.ipl-table tbody tr:hover { background: rgba(163,61,35,0.05); }
.ipl-table tbody td {
  padding: 12px 16px;
  color: #151c27;
  white-space: nowrap;
}
.ipl-table tbody td.right { text-align: right; }
.ipl-table tbody td.bold { font-weight: 700; }
.ipl-table tbody td.primary { color: #a33d23; font-weight: 700; }
.ipl-table tbody td.muted { color: #57423d; }
.ipl-table tbody td.player-name { font-family: 'Archivo Narrow', sans-serif; font-size: 18px; }

/* ── Sidebar filter label ── */
.sidebar-header {
  font-family: 'Archivo Narrow', sans-serif;
  font-size: 24px;
  font-weight: 600;
  color: #a33d23;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}
.sidebar-desc {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 14px;
  font-weight: 400;
  line-height: 1.5;
  color: #57423d;
  margin-bottom: 24px;
}
.filter-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.05em;
  color: #151c27;
  margin-bottom: 4px;
  display: block;
}

/* ── Tab panel label ── */
.tab-section-header {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 18px;
  font-weight: 600;
  color: #151c27;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid #dec0b9;
}

/* ── Horizontal bar chart (toss decision distribution) ── */
.hbar-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  font-weight: 500;
  color: #57423d;
}
.hbar-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  font-weight: 700;
  color: #151c27;
}
.hbar-track {
  width: 100%;
  height: 24px;
  background: #dce2f3;
  border-radius: 0 4px 4px 0;
  overflow: hidden;
  position: relative;
  display: flex;
  align-items: center;
}
.hbar-fill {
  height: 100%;
  border-radius: 0 4px 4px 0;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 8px;
}
.hbar-fill span {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  font-weight: 500;
  color: #ffffff;
}

/* ── Phases metric card ── */
.phase-card {
  background: #ffffff;
  border: 1px solid #dce2f3;
  border-radius: 0.75rem;
  padding: 24px;
  box-shadow: 0px 4px 20px rgba(231,111,81,0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.phase-card:hover {
  transform: translateY(-4px);
  box-shadow: 0px 8px 24px rgba(231,111,81,0.10);
}
.phase-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: #436370;
  margin-bottom: 8px;
}
.phase-value {
  font-family: 'Archivo Narrow', sans-serif;
  font-size: 48px;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.02em;
  color: #151c27;
}
.phase-unit {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 14px;
  color: #57423d;
  margin-left: 4px;
}
.phase-stat {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  font-weight: 500;
  color: #ba1a1a;
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 8px;
}

/* ── Player comparison grouped bar label ── */
.player-badge {
  display: inline-block;
  width: 12px; height: 12px;
  border-radius: 50%;
  margin-right: 4px;
  vertical-align: middle;
}

/* ── Player avatar (matchups profile pictures) ── */
.player-avatar,
.player-avatar-img {
  width: 44px; height: 44px;
  border-radius: 9999px;
  color: #ffffff;
  font-family: 'Archivo Narrow', sans-serif;
  font-size: 18px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #ffffff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.12);
  flex-shrink: 0;
}
.player-avatar-img {
  object-fit: cover;
  background: #f0f3ff;
}

/* ── Raw data expander ── */
details.raw-data summary {
  font-family: 'Archivo Narrow', sans-serif;
  font-size: 24px;
  font-weight: 600;
  color: #a33d23;
  padding: 24px;
  cursor: pointer;
  list-style: none;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid rgba(220,226,243,0.3);
}
details.raw-data { 
  background: #f9f9ff;
  border-radius: 0.75rem;
  box-shadow: var(--shadow-ambient);
  margin-top: 24px;
}

/* ── Main-area horizontal tab strip (Stitch-style nav) ── */
/* Hide Streamlit's default radio chrome; render a clean white tab bar */
[data-testid="stMainBlockContainer"] div[role="radiogroup"] {
  display: flex;
  flex-wrap: nowrap;
  align-items: stretch;
  justify-content: space-between;
  width: 100%;
  max-width: none;
  gap: 0;
  background: #ffffff;
  border: 1px solid #dec0b9;
  border-radius: 0.75rem;
  box-shadow: var(--shadow-ambient);
  padding: 6px;
  margin-bottom: 24px;
}
[data-testid="stMainBlockContainer"] div[role="radiogroup"] label {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: 1 1 0;
  min-width: 0;
  padding: 10px 8px;
  border-radius: 0.5rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.05em;
  color: #57423d;
  background: transparent;
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease;
  text-align: center;
  white-space: nowrap;
}
[data-testid="stMainBlockContainer"] div[role="radiogroup"] label:hover {
  background: #f0f3ff;
  color: #151c27;
}
[data-testid="stMainBlockContainer"] div[role="radiogroup"] label:has(input:checked) {
  background: #e7eefe;
  color: #a33d23;
  font-weight: 700;
  box-shadow: inset 0 -2px 0 #a33d23;
}
[data-testid="stMainBlockContainer"] div[role="radiogroup"] label > div:first-child {
  display: none;
}

/* ── Readability pass: force dark text on light backgrounds ── */
/* Global: prevent any element inheriting a light text color that vanishes
   against the cream/white background. Accents (terracotta/teal) stay where
   they are intentionally colored (handled below with targeted rules). */
[data-testid="stMainBlockContainer"],
[data-testid="stSidebar"] {
  color: #151c27 !important;
}
[data-testid="stMainBlockContainer"] p,
[data-testid="stMainBlockContainer"] li,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li {
  color: #151c27 !important;
}
/* Widget inner text (selects, radios, sliders, inputs) — always dark */
[data-testid="stSelectbox"] div,
[data-testid="stMultiSelect"] div,
[data-testid="stRadio"] div,
[data-testid="stCheckbox"] div,
[data-testid="stNumberInput"] div,
[data-testid="stTextInput"] div,
[data-testid="stSlider"] div {
  color: #151c27 !important;
}
/* Headings keep their design tokens but always dark enough to read */
[data-testid="stMainBlockContainer"] h1,
[data-testid="stMainBlockContainer"] h2,
[data-testid="stMainBlockContainer"] h3,
[data-testid="stMainBlockContainer"] h4 {
  color: #151c27 !important;
}
[data-testid="stMainBlockContainer"] .page-title,
[data-testid="stMainBlockContainer"] .page-subtitle,
[data-testid="stMainBlockContainer"] .card-title,
[data-testid="stMainBlockContainer"] .section-title,
[data-testid="stMainBlockContainer"] .card-section-label,
[data-testid="stMainBlockContainer"] .tab-section-header {
  color: #151c27 !important;
}
/* Custom table text */
[data-testid="stMainBlockContainer"] .ipl-table,
[data-testid="stMainBlockContainer"] .ipl-table th,
[data-testid="stMainBlockContainer"] .ipl-table td,
[data-testid="stMainBlockContainer"] .custom-table,
[data-testid="stMainBlockContainer"] .custom-table th,
[data-testid="stMainBlockContainer"] .custom-table td {
  color: #151c27 !important;
}
[data-testid="stMainBlockContainer"] .ipl-table thead th,
[data-testid="stMainBlockContainer"] .custom-table th {
  color: #436370 !important;
}
/* Metric / phase / kpi labels + values */
/* Values keep their design colors (dark #151c27 by default; terracotta
   accents set via inline style on specific cards are preserved). */
[data-testid="stMainBlockContainer"] .metric-label,
[data-testid="stMainBlockContainer"] .kpi-label,
[data-testid="stMainBlockContainer"] .phase-label {
  color: #436370 !important;
}
/* Sidebar controls (slider labels, select labels, buttons) */
[data-testid="stSidebar"] .sidebar-header,
[data-testid="stSidebar"] .sidebar-desc,
[data-testid="stSidebar"] .filter-label,
[data-testid="stSidebar"] .brand-title,
[data-testid="stSidebar"] .brand-tagline {
  color: #151c27 !important;
}
/* Streamlit widgets: any text inside select/radio/checkbox must be dark */
[data-testid="stSelectbox"] div,
[data-testid="stMultiSelect"] div,
[data-testid="stRadio"] div,
[data-testid="stCheckbox"] div,
[data-testid="stNumberInput"] div,
[data-testid="stTextInput"] div,
[data-testid="stSlider"] div {
  color: #151c27 !important;
}
/* Dropdown list + selected pill (BaseWeb) */
[data-testid="stSelectbox"] [data-baseweb="popover"] [role="listbox"] {
  background: #ffffff !important;
  color: #151c27 !important;
}
[data-testid="stSelectbox"] [data-baseweb="popover"] [role="option"] {
  color: #151c27 !important;
}
[data-testid="stSelectbox"] [data-baseweb="popover"] [role="option"]:hover,
[data-testid="stSelectbox"] [data-baseweb="popover"] [role="option"][aria-selected="true"] {
  background: #e7eefe !important;
  color: #a33d23 !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"] span,
[data-testid="stSelectbox"] [data-baseweb="select"] div {
  color: #151c27 !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"] > div {
  background: #ffffff !important;
}
/* The selected-value text itself (BaseWeb renders it as input value / span) */
[data-testid="stSelectbox"] input {
  color: #151c27 !important;
  caret-color: #151c27 !important;
}
[data-testid="stSelectbox"] input::placeholder {
  color: #8a716c !important;
  opacity: 1 !important;
}
[data-testid="stSelectbox"] [data-baseweb="tag"] span,
[data-testid="stSelectbox"] [data-baseweb="tag"] div {
  color: #151c27 !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"] [role="button"] {
  color: #151c27 !important;
}
/* Slider labels/values */
[data-testid="stSlider"] [data-baseweb="slider"] {
  color: #151c27 !important;
}
[data-testid="stSlider"] [role="slider"] {
  color: #151c27 !important;
}
/* Buttons */
button[kind="secondary"] {
  color: #151c27 !important;
  background: #ffffff !important;
  border: 1px solid #dec0b9 !important;
}
button[kind="primary"] {
  background: #e76f51 !important;
  color: #ffffff !important;
}
/* Expander text */
[data-testid="stExpander"] summary,
[data-testid="stExpander"] span {
  color: #151c27 !important;
}

/* ── Streamlit overrides ── */
[data-testid="stTabs"] [data-baseweb="tab"] {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 14px !important;
  font-weight: 500 !important;
  letter-spacing: 0.05em !important;
  color: #57423d !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
  color: #a33d23 !important;
  border-bottom-color: #a33d23 !important;
  border-bottom-width: 2px !important;
  font-weight: 700 !important;
}
[data-testid="stSelectbox"] label,
[data-testid="stMultiSelect"] label,
[data-testid="stSlider"] label {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 14px !important;
  font-weight: 500 !important;
  letter-spacing: 0.05em !important;
  color: #151c27 !important;
}
[data-testid="stSelectbox"] > div > div {
  background: #ffffff !important;
  border: 1px solid #dec0b9 !important;
  border-radius: 0.5rem !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 14px !important;
  color: #151c27 !important;
}
[data-testid="stSelectbox"] > div > div > div {
  color: #151c27 !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"] > div {
  background-color: #ffffff !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"] span {
  color: #151c27 !important;
}
/* Dropdown list (options) readability */
[data-testid="stSelectbox"] [data-baseweb="popover"] [role="listbox"] {
  background: #ffffff !important;
  color: #151c27 !important;
}
[data-testid="stSelectbox"] [data-baseweb="popover"] [role="option"] {
  color: #151c27 !important;
}
[data-testid="stSelectbox"] [data-baseweb="popover"] [role="option"]:hover,
[data-testid="stSelectbox"] [data-baseweb="popover"] [role="option"][aria-selected="true"] {
  background: #e7eefe !important;
  color: #a33d23 !important;
}
[data-testid="stSelectbox"] > div > div:focus-within {
  border-color: #a33d23 !important;
  box-shadow: 0 0 0 1px #a33d23 !important;
}
button[kind="primary"] {
  background: #e76f51 !important;
  color: #ffffff !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 14px !important;
  font-weight: 500 !important;
  border-radius: 0.5rem !important;
}
h1, h2, h3 { font-family: 'Archivo Narrow', sans-serif !important; }
</style>
""", unsafe_allow_html=True)

# ─── TOP HEADER BAR (from 01_shell.html / 04_venue.html) ──────────────────────
st.markdown("""
<div class="ipl-header">
  <div class="ipl-header-left">
    <div class="ipl-logo">IPL Insights Lab</div>
    <nav class="ipl-nav">
      <a href="#">Match Center</a>
      <a href="#">Fantasy Pro</a>
      <a href="#">Archives</a>
    </nav>
  </div>
  <div class="ipl-header-right">
    <div class="ipl-search">
      <span class="search-icon">🔍</span>
      <input placeholder="Search players, venues..." />
    </div>
    <span class="header-icon">🔔</span>
    <span class="header-icon">⚙️</span>
    <div class="header-avatar">👤</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── LOAD DATA ────────────────────────────────────────────────────────────────
with st.spinner("Loading IPL data…"):
    matches = load_matches()
    balls   = load_balls()
    players = load_players()

# Player image lookup (imgUrl from 2024_players_details.csv) for avatars
player_img = {}
if players is not None and not players.empty and "imgUrl" in players.columns:
    for _, row in players.dropna(subset=["imgUrl"]).iterrows():
        key = str(row.get("Name", "")).strip()
        if key:
            player_img[key] = str(row["imgUrl"]).strip()

# ─── SIDEBAR (from 01_shell.html / 04_venue.html) ─────────────────────────────
with st.sidebar:
    # Logo block (mirror venue screen sidebar) — aligned with the brand
    st.markdown("""
    <div class="sidebar-brand">
      <div class="brand-logo">🏏</div>
      <div class="brand-text">
        <div class="brand-title">Cricket Analytics</div>
        <div class="brand-tagline">Precision Data Engine</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Filters section
    st.markdown("""
    <div class="sidebar-header">⚙ Filters</div>
    <p class="sidebar-desc">The dashboard updates all charts, tables, and player summaries from the selected slice.</p>
    """, unsafe_allow_html=True)

    all_seasons = sorted(matches["season"].dropna().unique().astype(int))
    season_range = st.slider(
        "Season Range",
        min_value=int(min(all_seasons)),
        max_value=int(max(all_seasons)),
        value=(int(min(all_seasons)), int(max(all_seasons))),
    )

    all_venues = ["All Venues"] + sorted(matches["venue"].dropna().unique().tolist())
    sel_venue = st.selectbox("Venue", all_venues)

    all_teams = ["All Teams"] + sorted(
        pd.concat([matches["team1"], matches["team2"]]).dropna().unique().tolist()
    )
    sel_team = st.selectbox("Team", all_teams)

    st.markdown("<br>", unsafe_allow_html=True)
    st.button("Apply Filters", type="primary", use_container_width=True)

# ─── APPLY FILTERS ────────────────────────────────────────────────────────────
filt = matches[
    (matches["season"] >= season_range[0]) &
    (matches["season"] <= season_range[1])
].copy()
if sel_venue != "All Venues":
    filt = filt[filt["venue"] == sel_venue]
if sel_team != "All Teams":
    filt = filt[(filt["team1"] == sel_team) | (filt["team2"] == sel_team)]

filt_ids = set(filt["match_number"])
filt_balls = balls[balls["ID"].isin(filt_ids)]

# ─── HELPER: PLOTLY LAYOUT ────────────────────────────────────────────────────
def plotly_layout(fig, title="", height=300):
    """Apply Stitch design tokens to any Plotly figure."""
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(family="Archivo Narrow", size=18, color="#151c27"),
            x=0,
        ) if title else None,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(family="JetBrains Mono", size=12, color="#57423d"),
        margin=dict(l=8, r=8, t=32 if title else 8, b=8),
        height=height,
        showlegend=True,
        legend=dict(
            font=dict(family="JetBrains Mono", size=11, color="#57423d"),
            bgcolor="rgba(0,0,0,0)",
        ),
        xaxis=dict(
            gridcolor="#e2e8f8",
            zeroline=False,
            tickfont=dict(family="JetBrains Mono", size=11, color="#57423d"),
        ),
        yaxis=dict(
            gridcolor="#e2e8f8",
            zeroline=False,
            tickfont=dict(family="JetBrains Mono", size=11, color="#57423d"),
        ),
    )
    return fig

def bar_colors(n, primary=True):
    """Return n shades from terracotta (primary) or teal (secondary)."""
    if primary:
        scale = ["#a33d23","#c04b31","#e76f51","#f48b71","#ffb4a2","#ffdad2","#ffece8"]
    else:
        scale = ["#006a60","#007166","#2a9d8f","#6fd8c8","#8cf5e4","#c6e8f8","#e7eefe"]
    return [scale[i % len(scale)] for i in range(n)]

def render_table(rows, headers, right_cols=None, primary_col=None, player_name_col=None):
    """
    Render a styled HTML table matching Stitch designs exactly.
    headers: list of (key, label) tuples
    right_cols: set of keys to right-align
    primary_col: key whose values are bolded in primary color
    player_name_col: key rendered in Archivo Narrow 18px
    """
    right_cols = right_cols or set()
    cols_html = "".join(
        f'<th class="{"right primary" if k in right_cols and k == primary_col else ("right" if k in right_cols else "")}">{ lbl}</th>'
        for k, lbl in headers
    )
    rows_html = ""
    for row in rows:
        cells = ""
        for k, _ in headers:
            val = row.get(k, "")
            cls = "right " if k in right_cols else ""
            if k == primary_col:
                cls += "primary "
            if player_name_col and k == player_name_col:
                cls += "player-name "
            cells += f'<td class="{cls.strip()}">{val}</td>'
        rows_html += f"<tr>{cells}</tr>"
    return f"""
    <div class="ipl-table-wrap">
      <table class="ipl-table">
        <thead><tr>{cols_html}</tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>
    """

# ─── HERO CARD + KPI BAR (01_shell screen) ────────────────────────────────────
st.markdown("""
<div class="hero-card">
  <div class="hero-title">IPL Match Insights</div>
  <div class="hero-subtitle">Explore venue advantage, toss impact, team performance, and player matchups from the IPL dataset.</div>
</div>
""", unsafe_allow_html=True)

# KPI values from filtered data
total_matches  = len(filt)
total_venues   = filt["venue"].nunique()
total_teams    = pd.concat([filt["team1"], filt["team2"]]).nunique()
bat_first_wins = (filt[filt["toss_decision"] == "bat"]["winner"] == filt[filt["toss_decision"] == "bat"]["toss_winner"]).sum()
bat_first_total = len(filt[filt["toss_decision"] == "bat"])
bat_first_pct  = round(bat_first_wins / bat_first_total * 100) if bat_first_total else 0

filt_balls_1st = filt_balls[filt_balls["Innings"] == 1]
match_1st = filt_balls_1st.groupby("ID")["TotalRun"].sum()
avg_1st   = int(match_1st.mean()) if len(match_1st) else 165

kpi_data = [
    ("Matches",          f"{total_matches:,}",   "#e76f51", "100%"),
    ("Venues",           f"{total_venues}+",      "#8cf5e4", "80%"),
    ("Teams",            str(total_teams),         "#7797a6", "75%"),
    ("Batting-first wins", f"{bat_first_pct}%",   "#e76f51", f"{bat_first_pct}%"),
    ("Avg 1st inns runs",  str(avg_1st),           "#8cf5e4", "60%"),
]

cols = st.columns(5)
for col, (label, value, bar_color, bar_pct) in zip(cols, kpi_data):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
          <span class="kpi-label">{label}</span>
          <div class="kpi-value">{value}</div>
          <div class="kpi-bar-track">
            <div class="kpi-bar-fill" style="width:{bar_pct};background:{bar_color};"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── PAGE NAVIGATION — horizontal tab strip in the main area ──────────────────
# A visible, clickable nav strip (Stitch-style) sits at the top of the content
# area; the radio below it is visually replaced by the strip via CSS.
nav_selection = st.radio(
    "Page",
    ["📊 Overview", "🪙 Toss", "📍 Venue", "👥 Teams", "🙋 Players", "🔬 Insights Lab", "📈 Phases", "⚔️ Matchups"],
    index=0,
    label_visibility="collapsed",
    key="main_nav",
    horizontal=True,
)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE — OVERVIEW (02_overview.html)
# ══════════════════════════════════════════════════════════════════════════════
if nav_selection == "📊 Overview":
    st.markdown('<div class="page-title">Analytics Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Comprehensive match outcome data across seasons.</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Match outcome snapshot</div>', unsafe_allow_html=True)

        # ── Chart 1: Match Result Types (vertical bar, from 02_overview.html)
        st.markdown('<div class="card-section-label">Match Result Types</div>', unsafe_allow_html=True)
        result_counts = filt["result"].value_counts()
        result_map = {}
        for k, v in result_counts.items():
            key = str(k).strip().lower()
            if "run" in key:
                result_map["Runs"] = result_map.get("Runs", 0) + v
            elif "wicket" in key:
                result_map["Wickets"] = result_map.get("Wickets", 0) + v
            elif "tie" in key or "super" in key:
                result_map["Tie"] = result_map.get("Tie", 0) + v
            else:
                result_map["No Result"] = result_map.get("No Result", 0) + v

        labels = ["Runs", "Wickets", "Tie", "No Result"]
        values = [result_map.get(l, 0) for l in labels]
        colors_bar = ["#a33d23","#e76f51","#ffb4a2","#ffdad2"]

        fig1 = go.Figure(data=[
            go.Bar(
                x=labels, y=values,
                marker_color=colors_bar,
                marker_line_width=0,
                text=values,
                textposition="outside",
                textfont=dict(family="JetBrains Mono", size=11, color="#151c27"),
                hovertemplate="%{x}: %{y}<extra></extra>",
            )
        ])
        plotly_layout(fig1, height=260)
        fig1.update_layout(showlegend=False, bargap=0.4)
        fig1.update_traces(marker_cornerradius=4)
        st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

        # ── Bottom row: Venue win-rate + Matches per season
        c1, c2 = st.columns(2)

        with c1:
            st.markdown('<div class="card-section-label">Top Venues by Batting-First Win Rate</div>', unsafe_allow_html=True)
            vdata = filt.copy()
            bat_first = vdata[vdata["toss_decision"] == "bat"].copy()
            bat_first["bat_first_win"] = (bat_first["winner"] == bat_first["toss_winner"]).astype(int)
            venue_stats = bat_first.groupby("venue").agg(
                matches=("winner","count"),
                bat_wins=("bat_first_win","sum")
            ).reset_index()
            venue_stats["win_rate"] = venue_stats["bat_wins"] / venue_stats["matches"] * 100
            venue_stats = venue_stats[venue_stats["matches"] >= 5].sort_values("win_rate", ascending=False).head(8)

            fig_v = go.Figure(data=[
                go.Bar(
                    y=venue_stats["venue"].str[:18],
                    x=venue_stats["win_rate"].round(1),
                    orientation="h",
                    marker_color=bar_colors(len(venue_stats)),
                    marker_line_width=0,
                    text=[f"{v:.1f}%" for v in venue_stats["win_rate"]],
                    textposition="inside",
                    textfont=dict(family="JetBrains Mono", size=10, color="#ffffff"),
                    hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
                )
            ])
            plotly_layout(fig_v, height=280)
            fig_v.update_layout(showlegend=False)
            fig_v.update_xaxes(range=[0, 100], ticksuffix="%")
            st.plotly_chart(fig_v, use_container_width=True, config={"displayModeBar": False})

        with c2:
            st.markdown('<div class="card-section-label">Matches Per Season</div>', unsafe_allow_html=True)
            season_counts = filt.groupby("season").size().reset_index(name="matches")
            fig_s = go.Figure(data=[
                go.Scatter(
                    x=season_counts["season"].astype(str),
                    y=season_counts["matches"],
                    mode="lines+markers",
                    line=dict(color="#e76f51", width=3),
                    marker=dict(color="#e76f51", size=8, line=dict(color="#ffffff", width=2)),
                    hovertemplate="%{x}: %{y} matches<extra></extra>",
                )
            ])
            plotly_layout(fig_s, height=280)
            fig_s.update_layout(showlegend=False)
            st.plotly_chart(fig_s, use_container_width=True, config={"displayModeBar": False})

        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE — TOSS (03_toss.html)
# ══════════════════════════════════════════════════════════════════════════════
elif nav_selection == "🪙 Toss":
    st.markdown('<div class="page-title">Toss Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Analyzing the impact of the coin toss on match outcomes. Explore how decisions to bat or field first influence winning probabilities across historical data.</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid rgba(220,226,243,0.3);">
          <span style="color:#a33d23;font-size:28px;">🪙</span>
          <span class="card-title" style="margin-bottom:0;">Toss impact</span>
        </div>
        """, unsafe_allow_html=True)

        # 4 Metric cards (from 03_toss.html metrics row)
        toss_winner_won  = (filt["toss_winner"] == filt["winner"]).sum()
        toss_win_pct     = round(toss_winner_won / len(filt) * 100, 1) if len(filt) else 0
        field_dec  = filt[filt["toss_decision"] == "field"]
        bat_dec    = filt[filt["toss_decision"] == "bat"]
        field_wins = (field_dec["toss_winner"] == field_dec["winner"]).sum()
        bat_wins2  = (bat_dec["toss_winner"] == bat_dec["winner"]).sum()
        field_pct  = round(field_wins / len(field_dec) * 100, 1) if len(field_dec) else 0
        bat_pct2   = round(bat_wins2 / len(bat_dec) * 100, 1) if len(bat_dec) else 0

        mc1, mc2, mc3, mc4 = st.columns(4)
        with mc1:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-label">Matches</div>
              <div class="metric-value">{len(filt):,}</div>
              <div class="metric-info">Total matches analyzed</div>
            </div>
            """, unsafe_allow_html=True)
        with mc2:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-label">Toss winner match win %</div>
              <div class="metric-value">{toss_win_pct}<span class="unit">%</span></div>
              <div class="metric-mini-bar"><div class="fill" style="width:{toss_win_pct}%;background:#a33d23;"></div></div>
            </div>
            """, unsafe_allow_html=True)
        with mc3:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-label">Field decision win %</div>
              <div class="metric-value">{field_pct}<span class="unit">%</span></div>
              <div class="metric-mini-bar"><div class="fill" style="width:{field_pct}%;background:#006a60;"></div></div>
            </div>
            """, unsafe_allow_html=True)
        with mc4:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-label">Bat decision win %</div>
              <div class="metric-value">{bat_pct2}<span class="unit">%</span></div>
              <div class="metric-mini-bar"><div class="fill" style="width:{bat_pct2}%;background:#7797a6;"></div></div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Charts row (from 03_toss.html)
        cc1, cc2 = st.columns(2)

        with cc1:
            st.markdown('<div class="tab-section-header">Toss Decision Distribution</div>', unsafe_allow_html=True)
            n_bat   = len(bat_dec)
            n_field = len(field_dec)
            total   = n_bat + n_field or 1
            # horizontal bars as in Stitch HTML
            st.markdown(f"""
            <div style="padding:16px;background:#f9f9ff;border-radius:0.5rem;border:1px solid rgba(220,226,243,0.2);">
              <div style="margin-bottom:24px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                  <span class="hbar-label">Bat</span>
                  <span class="hbar-value">{n_bat:,}</span>
                </div>
                <div class="hbar-track">
                  <div class="hbar-fill" style="width:{n_bat/total*100:.1f}%;background:#66c2a5;">
                    <span>{n_bat/total*100:.1f}%</span>
                  </div>
                </div>
              </div>
              <div>
                <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                  <span class="hbar-label">Field</span>
                  <span class="hbar-value">{n_field:,}</span>
                </div>
                <div class="hbar-track">
                  <div class="hbar-fill" style="width:{n_field/total*100:.1f}%;background:#fc8d62;">
                    <span>{n_field/total*100:.1f}%</span>
                  </div>
                </div>
              </div>
              <div style="display:flex;justify-content:space-between;font-family:'JetBrains Mono',monospace;font-size:10px;color:rgba(87,66,61,0.5);margin-top:8px;padding-top:4px;border-top:1px solid rgba(220,226,243,0.2);">
                <span>0</span><span>Total: {total:,}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

        with cc2:
            st.markdown('<div class="tab-section-header">Toss-Winner Win Rate by Decision</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div style="padding:16px;background:#f9f9ff;border-radius:0.5rem;border:1px solid rgba(220,226,243,0.2);">
              <div style="margin-bottom:24px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                  <span class="hbar-label">Bat</span>
                  <span class="hbar-value">{bat_pct2}%</span>
                </div>
                <div class="hbar-track">
                  <div class="hbar-fill" style="width:{bat_pct2}%;background:linear-gradient(to right,#440154,#31688e);">
                    <span>{bat_pct2}%</span>
                  </div>
                </div>
              </div>
              <div>
                <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                  <span class="hbar-label">Field</span>
                  <span class="hbar-value">{field_pct}%</span>
                </div>
                <div class="hbar-track">
                  <div class="hbar-fill" style="width:{field_pct}%;background:linear-gradient(to right,#35b779,#fde725);">
                    <span>{field_pct}%</span>
                  </div>
                </div>
              </div>
              <div style="display:flex;justify-content:space-between;font-family:'JetBrains Mono',monospace;font-size:10px;color:rgba(87,66,61,0.5);margin-top:8px;padding-top:4px;border-top:1px solid rgba(220,226,243,0.2);">
                <span>0%</span><span>50%</span><span>100%</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE — VENUE (04_venue.html)
# ══════════════════════════════════════════════════════════════════════════════
elif nav_selection == "📍 Venue":
    # Venue selector
    venues_list = sorted(filt["venue"].dropna().unique().tolist())
    sel_v = st.selectbox("Select Venue", venues_list, key="venue_tab_sel") if venues_list else None

    if sel_v:
        venue_matches = filt[filt["venue"] == sel_v]
        v_total    = len(venue_matches)
        v_bat_dec  = venue_matches[venue_matches["toss_decision"] == "bat"]
        v_bat_wins = (v_bat_dec["winner"] == v_bat_dec["toss_winner"]).sum()
        v_bat_pct  = round(v_bat_wins / len(v_bat_dec) * 100, 1) if len(v_bat_dec) else 0
        v_chase_wins = v_total - v_bat_wins

        vm_ids = set(venue_matches["match_number"])
        vm_balls_1st = balls[(balls["ID"].isin(vm_ids)) & (balls["Innings"] == 1)]
        avg_1st_v = int(vm_balls_1st.groupby("ID")["TotalRun"].sum().mean()) if len(vm_balls_1st) else 0

        st.markdown(f'<div class="page-title">Venue Impact</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="page-subtitle">{sel_v}</div>', unsafe_allow_html=True)

        # 4 metric cards
        vm1, vm2, vm3, vm4 = st.columns(4)
        with vm1:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-label">Matches</div>
              <div class="metric-value">{v_total}</div>
              <div class="metric-mini-bar"><div class="fill" style="width:100%;background:#436370;"></div></div>
            </div>
            """, unsafe_allow_html=True)
        with vm2:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-label">Batting-first wins</div>
              <div class="metric-value" style="color:#a33d23;">{v_bat_wins}</div>
              <div class="metric-mini-bar">
                <div class="fill" style="width:{v_bat_pct}%;background:#a33d23;display:inline-block;"></div>
                <div class="fill" style="width:{100-v_bat_pct}%;background:#006a60;display:inline-block;"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        with vm3:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-label">Batting-first win rate %</div>
              <div class="metric-value">{v_bat_pct}<span class="unit">%</span></div>
            </div>
            """, unsafe_allow_html=True)
        with vm4:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-label">Avg first-innings runs</div>
              <div class="metric-value">{avg_1st_v}</div>
              <div class="metric-info">🏏 Scoring profile</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        venue_ball = balls[balls["ID"].isin(vm_ids)]
        batter_stats = venue_ball.groupby("Batter").agg(
            runs=("BatsmanRun","sum"),
            balls_faced=("BallNumber","count"),
        ).reset_index()
        batter_stats = batter_stats[batter_stats["balls_faced"] >= 10].sort_values("runs", ascending=False).head(10)

        rows_data = []
        for _, row in batter_stats.iterrows():
            rows_data.append({
                "batter": row["Batter"],
                "runs":   f'{row["runs"]:,}',
                "balls":  f'{row["balls_faced"]:,}',
            })

        vc1, vc2 = st.columns([1, 2])

        with vc1:
            with st.container(border=True):
                st.markdown('<div class="card-title">Win split at this venue</div>', unsafe_allow_html=True)
                fig_wsplit = go.Figure(data=[
                    go.Bar(
                        x=["Batting first", "Chasing"],
                        y=[v_bat_wins, v_chase_wins],
                        marker_color=["#a33d23", "#436370"],
                        marker_line_width=0,
                        text=[v_bat_wins, v_chase_wins],
                        textposition="outside",
                        textfont=dict(family="JetBrains Mono", size=13, color="#151c27"),
                        hovertemplate="%{x}: %{y}<extra></extra>",
                    )
                ])
                plotly_layout(fig_wsplit, height=340)
                fig_wsplit.update_layout(showlegend=False, bargap=0.5)
                fig_wsplit.update_traces(marker_cornerradius=4)
                st.plotly_chart(fig_wsplit, use_container_width=True, config={"displayModeBar": False})

        with vc2:
            with st.container(border=True):
                st.markdown('<div class="card-title">Top batters at this venue</div>', unsafe_allow_html=True)
                st.markdown(render_table(
                    rows_data,
                    [("batter","Batter"),("runs","Runs"),("balls","Balls")],
                    right_cols={"runs","balls"},
                    primary_col="runs",
                    player_name_col="batter",
                ), unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE — TEAMS (05_teams.html)
# ══════════════════════════════════════════════════════════════════════════════
elif nav_selection == "👥 Teams":
    all_team_names = sorted(pd.concat([filt["team1"], filt["team2"]]).dropna().unique().tolist())
    sel_t = st.selectbox("Select Team", all_team_names, key="team_tab_sel") if all_team_names else None

    if sel_t:
        t_matches = filt[(filt["team1"] == sel_t) | (filt["team2"] == sel_t)]
        t_wins    = (t_matches["winner"] == sel_t).sum()
        t_total   = len(t_matches)
        t_win_pct = round(t_wins / t_total * 100, 1) if t_total else 0

        t_bat_dec = t_matches[t_matches["toss_decision"] == "bat"]
        t_bat_wins = (t_bat_dec["winner"] == sel_t).sum()

        t_chase_dec   = t_matches[t_matches["toss_decision"] == "field"]
        t_chase_total = len(t_chase_dec)
        t_chase_wins  = (t_chase_dec["winner"] == sel_t).sum()
        t_bat_total   = len(t_bat_dec)
        t_bat_win_pct = round(t_bat_wins / t_bat_total * 100, 1) if t_bat_total else 0
        t_chase_pct   = round(t_chase_wins / t_chase_total * 100, 1) if t_chase_total else 0

        st.markdown(f'<div class="page-title">{sel_t}</div>', unsafe_allow_html=True)
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Team performance</div>', unsafe_allow_html=True)

        tm1, tm2, tm3, tm4 = st.columns(4)
        with tm1:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-value" style="color:#a33d23;">{t_total}</div>
              <div class="metric-label">Matches</div>
              <div class="metric-mini-bar"><div class="fill" style="width:100%;background:#7797a6;"></div></div>
            </div>""", unsafe_allow_html=True)
        with tm2:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-value" style="color:#a33d23;">{t_wins}</div>
              <div class="metric-label">Wins</div>
              <div class="metric-mini-bar"><div class="fill" style="width:{t_win_pct}%;background:#8cf5e4;"></div></div>
            </div>""", unsafe_allow_html=True)
        with tm3:
            st.markdown(f"""
            <div class="metric-card" style="position:relative;overflow:hidden;">
              <div class="metric-value" style="color:#e76f51;">{t_win_pct}<span class="unit">%</span></div>
              <div class="metric-label">Win rate</div>
            </div>""", unsafe_allow_html=True)
        with tm4:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-value" style="color:#a33d23;">{t_bat_wins}</div>
              <div class="metric-label">Batting-first wins</div>
              <div class="metric-mini-bar"><div class="fill" style="width:{t_bat_win_pct}%;background:#436370;"></div></div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        tc1, tc2 = st.columns([5, 7])
        with tc1:
            st.markdown('<div style="background:#f0f3ff;border-radius:0.5rem;padding:16px;border:1px solid #dce2f3;">', unsafe_allow_html=True)
            st.markdown('<div style="font-family:\'Plus Jakarta Sans\',sans-serif;font-size:16px;font-weight:600;color:#151c27;margin-bottom:24px;">Win rate by innings context</div>', unsafe_allow_html=True)
            fig_tc = go.Figure(data=[
                go.Bar(
                    x=["Bat First","Chasing"],
                    y=[t_bat_win_pct, t_chase_pct],
                    marker_color=["#e76f51","#436370"],
                    marker_line_width=0,
                    text=[f"{t_bat_win_pct}%", f"{t_chase_pct}%"],
                    textposition="outside",
                    textfont=dict(family="JetBrains Mono", size=12, color="#151c27", weight=700),
                    hovertemplate="%{x}: %{y}%<extra></extra>",
                )
            ])
            plotly_layout(fig_tc, height=240)
            fig_tc.update_layout(showlegend=False, bargap=0.5, yaxis=dict(range=[0, 110], ticksuffix="%"))
            fig_tc.update_traces(marker_cornerradius=4)
            st.plotly_chart(fig_tc, use_container_width=True, config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)

        with tc2:
            st.markdown('<div style="background:#f0f3ff;border-radius:0.5rem;padding:16px;border:1px solid #dce2f3;">', unsafe_allow_html=True)
            st.markdown('<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;"><span style="font-family:\'Plus Jakarta Sans\',sans-serif;font-size:16px;font-weight:600;color:#151c27;">Wins per season</span></div>', unsafe_allow_html=True)
            t_season = t_matches.groupby("season").apply(lambda x: (x["winner"] == sel_t).sum()).reset_index()
            t_season.columns = ["season","wins"]
            fig_ts = go.Figure(data=[
                go.Scatter(
                    x=t_season["season"].astype(str),
                    y=t_season["wins"],
                    mode="lines+markers",
                    line=dict(color="#2b4b58", width=2),
                    marker=dict(color="#ffffff", size=6, line=dict(color="#2b4b58", width=2)),
                    hovertemplate="%{x}: %{y} wins<extra></extra>",
                )
            ])
            plotly_layout(fig_ts, height=240)
            fig_ts.update_layout(showlegend=False)
            st.plotly_chart(fig_ts, use_container_width=True, config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE — PLAYERS (06_players.html)
# ══════════════════════════════════════════════════════════════════════════════
elif nav_selection == "🙋 Players":
    st.markdown('<div class="content-card">', unsafe_allow_html=True)

    # ── Section A: Player leaders header
    st.markdown("""
    <div style="margin-bottom:32px;">
      <div class="card-title">Player leaders</div>
      <p style="font-family:'Plus Jakarta Sans',sans-serif;font-size:14px;color:#57423d;margin-top:4px;">Compare individual performances and view top metrics.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Section A: Player Comparison
    st.markdown('<div class="tab-section-header">Player comparison</div>', unsafe_allow_html=True)

    pr1, pr2, pr3 = st.columns(3)
    with pr1:
        cmp_season = st.selectbox("Comparison season", ["All Seasons"] + [str(y) for y in sorted(filt["season"].dropna().unique(), reverse=True)], key="cmp_season")
    with pr2:
        cmp_team = st.selectbox("Comparison team", ["All Teams"] + sorted(pd.concat([filt["team1"], filt["team2"]]).dropna().unique().tolist()), key="cmp_team")
    with pr3:
        cmp_role = st.selectbox("Comparison role", ["All","Batter","Bowler"], key="cmp_role")

    # filter balls by selected season
    cmp_balls = filt_balls.copy()
    if cmp_season != "All Seasons":
        cmp_ids = set(filt[filt["season"] == int(cmp_season)]["match_number"])
        cmp_balls = cmp_balls[cmp_balls["ID"].isin(cmp_ids)]

    all_batters = sorted(cmp_balls["Batter"].dropna().unique().tolist())
    all_bowlers = sorted(cmp_balls["Bowler"].dropna().unique().tolist())

    def _player_img_html(name):
        if not name:
            return ""
        url = player_img.get(name.strip())
        if url:
            return f'<img class="player-avatar-img" src="{url}" alt="{name}" referrerpolicy="no-referrer" />'
        initials = "".join(p[0] for p in name.replace(".", " ").split()[:2]).upper() or "?"
        bg = f"hsl({(hash(name) % 360)}, 55%, 45%)"
        return f'<div class="player-avatar" style="background:{bg};">{initials}</div>'

    pc1, pc2 = st.columns(2)
    with pc1:
        p1 = st.selectbox("🟠 Player 1", all_batters, index=0, key="p1_sel")
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:10px;margin-top:8px;">{_player_img_html(p1)}'
            f'<span class="filter-label">{p1}</span></div>',
            unsafe_allow_html=True,
        )
    with pc2:
        default_p2_idx = 1 if len(all_batters) > 1 else 0
        p2 = st.selectbox("🟢 Player 2", all_batters, index=default_p2_idx, key="p2_sel")
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:10px;margin-top:8px;">{_player_img_html(p2)}'
            f'<span class="filter-label">{p2}</span></div>',
            unsafe_allow_html=True,
        )

    def get_batter_stats(name, ball_df):
        b = ball_df[ball_df["Batter"] == name]
        runs  = int(b["BatsmanRun"].sum())
        balls_f = len(b)
        sr    = round(runs / balls_f * 100, 2) if balls_f else 0
        outs  = ball_df[(ball_df["PlayerOut"] == name) & (ball_df["IsWicketDelivery"] == 1)]
        dismissals = len(outs)
        avg   = round(runs / dismissals, 2) if dismissals else runs
        fours = int(b[b["BatsmanRun"] == 4].shape[0])
        sixes = int(b[b["BatsmanRun"] == 6].shape[0])
        return {"Runs":runs,"SR":sr,"Avg":avg,"4s":fours,"6s":sixes,"Balls":balls_f}

    def get_bowler_stats(name, ball_df):
        b = ball_df[ball_df["Bowler"] == name]
        wkts = int(ball_df[(ball_df["Bowler"] == name) & (ball_df["IsWicketDelivery"] == 1)].shape[0])
        runs_given = int(b["TotalRun"].sum())
        balls_b = len(b[b["ExtraType"].isna() | (b["ExtraType"] == "")])
        econ = round(runs_given / (balls_b / 6), 2) if balls_b else 0
        return {"Wickets":wkts,"Economy":econ,"Runs":runs_given}

    s1 = get_batter_stats(p1, cmp_balls)
    s2 = get_batter_stats(p2, cmp_balls)

    # Grouped bar chart (06_players.html)
    metrics_keys = ["Runs","SR","Avg","4s","6s"]
    fig_cmp = go.Figure()
    fig_cmp.add_trace(go.Bar(
        name=p1,
        x=metrics_keys,
        y=[s1[k] for k in metrics_keys],
        marker_color="#e76f51",
        marker_line_width=0,
        text=[str(s1[k]) for k in metrics_keys],
        textposition="outside",
        textfont=dict(family="JetBrains Mono", size=10, color="#151c27"),
    ))
    fig_cmp.add_trace(go.Bar(
        name=p2,
        x=metrics_keys,
        y=[s2[k] for k in metrics_keys],
        marker_color="#8cf5e4",
        marker_line_width=0,
        text=[str(s2[k]) for k in metrics_keys],
        textposition="outside",
        textfont=dict(family="JetBrains Mono", size=10, color="#151c27"),
    ))
    plotly_layout(fig_cmp, title="Player comparison", height=280)
    fig_cmp.update_layout(barmode="group", bargroupgap=0.1, bargap=0.4)
    fig_cmp.update_traces(marker_cornerradius=4)
    st.plotly_chart(fig_cmp, use_container_width=True, config={"displayModeBar": False})

    # Comparison table (06_players.html)
    cmp_rows = [
        {"metric":"Batting runs",    "p1":str(s1["Runs"]),  "p2":str(s2["Runs"])},
        {"metric":"Strike rate",     "p1":str(s1["SR"]),    "p2":str(s2["SR"])},
        {"metric":"Batting average", "p1":str(s1["Avg"]),   "p2":str(s2["Avg"])},
        {"metric":"4s",              "p1":str(s1["4s"]),    "p2":str(s2["4s"])},
        {"metric":"6s",              "p1":str(s1["6s"]),    "p2":str(s2["6s"])},
    ]
    tbl_html = f"""
    <div class="ipl-table-wrap">
      <table class="ipl-table">
        <thead><tr>
          <th>Metric</th>
          <th class="right"><span class="player-badge" style="background:#e76f51;"></span> {p1}</th>
          <th class="right"><span class="player-badge" style="background:#8cf5e4;"></span> {p2}</th>
        </tr></thead>
        <tbody>
    """
    for row in cmp_rows:
        tbl_html += f"<tr><td class='bold'>{row['metric']}</td><td class='right bold'>{row['p1']}</td><td class='right muted'>{row['p2']}</td></tr>"
    tbl_html += "</tbody></table></div>"
    st.markdown(tbl_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Section B: Leaderboards
    st.markdown('<div class="tab-section-header">Leaderboards</div>', unsafe_allow_html=True)
    lb1, lb2 = st.columns(2)

    with lb1:
        st.markdown('<div style="font-family:\'Plus Jakarta Sans\',sans-serif;font-size:16px;font-weight:600;color:#a33d23;margin-bottom:12px;display:flex;align-items:center;gap:8px;">🏏 Batting leaders</div>', unsafe_allow_html=True)
        batt_lb = cmp_balls.groupby("Batter").agg(
            runs=("BatsmanRun","sum"),
            balls_f=("BallNumber","count"),
            fours=("BatsmanRun", lambda x: (x == 4).sum()),
            sixes=("BatsmanRun", lambda x: (x == 6).sum()),
        ).reset_index()
        batt_lb["sr"] = (batt_lb["runs"] / batt_lb["balls_f"] * 100).round(2)
        batt_lb = batt_lb[batt_lb["balls_f"] >= 20].sort_values("runs", ascending=False).head(10)

        rows_bl = []
        for _, r in batt_lb.iterrows():
            rows_bl.append({
                "batter": r["Batter"], "runs": f'{int(r["runs"]):,}',
                "balls": f'{int(r["balls_f"]):,}', "sr": f'{r["sr"]:.2f}',
                "fours": str(int(r["fours"])), "sixes": str(int(r["sixes"])),
            })
        st.markdown(render_table(
            rows_bl,
            [("batter","Batter"),("runs","Runs"),("balls","Balls"),("sr","SR"),("fours","4s"),("sixes","6s")],
            right_cols={"runs","balls","sr","fours","sixes"},
            primary_col="runs",
        ), unsafe_allow_html=True)

    with lb2:
        st.markdown('<div style="font-family:\'Plus Jakarta Sans\',sans-serif;font-size:16px;font-weight:600;color:#a33d23;margin-bottom:12px;display:flex;align-items:center;gap:8px;">⚾ Bowling leaders</div>', unsafe_allow_html=True)
        bowl_lb = cmp_balls[cmp_balls["IsWicketDelivery"] == 1].groupby("Bowler").size().reset_index(name="wickets")
        ball_totals = cmp_balls.groupby("Bowler")["TotalRun"].agg(["sum","count"]).reset_index()
        ball_totals.columns = ["Bowler","runs_c","balls_c"]
        bowl_lb = bowl_lb.merge(ball_totals, on="Bowler", how="left")
        bowl_lb["econ"] = (bowl_lb["runs_c"] / (bowl_lb["balls_c"] / 6)).round(2)
        bowl_lb = bowl_lb[bowl_lb["balls_c"] >= 60].sort_values("wickets", ascending=False).head(10)

        rows_bwl = []
        for _, r in bowl_lb.iterrows():
            rows_bwl.append({
                "bowler": r["Bowler"], "wkts": str(int(r["wickets"])),
                "balls": f'{int(r["balls_c"]):,}', "runs": f'{int(r["runs_c"]):,}',
                "econ": f'{r["econ"]:.2f}',
            })
        st.markdown(render_table(
            rows_bwl,
            [("bowler","Bowler"),("wkts","Wickets"),("balls","Balls"),("runs","Runs"),("econ","Econ")],
            right_cols={"wkts","balls","runs","econ"},
            primary_col="wkts",
        ), unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE — INSIGHTS LAB (07_insights_lab.html)
# ══════════════════════════════════════════════════════════════════════════════
elif nav_selection == "🔬 Insights Lab":
    st.markdown('<div class="page-title">Insights Lab</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Venue deep dive, team comparison, and player form tracker in one place.</div>', unsafe_allow_html=True)

    ic1, ic2 = st.columns(2)

    # ── Left: Venue deep dive
    with ic1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🏟 Venue deep dive</div>', unsafe_allow_html=True)

        # Horizontal bar chart for venues (cividis-ish colors)
        vstat = filt.copy()
        bat_fv = vstat[vstat["toss_decision"] == "bat"]
        bat_fv2 = bat_fv.copy()
        bat_fv2["win"] = (bat_fv2["winner"] == bat_fv2["toss_winner"]).astype(int)
        vg = bat_fv2.groupby("venue").agg(matches=("win","count"), wins=("win","sum")).reset_index()
        vg["wr"] = vg["wins"] / vg["matches"] * 100
        vg = vg[vg["matches"] >= 5].sort_values("wr", ascending=True).head(8)

        cividis = ["#00204d","#31446b","#666970","#958f78","#cbbe72","#ffea46","#fde725","#ffffa5"]
        fig_vdd = go.Figure(data=[
            go.Bar(
                y=vg["venue"].str[:18],
                x=vg["wr"].round(1),
                orientation="h",
                marker_color=cividis[:len(vg)],
                marker_line_width=0,
                text=[f"{v:.1f}%" for v in vg["wr"]],
                textposition="inside",
                textfont=dict(size=10, color="#ffffff"),
                hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
            )
        ])
        plotly_layout(fig_vdd, height=260)
        fig_vdd.update_layout(showlegend=False)
        fig_vdd.update_xaxes(range=[0,100], ticksuffix="%")
        st.plotly_chart(fig_vdd, use_container_width=True, config={"displayModeBar": False})

        # Venue table
        vg_full = bat_fv2.groupby("venue").agg(matches=("win","count"), wins=("win","sum")).reset_index()
        vg_full["wr"] = vg_full["wins"] / vg_full["matches"] * 100
        vg_full["chase_wins"] = vg_full["matches"] - vg_full["wins"]
        # avg 1st inns
        inn1_avg = filt_balls[filt_balls["Innings"]==1].groupby("ID")["TotalRun"].sum().reset_index()
        inn1_avg = inn1_avg.merge(filt[["match_number","venue"]], left_on="ID", right_on="match_number")
        inn1_avg_v = inn1_avg.groupby("venue")["TotalRun"].mean().reset_index()
        inn1_avg_v.columns = ["venue","avg1st"]
        vg_full = vg_full.merge(inn1_avg_v, on="venue", how="left")
        vg_full = vg_full[vg_full["matches"] >= 5].sort_values("matches", ascending=False).head(4)

        rows_vt = []
        for _, r in vg_full.iterrows():
            rows_vt.append({
                "v": str(r["venue"])[:16], "m": str(int(r["matches"])),
                "bw": str(int(r["wins"])), "cw": str(int(r["chase_wins"])),
                "wr": f'{r["wr"]:.1f}%', "avg1": str(int(r["avg1st"])) if pd.notna(r.get("avg1st")) else "-",
            })
        st.markdown(render_table(
            rows_vt,
            [("v","Venue"),("m","Matches"),("bw","Bat 1st Wins"),("cw","Chase Wins"),("wr","Bat 1st WR"),("avg1","Avg 1st Inn")],
            right_cols={"m","bw","cw","wr","avg1"},
            primary_col="wr",
        ), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Right: Team comparison
    with ic2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">👥 Team comparison</div>', unsafe_allow_html=True)

        team_names_ins = sorted(pd.concat([filt["team1"],filt["team2"]]).dropna().unique().tolist())
        tcmp1, tcmp2 = st.columns(2)
        with tcmp1:
            ins_t1 = st.selectbox("Team A", team_names_ins, index=0, key="ins_t1")
        with tcmp2:
            ins_t2 = st.selectbox("Team B", team_names_ins, index=min(1,len(team_names_ins)-1), key="ins_t2")

        def team_kpi(team):
            tm = filt[(filt["team1"]==team)|(filt["team2"]==team)]
            wins = (tm["winner"]==team).sum()
            total = len(tm)
            bat = tm[tm["toss_decision"]=="bat"]
            bat_w = (bat["winner"]==team).sum()
            chase = tm[tm["toss_decision"]=="field"]
            chase_w = (chase["winner"]==team).sum()
            return {
                "team":team, "mat":total, "wins":wins,
                "bat1w":int(bat_w), "chasew":int(chase_w),
                "wr": round(wins/total*100,1) if total else 0,
                "bat1wr": round(bat_w/len(bat)*100,1) if len(bat) else 0,
                "chasewr": round(chase_w/len(chase)*100,1) if len(chase) else 0,
            }

        k1 = team_kpi(ins_t1)
        k2 = team_kpi(ins_t2)

        metrics_t = ["Overall WR","Bat 1st WR","Chase WR"]
        fig_tcmp = go.Figure()
        fig_tcmp.add_trace(go.Bar(
            name=ins_t1, x=metrics_t,
            y=[k1["wr"],k1["bat1wr"],k1["chasewr"]],
            marker_color="#a33d23", marker_line_width=0,
            text=[f"{v}%" for v in [k1["wr"],k1["bat1wr"],k1["chasewr"]]],
            textposition="outside",
        ))
        fig_tcmp.add_trace(go.Bar(
            name=ins_t2, x=metrics_t,
            y=[k2["wr"],k2["bat1wr"],k2["chasewr"]],
            marker_color="#436370", marker_line_width=0,
            text=[f"{v}%" for v in [k2["wr"],k2["bat1wr"],k2["chasewr"]]],
            textposition="outside",
        ))
        plotly_layout(fig_tcmp, height=260)
        fig_tcmp.update_layout(barmode="group", bargroupgap=0.1, bargap=0.4, yaxis=dict(ticksuffix="%"))
        fig_tcmp.update_traces(marker_cornerradius=4)
        st.plotly_chart(fig_tcmp, use_container_width=True, config={"displayModeBar": False})

        rows_tc = [
            {"t":"Team","m":"Mat","w":"Wins","b1w":"Bat 1st W","cw":"Chase W","wr":"WR","b1wr":"Bat 1st WR","cwr":"Chase WR"},
        ]
        rows_tc2 = [
            {"t":k1["team"],"m":str(k1["mat"]),"w":str(k1["wins"]),"b1w":str(k1["bat1w"]),"cw":str(k1["chasew"]),"wr":f'{k1["wr"]}%',"b1wr":f'{k1["bat1wr"]}%',"cwr":f'{k1["chasewr"]}%'},
            {"t":k2["team"],"m":str(k2["mat"]),"w":str(k2["wins"]),"b1w":str(k2["bat1w"]),"cw":str(k2["chasew"]),"wr":f'{k2["wr"]}%',"b1wr":f'{k2["bat1wr"]}%',"cwr":f'{k2["chasewr"]}%'},
        ]
        st.markdown(render_table(
            rows_tc2,
            [("t","Team"),("m","Mat"),("w","Wins"),("b1w","Bat 1st W"),("cw","Chase W"),("wr","WR"),("b1wr","Bat 1st WR"),("cwr","Chase WR")],
            right_cols={"m","w","b1w","cw","wr","b1wr","cwr"},
            primary_col="wr",
        ), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Player form tracker
    st.markdown('<hr style="border-color:rgba(220,226,243,0.3);margin:32px 0;">', unsafe_allow_html=True)
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🏃 Player form tracker</div>', unsafe_allow_html=True)

    all_pnames = sorted(filt_balls["Batter"].dropna().unique().tolist())
    form_player = st.selectbox("Search player", all_pnames, key="form_player")

    pform_balls = filt_balls[filt_balls["Batter"] == form_player]
    pform_ids = pform_balls["ID"].unique()
    pform_matches = filt[filt["match_number"].isin(pform_ids)].copy()
    pform_matches = pform_matches.sort_values("season")

    # line chart: runs per season
    pform_season = pform_balls.merge(filt[["match_number","season"]], left_on="ID", right_on="match_number", how="left")
    pform_runs = pform_season.groupby("season")["BatsmanRun"].sum().reset_index()

    fc1, fc2 = st.columns([2, 1])
    with fc1:
        fig_pf = go.Figure()
        fig_pf.add_trace(go.Scatter(
            x=pform_runs["season"].astype(str), y=pform_runs["BatsmanRun"],
            mode="lines+markers",
            name="Runs",
            line=dict(color="#e76f51", width=2),
            marker=dict(color="#ffffff", size=4, line=dict(color="#e76f51", width=2)),
        ))
        plotly_layout(fig_pf, height=260)
        st.plotly_chart(fig_pf, use_container_width=True, config={"displayModeBar": False})

        # Season stats table
        outs_by_season = filt_balls[(filt_balls["PlayerOut"]==form_player) & (filt_balls["IsWicketDelivery"]==1)]
        outs_by_season2 = outs_by_season.merge(filt[["match_number","season"]], left_on="ID", right_on="match_number", how="left")
        outs_s = outs_by_season2.groupby("season").size().reset_index(name="dismissals")
        pform_runs2 = pform_season.groupby("season").agg(runs=("BatsmanRun","sum"), balls=("BallNumber","count")).reset_index()
        pform_runs2 = pform_runs2.merge(outs_s, on="season", how="left").fillna(0)
        pform_runs2["sr"] = (pform_runs2["runs"] / pform_runs2["balls"] * 100).round(1)

        rows_pf = []
        for _, r in pform_runs2.sort_values("season", ascending=False).head(6).iterrows():
            rows_pf.append({
                "season":str(int(r["season"])), "runs":str(int(r["runs"])),
                "balls":str(int(r["balls"])), "sr":str(r["sr"]),
                "wkts":str(int(r["dismissals"])), "econ":"-",
            })
        st.markdown(render_table(
            rows_pf,
            [("season","Season"),("runs","Runs"),("balls","Balls"),("sr","Strike Rate"),("wkts","Wickets"),("econ","Economy")],
            right_cols={"runs","balls","sr","wkts","econ"},
            primary_col="runs",
        ), unsafe_allow_html=True)

    with fc2:
        # Recent innings mini-table
        st.markdown('<div class="card-section-label" style="background:#f0f3ff;padding:8px 16px;border-radius:4px 4px 0 0;border-bottom:1px solid #dce2f3;">Recent batting innings (Last 10)</div>', unsafe_allow_html=True)
        recent_innings = pform_season.merge(
            filt[["match_number","match_date","venue"]], left_on="ID", right_on="match_number", how="left"
        )
        recent_by_match = recent_innings.groupby(["ID","match_date","venue"]).agg(
            runs=("BatsmanRun","sum"),
            team_total=("TotalRun","sum"),
        ).reset_index().sort_values("match_date", ascending=False).head(10)

        ri_rows = []
        for _, r in recent_by_match.iterrows():
            dt = str(r["match_date"])[:10] if pd.notna(r["match_date"]) else "-"
            venue_s = str(r["venue"])[:14] if pd.notna(r["venue"]) else "-"
            ri_rows.append({
                "date":dt[-5:], "venue":venue_s, "runs":str(int(r["runs"])), "total":str(int(r["team_total"])),
            })
        st.markdown(render_table(
            ri_rows,
            [("date","Date"),("venue","Venue"),("runs","Runs"),("total","Total")],
            right_cols={"runs","total"},
            primary_col="runs",
        ), unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE — PHASES (08_phases.html)
# ══════════════════════════════════════════════════════════════════════════════
elif nav_selection == "📈 Phases":
    st.markdown('<div class="page-title">Phases</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Powerplay, middle overs, and death overs</div>', unsafe_allow_html=True)

    # Phase boundaries (over 0-indexed in data: over 0-5 = powerplay, 6-14 = middle, 15-19 = death)
    pp   = filt_balls[filt_balls["Overs"].between(0, 5)]
    mid  = filt_balls[filt_balls["Overs"].between(6, 14)]
    death= filt_balls[filt_balls["Overs"].between(15, 19)]

    def phase_rr(df):
        total_runs = df["TotalRun"].sum()
        total_balls = len(df)
        return round(total_runs / (total_balls / 6), 2) if total_balls else 0

    def phase_wkts(df):
        return int(df["IsWicketDelivery"].sum())

    pp_rr  = phase_rr(pp);   pp_wkts  = phase_wkts(pp)
    mid_rr = phase_rr(mid);  mid_wkts = phase_wkts(mid)
    dth_rr = phase_rr(death);dth_wkts = phase_wkts(death)

    ph1, ph2, ph3 = st.columns(3)
    with ph1:
        st.markdown(f"""
        <div class="phase-card">
          <div class="phase-label">⚡ Powerplay</div>
          <div><span class="phase-value">{pp_rr}</span><span class="phase-unit">RR</span></div>
          <div class="phase-stat">↓ {pp_wkts:,} Wickets</div>
        </div>""", unsafe_allow_html=True)
    with ph2:
        st.markdown(f"""
        <div class="phase-card">
          <div class="phase-label">🔄 Middle Overs</div>
          <div><span class="phase-value">{mid_rr}</span><span class="phase-unit">RR</span></div>
          <div class="phase-stat">↓ {mid_wkts:,} Wickets</div>
        </div>""", unsafe_allow_html=True)
    with ph3:
        st.markdown(f"""
        <div class="phase-card">
          <div class="phase-label">🔥 Death Overs</div>
          <div><span class="phase-value">{dth_rr}</span><span class="phase-unit">RR</span></div>
          <div class="phase-stat">↓ {dth_wkts:,} Wickets</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 2 bar charts (run rate by phase | wickets by phase)
    pbc1, pbc2 = st.columns(2)

    with pbc1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div style="font-family:\'JetBrains Mono\',monospace;font-size:14px;font-weight:500;color:#151c27;margin-bottom:24px;">Run rate by phase</div>', unsafe_allow_html=True)
        fig_prr = go.Figure(data=[
            go.Bar(
                x=["Powerplay","Middle","Death"],
                y=[pp_rr, mid_rr, dth_rr],
                marker_color=["#f4a261","#2a9d8f","#e76f51"],
                marker_line_width=0,
                text=[str(pp_rr), str(mid_rr), str(dth_rr)],
                textposition="outside",
                textfont=dict(family="JetBrains Mono", size=12, color="#57423d"),
                hovertemplate="%{x}: %{y} RR<extra></extra>",
            )
        ])
        plotly_layout(fig_prr, height=260)
        fig_prr.update_layout(showlegend=False, bargap=0.5)
        fig_prr.update_traces(marker_cornerradius=4)
        st.plotly_chart(fig_prr, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with pbc2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div style="font-family:\'JetBrains Mono\',monospace;font-size:14px;font-weight:500;color:#151c27;margin-bottom:24px;">Wickets by phase</div>', unsafe_allow_html=True)
        fig_pwk = go.Figure(data=[
            go.Bar(
                x=["Powerplay","Middle","Death"],
                y=[pp_wkts, mid_wkts, dth_wkts],
                marker_color=["#f4a261","#2a9d8f","#e76f51"],
                marker_line_width=0,
                text=[str(pp_wkts), str(mid_wkts), str(dth_wkts)],
                textposition="outside",
                textfont=dict(family="JetBrains Mono", size=12, color="#57423d"),
                hovertemplate="%{x}: %{y} wickets<extra></extra>",
            )
        ])
        plotly_layout(fig_pwk, height=260)
        fig_pwk.update_layout(showlegend=False, bargap=0.5)
        fig_pwk.update_traces(marker_cornerradius=4)
        st.plotly_chart(fig_pwk, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    # Bottom: Avg run rate by over (line chart from 08_phases.html)
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'JetBrains Mono\',monospace;font-size:14px;font-weight:500;color:#151c27;margin-bottom:16px;">Average run rate by over</div>', unsafe_allow_html=True)

    over_rr = filt_balls.groupby("Overs").agg(
        total_runs=("TotalRun","sum"),
        n_balls=("BallNumber","count"),
    ).reset_index()
    over_rr["rr"] = (over_rr["total_runs"] / (over_rr["n_balls"] / 6)).round(2)
    over_rr = over_rr[over_rr["Overs"].between(0,19)].sort_values("Overs")

    fig_ov = go.Figure(data=[
        go.Scatter(
            x=(over_rr["Overs"] + 1).astype(str),
            y=over_rr["rr"],
            mode="lines+markers",
            line=dict(color="#2a9d8f", width=3),
            marker=dict(color="#ffffff", size=6, line=dict(color="#2a9d8f", width=2)),
            hovertemplate="Over %{x}: %{y:.2f} RR<extra></extra>",
        )
    ])
    plotly_layout(fig_ov, height=280)
    fig_ov.update_layout(showlegend=False)
    fig_ov.update_xaxes(title_text="Over")
    fig_ov.update_yaxes(title_text="Run Rate")
    st.plotly_chart(fig_ov, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE — MATCHUPS (09_matchups.html)
# ══════════════════════════════════════════════════════════════════════════════
elif nav_selection == "⚔️ Matchups":
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("""
    <div style="border-bottom:1px solid rgba(220,226,243,0.2);padding-bottom:16px;margin-bottom:24px;">
      <div class="page-title">Batter vs bowler matchup</div>
      <p class="page-subtitle" style="margin-bottom:0;">Head-to-head historical T20 statistics</p>
    </div>
    """, unsafe_allow_html=True)

    # Player selectors with profile images (imgUrl from players CSV, initials fallback)
    def _player_avatar(name):
        if not name:
            return ""
        url = player_img.get(name.strip())
        if url:
            return f'<img class="player-avatar-img" src="{url}" alt="{name}" referrerpolicy="no-referrer" />'
        initials = "".join(p[0] for p in name.replace(".", " ").split()[:2]).upper() or "?"
        bg = f"hsl({(hash(name) % 360)}, 55%, 45%)"
        return f'<div class="player-avatar" style="background:{bg};">{initials}</div>'

    mu1, mu2 = st.columns(2)
    with mu1:
        all_batters_mu = sorted(filt_balls["Batter"].dropna().unique().tolist())
        mu_batter = st.selectbox("Batter", all_batters_mu, key="mu_batter")
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:10px;margin-top:8px;">{_player_avatar(mu_batter)}'
            f'<span class="filter-label">{mu_batter}</span></div>',
            unsafe_allow_html=True,
        )
    with mu2:
        all_bowlers_mu = sorted(filt_balls["Bowler"].dropna().unique().tolist())
        mu_bowler = st.selectbox("Bowler", all_bowlers_mu, key="mu_bowler")
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:10px;margin-top:8px;">{_player_avatar(mu_bowler)}'
            f'<span class="filter-label">{mu_bowler}</span></div>',
            unsafe_allow_html=True,
        )

    matchup_df = filt_balls[(filt_balls["Batter"] == mu_batter) & (filt_balls["Bowler"] == mu_bowler)]
    mu_runs = int(matchup_df["BatsmanRun"].sum())
    mu_balls = len(matchup_df)
    mu_boundaries = int((matchup_df["BatsmanRun"] >= 4).sum())
    mu_dots = int((matchup_df["BatsmanRun"] == 0).sum())
    mu_dismissals = int(matchup_df["IsWicketDelivery"].sum())
    mu_common_kind = matchup_df[matchup_df["IsWicketDelivery"] == 1]["Kind"].mode()
    mu_kind_str = str(mu_common_kind.iloc[0]).capitalize() if len(mu_common_kind) else "N/A"

    # 5 metric cards (from 09_matchups.html)
    mc1, mc2, mc3, mc4, mc5 = st.columns(5)
    mu_metrics = [
        ("Runs", str(mu_runs), "#a33d23"),
        ("Balls", str(mu_balls), "#151c27"),
        ("Boundaries", str(mu_boundaries), "#151c27"),
        ("Dots", str(mu_dots), "#151c27"),
        ("Dismissals", str(mu_dismissals), "#ba1a1a"),
    ]
    for col, (label, val, color) in zip([mc1,mc2,mc3,mc4,mc5], mu_metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="text-align:center;padding:16px;">
              <span class="metric-label">{label}</span>
              <div style="font-family:'Archivo Narrow',sans-serif;font-size:48px;font-weight:700;line-height:1.1;letter-spacing:-0.02em;color:{color};">{val}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:#f0f3ff;border-radius:0.5rem;padding:12px 16px;text-align:center;margin:16px 0;border:1px solid rgba(220,226,243,0.2);">
      <p style="font-family:'Plus Jakarta Sans',sans-serif;font-size:14px;color:#151c27;margin:0;">
        ℹ Most common dismissal kind in this matchup: <strong>{mu_kind_str}</strong>
      </p>
    </div>
    """, unsafe_allow_html=True)

    # Bar chart: runs off bat distribution (0,1,2,3,4,6)
    st.markdown('<div class="card-title">Runs off bat distribution</div>', unsafe_allow_html=True)
    run_dist = matchup_df["BatsmanRun"].value_counts().sort_index()
    run_vals = [int(run_dist.get(r, 0)) for r in [0,1,2,3,4,6]]
    run_labels = ["0","1","2","3","4","6"]

    fig_mu = go.Figure(data=[
        go.Bar(
            x=run_labels,
            y=run_vals,
            marker_color=["rgba(231,111,81,0.8)","rgba(231,111,81,0.9)","rgba(231,111,81,0.7)",
                          "rgba(231,111,81,0.5)","rgba(231,111,81,0.8)","rgba(231,111,81,0.7)"],
            marker_line_width=0,
            text=run_vals,
            textposition="outside",
            textfont=dict(family="JetBrains Mono", size=11, color="#57423d"),
            hovertemplate="Runs %{x}: %{y} times<extra></extra>",
        )
    ])
    plotly_layout(fig_mu, height=260)
    fig_mu.update_layout(showlegend=False, bargap=0.3)
    fig_mu.update_xaxes(title_text="Runs off bat")
    fig_mu.update_traces(marker_cornerradius=4)
    st.plotly_chart(fig_mu, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ─── RAW DATA EXPANDER (01_shell.html bottom) ─────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("📋 Raw data preview / Filtered matches"):
    display_cols = ["match_date","team1","team2","venue","toss_winner","toss_decision","winner"]
    disp = filt[display_cols].copy()
    disp["match_date"] = disp["match_date"].dt.strftime("%Y-%m-%d")

    rows_raw = []
    for _, row in disp.head(50).iterrows():
        rows_raw.append({
            "date":    str(row["match_date"]),
            "team1":   str(row["team1"]),
            "team2":   str(row["team2"]),
            "venue":   str(row["venue"])[:30],
            "toss_w":  str(row["toss_winner"]),
            "decision":str(row["toss_decision"]),
            "winner":  str(row["winner"]),
        })
    st.markdown(render_table(
        rows_raw,
        [("date","Date"),("team1","Team 1"),("team2","Team 2"),("venue","Venue"),("toss_w","Toss Winner"),("decision","Decision"),("winner","Winner")],
        right_cols=set(),
        primary_col="winner",
    ), unsafe_allow_html=True)
    if len(filt) > 50:
        st.markdown(f'<p style="text-align:center;font-family:\'JetBrains Mono\',monospace;font-size:12px;color:#e76f51;margin-top:8px;">Showing 50 of {len(filt):,} matches</p>', unsafe_allow_html=True)
