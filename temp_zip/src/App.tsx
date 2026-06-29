/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useEffect } from "react";

export default function App() {
  useEffect(() => {
    window.location.replace("/test-temp-viz/index.html");
  }, []);

  return (
    <div style={{ padding: "24px", fontFamily: "sans-serif", color: "#1f2733", background: "#f6f8fb", minHeight: "100vh" }}>
      Loading TwoCascade Tutorial Visualizer...
    </div>
  );
}

