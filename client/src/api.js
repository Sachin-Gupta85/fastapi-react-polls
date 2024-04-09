const BASE = import.meta.env?.VITE_API_URL || "";
async function req(path, opts) {
  const res = await fetch(`${BASE}/api${path}`, {
    headers: { "Content-Type": "application/json" }, ...opts });
  if (!res.ok) throw new Error(`${res.status}`);
  return res.status === 204 ? null : res.json();
}
export const listPolls = () => req("/polls");
export const createPoll = (question, options) =>
  req("/polls", { method: "POST", body: JSON.stringify({ question, options }) });
export const castVote = (id, option) =>
  req(`/polls/${id}/vote`, { method: "POST", body: JSON.stringify({ option }) });
