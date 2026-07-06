import { useState } from "react";

function App() {
  const [invoices, setInvoices] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);

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
    setSummary({
      total: data.total_invoices,
      valid: data.valid,
      flagged: data.flagged,
    });
    setLoading(false);
  };

  return (
    <div style={{ display: "flex", minHeight: "100vh", fontFamily: "sans-serif" }}>
      {/* Sidebar */}
      <div style={{ width: 200, background: "#1a1a2e", padding: "1.5rem 1rem" }}>
        <div style={{ color: "#fff", fontSize: 15, fontWeight: 500, marginBottom: "2rem" }}>
          IVS Portal
        </div>
        <div style={{ color: "rgba(255,255,255,0.6)", fontSize: 13, padding: "8px 10px" }}>Dashboard</div>
        <div style={{ color: "rgba(255,255,255,0.6)", fontSize: 13, padding: "8px 10px" }}>Invoices</div>
        <div style={{ color: "rgba(255,255,255,0.6)", fontSize: 13, padding: "8px 10px" }}>Flagged</div>
      </div>

      {/* Main */}
      <div style={{ flex: 1, padding: "1.5rem", background: "#f9f9f9" }}>
        <div style={{ fontSize: 18, fontWeight: 500, marginBottom: 4 }}>Dashboard</div>
        <div style={{ fontSize: 13, color: "#888", marginBottom: "1.5rem" }}>ONGC Invoice Verification</div>

        {/* Stats */}
        {summary && (
          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 12, marginBottom: "1.5rem" }}>
            <div style={{ background: "#fff", border: "1px solid #eee", borderRadius: 8, padding: "1rem" }}>
              <div style={{ fontSize: 12, color: "#888" }}>Total</div>
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

        {/* Table */}
        {invoices.length > 0 && (
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13, background: "#fff", borderRadius: 8 }}>
            <thead>
              <tr style={{ borderBottom: "1px solid #eee" }}>
                <th style={{ padding: "10px", textAlign: "left", color: "#888", fontWeight: 400 }}>Invoice No.</th>
                <th style={{ padding: "10px", textAlign: "left", color: "#888", fontWeight: 400 }}>Telephone</th>
                <th style={{ padding: "10px", textAlign: "left", color: "#888", fontWeight: 400 }}>Sheet</th>
                <th style={{ padding: "10px", textAlign: "left", color: "#888", fontWeight: 400 }}>Amount</th>
                <th style={{ padding: "10px", textAlign: "left", color: "#888", fontWeight: 400 }}>Status</th>
                <th style={{ padding: "10px", textAlign: "left", color: "#888", fontWeight: 400 }}>Issue</th>
              </tr>
            </thead>
            <tbody>
              {invoices.map((inv, i) => (
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