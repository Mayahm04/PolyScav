export default function History({ history }) {
  if (!history || history.length === 0)
    return <p style={{ textAlign: "center", color: "gray" }}>Aucun historique…</p>;

  const getBadge = (output) => {
    const c = output.toLowerCase();
    if (c.includes("plastique")) return "badge badge-plastique";
    if (c.includes("métal")) return "badge badge-métal";
    if (c.includes("papier")) return "badge badge-papier";
    if (c.includes("verre")) return "badge badge-verre";
    if (c.includes("organique")) return "badge badge-organique";
    return "badge badge-autre";
  };

  return (
    <div className="card">
      <h2 className="text-xl mb-4 font-bold">🕒 Historique des prédictions</h2>

      <div className="timeline">
        {history.map((item) => (
          <div key={item.id} className="timeline-item">
            <div>
              <span className={getBadge(item.output)}>{item.output}</span>
              <p style={{ color: "gray", marginTop: "5px", fontSize: "0.85rem" }}>
                {item.type === "image" ? "📸 Image" : "✍️ Texte"} —{" "}
                {new Date(item.timestamp).toLocaleString()}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
