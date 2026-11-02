// O3: same-origin invalid-header CSRF probe. No draft identifier or draft content.
(async () => {
  if (location.origin !== "https://app.bussassistent.com") {
    throw new Error("Stopp: feil nettsted for O3-proeven.");
  }
  const response = await fetch("/private-api/draft-operations", {
    method: "POST",
    credentials: "same-origin",
    headers: { "Content-Type": "application/json", "X-CSRF-Token": "o3-invalid-proof" },
    body: "{}",
    cache: "no-store",
    redirect: "error"
  });
  console.log("Status:", response.status);
  console.log("Cache-Control:", response.headers.get("cache-control"));
  console.log("Content-Type:", response.headers.get("content-type"));
  if (response.status === 403 && response.headers.get("content-type")?.includes("application/json")) {
    const body = await response.json();
    console.log("Detail:", typeof body.detail === "string" ? body.detail : "Uventet svarformat");
  }
})();
