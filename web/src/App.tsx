import { useQuery } from "@tanstack/react-query";

import { getHealth } from "./api/client";

export default function App() {
  const { data, isPending, error } = useQuery({
    queryKey: ["health"],
    queryFn: getHealth,
    retry: false,
  });

  return (
    <main>
      <h1>Fantasy</h1>
      <p className="tagline">
        Free-agent valuation scored against your league&apos;s actual rules.
      </p>

      <section className="status">
        <h2>API connection</h2>
        {isPending && <p>Checking&hellip;</p>}
        {error && (
          <p className="bad">
            Cannot reach the API. Is it running on{" "}
            <code>{import.meta.env.VITE_API_URL ?? "http://localhost:8000"}</code>?
          </p>
        )}
        {data && (
          <p className="good">
            Connected &mdash; {data.environment}, v{data.version}
          </p>
        )}
      </section>
    </main>
  );
}
