import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import App from "./App.jsx";

describe("Polls App", () => {
  beforeEach(() => vi.restoreAllMocks());
  it("shows a poll with vote tallies and percentages", async () => {
    globalThis.fetch = vi.fn(() => Promise.resolve({
      ok: true, status: 200,
      json: async () => [{ id: "1", question: "Best?", total_votes: 4,
        options: [{ text: "A", votes: 3 }, { text: "B", votes: 1 }] }],
    }));
    render(<App />);
    await waitFor(() => expect(screen.getByText("Best?")).toBeInTheDocument());
    expect(screen.getByText(/75%/)).toBeInTheDocument();
  });
});
