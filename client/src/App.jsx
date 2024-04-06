import React, { useEffect, useState } from "react";
import { listPolls, createPoll, castVote } from "./api.js";

function pct(v, total) { return total ? Math.round((v / total) * 100) : 0; }

export default function App() {
  const [polls, setPolls] = useState([]);
  const [question, setQuestion] = useState("");
  const [optsText, setOptsText] = useState("");

  async function refresh() { setPolls(await listPolls()); }
  useEffect(() => { refresh(); }, []);

  async function onCreate(e) {
    e.preventDefault();
    const options = optsText.split("\n").map((s) => s.trim()).filter(Boolean);
    if (!question.trim() || options.length < 2) return;
    await createPoll(question.trim(), options);
    setQuestion(""); setOptsText(""); refresh();
  }

  return (
    <main style={{ maxWidth: 640, margin: "2rem auto", fontFamily: "system-ui" }}>
      <h1>📊 Polls</h1>
      <form onSubmit={onCreate} style={{ display: "grid", gap: 8, marginBottom: 20 }}>
        <input aria-label="question" placeholder="Question" value={question} onChange={(e) => setQuestion(e.target.value)} />
        <textarea aria-label="options" placeholder="One option per line (2+)" value={optsText} onChange={(e) => setOptsText(e.target.value)} />
        <button type="submit">Create poll</button>
      </form>
      {polls.map((p) => (
        <section key={p.id} style={{ border: "1px solid #ddd", borderRadius: 8, padding: 12, marginBottom: 12 }}>
          <h3>{p.question}</h3>
          {p.options.map((o, i) => (
            <div key={i} style={{ margin: "6px 0" }}>
              <button onClick={async () => { await castVote(p.id, i); refresh(); }}>Vote</button>{" "}
              {o.text} — <strong>{o.votes}</strong> ({pct(o.votes, p.total_votes)}%)
            </div>
          ))}
          <small>{p.total_votes} total votes</small>
        </section>
      ))}
    </main>
  );
}
