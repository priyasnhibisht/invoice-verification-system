import { useState } from "react";

function App() {
  const [invoices, setInvoices] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState("ALL");

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://127.0.0.1:8000/invoices/upload", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    setInvoices(data.results);
    setSummary({ total: data.total_invoices, valid: data.valid, flagged: data.flagged });
    setLoading(false);
  };

  const filtered = invoices.filter(inv => {
    if (filter === "VALID") return inv.status === "VALID";
    if (filter === "FLAGGED") return inv.status === "FLAGGED";
    return true;
  });

  return (
    <div style={{ minHeight: "100vh", background: "#f9f9f9", fontFamily: "sans-serif" }}>
      {/* Header */}
      <div style={{ background: "#1a1a2e", padding: "1rem 2rem", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div style={{ color: "#fff", fontSize: 16, fontWeight: 500 }}>IVS Portal — ONGC Invoice Verification</div>
        <div style={{ color: "rgba(255,255,255,0.5)", fontSize: 13 }}>Admin</div>
      </div>

      <div style={{ padding: "1.5rem 2rem" }}>
        {/* Stats */}
        {summary && (
          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 12, marginBottom: "1.5rem" }}>
            <div style={{ background: "#fff", border: "1px solid #eee", borderRadius: 8, padding: "1rem" }}>
              <div style={{ fontSize: 12, color: "#888" }}>Total invoices</div>
              <div style={{ fontSize: 24, fontWeight: 500 }}>{summary.total}</div>
            </div>
            <div style={{ background: "#fff", border: "1px solid #eee", borderRadius: 8, padding: "1rem" }}>
              <div style={{ fontSize: 12, color: "#888" }}>Valid</div>
              <div style={{ fontSize: 24, fontWeight: 500, color: "green" }}>{summary.valid}</div>
            </div>
            <div style={{ background: "#fff", border: "1px solid #eee", borderRadius: 8, padding: "1rem" }}>
              <div style={{ fontSize: 12, color: "#888" }}>Flagged</div>
              <div style={{ fontSize: 24, fontWeight: 500, color: "red" }}>{summary.flagged}</div>
            </div>
          </div>
        )}

        {/* Upload */}
        <div style={{ background: "#fff", border: "2px dashed #ccc", borderRadius: 12, padding: "1.5rem", textAlign: "center", marginBottom: "1.5rem" }}>
          <div style={{ fontSize: 14, fontWeight: 500, marginBottom: 4 }}>Upload Invoice File</div>
          <div style={{ fontSize: 13, color: "#888", marginBottom: 12 }}>PDF, Excel or scanned image</div>
          <input type="file" onChange={handleUpload} accept=".xlsx,.xls,.pdf,.png,.jpg" />
          {loading && <div style={{ marginTop: 8, color: "#888" }}>Processing...</div>}
        </div>

        {/* Filter buttons */}
        {invoices.length > 0 && (
          <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
            {["ALL", "VALID", "FLAGGED"].map(f => (
              <button key={f} onClick={() => setFilter(f)} style={{
                padding: "4px 14px", borderRadius: 20, border: "1px solid #ddd", cursor: "pointer", fontSize: 13,
                background: filter === f ? "#1a1a2e" : "#fff",
                color: filter === f ? "#fff" : "#555"
              }}>{f}</button>
            ))}
          </div>
        )}

        {/* Table */}
        {filtered.length > 0 && (
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13, background: "#fff", borderRadius: 8 }}>
            <thead>
              <tr style={{ borderBottom: "1px solid #eee" }}>
                {["Invoice No.", "Telephone", "Sheet", "Amount", "Status", "Issue"].map(h => (
                  <th key={h} style={{ padding: "10px", textAlign: "left", color: "#888", fontWeight: 400 }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtered.map((inv, i) => (
                <tr key={i} style={{ borderBottom: "1px solid #eee" }}>
                  <td style={{ padding: "10px" }}>{inv.invoice_number}</td>
                  <td style={{ padding: "10px" }}>{inv.telephone}</td>
                  <td style={{ padding: "10px" }}>{inv.sheet}</td>
                  <td style={{ padding: "10px" }}>₹{inv.total_payable}</td>
                  <td style={{ padding: "10px" }}>
                    <span style={{
                      padding: "2px 8px", borderRadius: 20, fontSize: 11,
                      background: inv.status === "VALID" ? "#e6f4ea" : "#fce8e6",
                      color: inv.status === "VALID" ? "green" : "red"
                    }}>{inv.status}</span>
                  </td>
                  <td style={{ padding: "10px", color: inv.errors.length > 0 ? "red" : "#888", fontSize: 12 }}>
                    {inv.errors.length > 0 ? inv.errors.join(", ") : "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default App;