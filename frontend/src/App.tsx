import { useEffect, useMemo, useState } from "react";

type Fuel = "regular" | "midgrade" | "premium" | "diesel";
type Station = { station: string; address: string; prices: Record<string, number> };
type Stats = {
  fuel_type: string;
  average_price: number;
  cheapest_station: { station: string; address: string; price: number };
  most_expensive_station: { station: string; address: string; price: number };
};
const choices: { key: Fuel; label: string; field: string }[] = [
  { key: "regular", label: "Regular", field: "Regular" },
  { key: "midgrade", label: "Midgrade", field: "MidGrade" },
  { key: "premium", label: "Premium", field: "Premium" },
  { key: "diesel", label: "Diesel", field: "Diesel" },
];
const api = (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000").replace(/\/$/, "");
const money = (n: number) => "$" + n.toFixed(2);

export default function App() {
  const [fuel, setFuel] = useState<Fuel>("regular");
  const [stations, setStations] = useState<Station[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [sort, setSort] = useState("price");
  const [gallons, setGallons] = useState(12);
  const [savedOnly, setSavedOnly] = useState(false);
  const [saved, setSaved] = useState<string[]>(() => {
    try { return JSON.parse(localStorage.getItem("peakfuel-saved") || "[]"); }
    catch { return []; }
  });
  const [retry, setRetry] = useState(0);
  const fuelKey = choices.find((choice) => choice.key === fuel)!.field;

  // This gets the station list and stats from our Python API.
  useEffect(() => {
    let active = true;
    setLoading(true);
    setError("");
    Promise.all([fetch(api + "/prices/latest"), fetch(api + "/prices/stats/" + fuel)])
      .then(async ([a, b]) => {
        if (!a.ok || !b.ok) throw new Error("The API returned an error.");
        const stationData = (await a.json()) as Station[];
        const statData = (await b.json()) as Stats;
        if (!Array.isArray(stationData) || typeof statData.average_price !== "number") {
          throw new Error("The data from the API wasn't formatted correctly.");
        }
        if (active) { setStations(stationData); setStats(statData); }
      })
      .catch((e: unknown) => {
        if (active) { setError(e instanceof Error ? e.message : "Unable to load prices."); setStations([]); setStats(null); }
      })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, [fuel, retry]);

  // Only display the stations that match the current filters.
  const visible = useMemo(() => stations
    .filter((s) => Number.isFinite(s.prices[fuelKey]))
    .filter((s) => (s.station + " " + s.address).toLowerCase().includes(search.toLowerCase()))
    .filter((s) => !savedOnly || saved.includes(s.address))
    .sort((a, b) => sort === "price" ? a.prices[fuelKey] - b.prices[fuelKey] : a.station.localeCompare(b.station)),
    [stations, fuelKey, search, savedOnly, saved, sort]);

  function toggleSaved(address: string) {
    setSaved((prev) => {
      const updated = prev.includes(address) ? prev.filter((a) => a !== address) : [...prev, address];
      localStorage.setItem("peakfuel-saved", JSON.stringify(updated));
      return updated;
    });
  }

  const savings = stats ? (stats.most_expensive_station.price - stats.cheapest_station.price) * gallons : 0;
  return (
    <div className="page">
      <header className="header">
        <div className="brand"><span className="logo">P</span><span><strong>PeakFuel</strong><small>COLORADO SPRINGS</small></span></div>
        <a className="api-link" href={api + "/docs"} target="_blank" rel="noreferrer">View API docs ↗</a>
      </header>

      <main>
        <section className="hero">
          <div className="eyebrow">↗  SMARTER STOPS. MORE SAVINGS.</div>
          <h1>Find your next<br/><span>better fill-up.</span></h1>
          <p>Explore gas station prices and compare how much your next fill-up could cost.</p>
          <div className="location">⌖ Colorado Springs, Colorado</div>
        </section>

        <aside className="demo" role="note"><span className="info">i</span><div>
          <strong>Demo mode — sample prices only</strong>
          <p>These are made-up stations and placeholder prices, not current gas prices. The app isn't ready for real fueling decisions yet.</p>
        </div></aside>

        <div className="fuel-header">
          <div><div className="label">CHOOSE YOUR FUEL</div><nav aria-label="Fuel types" className="fuel-tabs">
            {choices.map((c) => <button key={c.key} className={c.key === fuel ? "active" : ""} aria-pressed={c.key === fuel} onClick={() => setFuel(c.key)}>{c.label}</button>)}
          </nav></div>
          <span className="dataset">● SAMPLE DATASET</span>
        </div>

        <section className="stats">
          <article className="stat"><div className="label">LOWEST PRICE <span>↘</span></div><div className="stat-number">{stats ? money(stats.cheapest_station.price) : "—"}<small>/gal</small></div><p>{stats?.cheapest_station.station || "Waiting for prices"}</p></article>
          <article className="stat"><div className="label">AVERAGE PRICE <span>≋</span></div><div className="stat-number">{stats ? money(stats.average_price) : "—"}<small>/gal</small></div><p>Across the sample stations</p></article>
          <article className="stat highlight"><div className="label">POTENTIAL DIFFERENCE <span>✦</span></div><div className="stat-number">{stats ? money(savings) : "—"}</div><p>For a {gallons}-gallon fill-up</p></article>
        </section>

        <div className="columns">
          <section className="panel stations-panel">
            <div className="label">EXPLORE</div><h2>Gas stations <span className="count">{visible.length}</span></h2>
            <div className="search-row">
              <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search station or address" aria-label="Search station or address"/>
              <select value={sort} aria-label="Sort stations" onChange={(e) => setSort(e.target.value)}><option value="price">Lowest price</option><option value="name">Name A–Z</option></select>
            </div>
            <label className="saved-filter"><input type="checkbox" checked={savedOnly} onChange={(e) => setSavedOnly(e.target.checked)}/> Saved stations only</label>
            {loading && <div className="message">Loading the stations…</div>}
            {error && <div className="message error"><b>Couldn't reach the backend.</b><p>{error} Start the Python API and try again.</p><button onClick={() => setRetry((n) => n + 1)}>Retry</button></div>}
            {!loading && !error && visible.length === 0 && <div className="message">No stations match these filters.</div>}
            {!loading && !error && visible.map((s, i) => (
              <article className="station" key={s.address}>
                <div className="station-icon">⛽</div>
                <div className="station-info"><strong>{s.station}</strong><p>{s.address}</p><small>{i === 0 && sort === "price" && !savedOnly && !search ? "LOWEST IN SAMPLE" : "DEMO STATION"}</small></div>
                <div className="price">{money(s.prices[fuelKey])}<small>/gal</small></div>
                <button className={"heart " + (saved.includes(s.address) ? "selected" : "")} onClick={() => toggleSaved(s.address)} aria-label={(saved.includes(s.address) ? "Unsave " : "Save ") + s.station} aria-pressed={saved.includes(s.address)}>{saved.includes(s.address) ? "♥" : "♡"}</button>
              </article>
            ))}
          </section>
          <aside className="side-panels">
            <section className="panel">
              <div className="label">AT A GLANCE</div><h2>Price comparison</h2><p className="subhead">Fuel prices across the sample stations.</p>
              {stations.filter((s) => Number.isFinite(s.prices[fuelKey])).map((s) => (
                <div className="bar-section" key={s.address}>
                  <div className="bar-label"><span>{s.station}</span><strong>{money(s.prices[fuelKey])}</strong></div>
                  <div className="bar-bg"><div className="bar" style={{width: (100 * s.prices[fuelKey] / Math.max(1, stats?.most_expensive_station.price || 1)) + "%"}}/></div>
                </div>
              ))}
            </section>
            <section className="panel calculator">
              <div className="label">QUICK CALCULATOR</div><h2>What could you save?</h2>
              <p className="subhead">Compare the cheapest and most expensive example prices.</p>
              <div className="slider-label"><label htmlFor="gallons">Gallons to buy</label><strong>{gallons} gal</strong></div>
              <input id="gallons" type="range" min="1" max="30" value={gallons} onChange={(e) => setGallons(Number(e.target.value))}/>
              <div className="ends"><span>1 gal</span><span>30 gal</span></div>
              <div className="result"><span>Price difference</span><strong>{stats ? money(savings) : "—"}</strong><small>Example only. Does not include travel costs.</small></div>
            </section>
          </aside>
        </div>
      </main>
      <footer>PeakFuel · Colorado Springs Gas Tracker <span>Demo data is not live pricing.</span></footer>
    </div>
  );
}
