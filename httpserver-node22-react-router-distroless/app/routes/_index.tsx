import type { MetaFunction } from "react-router";

export const meta: MetaFunction = () => {
  return [
    { title: "React Router App" },
    { name: "description", content: "Welcome to React Router!" },
  ];
};

export default function Index() {
  return (
    <div style={{ fontFamily: "system-ui, sans-serif", lineHeight: "1.8" }}>
      <h1>Welcome to React Router</h1>
      <ul>
        <li>
          <a
            target="_blank"
            href="https://reactrouter.com/start/framework/routing"
            rel="noreferrer"
          >
            React Router Routing Guide
          </a>
        </li>
        <li>
          <a
            target="_blank"
            href="https://reactrouter.com/start/framework/data-loading"
            rel="noreferrer"
          >
            Data Loading Guide
          </a>
        </li>
        <li>
          <a target="_blank" href="https://reactrouter.com/home" rel="noreferrer">
            React Router Docs
          </a>
        </li>
      </ul>
    </div>
  );
}
